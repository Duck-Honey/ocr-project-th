# -*- coding: utf-8 -*-
"""
ส่งคำสั่งไป ESP8266 ผ่าน USB Serial เพื่อควบคุมเซอร์โว
Protocol: ส่งมุมเป็นตัวเลข 0–180 แล้วขึ้นบรรทัดใหม่ (ESP ใช้ Serial.parseInt() ได้สะดวก)

ตั้งค่าผ่านตัวแปรสภาพแวดล้อม (ไม่บังคับ):
  ESP_PORT   — เช่น COM3 (Windows) หรือ /dev/ttyUSB0; ถ้าว่าง = ปิดการใช้ serial
  ESP_BAUD   — default 115200
"""
from __future__ import annotations

import os

import serial


def _port() -> str:
    return os.environ.get("ESP_PORT", "").strip()


def _baud() -> int:
    return int(os.environ.get("ESP_BAUD", "115200"))


def try_open() -> serial.Serial | None:
    """เปิดพอร์ตถ้ามี ESP_PORT; ถ้าไม่ตั้งหรือเปิดไม่ได้ คืน None (ไม่ crash)"""
    port = _port()
    if not port:
        print("Serial: ไม่ได้ตั้ง ESP_PORT — ข้ามการเชื่อม ESP8266 (ตั้งเช่น $env:ESP_PORT='COM3')")
        return None
    try:
        ser = serial.Serial(port, _baud(), timeout=0.2)
        print(f"Serial: เชื่อม {port} @ {_baud()} baud")
        return ser
    except Exception as e:  # noqa: BLE001 — แสดงข้อความแล้วทำงานต่อได้
        print(f"Serial: เปิดพอร์ตไม่ได้ ({port}): {e}")
        return None


def send_servo_angle(ser: serial.Serial | None, angle: int) -> bool:
    """
    ส่งมุมเซอร์โว 0–180 เป็น ASCII บรรทัดเดียว (เช่น b'90\\n')
    คืน True ถ้าส่งได้
    """
    if ser is None or not ser.is_open:
        return False
    a = max(0, min(180, int(angle)))
    try:
        ser.write(f"{a}\n".encode("ascii", errors="ignore"))
        ser.flush()
        return True
    except Exception as e:  # noqa: BLE001
        print(f"Serial: ส่งคำสั่งไม่ได้: {e}")
        return False


def close(ser: serial.Serial | None) -> None:
    if ser is not None and ser.is_open:
        try:
            ser.close()
        except Exception:
            pass
