#CONFIGURATION FILE WITH OUR NETWORK DETAILS
#MQTT AND WIFI SENSOR CONNNECTINO TO TTGO BOARD

#ICS GROUP 4D GROUP 1 EMBEDDED SYSTEMS AND IOT
# ---------------------------------------------------------------------------

# ---------- WiFi ----------
WIFI_SSID = "ESP32TEST"
WIFI_PASS = "test12345"

# ---------- MQTT ----------
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT   = 1883
MQTT_TOPIC  = b"university/group1/dht22"
CLIENT_ID   = b"ttgo-dht22-group1"

# ---------- Sensor ----------
DHT_PIN = 23
PUBLISH_INTERVAL = 15
