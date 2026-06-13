#ICS GROUP 4D GROUP 1 EMBEDDED SYSTEMS AND IOT

from machine import Pin
import dht
import network
import time
import json
from umqtt.simple import MQTTClient

import config

print("BOOT TEST: running latest TTGO code")
print("Configured WiFi SSID:", config.WIFI_SSID)
print("Configured DHT pin:", config.DHT_PIN)

sensor = dht.DHT11(Pin(config.DHT_PIN))


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print("WiFi already connected.")
        print("Network config:", wlan.ifconfig())
        return wlan

    print("Connecting to WiFi:", config.WIFI_SSID)
    wlan.connect(config.WIFI_SSID, config.WIFI_PASS)

    start = time.time()

    while not wlan.isconnected():
        print("WiFi status:", wlan.status())

        if time.time() - start > 20:
            raise RuntimeError("WiFi connection failed")

        time.sleep(1)

    print("WiFi connected.")
    print("Network config:", wlan.ifconfig())
    return wlan


def connect_mqtt():
    client = MQTTClient(
        config.CLIENT_ID,
        config.MQTT_BROKER,
        port=config.MQTT_PORT,
        keepalive=60
    )

    client.connect()
    time.sleep(3)

    try:
        client.ping()
        time.sleep(1)
    except:
        pass

    print("Connected to MQTT broker:", config.MQTT_BROKER)
    return client


def read_sensor():
    sensor.measure()
    return sensor.temperature(), sensor.humidity()


def main():
    connect_wifi()
    client = connect_mqtt()

    print("Starting publish loop. Topic:", config.MQTT_TOPIC)

    while True:
        try:
            temperature, humidity = read_sensor()

            payload = json.dumps({
                "temperature": temperature,
                "humidity": humidity
            })

            try:
                client.publish(config.MQTT_TOPIC, payload)
                print("Published:", payload)

            except OSError as e:
                print("Publish failed:", e)

                try:
                    client.disconnect()
                except:
                    pass

                time.sleep(2)
                client = connect_mqtt()

        except OSError as e:
            print("Sensor/read error:", e)

        time.sleep(config.PUBLISH_INTERVAL)


if __name__ == "__main__":
    main()