# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import app_secrets as api_keys
import line_notify

print("Token:", api_keys.get_line_channel_access_token()[:20] + "...")
print("Push to:", api_keys.get_line_push_to())
print("LINE API ready:", line_notify.messaging_push_ready())

# Test send
result = line_notify.send_push_text("Test from Python - Thai: ป้ายเข้า")
print("Send result:", result)
