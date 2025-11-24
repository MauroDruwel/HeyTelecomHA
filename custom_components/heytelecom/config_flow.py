import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class HeyTelecomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HeyTelecom."""
    VERSION = 1
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="HeyTelecom", data={})
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            errors=errors,
        )
