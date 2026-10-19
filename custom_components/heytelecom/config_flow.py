"""Config flow for HeyTelecom integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)

from .const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)


class HeyTelecomConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HeyTelecom."""

    VERSION = 2

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._reauth_entry: ConfigEntry | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            await self.async_set_unique_id(email)
            self._abort_if_unique_id_configured()

            try:
                from heytelecom import HeyTelecomClient
                from heytelecom.exceptions import APIError, AuthenticationError

                def _test_login():
                    client = HeyTelecomClient(email=email, password=password)
                    try:
                        client.login()
                        return True
                    except (APIError, AuthenticationError) as err:
                        _LOGGER.warning("Login test failed: %s", err)
                        return False
                    finally:
                        try:
                            client.close()
                        except Exception as err:  # noqa: BLE001
                            _LOGGER.debug("Error closing test client: %s", err)

                result = await self.hass.async_add_executor_job(_test_login)
                if result:
                    return self.async_create_entry(
                        title=f"Hey! Telecom ({email})",
                        data={
                            CONF_EMAIL: email,
                            CONF_PASSWORD: password,
                        },
                    )
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected error during login")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EMAIL): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )

    async def async_step_reauth(self, entry_data: dict[str, Any]) -> FlowResult:
        """Handle reauthorization request from Home Assistant."""
        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Dialog to update credentials."""
        errors: dict[str, str] = {}
        assert self._reauth_entry is not None

        if user_input is not None:
            email = self._reauth_entry.data[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            try:
                from heytelecom import HeyTelecomClient
                from heytelecom.exceptions import APIError, AuthenticationError

                def _test_login():
                    client = HeyTelecomClient(email=email, password=password)
                    try:
                        client.login()
                        return True
                    except (APIError, AuthenticationError) as err:
                        _LOGGER.warning("Reauth test failed: %s", err)
                        return False
                    finally:
                        try:
                            client.close()
                        except Exception as err:  # noqa: BLE001
                            _LOGGER.debug("Error closing test client: %s", err)

                result = await self.hass.async_add_executor_job(_test_login)
                if result:
                    return self.async_update_reload_and_abort(
                        self._reauth_entry,
                        data={
                            **self._reauth_entry.data,
                            CONF_PASSWORD: password,
                        },
                    )
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected error during reauth")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_PASSWORD): str}),
            description_placeholders={
                "email": self._reauth_entry.data.get(CONF_EMAIL, "")
            },
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> HeyTelecomOptionsFlow:
        """Return the options flow."""
        return HeyTelecomOptionsFlow()


class HeyTelecomOptionsFlow(OptionsFlow):
    """Options flow to configure the poll interval."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the poll-interval option."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        current = self.config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )
        schema = vol.Schema(
            {
                vol.Required(CONF_SCAN_INTERVAL, default=current): NumberSelector(
                    NumberSelectorConfig(
                        min=MIN_SCAN_INTERVAL,
                        max=MAX_SCAN_INTERVAL,
                        step=1,
                        unit_of_measurement="min",
                        mode=NumberSelectorMode.BOX,
                    )
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
