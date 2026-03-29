# HW1 AIoT System — ESP32 DHT11 Monitor

> **Course:** AIoT Systems | **Author:** Shawn | **Date:** 2026-03-17  
> **Stack:** ESP32 Simulator → Flask API → SQLite3 → Streamlit Dashboard

---

## 📐 Architecture

```
esp32_sim.py          flask_app.py          aiotdb.db         streamlit_app.py
(Fake DHT11 +   →    (Flask REST API  →    (SQLite3      →   (Live Dashboard
 ESP32 metadata)      port 5000)            sensors table)    port 8501)
   every 5s             POST /sensor          INSERT              SELECT *
```

---

## 📁 File Overview

| File | Purpose |
|---|---|
| `flask_app.py` | Flask REST API — receives ESP32 POSTs, stores to SQLite |
| `esp32_sim.py` | ESP32 + DHT11 simulator — sends fake readings every 5 s |
| `streamlit_app.py` | Real-time dashboard — KPIs, temperature chart, humidity chart |
| `requirements.txt` | Python dependencies |
| `aiotdb.db` | SQLite3 database (auto-created on first Flask run) |

---

## 🗄️ Database Schema

```sql
CREATE TABLE sensors (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id   TEXT    NOT NULL,
    ssid        TEXT,
    ip_address  TEXT,
    temperature REAL    NOT NULL,
    humidity    REAL    NOT NULL,
    timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🚀 Quick Start (Local)

### 1. Install dependencies
```powershell
pip install -r requirements.txt
```

### 2. Terminal 1 — Start Flask API
```powershell
python flask_app.py
# Serving on http://127.0.0.1:5000
```

### 3. Terminal 2 — Start ESP32 Simulator
```powershell
python esp32_sim.py
# POSTing to http://127.0.0.1:5000/sensor every 5 s
```

### 4. Terminal 3 — Start Streamlit Dashboard
```powershell
python -m streamlit run streamlit_app.py --server.port 8501
# Open http://localhost:8501
```

### 5. Verify health endpoint
```powershell
python -c "import urllib.request, json; r=urllib.request.urlopen('http://127.0.0.1:5000/health'); print(json.loads(r.read()))"
# → {"status": "ok", "db": "...aiotdb.db"}
```

---

## 📊 Dashboard Features

| Component | Description |
|---|---|
| **KPI Cards** | Total Readings, Avg Temp, Avg Humidity, Last Device |
| **Temperature Chart** | Line chart (red), time-indexed |
| **Humidity Chart** | Line chart (teal), time-indexed |
| **Raw Data Table** | Last 200 rows, expandable |
| **Auto-refresh** | Every 5 s (local) / manual button (Streamlit Cloud) |

---

## 🌐 Streamlit Cloud (Live Demo)

`streamlit_app.py` detects whether `aiotdb.db` exists.  
- **Local**: reads live SQLite data, auto-refreshes every 5 s  
- **Cloud**: generates simulated ESP32 readings (200 rows), refresh on button click  

**Deploy steps:**
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select repo → set **Main file path** to `streamlit_app.py`
4. Click **Deploy**

---

## 📡 ESP32 Payload Format

```json
{
  "device_id":   "ESP32-AIOT-001",
  "ssid":        "HomeNetwork_5G",
  "ip_address":  "192.168.1.42",
  "temperature": 23.5,
  "humidity":    49.6
}
```

---

## 📝 Development Log

### Step 1 — Project Setup
Created four Python files: `flask_app.py`, `esp32_sim.py`, `streamlit_app.py`, `requirements.txt`.

### Step 2 — Flask API
Implemented `/health`, `/sensor` (POST), `/sensors` (GET), `/sensors/count` (GET).  
SQLite3 DB and `sensors` table auto-initialized on startup via `init_db()`.

### Step 3 — ESP32 Simulator
`esp32_sim.py` uses `random.uniform()` for temperature (20–35°C) and humidity (45–75%).  
Metadata hardcoded to match a real ESP32: device ID, SSID, local IP.

### Step 4 — Flask Verified
`/health` → `{"status": "ok"}` ✅  
Continuous `HTTP 201` responses confirmed inserts working ✅

### Step 5 — DB Inserts Verified
Sample rows confirmed all fields stored correctly (device_id, ssid, ip_address, temp, humidity, timestamp) ✅

### Step 6 — Streamlit Dashboard
4 KPI cards + 2 line charts (temp red, humidity teal) + raw data table.  
Auto-refreshes every 5 s locally; simulated data fallback for Streamlit Cloud ✅

### Step 7 — Deployment
Pushed to GitHub → deployed to Streamlit Cloud ✅

---

## 🔗 Links

- **GitHub Repo:** _(add your repo URL here)_
- **Live Demo:** _(add your Streamlit Cloud URL here)_
