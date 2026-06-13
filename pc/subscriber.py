#ICS GROUP 4D GROUP 1 EMBEDDED SYSTEMS AND IOT

"""
THIS , IN SIMPLE TERMS DOES THE FOLLOWING:
  1. It connects to the SAME MQTT broker and topic as the board.
  2. It receives every JSON message the board publishes.
  3. It parses the JSON and stores the reading into the SQLite database.
"""

import json
import sqlite3
from datetime import datetime

import paho.mqtt.client as mqtt

# ---- These readings match board/config.py  ----
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT   = 1883
MQTT_TOPIC  = "university/group1/dht22"
DB_FILE = "readings.db"


def save_reading(temperature, humidity):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO readings (temperature, humidity, timestamp) VALUES (?, ?, ?)",
        (temperature, humidity, timestamp),
    )
    conn.commit()
    conn.close()
    print("   -> saved to database at {}".format(timestamp))


def on_connect(client, userdata, flags, rc):
    # rc (return code) == 0 means success.
    if rc == 0:
        print("Connected to broker (code 0). Subscribing to:", MQTT_TOPIC)
        client.subscribe(MQTT_TOPIC)
    else:
        print("Connection failed, return code:", rc)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("Received:", payload)
    try:
        data = json.loads(payload)
        temperature = data["temperature"]
        humidity = data["humidity"]
        save_reading(temperature, humidity)
    except (ValueError, KeyError) as e:
        print("   !! could not parse message:", e)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print("Connecting to {}:{} ...".format(MQTT_BROKER, MQTT_PORT))
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    client.loop_forever()


if __name__ == "__main__":
    main()
