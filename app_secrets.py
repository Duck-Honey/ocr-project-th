# -*- coding: utf-8 -*-
import os

LINE_CHANNEL_ACCESS_TOKEN = "API Keys is here"
LINE_PUSH_TO = "Awwww i love Femboy"


def get_line_channel_access_token() -> str:
    return os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", LINE_CHANNEL_ACCESS_TOKEN).strip()


def get_line_push_to() -> str:
    return os.environ.get("LINE_PUSH_TO", LINE_PUSH_TO).strip()
