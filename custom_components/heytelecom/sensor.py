"""Sensor platform for HeyTelecom integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HeyTelecomDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HeyTelecom sensors based on a config entry."""
    coordinator: HeyTelecomDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []

    # Account sensors
    entities.append(HeyTelecomLastSyncSensor(coordinator, entry))

    # Product sensors (for each mobile/internet product)
    for product in coordinator.data.get("products", []):
        product_id = product.get("id", "unknown")
        product_type = product.get("type", "unknown")

        if product_type == "mobile":
            # Data usage sensors
            entities.append(HeyTelecomDataUsedSensor(coordinator, entry, product))
            entities.append(HeyTelecomDataLimitSensor(coordinator, entry, product))
            entities.append(HeyTelecomDataPercentageSensor(coordinator, entry, product))

            # Calls sensor
            entities.append(HeyTelecomCallsUsedSensor(coordinator, entry, product))

            # SMS/MMS sensor
            entities.append(HeyTelecomSmsUsedSensor(coordinator, entry, product))

            # Contract info sensors
            entities.append(HeyTelecomTariffSensor(coordinator, entry, product))
            entities.append(HeyTelecomPriceSensor(coordinator, entry, product))

            # Period sensors
            entities.append(HeyTelecomPeriodStartSensor(coordinator, entry, product))
            entities.append(HeyTelecomPeriodEndSensor(coordinator, entry, product))

    # Billing sensors
    if "billing" in coordinator.data:
        entities.append(HeyTelecomInvoiceAmountSensor(coordinator, entry))
        entities.append(HeyTelecomInvoiceStatusSensor(coordinator, entry))

    async_add_entities(entities)


def get_product_device_info(entry: ConfigEntry, product: dict) -> DeviceInfo:
    """Get device info for a product."""
    product_id = product.get("id", "unknown")
    phone_number = product.get("phone_number", "")
    tariff = product.get("tariff", "Hey! Mobile")

    return DeviceInfo(
        identifiers={(DOMAIN, f"{entry.entry_id}_{product_id}")},
        name=f"Hey! {phone_number}" if phone_number else f"Hey! {product_id}",
        manufacturer="Hey! Telecom",
        model=tariff,
        configuration_url="https://my.heytelecom.be",
    )


def get_account_device_info(entry: ConfigEntry) -> DeviceInfo:
    """Get device info for the account."""
    return DeviceInfo(
        identifiers={(DOMAIN, f"{entry.entry_id}_account")},
        name="Hey! Telecom Account",
        manufacturer="Hey! Telecom",
        model="Account",
        configuration_url="https://my.heytelecom.be",
    )


class HeyTelecomBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for HeyTelecom sensors."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: HeyTelecomDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entry = entry


class HeyTelecomProductSensor(HeyTelecomBaseSensor):
    """Base class for product-related sensors."""

    def __init__(
        self,
        coordinator: HeyTelecomDataUpdateCoordinator,
        entry: ConfigEntry,
        product: dict,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._product_id = product.get("id", "unknown")
        self._attr_device_info = get_product_device_info(entry, product)

    def _get_product(self) -> dict | None:
        """Get the current product data."""
        for product in self.coordinator.data.get("products", []):
            if product.get("id") == self._product_id:
                return product
        return None


# === DATA USAGE SENSORS ===


class HeyTelecomDataUsedSensor(HeyTelecomProductSensor):
    """Sensor for data used."""

    _attr_name = "Data gebruikt"
    _attr_native_unit_of_measurement = UnitOfInformation.GIGABYTES
    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_state_class = SensorStateClass.TOTAL
    _attr_icon = "mdi:download"

    def __init__(self, coordinator, entry, product) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, product)
        self._attr_unique_id = f"{entry.entry_id}_{self._product_id}_data_used"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        product = self._get_product()
        if product:
            return product.get("usage", {}).get("data", {}).get("used")
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        product = self._get_product()
        if product:
            data = product.get("usage", {}).get("data", {})
            return {
                "last_update": data.get("last_update"),
                "unlimited": data.get("unlimited", False),
            }
        return {}


class HeyTelecomDataLimitSensor(HeyTelecomProductSensor):
    """Sensor for data limit."""

    _attr_name = "Data limiet"
    _attr_native_unit_of_measurement = UnitOfInformation.GIGABYTES
    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_icon = "mdi:database"

    def __init__(self, coordinator, entry, product) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, product)
        self._attr_unique_id = f"{entry.entry_id}_{self._product_id}_data_limit"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        product = self._get_product()
        if product:
            data = product.get("usage", {}).get("data", {})
            if data.get("unlimited"):
                return None
            return data.get("limit")
        return None


class HeyTelecomDataPercentageSensor(HeyTelecomProductSensor):
    """Sensor for data usage percentage."""

    _attr_name = "Data percentage"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:percent"

    def __init__(self, coordinator, entry, product) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, product)
        self._attr_unique_id = f"{entry.entry_id}_{self._product_id}_data_percentage"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        product = self._get_product()
        if product:
            data = product.get("usage", {}).get("data", {})
            if data.get("unlimited"):
                return None
            used = data.get("used")
            limit = data.get("limit")
            if used is not None and limit is not None and limit > 0:
                return round((used / limit) * 100, 1)
        return None


# === CALLS SENSOR ===


