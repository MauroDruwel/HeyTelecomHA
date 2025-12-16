<p align="center">
  <img width="1280" height="668" alt="HeyTelecom Banner" src="https://github.com/user-attachments/assets/1205a154-7325-4cb7-9629-fb793f4db80f" />
</p>


<h1 align="center">📱 Hey! Telecom for Home Assistant</h1>
<p align="center"><b>Because checking your data shouldn't require opening an app 📶</b></p>

<p align="center">
	<a href="#-quick-install">Quick Install</a> |
	<a href="#-how-it-works">How it Works</a> |
	<a href="#-sensors">Sensors</a> |
	<a href="#-issues">Issues</a>
</p>

---

> **Your Hey! Telecom usage data, right where it belongs, in Home Assistant.**

---


## ⚠️ Requirements

This integration requires the **Hey! Telecom Add-on** running as a local Docker container.  
👉 [Get the add-on here](https://github.com/MauroDruwel/addons)

---


## 📦 Quick Install

### Via HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=MauroDruwel&repository=HeyTelecomHA)

<details>
<summary>Or manually...</summary>

1. Open HACS → **Integrations** → **⋮** → **Custom repositories**
2. Add: `https://github.com/MauroDruwel/HeyTelecomHA`
3. Search "Hey! Telecom" → **Download**

</details>

### Manual Installation

```sh
cd /config/custom_components
git clone https://github.com/MauroDruwel/HeyTelecomHA.git heytelecom
```

### Then...

1. Restart Home Assistant
2. **Settings** → **Devices & Services** → **Add Integration** → "Hey! Telecom"
3. Done! 🎉

No YAML. Just click and go. ✨

---


## ⚙️ Configuration

During setup, you can configure:

| Option | Default | Description |
|--------|---------|-------------|
| Host | `23118c7a-heytelecom-addon` | Hostname of the add-on |
| Port | `8099` | Port the add-on runs on |
| Update interval | `30` min | How often to fetch new data (2-40320 min or 2 min-28 days) |

> 💡 **Tip:** The add-on scrapes the website, so don't set the interval too low. 30 minutes is a good balance.

---


## 🧠 How it Works

```
┌─────────────────┐      REST API       ┌──────────────────────┐      Playwright      ┌─────────────────┐
│  Home Assistant │  ◄────────────────► │  Hey! Telecom Add-on │  ◄─────────────────► │  Hey! Telecom   │
│   Integration   │       (JSON)        │   (Docker/Add-on)    │    (Headless Browser)│     Website     │
└─────────────────┘                     └──────────────────────┘                      └─────────────────┘
```

Here's the magic behind the scenes:

1. **The Add-on** runs as a local Docker container on your Home Assistant instance
2. **Playwright** (headless browser) logs into Hey! Telecom's portal and scrapes your account data
3. **REST API** serves the scraped data as clean JSON on a local endpoint
4. **This Integration** polls the API and transforms it into beautiful Home Assistant sensors

Why this architecture? Hey! Telecom doesn't have a public API (shocker 🙄), so I had to get creative. Playwright handles all the login flows, session management, and data extraction, so you don't have to.

---


## 📊 Sensors

Once configured, you'll get a bunch of sensors for each product on your account:

### 📶 Mobile Data
| Sensor | Description |
|--------|-------------|
| Data Used | Your current data consumption (GB) |
| Data Limit | Your bundle's data cap (GB) |
| Data Percentage | How close you are to the limit (%) |

### 📞 Calls & SMS
| Sensor | Description |
|--------|-------------|
| Call Minutes | Minutes used this period |
| SMS/MMS | Messages sent this period |

### 💰 Billing
| Sensor | Description |
|--------|-------------|
| Invoice Amount | Latest invoice total (€) |
| Invoice Status | Paid or pending |
| Invoice Date | When it was issued |
| Due Date | When you need to pay |

### 📋 Contract Info
| Sensor | Description |
|--------|-------------|
| Tariff | Your current plan |
| Monthly Price | What you're paying (€) |
| Contract Start | When it all began |
| Phone Number | Your number (duh) |

All sensors come with extra attributes for even more details. 🤓

---

## 🐛 Issues

Something broken? [Open an issue](https://github.com/MauroDruwel/HeyTelecomHA/issues) and let's fix it.

## 🤝 Contributing

Got a better API Solution? Found another entity to expose? PRs are welcome! Let's make this thing even better. 🎉

---

*Made with ❤️, milk, and a lot of trial and error.*

