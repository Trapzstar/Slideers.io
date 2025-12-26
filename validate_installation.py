# ============================================
# INSTALLATION VALIDATOR
# ============================================
"""Validate that all components are working correctly"""

import sys
import os

def validate():
    """Run validation checks"""
    print("\n" + "="*60)
    print("VALIDATING INSTALLATION")
    print("="*60 + "\n")
    
    errors = []
    
    # Check 1: Required dependencies
    print("1️⃣  Checking dependencies...")
    dependencies = {
        'pyautogui': 'PyAutoGUI (PowerPoint control)',
        'speech_recognition': 'SpeechRecognition (Voice to text)',
        'pyaudio': 'PyAudio (Audio input)',
    }
    
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {description}")
        except ImportError:
            print(f"   ❌ {description}")
            errors.append(f"Missing: {module}")
    
    # Check 2: New modules
    print("\n2️⃣  Checking new modules...")
    new_modules = [
        'voice_quality_tester',
        'adaptive_matcher',
        'phoneme_variants',
        'error_handler',
        'config_manager',
        'input_validator',
        'feedback_ui',
        'interactive_setup',
        'accent_training',
    ]
    
    for module in new_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}.py")
        except ImportError as e:
            print(f"   ❌ {module}.py: {str(e)[:50]}")
            errors.append(f"Module import error: {module}")
    
    # Check 3: Core modules
    print("\n3️⃣  Checking core modules...")
    core_modules = [
        'hybrid_voice_recognizer',
        'voice_detector',
        'powerpoint_controller',
    ]
    
    for module in core_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}.py")
        except ImportError as e:
            print(f"   ❌ {module}.py: {str(e)[:50]}")
            errors.append(f"Module import error: {module}")
    
    # Check 4: Configuration files
    print("\n4️⃣  Checking configuration files...")
    config_files = [
        '.env.example',
        'requirements.txt',
    ]
    
    for filename in config_files:
        if os.path.exists(filename):
            print(f"   ✅ {filename}")
        else:
            print(f"   ⚠️  {filename} (optional)")
    
    # Check 5: Documentation
    print("\n5️⃣  Checking documentation...")
    docs = [
        'QUICK_START.md',
        'IMPROVEMENTS.md',
        'SECURITY_GUIDE.md',
        'CRITICAL_FIXES.md',
        'TROUBLESHOOTING.md',
        'USAGE_EXAMPLES.md',
    ]
    
    for doc in docs:
        if os.path.exists(doc):
            print(f"   ✅ {doc}")
        else:
            print(f"   ⚠️  {doc} (optional)")
    
    # Summary
    print("\n" + "="*60)
    if errors:
        print("❌ VALIDATION FAILED")
        print("="*60)
        print("\nErrors found:")
        for error in errors:
            print(f"  • {error}")
        print("\nFix:")
        print("  pip install -r requirements.txt")
        return False
    else:
        print("✅ VALIDATION PASSED")
        print("="*60)
        print("\n🎉 All components are installed correctly!")
        print("\nNext steps:")
        print("  1. Copy .env.example to .env")
        print("  2. Run: python main.py --test-mic")
        print("  3. Run: python main.py")
        return True

if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
