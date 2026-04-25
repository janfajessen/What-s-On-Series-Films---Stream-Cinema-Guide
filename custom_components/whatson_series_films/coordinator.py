"""Data update coordinators for What's On Series & Films."""
from __future__ import annotations

import logging
from datetime import date, timedelta

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_COUNTRY,
    CONF_LANGUAGE,
    CONF_PLATFORMS,
    CONF_PROVIDER_MAP,
    CONF_SHOWS,
    CONF_TMDB_API_KEY,
    DOMAIN,
    SCAN_INTERVAL_TMDB,
    SCAN_INTERVAL_TVMAZE,
    TMDB_BASE_URL,
    TMDB_IMAGE_BASE_URL,
    TMDB_IMAGE_ORIG_URL,
    TMDB_LOOKBACK_DAYS,
    TMDB_MAX_CINEMA_RESULTS,
    TMDB_MAX_RESULTS,
    TVMAZE_BASE_URL,
)

_LOGGER = logging.getLogger(__name__)


# ── TVmaze coordinator ────────────────────────────────────────────────────────

class TVmazeCoordinator(DataUpdateCoordinator[dict]):
    """Fetch data for all tracked TVmaze shows.

    Data shape:
        {
            <show_id: int>: {
                "show":             {...full TVmaze show object...},
                "next_episode":     {...episode object...} | None,
                "previous_episode": {...episode object...} | None,
            }, ...
        }
    """

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry,
                 session: aiohttp.ClientSession) -> None:
        super().__init__(hass, _LOGGER,
                         name=f"{DOMAIN}_tvmaze",
                         update_interval=SCAN_INTERVAL_TVMAZE)
        self._entry   = entry
        self._session = session

    async def _async_update_data(self) -> dict:
        shows: list[dict] = self._entry.data.get(CONF_SHOWS, [])
        if not shows:
            return {}

        data: dict = {}
        for show_meta in shows:
            show_id: int = show_meta["id"]
            try:
                url = (f"{TVMAZE_BASE_URL}/shows/{show_id}"
                       "?embed[]=nextepisode&embed[]=previousepisode")
                async with self._session.get(
                    url, timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    resp.raise_for_status()
                    payload: dict = await resp.json()

                embedded = payload.get("_embedded", {})
                data[show_id] = {
                    "show":             payload,
                    "next_episode":     embedded.get("nextepisode"),
                    "previous_episode": embedded.get("previousepisode"),
                }
            except Exception as err:
                _LOGGER.warning("TVmaze error for show %s (%s): %s",
                                show_id, show_meta.get("name"), err)
                data.setdefault(show_id, {
                    "show":             {"id": show_id, "name": show_meta.get("name", "")},
                    "next_episode":     None,
                    "previous_episode": None,
                })

        return data


# ── TMDB coordinator ──────────────────────────────────────────────────────────

class TMDBCoordinator(DataUpdateCoordinator[dict]):
    """Fetch TMDB data: streaming new releases + cinema programmes.

    Data shape:
        {
            # One key per selected streaming platform
            "<Platform Name>": {
                "movies": [...],
                "shows":  [...],
            },

            # Cinema block — always present when API key is set
            "__cinema__": {
                "now_playing": [...],   # currently in cinemas
                "upcoming":    [...],   # coming soon to cinemas
            },

            # Provider logos fetched once from TMDB
            "__logos__": {
                "<Platform Name>": "<full logo URL>",
                ...
            },
        }

    Each movie/show item:
        {
            "title":        str,
            "release_date": str,      # YYYY-MM-DD
            "genre_ids":    list[int],
            "vote_average": float,
            "poster_url":   str | None,
            "overview":     str,
            "tmdb_id":      int,
        }
    """

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry,
                 session: aiohttp.ClientSession) -> None:
        super().__init__(hass, _LOGGER,
                         name=f"{DOMAIN}_tmdb",
                         update_interval=SCAN_INTERVAL_TMDB)
        self._entry   = entry
        self._session = session

    async def _async_update_data(self) -> dict:
        api_key:      str            = self._entry.data.get(CONF_TMDB_API_KEY, "").strip()
        country:      str            = self._entry.data.get(CONF_COUNTRY, "US").strip().upper()
        language:     str            = self._entry.data.get(CONF_LANGUAGE, "en-US")
        platforms:    list[str]      = self._entry.data.get(CONF_PLATFORMS, [])
        provider_map: dict[str, int] = self._entry.data.get(CONF_PROVIDER_MAP, {})

        if not api_key:
            return {}

        data: dict = {}

        # ── Streaming platforms: new movies & shows ──────────────────────────
        today    = date.today()
        date_gte = (today - timedelta(days=TMDB_LOOKBACK_DAYS)).strftime("%Y-%m-%d")
        date_lte = today.strftime("%Y-%m-%d")

        for platform_name in platforms:
            provider_id = provider_map.get(platform_name)
            if provider_id is None:
                _LOGGER.warning("No provider ID for '%s' — skipping.", platform_name)
                continue

            # Date-filtered: new releases added in the last TMDB_LOOKBACK_DAYS
            movies_new = await self._discover(
                api_key, country, language, provider_id, "movie", date_gte, date_lte)
            shows_new  = await self._discover(
                api_key, country, language, provider_id, "tv",    date_gte, date_lte)

            # Popular: top content available now regardless of release date
            # (catches series like The Boys where first_air_date is old but
            # the latest season is on the platform)
            movies_pop = await self._discover_popular(
                api_key, country, language, provider_id, "movie")
            shows_pop  = await self._discover_popular(
                api_key, country, language, provider_id, "tv")

            # Merge: new releases first, then popular items not already present
            seen_ids: set[int] = set()
            movies: list[dict] = []
            shows:  list[dict] = []
            for item in movies_new + movies_pop:
                if item["tmdb_id"] not in seen_ids:
                    seen_ids.add(item["tmdb_id"])
                    movies.append(item)
            seen_ids.clear()
            for item in shows_new + shows_pop:
                if item["tmdb_id"] not in seen_ids:
                    seen_ids.add(item["tmdb_id"])
                    shows.append(item)

            data[platform_name] = {"movies": movies[:TMDB_MAX_RESULTS],
                                   "shows":  shows[:TMDB_MAX_RESULTS]}

        # ── Cinema: now playing + upcoming ───────────────────────────────────
        now_playing = await self._fetch_cinema(api_key, country, language, "now_playing")
        upcoming    = await self._fetch_cinema(api_key, country, language, "upcoming")
        data["__cinema__"] = {
            "now_playing": now_playing,
            "upcoming":    upcoming,
        }

        # ── Provider logos ───────────────────────────────────────────────────
        logos = await self._fetch_provider_logos(api_key, country, language, platforms, provider_map)
        data["__logos__"] = logos

        # ── Global weekly trending (no country/platform filter) ───────────────
        # Use user-configured language; HA frontend language as fallback
        ha_lang = getattr(self.hass.config, "language", "en")
        trend_language = language if language and language != "en-US" else (
            f"{ha_lang}-{ha_lang.upper()}" if "-" not in ha_lang else ha_lang
        )
        trending_films  = await self._fetch_trending(api_key, trend_language, "movie")
        trending_series = await self._fetch_trending(api_key, trend_language, "tv")
        data["__trending__"] = {
            "films":  trending_films,
            "series": trending_series,
        }

        return data

    # ── Private helpers ───────────────────────────────────────────────────────

    async def _discover(self, api_key: str, country: str, language: str,
                        provider_id: int, media_type: str,
                        date_gte: str, date_lte: str) -> list[dict]:
        """Call TMDB /discover and return normalised results."""
        date_field = ("primary_release_date" if media_type == "movie"
                      else "first_air_date")
        params = {
            "api_key":              api_key,
            "watch_region":         country,
            "language":             language,
            "with_watch_providers": str(provider_id),
            "sort_by":              f"{date_field}.desc",
            f"{date_field}.gte":    date_gte,
            f"{date_field}.lte":    date_lte,
            "page": 1,
        }
        return await self._get_results(
            f"{TMDB_BASE_URL}/discover/{media_type}", params, TMDB_MAX_RESULTS)

    async def _discover_popular(self, api_key: str, country: str, language: str,
                               provider_id: int, media_type: str) -> list[dict]:
        """Fetch top popular content on a platform (no date filter).

        Used to surface currently-popular content like running series whose
        first_air_date is old but whose latest season just dropped.
        Sorted by popularity descending.
        """
        params = {
            "api_key":              api_key,
            "watch_region":         country,
            "language":             language,
            "with_watch_providers": str(provider_id),
            "sort_by":              "popularity.desc",
            "page": 1,
        }
        results = await self._get_results(
            f"{TMDB_BASE_URL}/discover/{media_type}", params, TMDB_MAX_RESULTS)
        # Tag items so cards can distinguish new vs popular
        for item in results:
            item["source"] = "popular"
        return results

    async def _fetch_trending(self, api_key: str, language: str,
                              media_type: str) -> list[dict]:
        """Fetch global weekly trending movies or TV shows from TMDB.

        Uses /trending/{media_type}/week — no country or platform filter.
        Returns up to 20 items (one page = the natural size of a trending list).
        Items include a 'source': 'trending_week' tag.
        """
        params = {"api_key": api_key, "language": language}
        results = await self._get_results(
            f"{TMDB_BASE_URL}/trending/{media_type}/week", params, 20)
        for item in results:
            item["source"] = "trending_week"
        return results

    async def _fetch_cinema(self, api_key: str, country: str, language: str,
                            endpoint: str) -> list[dict]:
        """Fetch now_playing or upcoming cinema releases.

        Notes on regional availability:
          - Small countries (e.g. AD, LI, SM) may return 0 results because
            TMDB's regional release data relies on distributor submissions.
          - In that case the sensor state will be 0 — this is expected behaviour,
            not a bug. The fallback (no region filter) is NOT applied on purpose
            to avoid mixing unrelated releases.
        """
        params = {
            "api_key":  api_key,
            "region":   country,
            "language": language,
            "page":     1,
        }
        results = await self._get_results(
            f"{TMDB_BASE_URL}/movie/{endpoint}", params, TMDB_MAX_CINEMA_RESULTS)

        # If the country returned 0 results (small market like AD), try without
        # region filter so the sensor is at least populated with global data,
        # clearly labelled so the user knows.
        if not results:
            _LOGGER.debug(
                "Cinema %s: 0 results for region=%s, retrying without region.",
                endpoint, country)
            params_global = {"api_key": api_key, "language": language, "page": 1}
            results = await self._get_results(
                f"{TMDB_BASE_URL}/movie/{endpoint}", params_global,
                TMDB_MAX_CINEMA_RESULTS)
            # Mark items so the card can show a disclaimer
            for item in results:
                item["region_fallback"] = True

        return results

    async def _fetch_provider_logos(self, api_key: str, country: str, language: str,
                                    platforms: list[str],
                                    provider_map: dict[str, int]) -> dict[str, str]:
        """Return {platform_name: logo_url} for selected platforms.

        Fetches live from TMDB /watch/providers/movie using the stored provider_map
        for ID lookup — no hardcoded IDs needed.
        If the call fails, returns an empty dict (logo_url will be null in sensors).
        """
        logos: dict[str, str] = {}
        try:
            params = {"api_key": api_key, "watch_region": country, "language": language}
            url = f"{TMDB_BASE_URL}/watch/providers/movie"
            async with self._session.get(
                url, params=params, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                resp.raise_for_status()
                payload = await resp.json()

            id_to_logo: dict[int, str] = {
                p["provider_id"]: f"{TMDB_IMAGE_ORIG_URL}{p['logo_path']}"
                for p in payload.get("results", [])
                if p.get("provider_id") and p.get("logo_path")
            }
            for name in platforms:
                pid = provider_map.get(name)
                if pid and pid in id_to_logo:
                    logos[name] = id_to_logo[pid]

        except Exception as err:
            _LOGGER.warning(
                "Could not fetch provider logos from TMDB: %s. "
                "logo_url will be null until next update.", err
            )

        return logos

    async def _get_results(self, url: str, params: dict,
                           limit: int) -> list[dict]:
        """Generic TMDB GET → normalised item list.

        TMDB returns at most 20 results per page. When limit > 20 we fetch
        additional pages until we have enough results or run out of pages.
        Max pages fetched is capped at 3 to avoid excessive API calls.
        """
        collected: list[dict] = []
        page = 1
        total_pages = 1

        try:
            while len(collected) < limit and page <= total_pages:
                page_params = dict(params)
                page_params["page"] = page
                async with self._session.get(
                    url, params=page_params, timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    resp.raise_for_status()
                    payload = await resp.json()

                if page == 1:
                    total_pages = min(payload.get("total_pages", 1), 3)

                for item in payload.get("results", []):
                    if len(collected) >= limit:
                        break
                    collected.append({
                        "title":           item.get("title") or item.get("name", ""),
                        "release_date":    (item.get("release_date")
                                            or item.get("first_air_date", "")),
                        "genre_ids":       item.get("genre_ids", []),
                        "vote_average":    round(item.get("vote_average", 0.0), 1),
                        "poster_url":      (
                            f"{TMDB_IMAGE_BASE_URL}{item['poster_path']}"
                            if item.get("poster_path") else None
                        ),
                        "overview":        item.get("overview", ""),
                        "tmdb_id":         item.get("id"),
                        "region_fallback": False,
                    })
                page += 1

        except Exception as err:
            _LOGGER.warning("TMDB request failed (%s): %s", url, err)

        return collected
        