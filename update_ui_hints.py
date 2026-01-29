#!/usr/bin/env python3
"""
Script to add remaining type hints to ui_manager.py
"""

replacements = [
    ('    def show_microphone_list(self, devices):\n        """Show microphone list for manual selection"""',
     '    def show_microphone_list(self, devices: List[Dict[str, Any]]) -> Optional[int]:\n        """Show microphone list for manual selection"""'),
    
    ('    def show_auto_detect_progress(self):\n        """Show progress while auto-detecting microphone"""',
     '    def show_auto_detect_progress(self) -> None:\n        """Show progress while auto-detecting microphone"""'),
    
    ('    def show_device_found(self, device_name, device_index):\n        """Show device found message"""',
     '    def show_device_found(self, device_name: str, device_index: int) -> bool:\n        """Show device found message"""'),
    
    ('    def show_microphone_test_start(self, duration=3):\n        """Show microphone test starting"""',
     '    def show_microphone_test_start(self, duration: int = 3) -> None:\n        """Show microphone test starting"""'),
    
    ('    def show_test_progress(self, duration=3):\n        """Show test progress"""',
     '    def show_test_progress(self, duration: int = 3) -> None:\n        """Show test progress"""'),
    
    ('    def show_test_result(self, success, message=""):\n        """Show test result"""',
     '    def show_test_result(self, success: bool, message: str = "") -> None:\n        """Show test result"""'),
    
    ('    def show_voice_control_starting(self):\n        """Show voice control is starting"""',
     '    def show_voice_control_starting(self) -> None:\n        """Show voice control is starting"""'),
    
    ('    def show_voice_control_active(self):\n        """Show voice control active interface"""',
     '    def show_voice_control_active(self) -> None:\n        """Show voice control active interface"""'),
    
    ('    def show_listening(self):\n        """Show listening indicator"""',
     '    def show_listening(self) -> None:\n        """Show listening indicator"""'),
    
    ('    def show_command_detected(self, command, text, confidence):\n        """Show command detected with confidence"""',
     '    def show_command_detected(self, command: str, text: str, confidence: float) -> None:\n        """Show command detected with confidence"""'),
    
    ('    def show_command_feedback(self, feedback_text):\n        """Show command execution feedback"""',
     '    def show_command_feedback(self, feedback_text: str) -> None:\n        """Show command execution feedback"""'),
    
    ('    def show_no_speech(self):\n        """Show no speech detected"""',
     '    def show_no_speech(self) -> None:\n        """Show no speech detected"""'),
    
    ('    def show_unknown_command(self, text):\n        """Show unknown command"""',
     '    def show_unknown_command(self, text: str) -> None:\n        """Show unknown command"""'),
    
    ('    def show_tutorial(self):\n        """Show tutorial"""',
     '    def show_tutorial(self) -> None:\n        """Show tutorial"""'),
    
    ('    def show_about(self):\n        """Show about screen"""',
     '    def show_about(self) -> None:\n        """Show about screen"""'),
    
    ('    def show_error(self, title, message, suggestions=None):\n        """Show error with helpful suggestions"""',
     '    def show_error(self, title: str, message: str, suggestions: Optional[List[str]] = None) -> None:\n        """Show error with helpful suggestions"""'),
    
    ('    def show_goodbye(self):\n        """Show goodbye message"""',
     '    def show_goodbye(self) -> None:\n        """Show goodbye message"""'),
    
    ('    def show_initializing(self):\n        """Show initializing message"""',
     '    def show_initializing(self) -> None:\n        """Show initializing message"""'),
    
    ('    def show_initialization_step(self, step_name, success=True):\n        """Show initialization step result"""',
     '    def show_initialization_step(self, step_name: str, success: bool = True) -> None:\n        """Show initialization step result"""'),
    
    ('    def pause(self, message="Press Enter to continue..."):\n        """Pause with message"""',
     '    def pause(self, message: str = "Press Enter to continue...") -> None:\n        """Pause with message"""'),
]

# Read file
with open('ui_manager.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Apply replacements
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✓ Updated: {old.split(chr(10))[0][:50]}...")
    else:
        print(f"✗ NOT FOUND: {old.split(chr(10))[0][:50]}...")

# Write back
with open('ui_manager.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone! ui_manager.py type hints updated.")
