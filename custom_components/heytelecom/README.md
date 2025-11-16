# HeyTelecom Home Assistant Integration

This custom integration connects your HeyTelecom account to Home Assistant, exposing usage and account data as sensors.

## Installation
1. Copy the `heytelecom` folder to your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Add the integration via the Home Assistant UI and enter your HeyTelecom credentials.

## Features
- Sensors for each product (mobile/internet): data, calls, sms usage
- Account and invoice info as attributes

## Requirements
- Python package: `heytelecom` (installed automatically)

## Configuration
Configuration is done via the Home Assistant UI (Config Flow).
