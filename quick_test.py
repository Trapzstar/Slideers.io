#!/usr/bin/env python3
"""
Quick Test - Test program utama tanpa menjalankan voice recognition
"""

def test_main_program():
    """Test main program can import and initialize"""
    print("="*70)
    print("🚀 QUICK TEST - MAIN PROGRAM")
    print("="*70)
    print()
    
    # Test 1: Import semua module
    print("1️⃣ Testing imports...")
    try:
        from voice_detector import SmartVoiceDetector
        from hybrid_voice_recognizer import HybridVoiceRecognizer
        from powerpoint_controller import PowerPointController
        from accessibility_popup import AccessibilityPopup
        print("   ✅ All imports successful")
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test 2: Initialize components
    print("\n2️⃣ Testing component initialization...")
    try:
        detector = SmartVoiceDetector()
        print("   ✅ SmartVoiceDetector initialized")
        
        ppt = PowerPointController()
        print("   ✅ PowerPointController initialized")
        
        popup = AccessibilityPopup()
        print("   ✅ AccessibilityPopup initialized")
        
        voice = HybridVoiceRecognizer(debug_mode=False)
        print("   ✅ HybridVoiceRecognizer initialized")
        
    except Exception as e:
        print(f"   ❌ Initialization failed: {e}")
        return False
    
    # Test 3: Test command detection
    print("\n3️⃣ Testing command detection...")
    try:
        test_commands = [
            "next slide",
            "back slide", 
            "open slide show",
            "close slide show",
            "help menu",
            "stop program"
        ]
        
        for cmd in test_commands:
            result = detector.detect(cmd)
            if result and result.get("command") != "unknown":
                print(f"   ✅ '{cmd}' → {result['command']}")
            else:
                print(f"   ⚠️  '{cmd}' → not recognized")
                
    except Exception as e:
        print(f"   ❌ Command detection failed: {e}")
        return False
    
    # Test 4: Test PowerPoint commands
    print("\n4️⃣ Testing PowerPoint command execution...")
    try:
        test_cmds = [
            {"command": "next", "score": 10},
            {"command": "previous", "score": 10},
            {"command": "help", "score": 8},
        ]
        
        for cmd in test_cmds:
            result = ppt.execute_command(cmd)
            print(f"   ✅ {cmd['command']} → {result[:50]}...")
            
    except Exception as e:
        print(f"   ❌ PowerPoint commands failed: {e}")
        return False
    
    # Test 5: Test popup system
    print("\n5️⃣ Testing popup system...")
    try:
        popup.update_settings({'position': 'bottom-right'})
        print("   ✅ Popup settings updated")
        
        content = {
            'title': 'Test',
            'text': 'Quick test running',
            'progress': '1/5'
        }
        popup.current_content = content
        print("   ✅ Popup content set")
        
    except Exception as e:
        print(f"   ❌ Popup system failed: {e}")
        return False
    
    # Test 6: Check performance stats
    print("\n6️⃣ Testing performance stats...")
    try:
        if hasattr(voice, 'get_performance_stats'):
            stats = voice.get_performance_stats()
            print(f"   ✅ Performance stats available")
            print(f"      Keys: {list(stats.keys())[:5]}")
        else:
            print(f"   ⚠️  get_performance_stats not found (optional)")
            
    except Exception as e:
        print(f"   ❌ Performance stats failed: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("✅ QUICK TEST PASSED!")
    print("="*70)
    print()
    print("📝 Next steps:")
    print("   1. Run full test: python test_script.py")
    print("   2. Run main program: python main.py")
    print("   3. Test with actual voice: Say 'help menu'")
    print()
    
    return True

if __name__ == "__main__":
    success = test_main_program()
    exit(0 if success else 1)
