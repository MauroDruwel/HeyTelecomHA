"""
HeyTelecom integration for Home Assistant
"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .coordinator import HeyTelecomDataUpdateCoordinator

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the heytelecom integration via configuration.yaml (not used)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up heytelecom from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    coordinator = HeyTelecomDataUpdateCoordinator(
        hass,
        email=entry.data["email"],
        password=entry.data["password"],
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
