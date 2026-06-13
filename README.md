## Team

- Group: ICS 4D Group 1 Embedded Systems and IoT
- Members: 
           167077 Mepani Bhavin Ramesh
           169649 Kimathi Austin Muthomi
           161088 Muhia Robby Mwangi
           166991 Omwanda Philip Maxwell
           166529 Hope Wanjohi

# TTGO + DHT22 + MQTT IoT Lab

This is a complete beginner-friendly IoT system: a **TTGO LoRa32** board (ESP32 inside)
reads temperature & humidity from a **DHT22** sensor, connects to **WiFi**, and
**publishes JSON over MQTT**. A **Python subscriber** on a PC receives the
messages and stores them in an **SQLite** database.

> **Hardware note:** The lab originally specified a plain ESP32. Mr. Itotia
> instructed: *"Use TTGO (same approach, but we should check the datasheet before flying
> them) and use WiFi for data transmission."* The TTGO LoRa32 contains an ESP32
> chip, so the approach is somewha identical. **We used WiFi only — no LoRa.** We prototype
> in the **Wokwi** ESP32 simulator first, which maps 1:1 to the TTGO except for
> the DATA pin number (GPIO15 in sim, GPI023 on the real board).

---

## The system Architecture

```
 ┌──────────┐   reads    ┌─────────────────┐  WiFi   ┌──────────────┐
 │  DHT22   │ ─────────▶ │  TTGO (ESP32)   │ ──────▶ │  MQTT Broker  │
 │ (sensor) │ temp+hum   │  MicroPython    │  JSON   │ broker.hivemq │
 └──────────┘            └─────────────────┘         └──────┬───────┘
                                                            │ delivers
                                                            ▼
                                              ┌──────────────────────┐
                                              │  PC Python subscriber │
                                              │   (paho-mqtt)         │
                                              └──────────┬───────────┘
                                                         │ INSERT
                                                         ▼
                                              ┌──────────────────────┐
                                              │   SQLite (readings.db)│
                                              └──────────────────────┘
```

---

## Repository layout

```
ttgo-dht22-mqtt-iot/
├── README.md                 <- you are here 
├── .gitignore
├── board/                    <- This is the code that runs ON the TTGO
│   ├── main.py               <- main board program (uses config.py)
│   ├── config.py             <- your settings (git-ignored; holds WiFi pass)

├── pc/                       <- This is the code that runs on your laptop (CPython)
│   ├── init_db.py            <- It should run once: creates readings.db
│   ├── subscriber.py         <- It receives MQTT messages, saves to SQLite
│   ├── view_data.py          <- A way we used to print stored readings

├── wokwi/                    <- This folder is for the browser simulation
│   ├── diagram.json          <- the circuit (ESP32 + DHT22)
│   ├── diagram_oled.json     <- circuit variant with the OLED added
│   ├── main.py               <- self-contained code to paste into Wokwi

---

## Quick start (simulation) We did this before doing the lab 

```bash
# 1. PC side
cd pc
pip install -r requirements.txt
python init_db.py
python subscriber.py          # leave running

#   Below is the prototype we used 
#   2. Wokwi: new ESP32 MicroPython project
#    - paste wokwi/diagram.json into the diagram.json tab
#    - paste wokwi/main.py     into the main.py tab
#    - press Play

# 3. To check the stored data (on a new terminal, in pc/ run)
python view_data.py
```

> Remember to set the **same unique MQTT topic** in both `wokwi/main.py`
> (or `board/config.py`) and `pc/subscriber.py`.

---

## Wiring summary (3 wires)

| DHT22 | Wokwi ESP32 | Real TTGO LoRa32 |
|-------|-------------|------------------|
| VCC   | 3V3         | 3V3              |
| DATA  | GPIO15      | **GPIO23**       |
| GND   | GND         | GND              |


