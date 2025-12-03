"""Config flow for HeyTelecom integration."""
import logging
import voluptuous as vol
import aiohttp
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
    MAX_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class HeyTelecomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HeyTelecom."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            scan_interval = user_input[CONF_SCAN_INTERVAL]
            url = f"http://{host}:{port}"

            # Test connection (optional - continue even if it fails)
            try:
                session = async_get_clientsession(self.hass)
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=120)) as response:
                    if response.status == 200:
                        data = await response.json()
                        _LOGGER.debug("Received data from %s: %s", url, data)
                        # Validate it's HeyTelecom data
                        if "products" in data:
                            return self.async_create_entry(
                                title=f"Hey! Telecom ({host})",
                                data={
                                    CONF_HOST: host,
                                    CONF_PORT: port,
                                    CONF_SCAN_INTERVAL: scan_interval,
                                },
                            )
                        else:
                            errors["base"] = "invalid_response"
                    else:
                        _LOGGER.warning("Got status %s from %s", response.status, url)
                        errors["base"] = "cannot_connect"
            except aiohttp.ClientError as err:
                _LOGGER.warning("Connection error to %s: %s", url, err)
                errors["base"] = "cannot_connect"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected error connecting to %s: %s", url, err)
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                    vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                    vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
                        int, vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL)
                    ),
                }
            ),
            errors=errors,
        )
