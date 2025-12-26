#!/usr/bin/env python
"""Minimal test to check if main components initialize"""

import sys
sys.path.insert(0, '.')

from config_manager import get_config
from error_handler import get_error_handler
from voice_detector import SmartVoiceDetector
from hybrid_voice_recognizer import HybridVoiceRecognizer
from powerpoint_controller import PowerPointController

print("[1] Loading config...")
config = get_config()
print("    [OK] Config loaded")

print("[2] Loading error handler...")
error_handler = get_error_handler(config.get_bool("DEBUG_MODE"))
print("    [OK] Error handler ready")

print("[3] Creating detector...")
detector = SmartVoiceDetector(config=config)
print("    [OK] Voice detector initialized")

print("[4] Creating recognizer...")
voice = HybridVoiceRecognizer(debug_mode=config.get_bool("DEBUG_MODE"), config=config)
print("    [OK] Voice recognizer created")

print("[5] Creating controller...")
ppt = PowerPointController()
print("    [OK] PowerPoint controller ready")

print("\n[SUCCESS] All components initialized successfully!")
print("[INFO] Main application is ready to run")
print("[INFO] Run: python main.py")
