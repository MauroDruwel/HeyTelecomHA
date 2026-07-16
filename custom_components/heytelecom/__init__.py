"""HeyTelecom integration for Home Assistant."""
from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD
from .coordinator import HeyTelecomDataUpdateCoordinator

if TYPE_CHECKING:
    pass

PLATFORMS = ["sensor"]

type HeyTelecomConfigEntry = ConfigEntry[HeyTelecomDataUpdateCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: HeyTelecomConfigEntry) -> bool:
    """Set up HeyTelecom from a config entry."""
    from heytelecom import HeyTelecomClient

    def _create_client():
        client = HeyTelecomClient(
            email=entry.data[CONF_EMAIL],
            password=entry.data[CONF_PASSWORD],
        )
        client.login()
        return client

    client = await hass.async_add_executor_job(_create_client)

    coordinator = HeyTelecomDataUpdateCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    entry.async_on_unload(lambda: _close_client(client))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: HeyTelecomConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


def _close_client(client):
    """Close the HeyTelecom client session."""
    try:
        client.close()
    except Exception:
        pass
