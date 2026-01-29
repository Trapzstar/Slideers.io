"""
Performance Benchmarking and Optimization Module
Identifies hot paths and measures performance improvements
"""

import time
import sys
import json
from typing import Callable, Dict, Any, List, Tuple
from dataclasses import dataclass, asdict
from contextlib import contextmanager


@dataclass
class BenchmarkResult:
    """Results from a benchmark run"""
    function_name: str
    total_time: float
    avg_time: float
    min_time: float
    max_time: float
    iterations: int
    calls_per_second: float


class PerformanceProfiler:
    """Profile and measure performance of functions"""
    
    def __init__(self) -> None:
        """Initialize profiler"""
        self.results: Dict[str, BenchmarkResult] = {}
        self.hotspots: List[Tuple[str, float]] = []
    
    def benchmark(
        self, 
        func: Callable[[], Any], 
        iterations: int = 1000,
        name: str = ""
    ) -> BenchmarkResult:
        """
        Benchmark a function
        
        Args:
            func: Function to benchmark
            iterations: Number of times to call function
            name: Custom name for function
            
        Returns:
            BenchmarkResult with timing data
        """
        func_name = name or func.__name__
        times: List[float] = []
        
        # Warmup
        for _ in range(10):
            func()
        
        # Actual benchmark
        for _ in range(iterations):
            start = time.perf_counter()
            func()
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        
        total_time = sum(times)
        avg_time = total_time / iterations
        min_time = min(times)
        max_time = max(times)
        calls_per_second = 1.0 / avg_time if avg_time > 0 else 0
        
        result = BenchmarkResult(
            function_name=func_name,
            total_time=total_time,
            avg_time=avg_time,
            min_time=min_time,
            max_time=max_time,
            iterations=iterations,
            calls_per_second=calls_per_second
        )
        
        self.results[func_name] = result
        return result
    
    def compare_implementations(
        self,
        impl1: Callable[[], Any],
        impl2: Callable[[], Any],
        name1: str = "Implementation 1",
        name2: str = "Implementation 2",
        iterations: int = 1000
    ) -> Dict[str, Any]:
        """
        Compare performance of two implementations
        
        Args:
            impl1: First implementation
            impl2: Second implementation
            name1: Name for first implementation
            name2: Name for second implementation
            iterations: Iterations per implementation
            
        Returns:
            Dictionary with comparison results
        """
        result1 = self.benchmark(impl1, iterations, name1)
        result2 = self.benchmark(impl2, iterations, name2)
        
        speedup = result1.avg_time / result2.avg_time if result2.avg_time > 0 else 0
        improvement = ((result1.avg_time - result2.avg_time) / result1.avg_time * 100) if result1.avg_time > 0 else 0
        
        return {
            "implementation_1": asdict(result1),
            "implementation_2": asdict(result2),
            "speedup": speedup,
            "improvement_percent": improvement,
            "faster": name2 if speedup > 1 else name1
        }
    
    def identify_hotspots(self, threshold_percent: float = 10.0) -> List[Tuple[str, float]]:
        """
        Identify hotspot functions
        
        Args:
            threshold_percent: Minimum percentage of total time to consider hotspot
            
        Returns:
            List of (function_name, time_percent) tuples
        """
        total_time = sum(r.total_time for r in self.results.values())
        if total_time == 0:
            return []
        
        hotspots = []
        for name, result in self.results.items():
            percent = (result.total_time / total_time) * 100
            if percent >= threshold_percent:
                hotspots.append((name, percent))
        
        self.hotspots = sorted(hotspots, key=lambda x: x[1], reverse=True)
        return self.hotspots
    
    def report(self, verbose: bool = True) -> str:
        """
        Generate performance report
        
        Args:
            verbose: Include detailed information
            
        Returns:
            Formatted report string
        """
        if not self.results:
            return "No benchmarks to report"
        
        lines = [
            "\n" + "="*70,
            "PERFORMANCE BENCHMARK REPORT",
            "="*70
        ]
        
        for name, result in self.results.items():
            lines.append(f"\n{name}:")
            lines.append(f"  Avg Time:        {result.avg_time*1000:.4f} ms")
            lines.append(f"  Min Time:        {result.min_time*1000:.4f} ms")
            lines.append(f"  Max Time:        {result.max_time*1000:.4f} ms")
            lines.append(f"  Calls/Second:    {result.calls_per_second:.0f}")
            lines.append(f"  Total Time:      {result.total_time:.4f} s")
        
        if self.hotspots:
            lines.append("\n" + "="*70)
            lines.append("HOTSPOT ANALYSIS")
            lines.append("="*70)
            for name, percent in self.hotspots:
                lines.append(f"  {name}: {percent:.1f}%")
        
        lines.append("\n" + "="*70 + "\n")
        return "\n".join(lines)


