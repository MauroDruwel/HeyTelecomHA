"""Tests for HeyTelecom config and options flow."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from homeassistant.config_entries import SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.heytelecom.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    DOMAIN,
)


async def test_flow_user_success(hass: HomeAssistant) -> None:
    """Test successful user step configuration."""
    with patch("heytelecom.HeyTelecomClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client.login.return_value = True
        mock_client_cls.return_value = mock_client

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}
        )
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "user"

        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_EMAIL: "new@example.com",
                CONF_PASSWORD: "secret_password",
            },
        )
        assert result2["type"] is FlowResultType.CREATE_ENTRY
        assert result2["title"] == "Hey! Telecom (new@example.com)"
        assert result2["data"][CONF_EMAIL] == "new@example.com"


async def test_flow_user_invalid_auth(hass: HomeAssistant) -> None:
    """Test invalid credentials error."""
    with patch("heytelecom.HeyTelecomClient") as mock_client_cls:
        from heytelecom.exceptions import AuthenticationError

        mock_client = MagicMock()
        mock_client.login.side_effect = AuthenticationError("Unauthorized")
        mock_client_cls.return_value = mock_client

        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}
        )
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_EMAIL: "bad@example.com",
                CONF_PASSWORD: "wrong",
            },
        )
        assert result2["type"] is FlowResultType.FORM
        assert result2["errors"]["base"] == "invalid_auth"


async def test_options_flow(hass: HomeAssistant, mock_config_entry) -> None:
    """Test updating scan interval in options flow."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(mock_config_entry.entry_id)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    result2 = await hass.config_entries.options.async_configure(
        result["flow_id"],
        {CONF_SCAN_INTERVAL: 60},
    )
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert mock_config_entry.options[CONF_SCAN_INTERVAL] == 60
