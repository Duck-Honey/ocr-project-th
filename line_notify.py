"""LINE Messaging API push helper."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

import app_secrets as api_keys

LINE_PUSH_API = "https://api.line.me/v2/bot/message/push"


def messaging_push_ready() -> bool:
    """True when token and destination are configured."""
    token = api_keys.get_line_channel_access_token()
    target = api_keys.get_line_push_to()
    return bool(token) and "PUT_" not in token and bool(target) and "PUT_" not in target


def send_push_text(message: str) -> bool:
    """Send a text message through LINE Messaging API."""
    token = api_keys.get_line_channel_access_token()
    to = api_keys.get_line_push_to()
    if not token or not to:
        return False

    payload = {
        "to": to,
        "messages": [{"type": "text", "text": message}],
    }
    req = urllib.request.Request(
        LINE_PUSH_API,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return 200 <= resp.status < 300
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"LINE error {e.code}: {err}")
        return False
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"LINE connection error: {e}")
        return False
