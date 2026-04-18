"""Sensor platform for What's On Series & Films."""
from __future__ import annotations

import logging
from datetime import date
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_COUNTRY, CONF_PLATFORMS, CONF_SHOWS, DOMAIN, NAME
from .coordinator import TMDBCoordinator, TVmazeCoordinator

_LOGGER = logging.getLogger(__name__)


# ── Platform setup ─────────────────────────────────────────────────────────────

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create all sensor entities."""
    tvmaze: TVmazeCoordinator = entry.runtime_data["tvmaze"]
    tmdb:   TMDBCoordinator   = entry.runtime_data["tmdb"]
    country: str = entry.data.get(CONF_COUNTRY, "XX").upper()

    entities: list[SensorEntity] = []

    # TVmaze: 4 sensors per tracked show — no country prefix (global)
    for show_meta in entry.data.get(CONF_SHOWS, []):
        sid  = show_meta["id"]
        name = show_meta["name"]
        entities.extend([
            ShowNextEpisodeSensor(tvmaze,     entry.entry_id, sid, name),
            ShowPreviousEpisodeSensor(tvmaze, entry.entry_id, sid, name),
            ShowStatusSensor(tvmaze,          entry.entry_id, sid, name),
            ShowNetworkSensor(tvmaze,         entry.entry_id, sid, name),
        ])

    # TMDB streaming: 2 sensors per platform, prefixed with country
    for platform in entry.data.get(CONF_PLATFORMS, []):
        entities.extend([
            TMDBNewMoviesSensor(tmdb, entry.entry_id, platform, country),
            TMDBNewShowsSensor(tmdb,  entry.entry_id, platform, country),
        ])

    # TMDB cinema: 2 sensors per entry, prefixed with country
    entities.extend([
        CinemaNowPlayingSensor(tmdb, entry.entry_id, country),
        CinemaUpcomingSensor(tmdb,   entry.entry_id, country),
    ])

    async_add_entities(entities)


# ── Shared DeviceInfo builders ─────────────────────────────────────────────────

def _tvmaze_device(show_id: int, show_name: str, show_data: dict) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, f"tvmaze_{show_id}")},
        name=show_name,
        manufacturer="TVmaze",
        model=show_data.get("type", "Scripted"),
        entry_type=DeviceEntryType.SERVICE,
        configuration_url=(
            show_data.get("url") or f"https://www.tvmaze.com/shows/{show_id}"
        ),
    )


def _tmdb_streaming_device(entry_id: str, country: str) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, f"{entry_id}_tmdb_streaming_{country}")},
        name=f"{NAME} — {country} Streaming",
        manufacturer="The Movie Database",
        entry_type=DeviceEntryType.SERVICE,
        configuration_url="https://www.themoviedb.org",
    )


def _tmdb_cinema_device(entry_id: str, country: str) -> DeviceInfo:
    return DeviceInfo(
        identifiers={(DOMAIN, f"{entry_id}_tmdb_cinema_{country}")},
        name=f"{NAME} — {country} Cinema",
        manufacturer="The Movie Database",
        entry_type=DeviceEntryType.SERVICE,
        configuration_url="https://www.themoviedb.org",
    )


# ── TVmaze sensors ─────────────────────────────────────────────────────────────

class _TVmazeBase(CoordinatorEntity[TVmazeCoordinator], SensorEntity):
    def __init__(self, coordinator: TVmazeCoordinator, entry_id: str,
                 show_id: int, show_name: str) -> None:
        super().__init__(coordinator)
        self._show_id   = show_id
        self._show_name = show_name
        self._entry_id  = entry_id

    def _show_data(self) -> dict:
        return self.coordinator.data.get(self._show_id, {})

    @property
    def device_info(self) -> DeviceInfo:
        return _tvmaze_device(self._show_id, self._show_name,
                              self._show_data().get("show", {}))

    @property
    def available(self) -> bool:
        return (self.coordinator.last_update_success
                and self._show_id in self.coordinator.data)


class ShowNextEpisodeSensor(_TVmazeBase):
    _attr_icon = "mdi:television-play"

    def __init__(self, coordinator, entry_id, show_id, show_name):
        super().__init__(coordinator, entry_id, show_id, show_name)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_tvmaze_{show_id}_next_episode"
        self._attr_name      = f"whatson_series_films {show_name} next episode"

    @property
    def native_value(self) -> str:
        ep = self._show_data().get("next_episode")
        return ep.get("name") or "TBA" if ep else "No upcoming episode"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        ep = self._show_data().get("next_episode")
        if not ep:
            return {}
        airdate = ep.get("airdate", "")
        days_until: int | None = None
        if airdate:
            try:
                days_until = (date.fromisoformat(airdate) - date.today()).days
            except ValueError:
                pass
        return {
            "season":         ep.get("season"),
            "episode_number": ep.get("number"),
            "airdate":        airdate,
            "airtime":        ep.get("airtime"),
            "airstamp":       ep.get("airstamp"),
            "days_until_air": days_until,
            "summary":        ep.get("summary"),
        }


class ShowPreviousEpisodeSensor(_TVmazeBase):
    _attr_icon = "mdi:television-classic"

    def __init__(self, coordinator, entry_id, show_id, show_name):
        super().__init__(coordinator, entry_id, show_id, show_name)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_tvmaze_{show_id}_previous_episode"
        self._attr_name      = f"whatson_series_films {show_name} previous episode"

    @property
    def native_value(self) -> str:
        ep = self._show_data().get("previous_episode")
        return ep.get("name") or "N/A" if ep else "No previous episode"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        ep = self._show_data().get("previous_episode")
        if not ep:
            return {}
        return {
            "season":         ep.get("season"),
            "episode_number": ep.get("number"),
            "airdate":        ep.get("airdate"),
            "summary":        ep.get("summary"),
        }


class ShowStatusSensor(_TVmazeBase):
    _attr_icon            = "mdi:television-shimmer"
    _attr_translation_key = "show_status"

    def __init__(self, coordinator, entry_id, show_id, show_name):
        super().__init__(coordinator, entry_id, show_id, show_name)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_tvmaze_{show_id}_status"
        self._attr_name      = f"whatson_series_films {show_name} status"

    @property
    def native_value(self) -> str:
        return self._show_data().get("show", {}).get("status", "Unknown")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        show = self._show_data().get("show", {})
        return {
            "premiered": show.get("premiered"),
            "ended":     show.get("ended"),
            "language":  show.get("language"),
            "genres":    show.get("genres", []),
            "runtime":   show.get("runtime"),
            "rating":    (show.get("rating") or {}).get("average"),
            "summary":   show.get("summary"),
            "tvmaze_url": show.get("url"),
        }


class ShowNetworkSensor(_TVmazeBase):
    _attr_icon = "mdi:broadcast"

    def __init__(self, coordinator, entry_id, show_id, show_name):
        super().__init__(coordinator, entry_id, show_id, show_name)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_tvmaze_{show_id}_network"
        self._attr_name      = f"whatson_series_films {show_name} network"

    @property
    def native_value(self) -> str:
        show   = self._show_data().get("show", {})
        source = show.get("network") or show.get("webChannel") or {}
        return source.get("name", "Unknown")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        show        = self._show_data().get("show", {})
        network     = show.get("network") or {}
        web_channel = show.get("webChannel") or {}
        schedule    = show.get("schedule") or {}
        return {
            "network":          network.get("name"),
            "network_country":  (network.get("country") or {}).get("name"),
            "web_channel":      web_channel.get("name"),
            "schedule_days":    schedule.get("days", []),
            "schedule_time":    schedule.get("time"),
        }


# ── TMDB streaming sensors ─────────────────────────────────────────────────────

class _TMDBStreamingBase(CoordinatorEntity[TMDBCoordinator], SensorEntity):
    def __init__(self, coordinator: TMDBCoordinator, entry_id: str,
                 platform_name: str, country: str) -> None:
        super().__init__(coordinator)
        self._platform_name = platform_name
        self._entry_id      = entry_id
        self._country       = country.upper()
        self._slug = (platform_name.lower()
                      .replace(" ", "_").replace("+", "plus")
                      .replace("(", "").replace(")", ""))

    def _platform_data(self) -> dict:
        return self.coordinator.data.get(self._platform_name, {})

    @property
    def device_info(self) -> DeviceInfo:
        return _tmdb_streaming_device(self._entry_id, self._country)

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success


class TMDBNewMoviesSensor(_TMDBStreamingBase):
    _attr_icon                        = "mdi:movie-open"
    _attr_native_unit_of_measurement  = "movies"

    def __init__(self, coordinator, entry_id, platform_name, country):
        super().__init__(coordinator, entry_id, platform_name, country)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_{self._country.lower()}_tmdb_{self._slug}_new_movies"
        self._attr_name      = f"whatson_series_films {self._country} new movies on {platform_name}"

    @property
    def native_value(self) -> int:
        return len(self._platform_data().get("movies", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        logos = self.coordinator.data.get("__logos__", {})
        return {
            "movies":     self._platform_data().get("movies", []),
            "logo_url":   logos.get(self._platform_name),
            "platform":   self._platform_name,
        }


class TMDBNewShowsSensor(_TMDBStreamingBase):
    _attr_icon                        = "mdi:television-box"
    _attr_native_unit_of_measurement  = "titles"

    def __init__(self, coordinator, entry_id, platform_name, country):
        super().__init__(coordinator, entry_id, platform_name, country)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_{self._country.lower()}_tmdb_{self._slug}_new_shows"
        self._attr_name      = f"whatson_series_films {self._country} new series docs on {platform_name}"

    @property
    def native_value(self) -> int:
        return len(self._platform_data().get("shows", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        logos = self.coordinator.data.get("__logos__", {})
        return {
            "shows":    self._platform_data().get("shows", []),
            "logo_url": logos.get(self._platform_name),
            "platform": self._platform_name,
        }


# ── TMDB cinema sensors ────────────────────────────────────────────────────────

class _TMDBCinemaBase(CoordinatorEntity[TMDBCoordinator], SensorEntity):
    def __init__(self, coordinator: TMDBCoordinator,
                 entry_id: str, country: str) -> None:
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._country  = country.upper()

    def _cinema_data(self) -> dict:
        return self.coordinator.data.get("__cinema__", {})

    @property
    def device_info(self) -> DeviceInfo:
        return _tmdb_cinema_device(self._entry_id, self._country)

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success


class CinemaNowPlayingSensor(_TMDBCinemaBase):
    """Movies currently playing in cinemas in the configured country."""

    _attr_icon                        = "mdi:ticket-confirmation-outline"
    _attr_native_unit_of_measurement  = "movies"

    def __init__(self, coordinator, entry_id, country):
        super().__init__(coordinator, entry_id, country)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_{self._country.lower()}_cinema_now_playing"
        self._attr_name      = f"whatson_series_films {self._country} cinema now playing"

    @property
    def native_value(self) -> int:
        return len(self._cinema_data().get("now_playing", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        movies = self._cinema_data().get("now_playing", [])
        fallback = any(m.get("region_fallback") for m in movies)
        return {
            "movies":          movies,
            "region_fallback": fallback,
        }


class CinemaUpcomingSensor(_TMDBCinemaBase):
    """Movies coming soon to cinemas in the configured country."""

    _attr_icon                        = "mdi:movie-roll"
    _attr_native_unit_of_measurement  = "movies"

    def __init__(self, coordinator, entry_id, country):
        super().__init__(coordinator, entry_id, country)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_{self._country.lower()}_cinema_upcoming"
        self._attr_name      = f"whatson_series_films {self._country} cinema upcoming"

    @property
    def native_value(self) -> int:
        return len(self._cinema_data().get("upcoming", []))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        movies = self._cinema_data().get("upcoming", [])
        fallback = any(m.get("region_fallback") for m in movies)
        return {
            "movies":          movies,
            "region_fallback": fallback,
        }
        