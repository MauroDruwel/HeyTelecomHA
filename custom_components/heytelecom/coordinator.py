"""DataUpdateCoordinator for HeyTelecom."""
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class HeyTelecomDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching HeyTelecom data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self._email = entry.data[CONF_EMAIL]
        self._password = entry.data[CONF_PASSWORD]
        scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

        self.client = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from HeyTelecom API."""
        try:
            from heytelecom import HeyTelecomClient

            def _fetch():
                if self.client is None:
                    self.client = HeyTelecomClient(
                        email=self._email, password=self._password
                    )
                    self.client.login()
                else:
                    self.client._ensure_token()
                return self.client.get_account_data().to_dict()

            return await self.hass.async_add_executor_job(_fetch)
        except Exception as err:
            self.client = None
            raise UpdateFailed(f"Error fetching HeyTelecom data: {err}") from err
