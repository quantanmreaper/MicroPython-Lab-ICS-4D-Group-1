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

---

## Documentation & Resources

### � Board Folder - TTGO Code
The `board/` folder contains the MicroPython code that runs on the TTGO (ESP32):

- **`config.py`** - Configuration file containing:
  - WiFi credentials (SSID and password)
  - MQTT broker settings (broker address, port, topic, client ID)
  - Pin configuration for the TTGO (DHT sensor pin: GPIO23)
  - Publish interval settings

- **`main.py`** - Main program with core functions:
  - `connect_wifi()` - Establishes WiFi connection
  - `connect_mqtt()` - Connects to the MQTT broker
  - `read_sensor()` - Reads temperature and humidity from DHT22
  - `main()` - Main loop that reads sensor data and publishes JSON payloads to MQTT every 15 seconds

### �📄 Lab Report
View or download the complete lab report:
- [**📥 Download PDF Report**](https://github.com/quantanmreaper/MicroPython-Lab-ICS-4D-Group-1/raw/main/ICS_4D_Lab%20Report_Group1_Lab_MICROPYTHON.pdf) - Direct download
- [**👁️ View PDF in Browser**](https://github.com/quantanmreaper/MicroPython-Lab-ICS-4D-Group-1/blob/main/ICS_4D_Lab%20Report_Group1_Lab_MICROPYTHON.pdf) - GitHub viewer (may be slow)

### 📸 Screenshots

#### Main Deliverable Screenshots
Visual documentation of all required lab deliverables:
- [View Main Deliverable Screenshots](./screenshots/Main%20Deliverable%20Screenshots/)
  - [Deliverable 2.1: Wiring Diagram](./screenshots/Main%20Deliverable%20Screenshots/Deliverable%202.1%20Wiring%20Diagram.png)
  - [Deliverable 2.2: Wiring Diagram - TTGO Close-up](./screenshots/Main%20Deliverable%20Screenshots/Deliverable%202.2%20Wiring%20Diagram_Close%20up%20of%20TTGO.png)
  - [Deliverable 3: REPL Output - Live Sensor Readings](./screenshots/Main%20Deliverable%20Screenshots/Deliverable%203_REPL%20output%20showing%20live%20sensor%20readings.png)
  - [Deliverable 4: Terminal Receiving 10+ JSON Messages](./screenshots/Main%20Deliverable%20Screenshots/Deliverable%204_%20terminal%20receiving%20at%20least%2010%20JSON%20messages.png)
  - [Deliverable 5: SQLite Query Results with Timestamps](./screenshots/Main%20Deliverable%20Screenshots/Deliverable%205_%20SQLite%20SELECT%20query%20confirming%20rows%20stored%20with%20timestamps.png)

#### Development Process Screenshots
Behind-the-scenes documentation of our implementation journey:
- [View Process Screenshots](./screenshots/Screenshots_of_Process/)
  - Setup, flashing, debugging, and final working system captures
