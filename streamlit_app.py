"""
Streamlit Dashboard — streamlit_app.py

Dual-mode operation:
  LOCAL MODE  — reads live data from SQLite3 (aiotdb.db) created by flask_app.py
  CLOUD MODE  — generates simulated ESP32/DHT11 data when no DB is found
                (for deployment on Streamlit Cloud)

Run locally:
    streamlit run streamlit_app.py

Deploy to Streamlit Cloud:
    Push this repo to GitHub → connect at share.streamlit.io
"""

import streamlit as st
import pandas as pd
import sqlite3
import os
import random
from datetime import datetime, timedelta

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="AIoT ESP32 Dashboard",
    page_icon="🌡️",
    layout="wide",
)

# ── Helper: detect local DB ──────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "aiotdb.db")


def load_from_sqlite() -> pd.DataFrame:
    """Read last 200 rows from local SQLite DB."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT * FROM sensors ORDER BY id DESC LIMIT 200", conn
    )
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.sort_values("timestamp")


def generate_fake_data(n: int = 200) -> pd.DataFrame:
    """
    Simulate n ESP32 DHT11 readings for Streamlit Cloud demo.
    Readings are spaced 5 seconds apart going back from now.
    """
    now = datetime.utcnow()
    rows = []
    for i in range(n, 0, -1):
        ts   = now - timedelta(seconds=i * 5)
        temp = round(random.uniform(20.0, 35.0), 1)
        hum  = round(random.uniform(45.0, 75.0), 1)
        rows.append({
            "id":          n - i + 1,
            "device_id":   "ESP32-AIOT-001",
            "ssid":        "HomeNetwork_5G",
            "ip_address":  "192.168.1.42",
            "temperature": temp,
            "humidity":    hum,
            "timestamp":   ts,
        })
    return pd.DataFrame(rows)


# ── Data Loading ─────────────────────────────────────────────
USE_DB    = os.path.exists(DB_PATH)
DATA_MODE = "🟢 Live SQLite" if USE_DB else "🔵 Simulated (Cloud Demo)"

if USE_DB:
    df = load_from_sqlite()
else:
    if "df_sim" not in st.session_state:
        st.session_state.df_sim = generate_fake_data(200)
    df = st.session_state.df_sim

# ── Header ───────────────────────────────────────────────────
st.title("🌡️ AIoT ESP32 Sensor Dashboard")
st.caption(f"Data source: **{DATA_MODE}**  |  Stack: ESP32 → Flask → SQLite3 → Streamlit")
st.divider()

# ── KPI Cards ────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Readings", len(df))
with col2:
    avg_temp = round(df["temperature"].mean(), 1)
    st.metric("🌡️ Avg Temperature", f"{avg_temp} °C")
with col3:
    avg_hum = round(df["humidity"].mean(), 1)
    st.metric("💧 Avg Humidity", f"{avg_hum} %")
with col4:
    last_device = df["device_id"].iloc[-1] if not df.empty else "—"
    st.metric("📡 Last Device", last_device)

st.divider()

# ── Charts ───────────────────────────────────────────────────
chart_df = df.set_index("timestamp")[["temperature", "humidity"]]

col_t, col_h = st.columns(2)

with col_t:
    st.subheader("🌡️ Temperature Over Time (°C)")
    st.line_chart(chart_df[["temperature"]], color=["#FF4B4B"], height=280)

with col_h:
    st.subheader("💧 Humidity Over Time (%)")
    st.line_chart(chart_df[["humidity"]], color=["#00C9A7"], height=280)

st.divider()

# ── Raw Data Table ───────────────────────────────────────────
with st.expander("📋 Raw Data (last 200 rows)", expanded=False):
    st.dataframe(
        df[["id", "device_id", "ssid", "ip_address",
            "temperature", "humidity", "timestamp"]].sort_values(
            "timestamp", ascending=False
        ),
        use_container_width=True,
        hide_index=True,
    )

# ── Live Refresh (local only) ────────────────────────────────
if USE_DB:
    import time
    st.caption("⏱ Auto-refreshing every 5 s…")
    time.sleep(5)
    st.rerun()
else:
    if st.button("🔄 Regenerate Simulated Data"):
        st.session_state.df_sim = generate_fake_data(200)
        st.rerun()
    st.caption("ℹ️ Running in Cloud Demo mode — click the button to refresh simulated data.")
