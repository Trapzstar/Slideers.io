#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST_GUI_COMPONENTS.py - Test all GUI components

Menguji:
1. GUI Home dashboard
2. Stats panel
3. Interactive tutorial
4. Unified app
5. UI responsiveness
"""

import sys

def test_gui_imports():
    """Test that all GUI modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: GUI Module Imports")
    print("="*60)
    
    modules = [
        ("gui_home", "GUIHome"),
        ("gui_stats_panel", "StatsPanel"),
        ("gui_interactive_tutorial", "InteractiveTutorial"),
        ("gui_unified_app", "UnifiedGUIApp"),
    ]
    
    passed = 0
    failed = 0
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            print(f"✅ {module_name}.{class_name} - OK")
            passed += 1
        except ImportError as e:
            print(f"❌ {module_name} - Import Error: {e}")
            failed += 1
        except AttributeError as e:
            print(f"❌ {class_name} not found in {module_name}")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0

def test_gui_initialization():
    """Test GUI component initialization"""
    print("\n" + "="*60)
    print("TEST 2: GUI Component Initialization")
    print("="*60)
    
    try:
        from gui_home import GUIHome
        gui_home = GUIHome()
        print("✅ GUIHome initialized")
    except Exception as e:
        print(f"❌ GUIHome init failed: {e}")
        return False
    
    try:
        from gui_stats_panel import StatsPanel
        stats = StatsPanel()
        print("✅ StatsPanel initialized")
    except Exception as e:
        print(f"❌ StatsPanel init failed: {e}")
        return False
    
    try:
        from gui_interactive_tutorial import InteractiveTutorial
        tutorial = InteractiveTutorial()
        print(f"✅ InteractiveTutorial initialized ({len(tutorial.tutorial_steps)} steps)")
    except Exception as e:
        print(f"❌ InteractiveTutorial init failed: {e}")
        return False
    
    try:
        from gui_unified_app import UnifiedGUIApp
        app = UnifiedGUIApp()
        print("✅ UnifiedGUIApp initialized")
    except Exception as e:
        print(f"❌ UnifiedGUIApp init failed: {e}")
        return False
    
    print("\n✅ All components initialized successfully")
    return True

def test_stats_panel_functionality():
    """Test stats panel functionality"""
    print("\n" + "="*60)
    print("TEST 3: Stats Panel Functionality")
    print("="*60)
    
    try:
        from gui_stats_panel import StatsPanel
        stats = StatsPanel()
        
        # Test recording commands
        stats.record_command("next_slide")
        stats.record_command("next_slide")
        stats.record_command("previous_slide")
        print("✅ Commands recorded")
        
        # Test getting usage
        usage = stats.get_command_usage()
        print(f"✅ Command usage retrieved: {usage}")
        
        # Test most used
        most_used, count = stats.get_most_used_command()
        print(f"✅ Most used command: {most_used} (×{count})")
        
        # Test total
        total = stats.get_total_commands()
        print(f"✅ Total commands: {total}")
        
        return True
    except Exception as e:
        print(f"❌ Stats panel test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tutorial_structure():
    """Test tutorial structure"""
    print("\n" + "="*60)
    print("TEST 4: Tutorial Structure")
    print("="*60)
    
    try:
        from gui_interactive_tutorial import InteractiveTutorial
        tutorial = InteractiveTutorial()
        
        total_steps = len(tutorial.tutorial_steps)
        print(f"✅ Tutorial has {total_steps} steps")
        
        # Verify each step has required fields
        for i, step in enumerate(tutorial.tutorial_steps):
            required = ["title", "content", "command", "tips"]
            for field in required:
                if field not in step:
                    print(f"❌ Step {i} missing field: {field}")
                    return False
        
        print(f"✅ All {total_steps} steps have required fields")
        
        # Verify step flow
        print("\nTutorial Steps:")
        for i, step in enumerate(tutorial.tutorial_steps, 1):
            cmd = step["command"] or "INTRO/OUTRO"
            print(f"  {i}. {step['title']} ({cmd})")
        
        return True
    except Exception as e:
        print(f"❌ Tutorial structure test failed: {e}")
        return False

def test_constants_integration():
    """Test integration with constants"""
    print("\n" + "="*60)
    print("TEST 5: Constants Integration")
    print("="*60)
    
    try:
        from constants import MAIN_COMMANDS, KEYWORDS_INDEX
        from gui_home import GUIHome
        from gui_interactive_tutorial import InteractiveTutorial
        
        # Verify all commands are covered in tutorial
        tutorial = InteractiveTutorial()
        tutorial_commands = [
            step["command"] for step in tutorial.tutorial_steps 
            if step["command"] is not None
        ]
        
        print(f"✅ Tutorial covers {len(tutorial_commands)} commands")
        
        # Check command consistency
        main_cmd_names = list(MAIN_COMMANDS.keys())
        tutorial_cmd_names = [c for c in tutorial_commands if c]
        
        print(f"✅ Main commands: {main_cmd_names}")
        print(f"✅ Tutorial commands: {tutorial_cmd_names}")
        
        # Verify all tutorial commands exist in constants
        for cmd in tutorial_cmd_names:
            if cmd not in MAIN_COMMANDS:
                print(f"❌ Tutorial command '{cmd}' not in MAIN_COMMANDS")
                return False
        
        print(f"✅ All tutorial commands match MAIN_COMMANDS")
        return True
    except Exception as e:
        print(f"❌ Constants integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("GUI COMPONENTS TEST SUITE")
    print("="*60)
    
    results = []
    
    results.append(("GUI Imports", test_gui_imports()))
    results.append(("GUI Initialization", test_gui_initialization()))
    results.append(("Stats Functionality", test_stats_panel_functionality()))
    results.append(("Tutorial Structure", test_tutorial_structure()))
    results.append(("Constants Integration", test_constants_integration()))
    
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
        print("\n🎉 ALL GUI TESTS PASSED! Phase 2 Step 1 Complete!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
