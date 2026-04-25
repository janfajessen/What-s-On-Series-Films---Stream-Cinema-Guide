"""Config flow for What's On Series & Films."""
from __future__ import annotations

import logging

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.selector import (
    BooleanSelector,
    LanguageSelector,
    LanguageSelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .const import (
    CONF_COUNTRY,
    CONF_LANGUAGE,
    CONF_PLATFORMS,
    CONF_PROVIDER_MAP,
    CONF_SHOWS,
    CONF_TMDB_API_KEY,
    COUNTRY_TO_LANGUAGE,
    DEFAULT_LANGUAGE,
    DOMAIN,
    NAME,
    STREAMING_PLATFORMS_FALLBACK,
    TMDB_BASE_URL,
    TVMAZE_BASE_URL,
    TVMAZE_MAX_SEARCH_RESULTS,
)

_LOGGER = logging.getLogger(__name__)


# ── Helpers ────────────────────────────────────────────────────────────────────

def _flag_emoji(code: str) -> str:
    """Convert ISO 3166-1 alpha-2 to flag emoji. 'ES' -> '🇪🇸'"""
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in code.upper()[:2])


def _language_from(country: str, lang_raw: str) -> str:
    """Build TMDB language tag from LanguageSelector output or auto-detect."""
    lang = (lang_raw or "").strip()
    if lang:
        return f"{lang}-{country}" if "-" not in lang else lang
    return COUNTRY_TO_LANGUAGE.get(country, DEFAULT_LANGUAGE)


async def _validate_tmdb_key(session: aiohttp.ClientSession, api_key: str) -> bool:
    try:
        async with session.get(
            f"{TMDB_BASE_URL}/configuration",
            params={"api_key": api_key},
            timeout=aiohttp.ClientTimeout(total=10),
        ) as resp:
            return resp.status == 200
    except Exception:
        return False


async def _fetch_regions(session: aiohttp.ClientSession, api_key: str) -> list[dict]:
    """Return SelectSelector options for all TMDB-supported countries with flags."""
    try:
        async with session.get(
            f"{TMDB_BASE_URL}/watch/providers/regions",
            params={"api_key": api_key, "language": "en-US"},
            timeout=aiohttp.ClientTimeout(total=15),
        ) as resp:
            resp.raise_for_status()
            payload = await resp.json()
        return sorted(
            [
                {
                    "value": r["iso_3166_1"],
                    "label": f"{_flag_emoji(r['iso_3166_1'])} {r['english_name']}",
                }
                for r in payload.get("results", [])
                if r.get("iso_3166_1") and r.get("english_name")
            ],
            key=lambda x: x["label"],
        )
    except Exception as err:
        _LOGGER.warning("Could not fetch TMDB regions: %s", err)
        return []


async def _fetch_providers(
    session: aiohttp.ClientSession,
    api_key: str,
    country: str,
    language: str,
) -> dict[str, int]:
    """Return {provider_name: provider_id} for country, sorted A-Z."""
    merged: dict[str, int] = {}
    for media_type in ("movie", "tv"):
        try:
            async with session.get(
                f"{TMDB_BASE_URL}/watch/providers/{media_type}",
                params={"api_key": api_key, "watch_region": country, "language": language},
                timeout=aiohttp.ClientTimeout(total=15),
            ) as resp:
                resp.raise_for_status()
                payload = await resp.json()
            for p in payload.get("results", []):
                name = p.get("provider_name", "").strip()
                pid = p.get("provider_id")
                if name and pid:
                    merged[name] = pid
        except Exception as err:
            _LOGGER.warning("Could not fetch TMDB %s providers for %s: %s", media_type, country, err)
    if not merged:
        _LOGGER.warning("No providers fetched — using fallback list.")
        return dict(STREAMING_PLATFORMS_FALLBACK)
    return dict(sorted(merged.items()))


async def _search_tvmaze(session: aiohttp.ClientSession, query: str) -> list[dict]:
    try:
        async with session.get(
            f"{TVMAZE_BASE_URL}/search/shows",
            params={"q": query},
            timeout=aiohttp.ClientTimeout(total=10),
        ) as resp:
            resp.raise_for_status()
            results = await resp.json()
        return [
            {
                "id": r["show"]["id"],
                "name": r["show"]["name"],
                "premiered": r["show"].get("premiered") or "",
                "status": r["show"].get("status") or "",
                "network": (
                    (r["show"].get("network") or r["show"].get("webChannel") or {})
                    .get("name", "")
                ),
            }
            for r in results[:TVMAZE_MAX_SEARCH_RESULTS]
        ]
    except Exception:
        return []


