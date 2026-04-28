from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request

import line_notify
import plate_whitelist

BASE_DIR = Path(__file__).resolve().parent
MAIN_PY = BASE_DIR / "main.py"

app = Flask(__name__)
main_process: subprocess.Popen[str] | None = None


def _is_running() -> bool:
    global main_process
    if main_process is None:
        return False
    if main_process.poll() is None:
        return True
    main_process = None
    return False


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/status")
def status():
    return jsonify({"running": _is_running()})


@app.post("/api/run-main")
def run_main():
    global main_process
    if _is_running():
        return jsonify({"ok": True, "message": "main.py is already running"})

    child_env = os.environ.copy()
    child_env["PYTHONIOENCODING"] = "utf-8"

    main_process = subprocess.Popen(
        [sys.executable, str(MAIN_PY)],
        cwd=str(BASE_DIR),
        text=True,
        env=child_env,
    )
    return jsonify({"ok": True, "message": "Started main.py"})


@app.post("/api/stop-main")
def stop_main():
    global main_process
    if not _is_running():
        return jsonify({"ok": False, "message": "main.py is not running"}), 400
    assert main_process is not None
    main_process.terminate()
    main_process = None
    return jsonify({"ok": True, "message": "Stopped main.py"})


@app.get("/api/whitelist")
def get_whitelist():
    items = sorted(plate_whitelist.load_whitelist())
    return jsonify({"items": items})


@app.post("/api/whitelist")
def add_whitelist():
    data = request.get_json(silent=True) or {}
    plate = str(data.get("plate", "")).strip()
    if not plate:
        return jsonify({"ok": False, "message": "plate is required"}), 400
    items = sorted(plate_whitelist.add_plate(plate))
    return jsonify({"ok": True, "items": items})


@app.delete("/api/whitelist")
def delete_whitelist():
    data = request.get_json(silent=True) or {}
    plate = str(data.get("plate", "")).strip()
    if not plate:
        return jsonify({"ok": False, "message": "plate is required"}), 400
    items = sorted(plate_whitelist.remove_plate(plate))
    return jsonify({"ok": True, "items": items})


@app.post("/api/test-line")
def test_line():
    if not line_notify.messaging_push_ready():
        return jsonify({"ok": False, "message": "LINE token or destination is not configured"}), 400
    ok = line_notify.send_push_text("Test message from whitelist dashboard")
    if ok:
        return jsonify({"ok": True, "message": "LINE test message sent"})
    return jsonify({"ok": False, "message": "Failed to send LINE message"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
