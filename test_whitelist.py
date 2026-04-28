# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import plate_whitelist

# Test add_plate
wl = plate_whitelist.add_plate('กค 1234')
print('Added plate, whitelist:', wl)

# Test load
loaded = plate_whitelist.load_whitelist()
print('Loaded:', loaded)

# Test should_allow
result = plate_whitelist.should_allow_plate('กค 1234')
print('Allow กค 1234:', result)

result2 = plate_whitelist.should_allow_plate('นข 5678')
print('Allow นข 5678:', result2)
