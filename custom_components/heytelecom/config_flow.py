"""Config flow for HeyTelecom integration."""
import voluptuous as vol
import aiohttp
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, CONF_HOST, CONF_PORT, DEFAULT_HOST, DEFAULT_PORT


class HeyTelecomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HeyTelecom."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            url = f"http://{host}:{port}"

            # Test connection
            try:
                session = async_get_clientsession(self.hass)
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Validate it's HeyTelecom data
                        if "provider" in data and "products" in data:
                            return self.async_create_entry(
                                title=f"Hey! Telecom ({host})",
                                data={CONF_HOST: host, CONF_PORT: port},
                            )
                        else:
                            errors["base"] = "invalid_response"
                    else:
                        errors["base"] = "cannot_connect"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default=DEFAULT_HOST): str,
                    vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
                }
            ),
            errors=errors,
        )