class HeyTelecomCallsUsedSensor(HeyTelecomProductSensor):
    """Sensor for calls used."""

    _attr_name = "Belminuten gebruikt"
    _attr_native_unit_of_measurement = "min"
    _attr_state_class = SensorStateClass.TOTAL
    _attr_icon = "mdi:phone"

    def __init__(self, coordinator, entry, product) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, product)
        self._attr_unique_id = f"{entry.entry_id}_{self._product_id}_calls_used"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        product = self._get_product()
        if product:
            return product.get("usage", {}).get("calls", {}).get("used")
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        product = self._get_product()
        if product:
            calls = product.get("usage", {}).get("calls", {})
            return {
                "last_update": calls.get("last_update"),
                "unlimited": calls.get("unlimited", False),
            }
        return {}


# === SMS/MMS SENSOR ===


class HeyTelecomSmsUsedSensor(HeyTelecomProductSensor):
    """Sensor for SMS/MMS used."""

    _attr_name = "SMS/MMS gebruikt"
    _attr_native_unit_of_measurement = "berichten"
    _attr_state_class = SensorStateClass.TOTAL
    _attr_icon = "mdi:message-text"

    def __init__(self, coordinator, entry, product) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, product)
        self._attr_unique_id = f"{entry.entry_id}_{self._product_id}_sms_used"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        product = self._get_product()
        if product:
            return product.get("usage", {}).get("sms_mms", {}).get("used")
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        product = self._get_product()
        if product:
            sms = product.get("usage", {}).get("sms_mms", {})
            return {
                "last_update": sms.get("last_update"),
                "unlimited": sms.get("unlimited", False),
            }
        return {}


# === CONTRACT SENSORS ===


class HeyTelecomTariffSensor(HeyTelecomProductSensor):
    """Sensor for tariff plan."""

    _attr_name = "Abonnement"
    _attr_icon = "mdi:card-account-details"

    def __init__(self, coordinator, entry, product) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, product)
        self._attr_unique_id = f"{entry.entry_id}_{self._product_id}_tariff"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        product = self._get_product()
        if product:
            return product.get("tariff")
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        product = self._get_product()
        if product:
            return {
                "phone_number": product.get("phone_number"),
                "contract_start": product.get("contract", {}).get("start_date"),
            }
        return {}


class HeyTelecomPriceSensor(HeyTelecomProductSensor):
    """Sensor for monthly price."""

    _attr_name = "Maandprijs"
    _attr_native_unit_of_measurement = "€"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_icon = "mdi:currency-eur"

    def __init__(self, coordinator, entry, product) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, product)
        self._attr_unique_id = f"{entry.entry_id}_{self._product_id}_price"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        product = self._get_product()
        if product:
            return product.get("contract", {}).get("price_per_month_eur")
        return None


# === PERIOD SENSORS ===


class HeyTelecomPeriodStartSensor(HeyTelecomProductSensor):
    """Sensor for billing period start."""

    _attr_name = "Periode start"
    _attr_icon = "mdi:calendar-start"

    def __init__(self, coordinator, entry, product) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, product)
        self._attr_unique_id = f"{entry.entry_id}_{self._product_id}_period_start"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        product = self._get_product()
        if product:
            return product.get("usage", {}).get("period", {}).get("start")
        return None


class HeyTelecomPeriodEndSensor(HeyTelecomProductSensor):
    """Sensor for billing period end."""

    _attr_name = "Periode einde"
    _attr_icon = "mdi:calendar-end"

    def __init__(self, coordinator, entry, product) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry, product)
        self._attr_unique_id = f"{entry.entry_id}_{self._product_id}_period_end"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        product = self._get_product()
        if product:
            return product.get("usage", {}).get("period", {}).get("end")
        return None


# === ACCOUNT SENSORS ===


class HeyTelecomLastSyncSensor(HeyTelecomBaseSensor):
    """Sensor for last sync time."""

    _attr_name = "Laatste synchronisatie"
    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:sync"

    def __init__(self, coordinator, entry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_last_sync"
        self._attr_device_info = get_account_device_info(entry)

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("account", {}).get("last_sync")


# === BILLING SENSORS ===


class HeyTelecomInvoiceAmountSensor(HeyTelecomBaseSensor):
    """Sensor for latest invoice amount."""

    _attr_name = "Laatste factuur bedrag"
    _attr_native_unit_of_measurement = "€"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_icon = "mdi:receipt"

    def __init__(self, coordinator, entry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_invoice_amount"
        self._attr_device_info = get_account_device_info(entry)

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        billing = self.coordinator.data.get("billing", {})
        return billing.get("latest_invoice", {}).get("amount_eur")

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        invoice = self.coordinator.data.get("billing", {}).get("latest_invoice", {})
        return {
            "invoice_id": invoice.get("invoice_id"),
            "date": invoice.get("date"),
            "due_date": invoice.get("due_date"),
            "paid": invoice.get("paid"),
        }


class HeyTelecomInvoiceStatusSensor(HeyTelecomBaseSensor):
    """Sensor for latest invoice status."""

    _attr_name = "Laatste factuur status"
    _attr_icon = "mdi:file-document-check"

    def __init__(self, coordinator, entry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_invoice_status"
        self._attr_device_info = get_account_device_info(entry)

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        billing = self.coordinator.data.get("billing", {})
        return billing.get("latest_invoice", {}).get("status")

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes."""
        invoice = self.coordinator.data.get("billing", {}).get("latest_invoice", {})
        return {
            "invoice_id": invoice.get("invoice_id"),
            "paid": invoice.get("paid"),
        }
