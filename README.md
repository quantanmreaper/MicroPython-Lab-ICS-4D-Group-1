## Team

- **Group:** ICS 4D Group 1 Embedded Systems and IoT
- **Members:**
  - 167077 - Mepani Bhavin Ramesh
  - 169649 - Kimathi Austin Muthomi
  - 161088 - Muhia Robby Mwangi
  - 167999 - Samuel Mwesigwa
  - 166991 - Omwanda Philip Maxwell
  - 166529 - Hope Wanjohi

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

## Hardware Setup & Flashing Commands

This section documents the actual commands we used to flash MicroPython firmware to the TTGO LoRa32 board and deploy our code.

### Step 1: Install esptool
```bash
pip install esptool
```

### Step 2: Erase the Flash Memory
```bash
esptool.py --port COM5 erase_flash
```

### Step 3: Flash MicroPython Firmware
```bash
esptool.py --port COM5 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-xxxx.bin
```
> Replace `xxxx` with your actual firmware version number

### Step 4: Install mpremote Tool
```bash
python -m pip install mpremote
```

### Step 5: Test Board Connection
```bash
python -m mpremote connect COM5 exec "print('hello from the board')"
```

### Step 6: Install Required MicroPython Libraries
```bash
# Install MQTT library
python -m mpremote connect COM5 mip install umqtt.simple

# Install OLED display library (optional)
python -m mpremote connect COM5 mip install ssd1306
```

### Step 7: Upload Configuration and Main Files
```bash
# Copy config.py to the board
python -m mpremote connect COM10 fs cp board/config.py :config.py

# Copy main.py to the board
python -m mpremote connect COM10 fs cp board/main.py :main.py
```

### Step 8: Verify Files and Start REPL
```bash
# List files on the board
python -m mpremote connect COM10 fs ls

# Open REPL to see live output
python -m mpremote connect COM10 repl
```

> **Note:** The COM port may vary (COM5, COM10, etc.). Check Device Manager (Windows) or `/dev/ttyUSB*` (Linux) to find your board's port.

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
- [**📥 Download PDF Report**](https://raw.githubusercontent.com/quantanmreaper/MicroPython-Lab-ICS-4D-Group-1/main/GROUP1_ICS4D_MICRO_PYTHON_Lab_Report.pdf) - Direct download (right-click → Save Link As)
- [**👁️ View PDF in Browser**](https://github.com/quantanmreaper/MicroPython-Lab-ICS-4D-Group-1/blob/main/GROUP1_ICS4D_MICRO_PYTHON_Lab_Report.pdf) - GitHub viewer (may be slow)

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
