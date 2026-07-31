"""DataUpdateCoordinator for HeyTelecom."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class HeyTelecomDataUpdateCoordinator(DataUpdateCoordinator[dict]):
    """Class to manage fetching HeyTelecom data."""

    def __init__(
        self, hass: HomeAssistant, entry: ConfigEntry, client
    ) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.client = client
        self.last_update_time: datetime | None = None

        try:
            scan_interval = int(entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
        except (ValueError, TypeError):
            scan_interval = DEFAULT_SCAN_INTERVAL

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from HeyTelecom API."""
        try:
            data = await self.hass.async_add_executor_job(
                self._fetch_data
            )
            self.last_update_time = dt_util.now()
            return data
        except Exception as err:
            raise UpdateFailed(f"Error fetching HeyTelecom data: {err}") from err

    def _fetch_data(self) -> dict:
        """Fetch data synchronously (runs in executor)."""
        account_data = self.client.get_account_data(use_cache=False)
        data = account_data.to_dict()

        # Add latest_invoice under "billing" key for backward compat with sensors
        if data.get("latest_invoice"):
            data["billing"] = {"latest_invoice": data["latest_invoice"]}

        return data