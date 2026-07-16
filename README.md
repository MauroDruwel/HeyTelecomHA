<p align="center">
  <img width="1280" height="668" alt="HeyTelecom Banner" src="https://github.com/user-attachments/assets/1205a154-7325-4cb7-9629-fb793f4db80f" />
</p>


<h1 align="center">Hey! Telecom for Home Assistant</h1>
<p align="center"><b>Your usage data, directly in Home Assistant.</b></p>

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

- **Home Assistant 2022.8+**
- A **Hey! Telecom** account (email + password)
- The [`heytelecom`](https://pypi.org/project/heytelecom/) Python package (installed automatically)

No Docker add-on required. No headless browser. Just pure HTTP.

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

## Configuration

During setup, you can configure:

| Option | Default | Description |
|--------|---------|-------------|
| Email | (required) | Your Hey! Telecom account email |
| Password | (required) | Your Hey! Telecom account password |
| Update interval | `30` min | How often to fetch new data (2-40320 min) |

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

Once configured, you'll get sensors for each product on your account:

### Mobile Data
| Sensor | Description |
|--------|-------------|
| Data Used | Your current data consumption (GB) |
| Data Limit | Your bundle's data cap (GB) |
| Data Percentage | How close you are to the limit (%) |

### Calls & SMS
| Sensor | Description |
|--------|-------------|
| Call Minutes | Minutes used this period |
| SMS/MMS | Messages sent this period |

### Billing
| Sensor | Description |
|--------|-------------|
| Invoice Amount | Latest invoice total |
| Invoice Status | Paid or pending |
| Invoice Date | When it was issued |
| Due Date | When you need to pay |

### Contract Info
| Sensor | Description |
|--------|-------------|
| Tariff | Your current plan |
| Monthly Price | What you're paying |
| Contract Start | When it all began |
| Phone Number | Your number |

---

## Issues

Something broken? [Open an issue](https://github.com/MauroDruwel/HeyTelecomHA/issues) and let's fix it.

## Contributing

PRs are welcome! Let's make this thing even better.

---

*Made with love and a lot of trial and error.*
