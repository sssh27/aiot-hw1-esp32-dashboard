import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

st.set_page_config(page_title="AIoT ESP32 Dashboard", layout="wide")

st.title("ESP32 Sensor Real-time Dashboard")
st.write("Device Info: ESP32-AIOT-001 (HomeNetwork_5G - 192.168.1.42)")

# Mock data generation
def get_data():
      now = datetime.now()
      temp = np.random.uniform(20, 35)
      humi = np.random.uniform(45, 70)
      return {"time": now, "temperature": temp, "humidity": humi}

if 'data' not in st.session_state:
      st.session_state.data = pd.DataFrame(columns=["time", "temperature", "humidity"])

# Add new data point
new_data = get_data()
st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_data])], ignore_index=True)

# Dashboard layout
col1, col2 = st.columns(2)
with col1:
      st.metric("Temperature", f"{new_data['temperature']:.1f} degC")
  with col2:
        st.metric("Humidity", f"{new_data['humidity']:.1f} %")

st.subheader("Time Series Data")
st.line_chart(st.session_state.data.set_index("time"))

st.subheader("Data Log")
st.dataframe(st.session_state.data.tail(10))

# Auto refresh logic
time.sleep(2)
st.rerun()
