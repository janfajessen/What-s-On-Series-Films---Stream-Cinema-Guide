"""Camera platform for What's On Series & Films — show poster images via TVmaze."""
from __future__ import annotations

import logging

import aiohttp
from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_SHOWS, DOMAIN
from .coordinator import TVmazeCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create one camera entity per tracked show."""
    coordinator: TVmazeCoordinator = entry.runtime_data["tvmaze"]
    entities = [
        ShowPosterCamera(coordinator, entry.entry_id, show["id"], show["name"])
        for show in entry.data.get(CONF_SHOWS, [])
    ]
    async_add_entities(entities)


class ShowPosterCamera(CoordinatorEntity[TVmazeCoordinator], Camera):
    _attr_has_entity_name = False  # full name already in _attr_name
    """Camera entity that serves the TVmaze show poster image."""

    _attr_is_streaming = False
    _attr_is_recording = False

    def __init__(
        self,
        coordinator: TVmazeCoordinator,
        entry_id: str,
        show_id: int,
        show_name: str,
    ) -> None:
        CoordinatorEntity.__init__(self, coordinator)
        Camera.__init__(self)
        self._show_id   = show_id
        self._show_name = show_name
        self._entry_id  = entry_id
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_tvmaze_{show_id}_poster"
        self._attr_name      = f"{show_name} Poster"
        self.entity_id       = f"camera.whatson_series_films_{show_name.lower().replace(' ','_').replace('-','_')}_poster"

    @property
    def device_info(self) -> DeviceInfo:
        show = self.coordinator.data.get(self._show_id, {}).get("show", {})
        return DeviceInfo(
            identifiers={(DOMAIN, f"tvmaze_{self._show_id}")},
            name=self._show_name,
            manufacturer="TVmaze",
            model=show.get("type", "Scripted"),
            entry_type=DeviceEntryType.SERVICE,
            configuration_url=(
                show.get("url") or f"https://www.tvmaze.com/shows/{self._show_id}"
            ),
        )

    @property
    def available(self) -> bool:
        return (
            self.coordinator.last_update_success
            and self._show_id in self.coordinator.data
        )

    def _poster_url(self) -> str | None:
        show  = self.coordinator.data.get(self._show_id, {}).get("show", {})
        image = show.get("image") or {}
        return image.get("original") or image.get("medium")

    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return the latest poster image bytes from TVmaze CDN."""
        url = self._poster_url()
        if not url:
            return None
        try:
            session = async_get_clientsession(self.hass)
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                resp.raise_for_status()
                return await resp.read()
        except Exception as err:
            _LOGGER.warning("Failed to fetch poster for %s: %s", self._show_name, err)
            return None
            