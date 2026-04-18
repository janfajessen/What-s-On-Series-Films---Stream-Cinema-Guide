"""Diagnostics support for What's On Series & Films.

Go to Settings → Devices & Services → What's On Series & Films → ⋮ → Download diagnostics
to get a JSON report with coordinator state, config (API key redacted) and entity counts.
"""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_TMDB_API_KEY, CONF_SHOWS, CONF_PLATFORMS, CONF_COUNTRY
from .coordinator import TMDBCoordinator, TVmazeCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    tvmaze: TVmazeCoordinator = entry.runtime_data["tvmaze"]
    tmdb:   TMDBCoordinator   = entry.runtime_data["tmdb"]

    # Redact API key
    safe_data = dict(entry.data)
    if CONF_TMDB_API_KEY in safe_data and safe_data[CONF_TMDB_API_KEY]:
        safe_data[CONF_TMDB_API_KEY] = "**REDACTED**"

    # TVmaze summary
    tvmaze_summary = {}
    for show_id, show_data in (tvmaze.data or {}).items():
        show = show_data.get("show", {})
        tvmaze_summary[show_id] = {
            "name":             show.get("name"),
            "status":           show.get("status"),
            "has_next_episode": show_data.get("next_episode") is not None,
            "has_prev_episode": show_data.get("previous_episode") is not None,
            "tvmaze_url":       show.get("url"),
        }

    # TMDB summary
    tmdb_data = tmdb.data or {}
    tmdb_summary: dict[str, Any] = {}
    for platform in entry.data.get(CONF_PLATFORMS, []):
        pd = tmdb_data.get(platform, {})
        tmdb_summary[platform] = {
            "new_movies_count": len(pd.get("movies", [])),
            "new_shows_count":  len(pd.get("shows", [])),
            "logo_url":         tmdb_data.get("__logos__", {}).get(platform),
        }

    cinema = tmdb_data.get("__cinema__", {})
    now_playing = cinema.get("now_playing", [])
    upcoming    = cinema.get("upcoming", [])

    return {
        "config": safe_data,
        "tvmaze": {
            "last_update_success": tvmaze.last_update_success,
            "last_exception":      str(tvmaze.last_exception) if tvmaze.last_exception else None,
            "tracked_shows":       tvmaze_summary,
        },
        "tmdb": {
            "last_update_success":  tmdb.last_update_success,
            "last_exception":       str(tmdb.last_exception) if tmdb.last_exception else None,
            "streaming_platforms":  tmdb_summary,
            "cinema_now_playing":   len(now_playing),
            "cinema_upcoming":      len(upcoming),
            "cinema_region_fallback": any(m.get("region_fallback") for m in now_playing + upcoming),
            "logos_fetched":        len(tmdb_data.get("__logos__", {})),
        },
    }
    