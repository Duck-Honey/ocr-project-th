# -*- coding: utf-8 -*-
"""
โมดูลตรวจจับกรอบป้ายทะเบียนและอ่านข้อความด้วย EasyOCR
Plate detection (contours) + OCR utilities for Thai license plates.
"""

from __future__ import annotations

import re
from typing import Any

import cv2
import numpy as np

# รูปแบบป้ายไทย: พยัญชนะไทย 1-3 ตัว + ตัวเลข 1-4 ตัว (ชื่อจังหวัดตัดออกจาก regex หลักเพื่อความเสถียร)
THAI_PLATE_PATTERN = re.compile(r"[ก-ฮ]{1,3}\s*\d{1,4}")

# อัตราส่วนป้ายทะเบียนโดยประมาณ (กว้าง:สูง) ~ 2:1 ถึง 5:1
ASPECT_MIN = 2.0
ASPECT_MAX = 5.0
MIN_CONTOUR_AREA = 2000
OCR_CONFIDENCE_THRESHOLD = 0.5


def create_reader() -> Any:
    """สร้าง EasyOCR reader — ไทย + อังกฤษ, ปิด GPU เพื่อความเข้ากันได้"""
    import easyocr

    return easyocr.Reader(["th", "en"], gpu=False, verbose=False)


def _filter_plate_text(raw: str) -> str | None:
    """คัดเฉพาะข้อความที่ตรงรูปแบบป้ายไทย"""
    s = raw.strip()
    if not s:
        return None
    m = THAI_PLATE_PATTERN.search(s.replace(" ", " ").replace("  ", " "))
    if m:
        return m.group(0).strip()
    # ลองตัดช่องว่างแปลก ๆ
    compact = re.sub(r"\s+", "", s)
    m2 = THAI_PLATE_PATTERN.search(compact)
    if m2:
        return m2.group(0).strip()
    return None


def detect_plate_roi(frame: np.ndarray) -> tuple[int, int, int, int] | None:
    """
    หา ROI ป้ายทะเบียนจากเฟรม:
    grayscale -> bilateral -> Canny -> contours -> กรอง aspect ratio และพื้นที่
    คืน (x, y, w, h) หรือ None ถ้าไม่พบ
    """
    if frame is None or frame.size == 0:
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # bilateral ลดสัญญาณรบกวนโดยยังเก็บขอบ
    blur = cv2.bilateralFilter(gray, 11, 17, 17)
    edges = cv2.Canny(blur, 30, 200)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    h_frame, w_frame = frame.shape[:2]
    best: tuple[float, tuple[int, int, int, int]] | None = None

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < MIN_CONTOUR_AREA:
            continue
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)

        if h <= 0 or w <= 0:
            continue
        aspect = w / float(h)
        if not (ASPECT_MIN <= aspect <= ASPECT_MAX):
            continue

        # อยู่ในกรอบภาพ
        x = max(0, min(x, w_frame - 1))
        y = max(0, min(y, h_frame - 1))
        w = min(w, w_frame - x)
        h = min(h, h_frame - y)
        if w < 10 or h < 10:
            continue

        score = area
        if best is None or score > best[0]:
            best = (score, (x, y, w, h))

    return best[1] if best else None


def read_plate_text(reader: Any, plate_bgr: np.ndarray) -> tuple[str, float] | None:
    """
    รัน EasyOCR เฉพาะบริเวณ crop ของป้าย
    คืน (ข้อความที่ผ่าน regex, confidence สูงสุดของ segment ที่ใช้) หรือ None
    """
    if plate_bgr is None or plate_bgr.size == 0:
        return None

    rgb = cv2.cvtColor(plate_bgr, cv2.COLOR_BGR2RGB)
    results = reader.readtext(rgb, detail=1)

    best_text: str | None = None
    best_conf = 0.0
    merged_parts: list[str] = []
    merged_conf_sum = 0.0
    merged_conf_n = 0

    for item in results:
        # easyocr: (bbox, text, conf) หรือบางเวอร์ชันมีรูปแบบต่างกันเล็กน้อย
        if len(item) < 3:
            continue
        _bbox, text, conf = item[0], item[1], float(item[2])
        if conf < OCR_CONFIDENCE_THRESHOLD:
            continue
        merged_parts.append(text.strip())
        merged_conf_sum += conf
        merged_conf_n += 1
        cleaned = _filter_plate_text(text)
        if cleaned and conf > best_conf:
            best_conf = conf
            best_text = cleaned

    # รวมข้อความหลายกล่อง (เช่น พยัญชนะ / ตัวเลข แยกกล่อง) แล้วลองจับรูปแบบอีกครั้ง
    if merged_parts and merged_conf_n:
        combined = " ".join(merged_parts)
        merged_clean = _filter_plate_text(combined)
        avg_conf = merged_conf_sum / merged_conf_n
        if merged_clean and avg_conf >= OCR_CONFIDENCE_THRESHOLD:
            if best_text is None or len(merged_clean) >= len(best_text):
                best_text = merged_clean
                best_conf = max(best_conf, avg_conf)

    if best_text is None:
        return None
    return (best_text, best_conf)
