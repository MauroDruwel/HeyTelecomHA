"""DataUpdateCoordinator for HeyTelecom."""
from datetime import timedelta
import logging

import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class HeyTelecomDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching HeyTelecom data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        host = entry.data[CONF_HOST]
        port = entry.data[CONF_PORT]
        scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        self.url = f"http://{host}:{port}"

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from HeyTelecom API."""
        session = async_get_clientsession(self.hass)
        try:
            async with async_timeout.timeout(120):
                async with session.get(self.url) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching data: {response.status}")
                    data = await response.json()
                    _LOGGER.debug("Received data from %s: %s", self.url, data)
                    return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
