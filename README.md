<p align="center">
  <img width="1280" height="668" alt="HeyTelecom Banner" src="https://github.com/user-attachments/assets/1205a154-7325-4cb7-9629-fb793f4db80f" />
</p>

<h1 align="center">Hey! Telecom for Home Assistant</h1>
<p align="center"><b>Your mobile usage data, directly in Home Assistant.</b></p>

<p align="center">
  <a href="#quick-install">Quick Install</a> |
  <a href="#how-it-works">How it Works</a> |
  <a href="#sensors">Sensors</a> |
  <a href="#issues">Issues</a>
</p>

<p align="center">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/heytelecom"/>
  <img alt="License" src="https://img.shields.io/github/license/MauroDruwel/HeyTelecomHA"/>
</p>

---

> **Your Hey! Telecom usage data, right where it belongs, in Home Assistant.**

---

## Requirements

- **Home Assistant 2024.8+**
- A **Hey! Telecom** account (email + password)
- The [`heytelecom`](https://pypi.org/project/heytelecom/) Python package (installed automatically)

No Docker add-on required. No headless browser. Just pure HTTP + OAuth2/PKCE.

---

## Quick Install

### Via HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=MauroDruwel&repository=HeyTelecomHA)

<details>
<summary>Or manually...</summary>

1. Open HACS -> **Integrations** -> **...** -> **Custom repositories**
2. Add: `https://github.com/MauroDruwel/HeyTelecomHA`
3. Search "Hey! Telecom" -> **Download**

</details>

### Manual Installation

```sh
cd /config/custom_components
git clone https://github.com/MauroDruwel/HeyTelecomHA.git heytelecom
```

### Then...

1. Restart Home Assistant
2. **Settings** -> **Devices & Services** -> **Add Integration** -> "Hey! Telecom"
3. Enter your email and password
4. Done!

---

## How it Works

```
+-----------------+     heytelecom lib      +------------------+
|  Home Assistant | <-----(OAuth2)---------> |  Hey! Telecom    |
|   Integration   |      (PKCE flow)        |     API          |
+-----------------+                          +------------------+
```

1. The integration authenticates via the same OAuth2/PKCE flow the web app uses
2. It calls the same BFF JSON APIs to fetch products, usage, and invoices
3. All data is transformed into Home Assistant sensors automatically

No browser, no scraping, no Docker add-on. Just the `heytelecom` Python library talking directly to the API.

---

## Sensors

Once configured, you'll get sensors for each mobile product on your account:

### Usage (Mobile)

| Sensor | Unit | Description | Source |
|--------|------|-------------|--------|
| Data Used | GB | Current data consumption | `/usage` endpoint |
| Data Limit | GB | Monthly data allowance | `/usage` endpoint |
| Data Percentage | % | Usage percentage (used/limit) | computed |
| Calls Used | min | Call minutes this period | `/usage` endpoint |
| SMS/MMS Used | messages | Messages sent this period | `/usage` endpoint |
| Period Start | — | Billing period start date | `/usage` endpoint |
| Period End | — | Billing period end date | `/usage` endpoint |

### Contract

| Sensor | Unit | Description | Source |
|--------|------|-------------|--------|
| Tariff | — | Your current plan name | `/productInventory` |
| Monthly Price | EUR | Monthly subscription cost | `/productInventory` |
| Phone Number | — | Your mobile number | `/productInventory` |
| Easy Switch | — | Easy Switch code (internet only) | `/productInventory` |

### Billing

| Sensor | Unit | Description | Source |
|--------|------|-------------|--------|
| Invoice Amount | EUR | Latest invoice total | `/invoices/latest` |
| Invoice Status | — | Payment status (paid/pending) | `/invoices/latest` |
| Invoice Date | — | Invoice issue date | `/invoices/latest` |
| Due Date | — | Payment due date | `/invoices/latest` |

### System

| Sensor | Unit | Description | Source |
|--------|------|-------------|--------|
| Last Sync | — | Timestamp of last data fetch | coordinator |

---

## Configuration

### Initial Setup

You'll be asked for your **email** and **password**. The integration validates your credentials before saving.

### Options

After setup, you can configure the **poll interval** (how often to fetch new data):

1. Go to **Settings** -> **Devices & Services** -> **Hey! Telecom** -> **Configure**
2. Set the poll interval (default: 30 minutes)

> Tip: 30 minutes is a good balance. The API is rate-limited, so don't go too low.

---

## Issues

Something broken? [Open an issue](https://github.com/MauroDruwel/HeyTelecomHA/issues) and let's fix it.

## Contributing

PRs are welcome! Let's make this thing even better.

---

*Made with love and a lot of trial and error.*
