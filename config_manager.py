# ============================================
# CONFIG MANAGER - Environment & Configuration Management
# ============================================
import os
from pathlib import Path

class ConfigManager:
    """Manage configuration from .env file and defaults"""
    
    DEFAULTS = {
        # Voice recognition
        "GOOGLE_LANGUAGE": "id-ID",
        "FUZZY_THRESHOLD": "80",
        "PHONETIC_BONUS": "2",
        "CONFIDENCE_DISPLAY": "True",
        
        # Timing
        "COOLDOWN_SECONDS": "2",
        "LISTEN_TIMEOUT": "5",
        "PHRASE_LIMIT": "4",
        
        # Audio
        "DEFAULT_DEVICE": "1",
        "CALIBRATION_DURATION": "0.5",
        "NOISE_REDUCTION_ENABLED": "False",
        
        # Application
        "DEBUG_MODE": "True",
        "REQUIRE_COMMAND_CONFIRMATION": "False",
        "MAX_RETRIES": "3",
        "RETRY_DELAY": "1",
        
        # Features
        "ENABLE_OFFLINE_MODE": "False",
        "ENABLE_ACCENT_TRAINING": "False",
        "ENABLE_ANALYTICS": "True"
    }
    
    def __init__(self, env_file=".env"):
        self.env_file = env_file
        self.config = self.DEFAULTS.copy()
        self.load_env()
    
    def load_env(self):
        """Load configuration from .env file"""
        if not os.path.exists(self.env_file):
            print(f"⚠️  .env file not found. Using defaults.")
            print(f"   Create one from .env.example")
            return
        
        try:
            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in self.DEFAULTS:
                            self.config[key] = value
            
            print(f"✅ Configuration loaded from {self.env_file}")
        except Exception as e:
            print(f"⚠️  Error loading .env: {e}")
            print(f"   Using default configuration")
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default or self.DEFAULTS.get(key))
    
    def get_int(self, key):
        """Get integer configuration value"""
        return int(self.get(key, "0"))
    
    def get_float(self, key):
        """Get float configuration value"""
        return float(self.get(key, "0.0"))
    
    def get_bool(self, key):
        """Get boolean configuration value"""
        return self.get(key, "False").lower() in ("true", "1", "yes")
    
    def set(self, key, value):
        """Set configuration value (in memory only)"""
        self.config[key] = str(value)
    
    def save_env(self, env_file=None):
        """Save current configuration to .env file"""
        target_file = env_file or self.env_file
        try:
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write("# ============================================\n")
                f.write("# Auto-generated configuration file\n")
                f.write("# ============================================\n\n")
                
                for key, value in sorted(self.config.items()):
                    f.write(f"{key}={value}\n")
            
            print(f"✅ Configuration saved to {target_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False
    
    def validate(self):
        """Validate configuration values"""
        errors = []
        
        # Validate numeric values
        try:
            int(self.get("FUZZY_THRESHOLD"))
        except ValueError:
            errors.append("FUZZY_THRESHOLD must be integer (0-100)")
        
        try:
            int(self.get("COOLDOWN_SECONDS"))
        except ValueError:
            errors.append("COOLDOWN_SECONDS must be integer")
        
        try:
            int(self.get("MAX_RETRIES"))
        except ValueError:
            errors.append("MAX_RETRIES must be integer")
        
        # Validate ranges
        threshold = self.get_int("FUZZY_THRESHOLD")
        if not (0 <= threshold <= 100):
            errors.append("FUZZY_THRESHOLD must be between 0-100")
        
        if errors:
            print("⚠️  Configuration validation errors:")
            for error in errors:
                print(f"   • {error}")
            return False
        
        return True
    
    def show_config(self):
        """Display current configuration"""
        print("\n" + "=" * 60)
        print("CURRENT CONFIGURATION")
        print("=" * 60)
        
        for key, value in sorted(self.config.items()):
            print(f"  {key:<30} = {value}")
        
        print("=" * 60 + "\n")

# Singleton instance
_config_manager = None

def get_config(env_file=".env"):
    """Get or create singleton config manager"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(env_file)
    return _config_manager
