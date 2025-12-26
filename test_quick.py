#!/usr/bin/env python
"""Quick test to verify components work"""

import sys

print("Testing imports...")

try:
    print("1. config_manager...", end="", flush=True)
    from config_manager import get_config
    print(" [OK]")
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)

try:
    print("2. error_handler...", end="", flush=True)
    from error_handler import get_error_handler
    print(" [OK]")
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)

try:
    print("3. feedback_ui...", end="", flush=True)
    from feedback_ui import get_feedback_ui
    print(" [OK]")
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)

try:
    print("4. input_validator...", end="", flush=True)
    from input_validator import InputValidator
    print(" [OK]")
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)

try:
    print("5. adaptive_matcher...", end="", flush=True)
    from adaptive_matcher import AdaptiveMatcher
    print(" [OK]")
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)

try:
    print("6. phoneme_variants...", end="", flush=True)
    from phoneme_variants import PhonemeVariants
    print(" [OK]")
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)

try:
    print("7. voice_quality_tester...", end="", flush=True)
    from voice_quality_tester import VoiceQualityTester
    print(" [OK]")
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)

try:
    print("8. voice_detector...", end="", flush=True)
    from voice_detector import SmartVoiceDetector
    print(" [OK]")
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)

try:
    print("9. hybrid_voice_recognizer...", end="", flush=True)
    from hybrid_voice_recognizer import HybridVoiceRecognizer
    print(" [OK]")
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)

try:
    print("10. powerpoint_controller...", end="", flush=True)
    from powerpoint_controller import PowerPointController
    print(" [OK]")
except Exception as e:
    print(f" [ERROR] {e}")
    sys.exit(1)

print("\n[SUCCESS] All modules load successfully!")
print("[INFO] You can now run: python main.py")
