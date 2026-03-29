"""
Flask API — flask_app.py
Receives DHT11 sensor data from ESP32 simulator via HTTP POST,
stores into SQLite3 (aiotdb.db), and exposes query endpoints.

Endpoints:
  GET  /health          — liveness check
  POST /sensor          — insert sensor reading
  GET  /sensors         — last 100 readings (JSON)
  GET  /sensors/count   — total row count (JSON)
"""

from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "aiotdb.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sensors (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id   TEXT    NOT NULL,
            ssid        TEXT,
            ip_address  TEXT,
            temperature REAL    NOT NULL,
            humidity    REAL    NOT NULL,
            timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"[Flask] DB ready at {DB_PATH}")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "db": DB_PATH}), 200


@app.route("/sensor", methods=["POST"])
def add_sensor():
    data = request.get_json(force=True)
    required = {"device_id", "temperature", "humidity"}
    if not required.issubset(data.keys()):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db()
    conn.execute(
        "INSERT INTO sensors (device_id, ssid, ip_address, temperature, humidity) "
        "VALUES (?, ?, ?, ?, ?)",
        (data["device_id"], data.get("ssid"), data.get("ip_address"),
         data["temperature"], data["humidity"])
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "inserted"}), 201


@app.route("/sensors", methods=["GET"])
def get_sensors():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM sensors ORDER BY id DESC LIMIT 100"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows]), 200


@app.route("/sensors/count", methods=["GET"])
def count_sensors():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM sensors").fetchone()[0]
    conn.close()
    return jsonify({"count": count}), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
