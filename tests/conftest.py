"""Fixtures for HeyTelecom tests."""
from __future__ import annotations

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.heytelecom.const import (
    CONF_EMAIL,
    CONF_PASSWORD,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
)

@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations: None,
) -> Generator[None]:
    """Enable loading of the custom integration in every test."""
    yield


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return a mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Hey! Telecom (user@example.com)",
        data={
            CONF_EMAIL: "user@example.com",
            CONF_PASSWORD: "secret_password",
        },
        options={
            CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
        },
        entry_id="heytelecom_test_entry_id",
        unique_id="user@example.com",
        version=2,
    )


@pytest.fixture
def mock_heytelecom_client() -> Generator[MagicMock]:
    """Patch HeyTelecomClient."""
    with patch("heytelecom.HeyTelecomClient") as mock_cls:
        client = MagicMock()
        client.login.return_value = True
        client.close.return_value = None
        client.get_accounts.return_value = [
            MagicMock(account_id="acc_1", name="Mobile Subscription")
        ]
        mock_cls.return_value = client
        yield client
