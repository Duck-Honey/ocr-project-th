# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os

# Set from api_keys
os.environ["LINE_CHANNEL_ACCESS_TOKEN"] = "ILzcTBwslUSZbQq5g2JLPo99m0kTvjYOhN2rIUhyIZDxuh9TOrX7DEF6iPB718NTdmgnbMZ86QddoufkGs94vbyJWStWvHZxcCOZPuttCLK2iPm22ZfsxS3BNEFgCouU0BoXvA+nHt96asve+klrCwdB04t89/1O/w1cDnyilFU="
os.environ["LINE_PUSH_TO"] = "U986fb0aeca4be80b25d681ddbc2d68a6"

import line_notify

print("LINE API ready:", line_notify.messaging_push_ready())

# Test send
result = line_notify.send_push_text("Test from Python - Thai: ป้ายเข้า")
print("Send result:", result)
