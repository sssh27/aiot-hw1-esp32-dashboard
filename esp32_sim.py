"""
ESP32 Simulator — esp32_sim.py
Mimics a WiFi-connected ESP32 with a DHT11 sensor.
Sends fake temperature + humidity readings every 5 seconds
via HTTP POST to the local Flask API.

Simulated ESP32 metadata:
  device_id  : ESP32-AIOT-001
  ssid       : HomeNetwork_5G
  ip_address : 192.168.1.42
"""

import requests
import random
import time

# ── Config ──────────────────────────────────────────────────
FLASK_URL  = "http://127.0.0.1:5000/sensor"
INTERVAL_S = 5          # seconds between readings

DEVICE_META = {
    "device_id":  "ESP32-AIOT-001",
    "ssid":       "HomeNetwork_5G",
    "ip_address": "192.168.1.42",
}
# ────────────────────────────────────────────────────────────


def read_dht11():
    """Return simulated DHT11 (temperature °C, humidity %)."""
    temperature = round(random.uniform(20.0, 35.0), 1)
    humidity    = round(random.uniform(45.0, 75.0), 1)
    return temperature, humidity


def main():
    print(f"[ESP32 Sim] Started — POSTing to {FLASK_URL} every {INTERVAL_S}s")
    print("[ESP32 Sim] Press Ctrl+C to stop.\n")

    while True:
        temp, hum = read_dht11()
        payload = {**DEVICE_META, "temperature": temp, "humidity": hum}

        try:
            resp = requests.post(FLASK_URL, json=payload, timeout=5)
            ts   = time.strftime("%H:%M:%S")
            print(f"[{ts}] POST {resp.status_code} | "
                  f"temp={temp:5.1f}°C  hum={hum:5.1f}%")
        except requests.exceptions.ConnectionError:
            print("[ESP32 Sim] ⚠  Flask not reachable — retrying in 5 s...")

        time.sleep(INTERVAL_S)


if __name__ == "__main__":
    main()
