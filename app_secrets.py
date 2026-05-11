# -*- coding: utf-8 -*-
import os

LINE_CHANNEL_ACCESS_TOKEN = "Dfdg93dPL5j6yKnbHsKXbSdJVZxsqDTReKOslUnv3Qk295xPxAmpQPXIL4fZUHpkdmgnbMZ86QddoufkGs94vbyJWStWvHZxcCOZPuttCLIQHqBoHXnDV/6YKQTR7Uyql7jU8irt5nytfcgAylsFbQdB04t89/1O/w1cDnyilFU="
LINE_PUSH_TO = "U986fb0aeca4be80b25d681ddbc2d68a6"


def get_line_channel_access_token() -> str:
    return os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", LINE_CHANNEL_ACCESS_TOKEN).strip()


def get_line_push_to() -> str:
    return os.environ.get("LINE_PUSH_TO", LINE_PUSH_TO).strip()