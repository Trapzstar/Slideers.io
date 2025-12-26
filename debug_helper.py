"""
Debug Helper - Find where the error occurs
"""

import sys
import traceback

def test_imports():
    """Test each import separately"""
    
    print("=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)
    
    imports = [
        ("ui_manager", "from ui_manager import ui, console"),
        ("voice_detector", "from voice_detector import SmartVoiceDetector"),
        ("voice_recognizer", "from hybrid_voice_recognizer import HybridVoiceRecognizer"),
        ("ppt_controller", "from powerpoint_controller import PowerPointController"),
        ("popup", "from accessibility_popup import AccessibilityPopup"),
    ]
    
    for name, import_cmd in imports:
        try:
            print(f"\n{name}... ", end="", flush=True)
            exec(import_cmd)
            print("✅ OK")
        except Exception as e:
            print(f"❌ FAILED")
            print(f"   Error: {e}")
            print(f"\n   Full traceback:")
            traceback.print_exc()
            return False
    
    return True

def test_ui_creation():
    """Test UI Manager instantiation"""
    
    print("\n" + "=" * 60)
    print("TESTING UI MANAGER")
    print("=" * 60)
    
    try:
        from ui_manager import ui, console
        print("\n✅ UI Manager imported")
        
        # Test methods
        print("\nTesting methods:")
        print("  - clear()... ", end="", flush=True)
        # Don't actually clear, just test callable
        assert callable(ui.clear)
        print("✅")
        
        print("  - show_welcome()... ", end="", flush=True)
        assert callable(ui.show_welcome)
        print("✅")
        
        print("  - show_main_menu()... ", end="", flush=True)
        assert callable(ui.show_main_menu)
        print("✅")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED")
        print(f"\nError: {e}")
        traceback.print_exc()
        return False

def test_class_instantiation():
    """Test creating instances of main classes"""
    
    print("\n" + "=" * 60)
    print("TESTING CLASS INSTANTIATION")
    print("=" * 60)
    
    classes = [
        ("SmartVoiceDetector", "from voice_detector import SmartVoiceDetector; SmartVoiceDetector()"),
        ("PowerPointController", "from powerpoint_controller import PowerPointController; PowerPointController()"),
        ("AccessibilityPopup", "from accessibility_popup import AccessibilityPopup; AccessibilityPopup()"),
        ("HybridVoiceRecognizer", "from hybrid_voice_recognizer import HybridVoiceRecognizer; HybridVoiceRecognizer(debug_mode=False)"),
    ]
    
    for name, code in classes:
        try:
            print(f"\n{name}... ", end="", flush=True)
            exec(code)
            print("✅ OK")
        except Exception as e:
            print(f"❌ FAILED")
            print(f"   Error: {e}")
            
            # Check if it's the .dict() error
            if "'dict' object has no attribute 'dict'" in str(e):
                print("\n   🔍 FOUND THE ERROR!")
                print(f"   This error is in {name}")
                print("\n   Full traceback:")
                traceback.print_exc()
                return False, name
            else:
                traceback.print_exc()
                return False, name
    
    return True, None

def test_main_app():
    """Test main app creation"""
    
    print("\n" + "=" * 60)
    print("TESTING MAIN APP")
    print("=" * 60)
    
    try:
        print("\nImporting main... ", end="", flush=True)
        import main
        print("✅ OK")
        
        print("Creating SlideSenseApp... ", end="", flush=True)
        app = main.SlideSenseApp()
        print("✅ OK")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED")
        print(f"\nError: {e}")
        
        if "'dict' object has no attribute 'dict'" in str(e):
            print("\n🔍 FOUND THE ERROR!")
            print("   Error is in main.py or SlideSenseApp initialization")
        
        print("\nFull traceback:")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    
    print("\n" + "=" * 60)
    print("🔍 DEBUG HELPER - FINDING THE ERROR")
    print("=" * 60)
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ Error found in imports!")
        return
    
    print("\n✅ All imports successful")
    
    # Test 2: UI Manager
    if not test_ui_creation():
        print("\n❌ Error found in UI Manager!")
        return
    
    print("\n✅ UI Manager working")
    
    # Test 3: Class instantiation
    result = test_class_instantiation()
    if isinstance(result, tuple):
        success, class_name = result
        if not success:
            print(f"\n❌ Error found in {class_name}!")
            return
    
    print("\n✅ All classes instantiate successfully")
    
    # Test 4: Main app
    if not test_main_app():
        print("\n❌ Error found in main app!")
        return
    
    print("\n✅ Main app working")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nIf you see this, the error might be:")
    print("  1. During runtime (not during initialization)")
    print("  2. In a specific function that hasn't been called yet")
    print("  3. Related to user input or specific conditions")
    print("\nTry running the main program and see where it crashes.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}")
        traceback.print_exc()
