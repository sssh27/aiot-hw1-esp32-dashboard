# AIoT Homework 1 - ESP32 Sensor Dashboard

## Project Overview
This project simulates an ESP32 device showing real-time sensor data via a Streamlit dashboard.
Since SQLite is not persistent on Streamlit Cloud, this version uses generated data for the live demo.

## System Info
- **Device ID**: ESP32-AIOT-001
- - **Network**: HomeNetwork_5G (192.168.1.42)
  - - **Sensors**: Temperature (20-35 degC), Humidity (45-70%)
   
    - ## How to Run
    - 1. Log in to GitHub and connect to Streamlit Cloud.
      2. 2. Select this repository and the entry point `streamlit_app.py`.
         3. 3. The dashboard will automatically update with mock sensor readings.
           
            4. ## Development Log
            5. - Initialized local Flask API and ESP32 simulated device.
               - - Implemented Streamlit dashboard for data visualization.
                 - - Adapted for Streamlit Cloud deployment with mock data generator.