def _result_options(results: list[dict]) -> list[dict]:
    options = []
    for s in results:
        year = s["premiered"][:4] if len(s["premiered"]) >= 4 else "?"
        parts = [s["name"], f"({year})"]
        if s["status"]:
            parts.append(f"— {s['status']}")
        if s["network"]:
            parts.append(f"· {s['network']}")
        options.append({"value": str(s["id"]), "label": " ".join(parts)})
    return options


# ── Config flow ────────────────────────────────────────────────────────────────

class WhatsonSeriesFilmsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """One entry per country.

    Step 1 (user)        — TMDB API key only.
    Step 2 (country)     — Country dropdown (TMDB regions + flag emojis) + language.
    Step 3 (platforms)   — Streaming platforms for chosen country.
    Step 4 (tvmaze)      — Search for a series / doc.
    Step 5 (tvmaze_pick) — Pick from results.
    Step 6 (add_another) — Add more.
    """

    VERSION = 1

    def __init__(self) -> None:
        self._api_key:        str            = ""
        self._regions:        list[dict]     = []
        self._data:           dict           = {}
        self._provider_map:   dict[str, int] = {}
        self._shows:          list[dict]     = []
        self._tvmaze_results: list[dict]     = []
        self._reconfiguring:  bool           = False

    # Step 1 — API key

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input is not None:
            api_key = user_input.get(CONF_TMDB_API_KEY, "").strip()

            if not api_key:
                self._data = {
                    CONF_TMDB_API_KEY: "",
                    CONF_COUNTRY:      "US",
                    CONF_LANGUAGE:     DEFAULT_LANGUAGE,
                    CONF_PLATFORMS:    [],
                    CONF_PROVIDER_MAP: {},
                }
                return await self.async_step_tvmaze()

            session = async_get_clientsession(self.hass)
            if not await _validate_tmdb_key(session, api_key):
                errors["base"] = "invalid_tmdb_key"
            else:
                self._api_key = api_key
                self._regions = await _fetch_regions(session, api_key)
                return await self.async_step_country()

        return self.async_show_form(
            step_id="user",
            errors=errors,
            data_schema=vol.Schema({
                vol.Optional(CONF_TMDB_API_KEY, default=""): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.PASSWORD)
                ),
            }),
        )

    # Step 2 — Country + language

    async def async_step_country(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input is not None:
            country  = str(user_input.get(CONF_COUNTRY, "ES")).strip().upper()
            language = _language_from(country, user_input.get(CONF_LANGUAGE) or "")

            await self.async_set_unique_id(country)
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            self._provider_map = await _fetch_providers(
                session, self._api_key, country, language
            )
            _LOGGER.debug("Fetched %d providers for %s (%s)",
                          len(self._provider_map), country, language)
            self._data = {
                CONF_TMDB_API_KEY: self._api_key,
                CONF_COUNTRY:      country,
                CONF_LANGUAGE:     language,
            }
            return await self.async_step_platforms()

        options = self._regions or [
            {"value": "AD", "label": "\U0001f1e6\U0001f1e9 Andorra"},
            {"value": "AR", "label": "\U0001f1e6\U0001f1f7 Argentina"},
            {"value": "AU", "label": "\U0001f1e6\U0001f1fa Australia"},
            {"value": "BR", "label": "\U0001f1e7\U0001f1f7 Brazil"},
            {"value": "CA", "label": "\U0001f1e8\U0001f1e6 Canada"},
            {"value": "DE", "label": "\U0001f1e9\U0001f1ea Germany"},
            {"value": "ES", "label": "\U0001f1ea\U0001f1f8 Spain"},
            {"value": "FR", "label": "\U0001f1eb\U0001f1f7 France"},
            {"value": "GB", "label": "\U0001f1ec\U0001f1e7 United Kingdom"},
            {"value": "HR", "label": "\U0001f1ed\U0001f1f7 Croatia"},
            {"value": "IT", "label": "\U0001f1ee\U0001f1f9 Italy"},
            {"value": "MX", "label": "\U0001f1f2\U0001f1fd Mexico"},
            {"value": "PL", "label": "\U0001f1f5\U0001f1f1 Poland"},
            {"value": "PT", "label": "\U0001f1f5\U0001f1f9 Portugal"},
            {"value": "RU", "label": "\U0001f1f7\U0001f1fa Russia"},
            {"value": "US", "label": "\U0001f1fa\U0001f1f8 United States"},
        ]

        return self.async_show_form(
            step_id="country",
            errors=errors,
            data_schema=vol.Schema({
                vol.Required(CONF_COUNTRY, default="ES"): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        mode=SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Optional(CONF_LANGUAGE): LanguageSelector(
                    LanguageSelectorConfig()
                ),
            }),
        )

    # Step 3 — Platforms

    async def async_step_platforms(self, user_input=None):
        if user_input is not None:
            selected = user_input.get(CONF_PLATFORMS, [])
            self._data[CONF_PLATFORMS]    = selected
            self._data[CONF_PROVIDER_MAP] = {
                n: self._provider_map[n] for n in selected if n in self._provider_map
            }
            if self._reconfiguring:
                return self._finish_reconfigure()
            return await self.async_step_tvmaze()

        options = [{"value": n, "label": n} for n in self._provider_map]
        return self.async_show_form(
            step_id="platforms",
            data_schema=vol.Schema({
                vol.Optional(CONF_PLATFORMS, default=[]): SelectSelector(
                    SelectSelectorConfig(
                        options=options,
                        multiple=True,
                        mode=SelectSelectorMode.LIST,
                    )
                ),
            }),
        )

    # Step 4 — TVmaze search

    async def async_step_tvmaze(self, user_input=None):
        errors: dict[str, str] = {}
        if user_input is not None:
            query = user_input.get("show_name", "").strip()
            if not query:
                return self._create_entry()
            session = async_get_clientsession(self.hass)
            results = await _search_tvmaze(session, query)
            if results:
                self._tvmaze_results = results
                return await self.async_step_tvmaze_pick()
            errors["base"] = "no_results"

        return self.async_show_form(
            step_id="tvmaze",
            errors=errors,
            data_schema=vol.Schema({
                vol.Optional("show_name", default=""): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.TEXT)
                ),
            }),
        )

    # Step 5 — Pick

    async def async_step_tvmaze_pick(self, user_input=None):
        if user_input is not None:
            sid   = int(user_input["show_id"])
            match = next((s for s in self._tvmaze_results if s["id"] == sid), None)
            if match and not any(s["id"] == sid for s in self._shows):
                self._shows.append({"id": match["id"], "name": match["name"]})
            return await self.async_step_add_another()

        return self.async_show_form(
            step_id="tvmaze_pick",
            data_schema=vol.Schema({
                vol.Required("show_id"): SelectSelector(
                    SelectSelectorConfig(
                        options=_result_options(self._tvmaze_results),
                        mode=SelectSelectorMode.LIST,
                    )
                ),
            }),
        )

    # Step 6 — Add another?

    async def async_step_add_another(self, user_input=None):
        if user_input is not None:
            if user_input.get("add_another", False):
                self._tvmaze_results = []
                return await self.async_step_tvmaze()
            return self._create_entry()

        shows_added = ", ".join(s["name"] for s in self._shows) if self._shows else "—"
        return self.async_show_form(
            step_id="add_another",
            data_schema=vol.Schema({
                vol.Required("add_another", default=False): BooleanSelector(),
            }),
            description_placeholders={"shows_added": shows_added},
        )

    def _create_entry(self):
        data = dict(self._data)
        data[CONF_SHOWS] = self._shows
        country = data.get(CONF_COUNTRY, "XX")
        return self.async_create_entry(title=f"{NAME} — {country}", data=data)


    async def async_step_reconfigure(self, user_input=None):
        """Handle reconfiguration from ⋮ → Reconfigurar.

        Reuses the same API-key → country → platforms flow but updates
        the existing entry instead of creating a new one.
        """
        existing = self._get_reconfigure_entry()
        # Pre-populate with current values
        if not self._api_key and existing.data.get(CONF_TMDB_API_KEY):
            self._api_key = existing.data[CONF_TMDB_API_KEY]

        if user_input is None:
            # Show the API key step pre-filled
            return self.async_show_form(
                step_id="reconfigure",
                data_schema=vol.Schema({
                    vol.Optional(
                        CONF_TMDB_API_KEY,
                        default=existing.data.get(CONF_TMDB_API_KEY, ""),
                    ): TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD)),
                }),
            )

        api_key = user_input.get(CONF_TMDB_API_KEY, "").strip()
        errors: dict[str, str] = {}

        if api_key:
            session = async_get_clientsession(self.hass)
            if not await _validate_tmdb_key(session, api_key):
                errors["base"] = "invalid_tmdb_key"
                return self.async_show_form(
                    step_id="reconfigure",
                    errors=errors,
                    data_schema=vol.Schema({
                        vol.Optional(CONF_TMDB_API_KEY, default=api_key): TextSelector(
                            TextSelectorConfig(type=TextSelectorType.PASSWORD)
                        ),
                    }),
                )
            self._api_key = api_key
            self._regions = await _fetch_regions(session, api_key)
        else:
            self._api_key = ""

        # Reuse country step — will call async_step_platforms then finish
        self._reconfiguring = True
        return await self.async_step_country()

    def _finish_reconfigure(self) -> config_entries.FlowResult:
        """Commit updated data back to the existing entry and reload it."""
        existing = self._get_reconfigure_entry()
        data = dict(self._data)
        # Preserve existing shows — reconfigure only touches TMDB settings
        data[CONF_SHOWS] = existing.data.get(CONF_SHOWS, [])
        return self.async_update_reload_and_abort(
            existing,
            data_updates=data,
            reason="reconfigure_successful",
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return WhatsonSeriesFilmsOptionsFlow()


# ── Options flow ───────────────────────────────────────────────────────────────

class WhatsonSeriesFilmsOptionsFlow(config_entries.OptionsFlow):

    def __init__(self) -> None:
        self._shows:          list[dict]     = []
        self._provider_map:   dict[str, int] = {}
        self._regions:        list[dict]     = []
        self._tvmaze_results: list[dict]     = []
        self._initialized:    bool           = False

    async def async_step_init(self, user_input=None):
        if not self._initialized:
            self._shows        = list(self.config_entry.data.get(CONF_SHOWS, []))
            self._provider_map = dict(self.config_entry.data.get(CONF_PROVIDER_MAP, {}))
            self._initialized  = True
        return await self.async_step_menu()

    async def async_step_menu(self, user_input=None):
        if user_input is not None:
            action = user_input.get("action")
            if action == "add_show":         return await self.async_step_tvmaze()
            if action == "remove_show":      return await self.async_step_remove_show()
            if action == "update_platforms": return await self.async_step_update_platforms()
            if action == "update_tmdb":      return await self.async_step_update_tmdb()
            return self.async_create_entry(title="", data={})  # fallback

        return self.async_show_form(
            step_id="menu",
            data_schema=vol.Schema({
                vol.Required("action"): SelectSelector(
                    SelectSelectorConfig(
                        mode=SelectSelectorMode.LIST,
                        options=[
                            {"value": "add_show",         "label": "Añadir serie o documental (TVmaze)"},
                            {"value": "remove_show",       "label": "Eliminar una serie o documental"},
                            {"value": "update_platforms",  "label": "Cambiar plataformas de streaming"},
                            {"value": "update_tmdb",       "label": "Actualizar clave TMDB / país / idioma"},
                        ],
                    )
                ),
            }),
        )

    async def async_step_tvmaze(self, user_input=None):
        errors: dict[str, str] = {}
        if user_input is not None:
            query = user_input.get("show_name", "").strip()
            if query:
                session = async_get_clientsession(self.hass)
                results = await _search_tvmaze(session, query)
                if results:
                    self._tvmaze_results = results
                    return await self.async_step_tvmaze_pick()
                errors["base"] = "no_results"

        return self.async_show_form(
            step_id="tvmaze",
            errors=errors,
            data_schema=vol.Schema({
                vol.Optional("show_name", default=""): TextSelector(
                    TextSelectorConfig(type=TextSelectorType.TEXT)
                ),
            }),
        )

    async def async_step_tvmaze_pick(self, user_input=None):
        if user_input is not None:
            sid   = int(user_input["show_id"])
            match = next((s for s in self._tvmaze_results if s["id"] == sid), None)
            if match and not any(s["id"] == sid for s in self._shows):
                self._shows.append({"id": match["id"], "name": match["name"]})
            self._commit()
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="tvmaze_pick",
            data_schema=vol.Schema({
                vol.Required("show_id"): SelectSelector(
                    SelectSelectorConfig(
                        options=_result_options(self._tvmaze_results),
                        mode=SelectSelectorMode.LIST,
                    )
                ),
            }),
        )

    async def async_step_remove_show(self, user_input=None):
        if not self._shows:
            return self.async_create_entry(title="", data={})
        if user_input is not None:
            self._shows = [s for s in self._shows if s["id"] != int(user_input["show_id"])]
            self._commit()
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="remove_show",
            data_schema=vol.Schema({
                vol.Required("show_id"): SelectSelector(
                    SelectSelectorConfig(
                        mode=SelectSelectorMode.LIST,
                        options=[{"value": str(s["id"]), "label": s["name"]} for s in self._shows],
                    )
                ),
            }),
        )

    async def async_step_update_platforms(self, user_input=None):
        current  = self.config_entry.data
        api_key  = current.get(CONF_TMDB_API_KEY, "")
        country  = current.get(CONF_COUNTRY, "US")
        language = current.get(CONF_LANGUAGE, DEFAULT_LANGUAGE)

        # Always fetch fresh from TMDB — self._provider_map from init only
        # contains the selected platforms, not the full country list
        if api_key and user_input is None:
            session = async_get_clientsession(self.hass)
            self._provider_map = await _fetch_providers(session, api_key, country, language)

        if user_input is not None:
            selected = user_input.get(CONF_PLATFORMS, [])
            new_data = dict(current)
            new_data[CONF_PLATFORMS]    = selected
            new_data[CONF_PROVIDER_MAP] = {
                n: self._provider_map[n] for n in selected if n in self._provider_map
            }
            self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
            return self.async_create_entry(title="", data={})

        options = [{"value": n, "label": n} for n in self._provider_map]
        return self.async_show_form(
            step_id="update_platforms",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_PLATFORMS,
                    default=current.get(CONF_PLATFORMS, []),
                ): SelectSelector(
                    SelectSelectorConfig(options=options, multiple=True, mode=SelectSelectorMode.LIST)
                ),
            }),
        )

    async def async_step_update_tmdb(self, user_input=None):
        errors: dict[str, str] = {}
        current = self.config_entry.data

        if not self._regions:
            api_key = current.get(CONF_TMDB_API_KEY, "")
            if api_key:
                session = async_get_clientsession(self.hass)
                self._regions = await _fetch_regions(session, api_key)

        if user_input is not None:
            api_key  = user_input.get(CONF_TMDB_API_KEY, "").strip()
            country  = str(user_input.get(CONF_COUNTRY, "ES")).strip().upper()
            language = _language_from(country, user_input.get(CONF_LANGUAGE) or "")

            if api_key:
                session = async_get_clientsession(self.hass)
                if not await _validate_tmdb_key(session, api_key):
                    errors["base"] = "invalid_tmdb_key"
                else:
                    self._regions  = await _fetch_regions(session, api_key)
                    new_providers  = await _fetch_providers(session, api_key, country, language)
                    new_data = dict(current)
                    new_data.update({
                        CONF_TMDB_API_KEY:  api_key,
                        CONF_COUNTRY:       country,
                        CONF_LANGUAGE:      language,
                        CONF_PROVIDER_MAP:  new_providers,
                    })
                    self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
                    return self.async_create_entry(title="", data={})
            else:
                new_data = dict(current)
                new_data.update({CONF_TMDB_API_KEY: "", CONF_COUNTRY: country, CONF_LANGUAGE: language})
                self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
                return self.async_create_entry(title="", data={})

        options = self._regions or [
            {"value": "ES", "label": "\U0001f1ea\U0001f1f8 Spain"},
            {"value": "US", "label": "\U0001f1fa\U0001f1f8 United States"},
        ]

        return self.async_show_form(
            step_id="update_tmdb",
            errors=errors,
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_TMDB_API_KEY,
                    default=current.get(CONF_TMDB_API_KEY, ""),
                ): TextSelector(TextSelectorConfig(type=TextSelectorType.PASSWORD)),
                vol.Required(
                    CONF_COUNTRY,
                    default=current.get(CONF_COUNTRY, "ES"),
                ): SelectSelector(
                    SelectSelectorConfig(options=options, mode=SelectSelectorMode.DROPDOWN)
                ),
                vol.Optional(CONF_LANGUAGE): LanguageSelector(LanguageSelectorConfig()),
            }),
        )

    def _commit(self) -> None:
        new_data = dict(self.config_entry.data)
        new_data[CONF_SHOWS] = self._shows
        self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
        # Schedule reload as a background task so it runs after the flow closes
        self.hass.async_create_task(
            self.hass.config_entries.async_reload(self.config_entry.entry_id)
        )