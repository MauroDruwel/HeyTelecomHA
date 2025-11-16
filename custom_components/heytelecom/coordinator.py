from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN
import async_timeout
import logging

_LOGGER = logging.getLogger(__name__)

class HeyTelecomDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, email: str, password: str):
        super().__init__(
            hass,
            _LOGGER,
            name="HeyTelecom data",
            update_interval=timedelta(minutes=30),
        )
        self.email = email
        self.password = password

    async def _async_update_data(self):
        import heytelecom
        async with async_timeout.timeout(30):
            client = heytelecom.HeyTelecomClient(email=self.email, password=self.password)
            client.login()
            account_data = client.get_account_data()
            return account_data.to_dict()
