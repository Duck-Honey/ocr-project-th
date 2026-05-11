# 🚗 OCR Barrier Gate — ระบบเปิด-ปิดไม้กั้นอัตโนมัติด้วย OCR

> Automatic vehicle license plate recognition system for barrier gate control  
> ระบบอ่านทะเบียนรถอัตโนมัติเพื่อควบคุมไม้กั้นประตู

---
<!-- if you're reading this, you're a nerd :D -->
## 📋 ภาพรวม / Overview

ระบบนี้ใช้ **EasyOCR** + **YOLO** เพื่ออ่านทะเบียนรถจากกล้อง แล้วเปรียบเทียบกับ whitelist — ถ้าตรง จะส่งคำสั่งไปยัง **ESP8266** ผ่าน Serial เพื่อเปิดไม้กั้น พร้อมแจ้งเตือนผ่าน **LINE Messaging API**

This system uses **EasyOCR** + **YOLO** to read license plates from a camera, compares them against a whitelist, then sends a command to an **ESP8266** via Serial to open the barrier gate, with **LINE Messaging API** notifications.

---

## ✨ ฟีเจอร์ / Features

- 📷 อ่านทะเบียนรถแบบ Real-time ผ่านกล้อง
- 🤖 ตรวจจับป้ายทะเบียนด้วย YOLO11n
- 🔤 OCR ด้วย EasyOCR (รองรับภาษาไทย + อังกฤษ)
- ✅ ระบบ Whitelist ทะเบียนที่อนุญาต
- 🔌 ควบคุม ESP8266 ผ่าน Serial (servo motor)
- 📲 แจ้งเตือน LINE ทุกครั้งที่มีรถเข้า-ออก
- 🖥️ Web UI สำหรับดู log และจัดการ whitelist
- 📝 บันทึก log ทะเบียนทุกคันพร้อม timestamp

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Object Detection | YOLO11n |
| OCR | EasyOCR |
| Backend | Python |
| Web UI | Flask |
| Microcontroller | ESP8266 (Arduino) |
| Notification | LINE Messaging API |
| Serial Comm | pyserial |

---

## 📁 โครงสร้างไฟล์ / File Structure

```
ocr-project-th/
├── main.py              # Main loop — camera + OCR + serial
├── app.py               # Flask web UI
├── plate_utils.py       # OCR & plate processing logic
├── plate_whitelist.py   # Whitelist management
├── esp_serial.py        # ESP8266 serial communication
├── line_notify.py       # LINE Messaging API
├── api_keys.py          # API keys (gitignored)
├── requirements.txt     # Python dependencies
├── static/              # Web UI assets
├── templates/           # Flask HTML templates
└── plate_whitelist.txt  # Whitelist ทะเบียน (gitignored)
```

---

## 🚀 การติดตั้ง / Installation

```bash
# 1. Clone repo
git clone https://github.com/Duck-Honey/ocr-project-th.git
cd ocr-project-th

# 2. สร้าง virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. ติดตั้ง dependencies
pip install -r requirements.txt

# 4. ตั้งค่า API keys
# สร้างไฟล์ api_keys.py แล้วใส่:
# LINE_CHANNEL_ACCESS_TOKEN = "your_token"
# LINE_PUSH_TO = "your_user_id"
```

---

## ⚙️ การตั้งค่า / Configuration

สร้างไฟล์ `api_keys.py` (ไม่ถูก commit ขึ้น git):

```python
LINE_CHANNEL_ACCESS_TOKEN = "your_line_token_here"
LINE_PUSH_TO = "Uxxxxxxxxxxxxxxxxx"  # LINE userId
```

ตั้งค่า ESP_PORT ใน environment:
```bash
# Windows
set ESP_PORT=COM3

# Linux
export ESP_PORT=/dev/ttyUSB0
```

---

## 🖥️ การใช้งาน / Usage

```bash
# รัน main system
python main.py

# รัน web UI (แยก terminal)
python app.py
```

Web UI จะเปิดที่ `http://localhost:5000`

---

## 📲 LINE Notification

ระบบจะส่งข้อความแจ้งเตือนไปยัง LINE ทุกครั้งที่:
- ✅ ทะเบียนอยู่ใน whitelist → เปิดไม้กั้น
- ❌ ทะเบียนไม่อยู่ใน whitelist → ปฏิเสธ

---

## 📦 Requirements

```
easyocr
ultralytics
pyserial
flask
opencv-python
torch
```

ดูรายละเอียดทั้งหมดใน `requirements.txt`

---

## 👤 Author

**Duck-Honey** — [@Duck-Honey](https://github.com/Duck-Honey)