@contextmanager
def measure_time(name: str = "Operation"):
    """Context manager to measure execution time"""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name} took {elapsed*1000:.2f} ms")


class CacheOptimizer:
    """Simple caching optimizer for frequently called functions"""
    
    def __init__(self, max_size: int = 128) -> None:
        """Initialize cache"""
        self.cache: Dict[Any, Any] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def memoize(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Memoize a function (cache results)
        
        Args:
            func: Function to memoize
            
        Returns:
            Wrapped function with caching
        """
        def wrapper(*args, **kwargs) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            
            if key in self.cache:
                self.hits += 1
                return self.cache[key]
            
            self.misses += 1
            result = func(*args, **kwargs)
            
            if len(self.cache) >= self.max_size:
                # Simple eviction: remove first item (FIFO)
                self.cache.pop(next(iter(self.cache)))
            
            self.cache[key] = result
            return result
        
        return wrapper
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total": total,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache)
        }


class OptimizationAnalyzer:
    """Analyze code for optimization opportunities"""
    
    def __init__(self) -> None:
        """Initialize analyzer"""
        self.issues: List[Dict[str, str]] = []
    
    def check_list_operations(self, code: str) -> List[str]:
        """Check for inefficient list operations"""
        issues = []
        
        # Check for repeated list operations
        if code.count(".append(") > 10:
            issues.append("High frequency of list.append() - consider pre-allocating")
        
        if code.count(".remove(") > 0:
            issues.append("Using list.remove() - consider set operations")
        
        return issues
    
    def check_loop_operations(self, code: str) -> List[str]:
        """Check for inefficient loop operations"""
        issues = []
        
        if ".append(" in code and code.count("for ") > 3:
            issues.append("Multiple loops with append - consider list comprehensions")
        
        return issues
    
    def check_string_operations(self, code: str) -> List[str]:
        """Check for inefficient string operations"""
        issues = []
        
        if code.count(" + ") > 10 and "str" in code:
            issues.append("Frequent string concatenation - consider using join()")
        
        return issues
    
    def analyze(self, code: str) -> Dict[str, List[str]]:
        """Analyze code for optimization opportunities"""
        return {
            "list_operations": self.check_list_operations(code),
            "loop_operations": self.check_loop_operations(code),
            "string_operations": self.check_string_operations(code)
        }


# Performance guidelines
PERFORMANCE_TARGETS = {
    "device_detection": 0.1,  # 100ms max
    "command_matching": 0.05,  # 50ms max
    "ui_rendering": 0.016,  # 16ms max (60 FPS)
    "voice_recognition": 1.0,  # 1s max
    "file_operations": 0.5,  # 500ms max
}


def check_performance_target(actual_time: float, target_name: str) -> bool:
    """
    Check if performance meets target
    
    Args:
        actual_time: Actual execution time in seconds
        target_name: Target name from PERFORMANCE_TARGETS
        
    Returns:
        True if meets target, False otherwise
    """
    target = PERFORMANCE_TARGETS.get(target_name, 1.0)
    return actual_time <= target
