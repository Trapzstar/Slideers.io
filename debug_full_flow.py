#!/usr/bin/env python
"""Debug full menu flow"""

import sys
import io
import signal
from main2 import SlideSenseApp

# Override CTRL+C handling
def handle_interrupt(sig, frame):
    print("\n[INTERRUPT] Caught Ctrl+C")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_interrupt)

print("Starting SlideSense with menu 1 (Start Voice Control)...")
print("-" * 60)

# Create app
app = SlideSenseApp()

# Simulate input: menu 1
sys.stdin = io.StringIO('1\n')

try:
    app.run()
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
