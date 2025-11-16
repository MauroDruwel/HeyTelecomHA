from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = []
    for product in coordinator.data.get("products", []):
        sensors.append(HeyTelecomUsageSensor(coordinator, product, "data"))
        sensors.append(HeyTelecomUsageSensor(coordinator, product, "calls"))
        sensors.append(HeyTelecomUsageSensor(coordinator, product, "sms_mms"))
    async_add_entities(sensors)

class HeyTelecomUsageSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, product, usage_type):
        super().__init__(coordinator)
        self._product = product
        self._usage_type = usage_type
        self._attr_name = f"{product['product_type']} {product['phone_number'] or product['product_id']} {usage_type}"
        self._attr_unique_id = f"heytelecom_{product['product_id']}_{usage_type}"

    @property
    def state(self):
        return self._product["usage"].get(self._usage_type, {}).get("used")

    @property
    def extra_state_attributes(self):
        return {
            "limit": self._product["usage"].get(self._usage_type, {}).get("limit"),
            "unlimited": self._product["usage"].get(self._usage_type, {}).get("unlimited"),
            "last_update": self._product["usage"].get(self._usage_type, {}).get("last_update"),
            "tariff": self._product.get("tariff"),
            "contract_start": self._product.get("contract", {}).get("start_date"),
            "price_per_month_eur": self._product.get("contract", {}).get("price_per_month_eur"),
        }
