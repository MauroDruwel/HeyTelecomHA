from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN
import async_timeout
import logging

_LOGGER = logging.getLogger(__name__)

class HeyTelecomDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant):
        super().__init__(
            hass,
            _LOGGER,
            name="HeyTelecom data",
            update_interval=timedelta(minutes=30),
        )
        self.url = "http://local-heytelecom-addon:8099"

    async def _async_update_data(self):
        session = async_get_clientsession(self.hass)
        async with async_timeout.timeout(30):
            async with session.get(self.url) as response:
                response.raise_for_status()
                return await response.json()
