from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    _LOGGER.debug("Coordinator data: %s", coordinator.data)
    sensors = []
    for product in coordinator.data.get("products", []):
        _LOGGER.debug("Product data: %s", product)
        sensors.append(HeyTelecomUsageSensor(coordinator, product, "data"))
        sensors.append(HeyTelecomUsageSensor(coordinator, product, "calls"))
        sensors.append(HeyTelecomUsageSensor(coordinator, product, "sms_mms"))
    async_add_entities(sensors)

class HeyTelecomUsageSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, product, usage_type):
        super().__init__(coordinator)
        self._product = product
        self._usage_type = usage_type
        
        # Safely get product info with fallbacks
        product_type = product.get('product_type', 'Unknown')
        phone_number = product.get('phone_number', '')
        product_id = product.get('product_id', 'unknown')
        
        self._attr_name = f"{product_type} {phone_number or product_id} {usage_type}"
        self._attr_unique_id = f"heytelecom_{product_id}_{usage_type}"

    @property
    def state(self):
        usage = self._product.get("usage", {})
        usage_data = usage.get(self._usage_type, {})
        return usage_data.get("used")

    @property
    def extra_state_attributes(self):
        usage = self._product.get("usage", {})
        usage_data = usage.get(self._usage_type, {})
        contract = self._product.get("contract", {})
        
        return {
            "limit": usage_data.get("limit"),
            "unlimited": usage_data.get("unlimited"),
            "last_update": usage_data.get("last_update"),
            "tariff": self._product.get("tariff"),
            "contract_start": contract.get("start_date"),
            "price_per_month_eur": contract.get("price_per_month_eur"),
        }
