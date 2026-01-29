#!/usr/bin/env python
"""Test menu interaction"""

import sys
from ui_manager import ui

print("Testing show_main_menu()...")
print()

# Simulate user input
import io
sys.stdin = io.StringIO("1\n")

result = ui.show_main_menu()
print(f"Result: {result}")
