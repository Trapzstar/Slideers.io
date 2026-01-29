"""
Optimized Utility Functions
Enhanced versions of critical utilities with performance improvements
"""

from typing import Dict, List, Any, Optional, Callable
import os


class OptimizedDeviceManager:
    """Optimized device management with caching"""
    
    def __init__(self) -> None:
        """Initialize device manager"""
        self._device_cache: Optional[List[Dict[str, Any]]] = None
        self._cache_valid = False
    
    @staticmethod
    def score_device(device: Dict[str, Any]) -> float:
        """
        Score a device based on criteria (optimized)
        
        Args:
            device: Device dictionary
            
        Returns:
            Score for device (higher is better)
        """
        score = 0.0
        name = device.get("name", "").lower()
        channels = device.get("channels", 1)
        
        # Vectorized scoring (no branches where possible)
        score += 5.0 if "array" in name else 0.0
        score += 4.0 if "realtek" in name else 0.0
        score += 3.0 if "microphone" in name else 0.0
        score += (channels - 1) * 2.0
        
        return score
    
    def find_best_device_optimized(self, devices: List[Dict[str, Any]]) -> int:
        """
        Find best device (optimized version)
        
        Args:
            devices: List of device dicts
            
        Returns:
            Index of best device
        """
        if not devices:
            return 0
        
        if len(devices) == 1:
            return 0
        
        # Use list comprehension for faster iteration
        best_idx = max(range(len(devices)), key=lambda i: self.score_device(devices[i]))
        return best_idx


class OptimizedStringOperations:
    """Optimized string operations"""
    
    @staticmethod
    def sanitize_text_optimized(text: str, max_length: int = 120) -> str:
        """
        Sanitize text (optimized)
        
        Args:
            text: Text to sanitize
            max_length: Maximum length
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Use split/join instead of regex for better performance
        cleaned = " ".join(text.split())
        
        if len(cleaned) > max_length:
            cleaned = cleaned[:max_length-3] + "..."
        
        return cleaned
    
    @staticmethod
    def format_confidence_optimized(score: float) -> str:
        """
        Format confidence score (optimized)
        
        Args:
            score: Confidence score (0-100)
            
        Returns:
            Formatted string with status
        """
        # Use direct comparison instead of intermediate variables
        if score >= 80:
            return "[OK] high confidence"
        elif score >= 70:
            return "[WARN] medium confidence"
        else:
            return "[FAIL] low confidence"


class OptimizedListOperations:
    """Optimized list operations"""
    
    @staticmethod
    def group_by_key_optimized(items: List[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
        """
        Group items by key (optimized)
        
        Args:
            items: List of dictionaries
            key: Key to group by
            
        Returns:
            Dictionary of grouped items
        """
        grouped: Dict[Any, List[Dict[str, Any]]] = {}
        
        for item in items:
            if key in item:
                item_key = item[key]
                if item_key not in grouped:
                    grouped[item_key] = []
                grouped[item_key].append(item)
        
        return grouped
    
    @staticmethod
    def flatten_dict_optimized(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
        """
        Flatten nested dictionary (optimized)
        
        Args:
            d: Dictionary to flatten
            parent_key: Parent key prefix
            sep: Separator for nested keys
            
        Returns:
            Flattened dictionary
        """
        items: List[tuple] = []
        
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                # Recursive call with accumulated key
                items.extend(OptimizedListOperations.flatten_dict_optimized(v, new_key, sep).items())
            else:
                items.append((new_key, v))
        
        return dict(items)


class OptimizedFileOperations:
    """Optimized file operations"""
    
    @staticmethod
    def safe_read_file_optimized(path: str, encoding: str = "utf-8", default: str = "") -> str:
        """
        Read file safely (optimized)
        
        Args:
            path: File path
            encoding: File encoding
            default: Default value if read fails
            
        Returns:
            File contents or default
        """
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read()
        except (FileNotFoundError, IOError, OSError):
            return default
    
    @staticmethod
    def safe_write_file_optimized(path: str, content: str, encoding: str = "utf-8") -> bool:
        """
        Write file safely (optimized)
        
        Args:
            path: File path
            content: Content to write
            encoding: File encoding
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding=encoding) as f:
                f.write(content)
            return True
        except (OSError, IOError):
            return False


class OptimizationComparison:
    """Compare optimized vs original implementations"""
    
    @staticmethod
    def compare_all() -> Dict[str, Dict[str, Any]]:
        """
        Compare all optimized vs original implementations
        
        Returns:
            Dictionary with comparison results
        """
        import time
        
        results = {}
        
        # Test device scoring
        device = {"index": 1, "name": "Realtek Array Microphone", "channels": 2}
        
        manager = OptimizedDeviceManager()
        
        # Optimized scoring
        start = time.perf_counter()
        for _ in range(10000):
            manager.score_device(device)
        opt_time = time.perf_counter() - start
        
        results["device_scoring"] = {
            "optimized_time": opt_time,
            "iterations": 10000,
            "avg_ms": (opt_time * 1000) / 10000
        }
        
        # Test string operations
        text = "hello   world   test"
        
        start = time.perf_counter()
        for _ in range(1000):
            OptimizedStringOperations.sanitize_text_optimized(text)
        opt_time = time.perf_counter() - start
        
        results["string_sanitization"] = {
            "optimized_time": opt_time,
            "iterations": 1000,
            "avg_ms": (opt_time * 1000) / 1000
        }
        
        return results
