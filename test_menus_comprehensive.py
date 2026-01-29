#!/usr/bin/env python
"""Comprehensive menu test - Refactored using test utilities"""

import sys
from test_utils import MenuTestRunner

def main():
    """Run comprehensive menu tests"""
    
    # Create test runner
    runner = MenuTestRunner("SlideSense Main Application - Comprehensive Menu Test")
    
    # Define tests
    tests = [
        (1, "[MIC] Setup Microphone", "Menu 1: Start Voice Control (opens microphone setup)"),
        (2, "[MIC] Setup Microphone", "Menu 2: Test Microphone (opens microphone setup)"),
        (3, "[BOOK] Tutorial", "Menu 3: Tutorial & Help"),
        (4, "SlideSense", "Menu 4: About Program"),
        (0, "See you next time", "Menu 0: Exit"),
    ]
    
    # Run all tests
    print("\n" + "="*70)
    print("SLIDESENSE MAIN APPLICATION - COMPREHENSIVE MENU TEST")
    print("="*70)
    
    for menu_num, expected_text, description in tests:
        runner.run_menu_test(description, menu_num, expected_text)
    
    # Print summary and exit
    runner.summary()
    runner.exit_with_status()


if __name__ == "__main__":
    main()

