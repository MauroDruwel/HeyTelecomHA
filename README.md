
# HeyTelecom Home Assistant Integration

Integrate your HeyTelecom account with [Home Assistant](https://www.home-assistant.io/) to monitor your usage, account, and invoice data directly from your smart home dashboard.

## Features
- Sensors for each product (mobile/internet): data, calls, and SMS usage
- Account and invoice information as sensor attributes
- Easy configuration via the Home Assistant UI

## Requirements
- Home Assistant 2022.0 or newer
- Python package: `heytelecom` (installed automatically)

## Installation
1. Download or clone this repository.
2. Copy the `heytelecom` folder into your Home Assistant `custom_components` directory:
	- Example: `/config/custom_components/heytelecom`
3. Restart Home Assistant.
4. In Home Assistant, go to **Settings > Devices & Services > Add Integration** and search for "HeyTelecom".
5. Enter your HeyTelecom credentials in the setup form.

## Usage
Once configured, new sensors will be available in Home Assistant for each HeyTelecom product (mobile, internet, etc.).

You can add these sensors to your dashboard to monitor:
- Data usage
- Call and SMS usage
- Account and invoice details

## Configuration
All configuration is handled via the Home Assistant UI (Config Flow). No YAML configuration is required.

## Support
For issues, feature requests, or questions, please open an [issue on GitHub](https://github.com/MauroDruwel/HeyTelecomHA/issues).

---
This project is not affiliated with or endorsed by HeyTelecom or Home Assistant.
