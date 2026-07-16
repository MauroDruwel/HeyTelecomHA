"""DataUpdateCoordinator for HeyTelecom."""
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class HeyTelecomDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching HeyTelecom data."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, client
    ) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.client = client

        scan_interval = int(entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from HeyTelecom API."""
        try:
            return await self.hass.async_add_executor_job(
                self._fetch_data
            )
        except Exception as err:
            raise UpdateFailed(f"Error fetching HeyTelecom data: {err}") from err

    def _fetch_data(self) -> dict:
        """Fetch data synchronously (runs in executor)."""
        self.client._ensure_token()
        return self.client.get_account_data().to_dict()
