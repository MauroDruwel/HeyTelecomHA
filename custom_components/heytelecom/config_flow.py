"""Config flow for HeyTelecom integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries

from .const import (
    DOMAIN,
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
    MAX_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class HeyTelecomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HeyTelecom."""

    VERSION = 2

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]
            scan_interval = user_input[CONF_SCAN_INTERVAL]

            try:
                from heytelecom import HeyTelecomClient

                def _test_login():
                    client = HeyTelecomClient(email=email, password=password)
                    try:
                        client.login()
                        client.close()
                        return True
                    except Exception as err:
                        _LOGGER.warning("Login test failed: %s", err)
                        return False

                result = await self.hass.async_add_executor_job(_test_login)
                if result:
                    return self.async_create_entry(
                        title=f"Hey! Telecom ({email})",
                        data={
                            CONF_EMAIL: email,
                            CONF_PASSWORD: password,
                            CONF_SCAN_INTERVAL: scan_interval,
                        },
                    )
                else:
                    errors["base"] = "invalid_auth"
            except Exception as err:
                _LOGGER.exception("Unexpected error during login: %s", err)
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                    vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
                        int, vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL)
                    ),
                }
            ),
            errors=errors,
        )
