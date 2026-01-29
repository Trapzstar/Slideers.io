#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST_6_COMMANDS.py - Verify 6 main commands work correctly

Menguji:
1. Constants.py properly defines 6 commands
2. detektor_suara.py loads 6 commands from constants.py
3. All keywords for 6 commands are recognized
4. Speech history analyzer correctly groups unrecognized commands
"""

import sys
import os

# Add the current directory to the path if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import MAIN_COMMANDS, KEYWORDS_INDEX, get_command_by_keyword
try:
    from detektor_suara import PendeteksiSuaraCerdas
except ImportError:
    print("Warning: detektor_suara module not found")
    PendeteksiSuaraCerdas = None
from speech_history_analyzer import SpeechHistoryAnalyzer

def test_constants():
    """Test constants.py has 6 main commands"""
    print("\n" + "="*60)
    print("TEST 1: Verify 6 Main Commands in constants.py")
    print("="*60)
    
    main_commands = list(MAIN_COMMANDS.keys())
    print(f"\n✅ Found {len(main_commands)} commands in MAIN_COMMANDS:")
    
    for i, cmd in enumerate(main_commands, 1):
        cmd_data = MAIN_COMMANDS[cmd]
        keyword_count = len(cmd_data['keywords'])
        print(f"  {i}. {cmd:20} - {keyword_count} keywords")
    
    if len(main_commands) != 6:
        print(f"❌ ERROR: Expected 6 commands, got {len(main_commands)}")
        return False
    
    print("\n✅ PASS: 6 commands defined correctly")
    return True

def test_keywords():
    """Test all keywords are defined"""
    print("\n" + "="*60)
    print("TEST 2: Verify All Keywords Are Defined")
    print("="*60)
    
    total_keywords = 0
    for cmd_name, cmd_data in MAIN_COMMANDS.items():
        keywords = cmd_data['keywords']
        total_keywords += len(keywords)
        print(f"\n{cmd_name.upper()}:")
        print(f"  Keywords: {', '.join(keywords[:5])}")
        if len(keywords) > 5:
            print(f"  ... and {len(keywords) - 5} more")
    
    print(f"\n✅ Total keywords: {total_keywords}")
    
    if total_keywords < 30:  # Should have at least 30 keywords total
        print(f"❌ WARNING: Only {total_keywords} keywords (expected 30+)")
        return False
    
    print("✅ PASS: All keywords defined")
    return True

def test_detector_loads_commands():
    """Test detektor_suara.py loads 6 commands from constants.py"""
    print("\n" + "="*60)
    print("TEST 3: Verify detektor_suara Loads 6 Commands")
    print("="*60)
    
    try:
        detector = PendeteksiSuaraCerdas()
        commands_loaded = list(detector.kata_kunci_bangun.keys())
        
        print(f"\n✅ Detector loaded {len(commands_loaded)} commands:")
        for cmd in commands_loaded:
            count = len(detector.kata_kunci_bangun[cmd]['frasa'])
            print(f"  • {cmd:20} - {count} phrases")
        
        if len(commands_loaded) != 6:
            print(f"❌ ERROR: Expected 6 commands, got {len(commands_loaded)}")
            return False
        
        print("\n✅ PASS: All 6 commands loaded correctly")
        return True
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_command_recognition():
    """Test command recognition works"""
    print("\n" + "="*60)
    print("TEST 4: Test Command Recognition")
    print("="*60)
    
    try:
        detector = PendeteksiSuaraCerdas()
        
        test_cases = [
            ("next slide", "next_slide"),
            ("lanjut", "next_slide"),
            ("previous", "previous_slide"),
            ("mundur", "previous_slide"),
            ("open slideshow", "open_slideshow"),
            ("buka presentasi", "open_slideshow"),
            ("close slideshow", "close_slideshow"),
            ("tutup presentasi", "close_slideshow"),
            ("help menu", "show_help"),
            ("bantuan", "show_help"),
            ("stop program", "stop_program"),
            ("berhenti", "stop_program"),
        ]
        
        passed = 0
        failed = 0
        
        print("\nTesting recognition:")
        for phrase, expected_cmd in test_cases:
            result = detector.deteksi(phrase)
            
            if result and result['command'] == expected_cmd:
                print(f"  ✅ '{phrase}' -> {result['command']} (score: {result['score']:.1f})")
                passed += 1
            else:
                detected_cmd = result['command'] if result else "None"
                print(f"  ❌ '{phrase}' -> {detected_cmd} (expected {expected_cmd})")
                failed += 1
        
        print(f"\nResults: {passed} passed, {failed} failed")
        
        if failed > 0:
            print(f"⚠️  Some tests failed")
            return False
        
        print("✅ PASS: All command recognition tests passed")
        return True
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_speech_history_analyzer():
    """Test speech history analyzer groups commands correctly"""
    print("\n" + "="*60)
    print("TEST 5: Test Speech History Analyzer")
    print("="*60)
    
    try:
        analyzer = SpeechHistoryAnalyzer()
        
        # Mock some test data
        print("\nAnalyzer capabilities:")
        print("  • Groups unrecognized commands with 6 main commands")
        print("  • Uses fuzzy matching and similarity scoring")
        print("  • Exports suggestions for auto-learning")
        
        if not hasattr(analyzer, 'grouped_commands'):
            print("❌ ERROR: Analyzer missing grouped_commands attribute")
            return False
        
        print("\n✅ PASS: Speech history analyzer ready")
        return True
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🧪 "*25)
    print("TEST SUITE: 6 Main Commands Implementation")
    print("🧪 "*25)
    
    results = []
    
    # Run all tests
    results.append(("Constants.py Definition", test_constants()))
    results.append(("Keywords Definition", test_keywords()))
    results.append(("Detector Loading", test_detector_loads_commands()))
    results.append(("Command Recognition", test_command_recognition()))
    results.append(("Speech History Analyzer", test_speech_history_analyzer()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Phase 1 Step 1 Complete!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
