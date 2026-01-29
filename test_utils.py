"""
Test Utilities - Common test patterns and helpers
Reduces duplication in test files
"""

import subprocess
import sys
from typing import Callable, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TestResult:
    """Single test result"""
    name: str
    passed: bool
    message: str = ""
    error: Optional[str] = None


class TestRunner:
    """Base test runner with common patterns"""
    
    def __init__(self, test_name: str = "Test Suite", verbose: bool = True):
        self.test_name = test_name
        self.verbose = verbose
        self.results: List[TestResult] = []
        self.passed_count = 0
        self.failed_count = 0
        self.warning_count = 0
    
    def run_test(self, name: str, func: Callable[[], bool]) -> TestResult:
        """
        Run a single test function.
        
        Args:
            name: Test name
            func: Test function returning True/False
            
        Returns:
            TestResult with test outcome
        """
        if self.verbose:
            print(f"🧪 Testing: {name}... ", end="", flush=True)
        
        try:
            result = func()
            if result:
                if self.verbose:
                    print("✅ PASS")
                self.passed_count += 1
                test_result = TestResult(name, True, "PASS")
            else:
                if self.verbose:
                    print("⚠️  WARNING")
                self.warning_count += 1
                test_result = TestResult(name, False, "WARNING")
        except Exception as e:
            if self.verbose:
                print(f"❌ FAIL")
            self.failed_count += 1
            error_msg = f"{type(e).__name__}: {str(e)}"
            test_result = TestResult(name, False, "FAIL", error_msg)
            
            if self.verbose and "--verbose" in sys.argv:
                import traceback
                traceback.print_exc()
        
        self.results.append(test_result)
        return test_result
    
    def summary(self) -> Tuple[int, int, int]:
        """
        Print test summary.
        
        Returns:
            Tuple of (passed, failed, warnings)
        """
        total = len(self.results)
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"\nPassed:  {self.passed_count}/{total}")
        print(f"Failed:  {self.failed_count}/{total}")
        print(f"Warnings: {self.warning_count}/{total}")
        
        if self.failed_count == 0 and self.warning_count == 0:
            print("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
            return (self.passed_count, 0, 0)
        else:
            print(f"\n✗ {self.failed_count + self.warning_count} issue(s) found")
            return (self.passed_count, self.failed_count, self.warning_count)
    
    def exit_with_status(self) -> None:
        """Exit with appropriate status code"""
        if self.failed_count > 0:
            sys.exit(1)
        elif self.warning_count > 0:
            sys.exit(0)  # Warnings don't fail
        else:
            sys.exit(0)


class MenuTestRunner(TestRunner):
    """Specialized test runner for menu testing"""
    
    def run_menu_test(
        self,
        description: str,
        menu_num: int,
        expected_text: str,
        input_sequence: str = None,
        timeout: int = 10
    ) -> TestResult:
        """
        Run a menu test by executing script with input.
        
        Args:
            description: Test description
            menu_num: Menu number to test
            expected_text: Expected output text
            input_sequence: Input sequence (default: "{menu_num}\\n0\\n")
            timeout: Timeout in seconds
            
        Returns:
            TestResult with test outcome
        """
        if input_sequence is None:
            input_sequence = f"{menu_num}\n0\n"
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"TEST: {description}")
            print(f"Menu: {menu_num}")
            print('='*70)
        
        try:
            result = subprocess.run(
                [sys.executable, "main2.py"],
                input=input_sequence,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = result.stdout + result.stderr
            
            # Check for expected text
            if expected_text in output:
                if self.verbose:
                    print(f"✓ PASS - Found expected text: {expected_text}")
                self.passed_count += 1
                return TestResult(description, True, "PASS")
            else:
                if self.verbose:
                    print(f"✗ FAIL - Did not find: {expected_text}")
                    print(f"Output preview: {output[:200]}")
                self.failed_count += 1
                return TestResult(description, False, "FAIL", f"Expected text not found: {expected_text}")
                
        except subprocess.TimeoutExpired:
            if self.verbose:
                print(f"✗ FAIL - Timeout")
            self.failed_count += 1
            return TestResult(description, False, "FAIL", "Timeout exceeded")
        except Exception as e:
            if self.verbose:
                print(f"✗ FAIL - {e}")
            self.failed_count += 1
            return TestResult(description, False, "FAIL", str(e))


class ImportTestRunner(TestRunner):
    """Specialized test runner for import testing"""
    
    def run_import_test(self, name: str, module_path: str) -> TestResult:
        """
        Test if module can be imported.
        
        Args:
            name: Display name
            module_path: Module path (e.g., "config_manager.get_config")
            
        Returns:
            TestResult with import outcome
        """
        if self.verbose:
            print(f"📦 Importing: {name}... ", end="", flush=True)
        
        try:
            # Split module_path into module and item
            parts = module_path.rsplit(".", 1)
            if len(parts) == 2:
                module_name, item_name = parts
                module = __import__(module_name, fromlist=[item_name])
                getattr(module, item_name)
            else:
                __import__(module_path)
            
            if self.verbose:
                print("✓ OK")
            self.passed_count += 1
            return TestResult(name, True, "OK")
            
        except Exception as e:
            if self.verbose:
                print(f"✗ ERROR - {e}")
            self.failed_count += 1
            return TestResult(name, False, "ERROR", str(e))
    
    def run_multiple_imports(self, imports: List[Tuple[str, str]]) -> None:
        """
        Run multiple import tests.
        
        Args:
            imports: List of (name, module_path) tuples
        """
        for name, module_path in imports:
            self.run_import_test(name, module_path)
