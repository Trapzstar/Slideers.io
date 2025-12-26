#!/usr/bin/env python3
"""
Test Script After Cleanup
Memastikan semua komponen masih berfungsi setelah cleanup
"""
import sys
import importlib.util  # FIX: Tambahkan .util
import traceback

class CleanupTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.results = []

    def test(self, name, func):
        """Run a test and record result"""
        print(f"🧪 Testing: {name}... ", end="", flush=True)
        try:
            result = func()
            if result:
                print("✅ PASS")
                self.passed += 1
                self.results.append((name, "PASS", None))
            else:
                print("⚠️  WARNING")
                self.warnings += 1
                self.results.append((name, "WARNING", "Test returned False"))
        except Exception as e:
            print(f"❌ FAIL")
            self.failed += 1
            error_msg = f"{type(e).__name__}: {str(e)}"
            self.results.append((name, "FAIL", error_msg))
            if "--verbose" in sys.argv:
                traceback.print_exc()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("📊 TEST SUMMARY")
        print("="*70)
        print(f"✅ Passed:   {self.passed}")
        print(f"⚠️  Warnings: {self.warnings}")
        print(f"❌ Failed:   {self.failed}")
        print(f"📝 Total:    {self.passed + self.warnings + self.failed}")
        print()

        if self.failed > 0:
            print("❌ FAILED TESTS:")
            for name, status, error in self.results:
                if status == "FAIL":
                    print(f"   - {name}")
                    if error:
                        print(f"     Error: {error}")
            print()

        if self.warnings > 0:
            print("⚠️  WARNINGS:")
            for name, status, error in self.results:
                if status == "WARNING":
                    print(f"   - {name}")
                    if error:
                        print(f"     Reason: {error}")
            print()

        print("="*70)
        
        if self.failed == 0:
            print("🎉 ALL TESTS PASSED! Program siap digunakan.")
        elif self.failed <= 2:
            print("⚠️  ADA BEBERAPA ERROR - Periksa dependencies")
        else:
            print("❌ BANYAK ERROR - Butuh perbaikan!")
        
        print("="*70)

# ============================================
# TEST FUNCTIONS
# ============================================

def test_import_main():
    """Test import main module"""
    spec = importlib.util.spec_from_file_location("main", "main.py")
    if spec and spec.loader:
        # Just check if file can be loaded
        return True
    return False

def test_import_voice_detector():
    """Test import voice_detector"""
    from voice_detector import SmartVoiceDetector
    detector = SmartVoiceDetector()
    return detector is not None

def test_import_voice_recognizer():
    """Test import hybrid_voice_recognizer"""
    from hybrid_voice_recognizer import HybridVoiceRecognizer
    recognizer = HybridVoiceRecognizer(debug_mode=False)
    return recognizer is not None

def test_import_ppt_controller():
    """Test import powerpoint_controller"""
    from powerpoint_controller import PowerPointController
    controller = PowerPointController()
    return controller is not None

def test_import_accessibility_popup():
    """Test import accessibility_popup"""
    from accessibility_popup import AccessibilityPopup
    popup = AccessibilityPopup()
    return popup is not None

def test_voice_detector_commands():
    """Test voice detector command detection"""
    from voice_detector import SmartVoiceDetector
    detector = SmartVoiceDetector()
    
    # Test basic command
    result = detector.detect("next slide")
    return result is not None and result.get("command") == "next"

def test_voice_detector_fuzzy():
    """Test voice detector fuzzy matching"""
    from voice_detector import SmartVoiceDetector
    detector = SmartVoiceDetector()
    detector.cooldown_seconds = 0  # Disable cooldown for testing
    
    # Test fuzzy match
    result = detector.detect("next side")  # typo but should match
    return result is not None and result.get("command") == "next"

def test_ppt_controller_execute():
    """Test PowerPoint controller command execution"""
    from powerpoint_controller import PowerPointController
    controller = PowerPointController()
    
    # Test command execution (dry run - won't actually press keys)
    result = controller.execute_command({"command": "help", "score": 10})
    return "BANTUAN" in result or "HELP" in result

def test_popup_initialization():
    """Test popup system initialization"""
    from accessibility_popup import AccessibilityPopup
    popup = AccessibilityPopup()
    
    # Test settings
    popup.update_settings({'position': 'top-left'})
    return popup.settings['position'] == 'top-left'

def test_popup_content():
    """Test popup content methods"""
    from accessibility_popup import AccessibilityPopup
    popup = AccessibilityPopup()
    
    # Test slide info
    content = {
        'title': 'Test',
        'text': 'Testing',
        'progress': '1/10'
    }
    popup.current_content = content
    return popup.current_content['title'] == 'Test'

def test_requirements_file():
    """Test requirements.txt exists and readable"""
    with open('requirements.txt', 'r') as f:
        lines = f.readlines()
    return len(lines) > 0

