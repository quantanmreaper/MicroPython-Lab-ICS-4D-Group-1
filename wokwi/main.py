#ICS GROUP 4D GROUP 1 EMBEDDED SYSTEMS AND IOT
#This is the code that we ran on wokwi for simulation

from machine import Pin
import dht
import network
import time
import json
from umqtt.simple import MQTTClient

# ---------- SETTINGS ----------
WIFI_SSID = "Wokwi-GUEST"    # Wokwi's built-in test WiFi
WIFI_PASS = ""               # no password in Wokwi

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT   = 1883
MQTT_TOPIC  = b"university/group1/dht22"
CLIENT_ID   = b"ttgo-dht22-group1-wokwi"      # CHANGE to something unique

DHT_PIN = 15                 # GPIO15 in the simulation
PUBLISH_INTERVAL = 5         # seconds between readings

# ---------- OBJECTS ----------
sensor = dht.DHT22(Pin(DHT_PIN))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print("WiFi already connected.")
        print("Network config:", wlan.ifconfig())
        return wlan

    print("Connecting to WiFi:", WIFI_SSID)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    start = time.time()
    timeout_seconds = 20

    while not wlan.isconnected():
        status = wlan.status()
        print("WiFi status:", status)

        if time.time() - start > timeout_seconds:
            print("WiFi connection timed out.")
            print("Final WiFi status:", wlan.status())
            print("Check SSID, password, 2.4 GHz support, and hotspot settings.")
            raise RuntimeError("Could not connect to WiFi")

        time.sleep(1)

    print("WiFi connected.")
    print("Network config:", wlan.ifconfig())

    return wlan

def connect_mqtt():
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Connected to MQTT broker:", MQTT_BROKER)
    return client


connect_wifi()
client = connect_mqtt()

while True:
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        payload = json.dumps({
            "temperature": temperature,
            "humidity": humidity
        })
        client.publish(MQTT_TOPIC, payload)
        print("Published:", payload)

    except OSError as e:
        print("Error:", e)

    time.sleep(PUBLISH_INTERVAL)
