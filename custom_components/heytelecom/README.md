# Hey! Telecom Home Assistant Integration

Custom integration voor Home Assistant om je Hey! Telecom data te monitoren.

## Features

Deze integratie haalt data op van een lokale server en maakt de volgende sensors aan:

### Per mobiel product:
- **Data gebruikt** - Hoeveel GB je hebt verbruikt
- **Data limiet** - Je data bundel limiet
- **Data percentage** - Percentage van je bundel verbruikt
- **Belminuten gebruikt** - Aantal belminuten verbruikt
- **SMS/MMS gebruikt** - Aantal verzonden berichten
- **Abonnement** - Je huidige tariefplan
- **Maandprijs** - Maandelijkse kosten
- **Periode start/einde** - Huidige factureringsperiode

### Account:
- **Laatste synchronisatie** - Wanneer data laatst is gesynct
- **Laatste factuur bedrag** - Bedrag van de laatste factuur
- **Laatste factuur status** - Betaalstatus

## Installatie

1. Kopieer de `heytelecom` folder naar je Home Assistant `custom_components` directory
2. Herstart Home Assistant
3. Ga naar Instellingen → Apparaten & Services → Integratie toevoegen
4. Zoek naar "Hey! Telecom"
5. Voer de host en poort in van je data server (standaard: `localhost:8099`)

## JSON Data Formaat

De integratie verwacht de volgende JSON structuur van de API:

```json
{
  "provider": "hey!",
  "account": {
    "last_sync": "2025-11-09T15:30:00"
  },
  "products": [
    {
      "id": "mobile_0412345678",
      "type": "mobile",
      "phone_number": "0412 34 56 78",
      "tariff": "Hey! Mobile Plus",
      "contract": {
        "start_date": "2024-01-15",
        "price_per_month_eur": 15.0
      },
      "usage": {
        "period": { "start": "2025-10-11", "end": "2025-11-11" },
        "data": { "used": 2.5, "limit": 10.0, "unlimited": false },
        "calls": { "used": 45.0, "unlimited": true },
        "sms_mms": { "used": 12, "unlimited": true }
      }
    }
  ],
  "billing": {
    "latest_invoice": {
      "invoice_id": "INV-20251101",
      "amount_eur": 15.0,
      "status": "betaald",
      "paid": true
    }
  }
}
```

## Configuratie

De integratie pollt standaard elke 30 minuten. Dit wordt door Home Assistant automatisch afgehandeld via de DataUpdateCoordinator.
