"""What's On Series & Films — Home Assistant integration.

Combines:
  - TVmaze (no key required): per-show sensors for next/previous episode,
    status, network and a camera entity for the show poster.
  - TMDB (free API key required):
      · Weekly new movies & TV shows on selected streaming platforms.
      · Movies currently playing in cinemas (now_playing).
      · Upcoming cinema releases (upcoming).
"""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .coordinator import TMDBCoordinator, TVmazeCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor", "camera"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up What's On Series & Films from a config entry."""
    session = async_get_clientsession(hass)

    tvmaze_coordinator = TVmazeCoordinator(hass, entry, session)
    tmdb_coordinator   = TMDBCoordinator(hass, entry, session)

    await tvmaze_coordinator.async_config_entry_first_refresh()
    await tmdb_coordinator.async_config_entry_first_refresh()

    entry.runtime_data = {
        "tvmaze": tvmaze_coordinator,
        "tmdb":   tmdb_coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload when options / data change (show added or removed)."""
    await hass.config_entries.async_reload(entry)
    