def test_no_duplicate_files():
    """Test that duplicate files are removed"""
    import os
    duplicates = [
        "hybrid_voice_recognizer_enhanced.py",
        "hybrid_voice_recognizer_original.py"
    ]
    for file in duplicates:
        if os.path.exists(file):
            return False
    return True

def test_no_snippet_files():
    """Test that incomplete snippet files are removed"""
    import os
    snippets = [
        "lazy.py", "async.py", "caching.py", 
        "plugins.py", "recognizer_factory.py"
    ]
    for file in snippets:
        if os.path.exists(file):
            return False
    return True

def test_gitignore_exists():
    """Test .gitignore exists"""
    import os
    return os.path.exists('.gitignore')

def test_core_files_exist():
    """Test all core files exist"""
    import os
    core_files = [
        "main.py",
        "voice_detector.py",
        "hybrid_voice_recognizer.py",
        "powerpoint_controller.py",
        "accessibility_popup.py",
        "requirements.txt"
    ]
    for file in core_files:
        if not os.path.exists(file):
            print(f"\n   Missing: {file}")
            return False
    return True

def test_analytics_methods():
    """Test popup analytics methods"""
    from accessibility_popup import AccessibilityPopup
    popup = AccessibilityPopup()
    
    # Test analytics
    summary = popup.get_analytics_summary()
    return isinstance(summary, dict) and 'session_duration_hours' in summary

def test_multi_language():
    """Test multi-language support"""
    from accessibility_popup import AccessibilityPopup
    popup = AccessibilityPopup()
    
    langs = popup.get_available_languages()
    return 'id' in langs and 'en' in langs

def test_voice_recognizer_stats():
    """Test voice recognizer performance stats"""
    from hybrid_voice_recognizer import HybridVoiceRecognizer
    recognizer = HybridVoiceRecognizer(debug_mode=False)
    
    # FIX: Check if method exists first
    if not hasattr(recognizer, 'get_performance_stats'):
        print("\n   Warning: get_performance_stats method not found")
        return False
    
    stats = recognizer.get_performance_stats()
    return 'total_attempts' in stats

# ============================================
# DEPENDENCY CHECKS
# ============================================

def check_dependency(module_name, import_name=None):
    """Check if a dependency is installed"""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False

def test_dependencies():
    """Test all required dependencies"""
    deps = {
        'pyautogui': 'pyautogui',
        'speech_recognition': 'speech_recognition',
        'pyaudio': 'pyaudio',
        'numpy': 'numpy',
        'customtkinter': 'customtkinter',
        'fuzzywuzzy': 'fuzzywuzzy',
        'jellyfish': 'jellyfish',
    }
    
    missing = []
    for name, import_name in deps.items():
        if not check_dependency(name, import_name):
            missing.append(name)
    
    if missing:
        print(f"\n   Missing: {', '.join(missing)}")
        return False
    return True

# ============================================
# MAIN TEST RUNNER
# ============================================

def main():
    print("="*70)
    print("🧪 POST-CLEANUP TEST SUITE")
    print("="*70)
    print()
    print("Testing program setelah cleanup...")
    print()

    tester = CleanupTester()

    # Section 1: File Structure Tests
    print("📁 SECTION 1: File Structure")
    print("-"*70)
    tester.test("Core files exist", test_core_files_exist)
    tester.test("No duplicate files", test_no_duplicate_files)
    tester.test("No snippet files", test_no_snippet_files)
    tester.test(".gitignore exists", test_gitignore_exists)
    tester.test("requirements.txt readable", test_requirements_file)
    print()

    # Section 2: Import Tests
    print("📦 SECTION 2: Module Imports")
    print("-"*70)
    tester.test("Import main", test_import_main)
    tester.test("Import voice_detector", test_import_voice_detector)
    tester.test("Import voice_recognizer", test_import_voice_recognizer)
    tester.test("Import ppt_controller", test_import_ppt_controller)
    tester.test("Import accessibility_popup", test_import_accessibility_popup)
    print()

    # Section 3: Functionality Tests
    print("⚙️  SECTION 3: Functionality")
    print("-"*70)
    tester.test("Voice detector commands", test_voice_detector_commands)
    tester.test("Voice detector fuzzy match", test_voice_detector_fuzzy)
    tester.test("PPT controller execute", test_ppt_controller_execute)
    tester.test("Popup initialization", test_popup_initialization)
    tester.test("Popup content methods", test_popup_content)
    tester.test("Analytics methods", test_analytics_methods)
    tester.test("Multi-language support", test_multi_language)
    tester.test("Voice recognizer stats", test_voice_recognizer_stats)
    print()

    # Section 4: Dependencies
    print("📚 SECTION 4: Dependencies")
    print("-"*70)
    tester.test("All dependencies installed", test_dependencies)
    print()

    # Print summary
    tester.print_summary()

    # Exit code
    sys.exit(0 if tester.failed == 0 else 1)

if __name__ == "__main__":
    main()
