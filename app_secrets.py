# -*- coding: utf-8 -*-
import os

LINE_CHANNEL_ACCESS_TOKEN = "npDbdiA7FPORzL3LrtUnahsa4mPImx8mVSpWPON/RTT/VzOU+3IwqmPYfj0Tip4XdmgnbMZ86QddoufkGs94vbyJWStWvHZxcCOZPuttCLLlFT2e3SHy6TW8a4xVeBt10LV+y2Nh7pn3jOUSfOcYWAdB04t89/1O/w1cDnyilFU="
LINE_PUSH_TO = "U986fb0aeca4be80b25d681ddbc2d68a6"


def get_line_channel_access_token() -> str:
    return os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", LINE_CHANNEL_ACCESS_TOKEN).strip()


def get_line_push_to() -> str:
    return os.environ.get("LINE_PUSH_TO", LINE_PUSH_TO).strip() 