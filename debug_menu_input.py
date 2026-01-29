#!/usr/bin/env python
"""Debug menu input"""

from ui_manager import ui, console
import sys
import io

# Test with input "1"
print("Testing menu with input '1'...")
sys.stdin = io.StringIO('1\n')

result = ui.show_main_menu()

print(f"\nResult: {repr(result)}")
print(f"Type: {type(result)}")
print(f"Equals 'start': {result == 'start'}")
print(f"Result value: '{result}'")

if result == "start":
    print("✓ CORRECT - Would execute start_voice_control()")
elif result == "invalid":
    print("✗ WRONG - Got 'invalid'")
else:
    print(f"✗ WRONG - Got unexpected value: {repr(result)}")
