"""
Test Infrastructure Module
Shared test utilities and base classes for testing
"""

from dataclasses import dataclass, field
from typing import Callable, Any, Optional, List
from datetime import datetime


@dataclass
class TestResult:
    """Dataclass for test execution results"""
    name: str
    passed: bool
    message: str = ""
    error: Optional[str] = None
    duration: float = 0.0


class TestRunner:
    """Base class for running tests with comprehensive tracking"""
    
    def __init__(self, verbose: bool = True) -> None:
        """
        Initialize test runner
        
        Args:
            verbose: Whether to print detailed output
        """
        self.verbose = verbose
        self.passed_count = 0
        self.failed_count = 0
        self.warning_count = 0
        self.results: List[TestResult] = []
        self.start_time: Optional[datetime] = None
    
    def run_test(self, name: str, test_func: Callable[[], bool]) -> TestResult:
        """
        Run a single test
        
        Args:
            name: Name of the test
            test_func: Function that returns True if passed
            
        Returns:
            TestResult with test outcome
        """
        import time
        
        start = time.time()
        try:
            result = test_func()
            elapsed = time.time() - start
            
            if result:
                self.passed_count += 1
                status = "[OK]"
                result_obj = TestResult(name, True, "Passed", None, elapsed)
            else:
                self.warning_count += 1
                status = "[WARN]"
                result_obj = TestResult(name, False, "Failed", None, elapsed)
            
            if self.verbose:
                print(f"{status} {name} ({elapsed:.3f}s)")
            
            self.results.append(result_obj)
            return result_obj
            
        except Exception as e:
            elapsed = time.time() - start
            self.failed_count += 1
            error_msg = str(e)
            result_obj = TestResult(name, False, "Error", error_msg, elapsed)
            
            if self.verbose:
                print(f"[FAIL] {name}: {error_msg} ({elapsed:.3f}s)")
            
            self.results.append(result_obj)
            return result_obj
    
    def summary(self) -> str:
        """Get summary of all test results"""
        total = self.passed_count + self.failed_count + self.warning_count
        return (
            f"\n{'='*50}\n"
            f"Test Summary\n"
            f"{'='*50}\n"
            f"Total: {total}\n"
            f"Passed: {self.passed_count}\n"
            f"Failed: {self.failed_count}\n"
            f"Warnings: {self.warning_count}\n"
            f"{'='*50}\n"
        )
    
    def exit_with_status(self) -> int:
        """Return exit code based on test results"""
        return 0 if self.failed_count == 0 else 1


class MenuTestRunner(TestRunner):
    """Specialized test runner for menu testing"""
    
    def run_menu_test(self, menu_name: str, test_func: Callable[[], bool]) -> TestResult:
        """
        Run menu-specific test
        
        Args:
            menu_name: Name of the menu
            test_func: Function that tests the menu
            
        Returns:
            TestResult with menu test outcome
        """
        return self.run_test(f"Menu: {menu_name}", test_func)


class ImportTestRunner(TestRunner):
    """Specialized test runner for import testing"""
    
    def run_import_test(self, module_name: str, item_path: str) -> TestResult:
        """
        Run import test
        
        Args:
            module_name: Module to import
            item_path: Dot-path to item within module (e.g., "module.function")
            
        Returns:
            TestResult with import test outcome
        """
        def test() -> bool:
            try:
                parts = item_path.split('.')
                module = __import__(parts[0])
                for part in parts[1:-1]:
                    module = getattr(module, part)
                getattr(module, parts[-1])
                return True
            except (ImportError, AttributeError):
                return False
        
        return self.run_test(f"Import: {item_path}", test)
