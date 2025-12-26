"""
SlideSense.id - Main Program (Beautiful UI Version)
Voice-Controlled PowerPoint Presentation with Accessibility Features
"""

import sys
import time
from ui_manager import ui, console
from voice_detector import SmartVoiceDetector
from hybrid_voice_recognizer import HybridVoiceRecognizer
from powerpoint_controller import PowerPointController
from accessibility_popup import AccessibilityPopup

class SlideSenseApp:
    """Main application controller"""
    
    def __init__(self):
        self.voice = None
        self.detector = None
        self.ppt = None
        self.popup = None
        self.running = False
    
    def initialize_components(self):
        """Initialize all components with UI feedback"""
        
        ui.show_initializing()
        
        try:
            # Initialize detector
            self.detector = SmartVoiceDetector()
            ui.show_initialization_step("Voice Detector", True)
            
            # Initialize PowerPoint controller
            self.ppt = PowerPointController()
            ui.show_initialization_step("PowerPoint Controller", True)
            
            # Initialize popup system
            self.popup = AccessibilityPopup()
            self.popup.start()
            self.ppt.set_popup_system(self.popup)
            ui.show_initialization_step("Accessibility Popup", True)
            
            # Initialize voice recognizer
            self.voice = HybridVoiceRecognizer(debug_mode=False)
            ui.show_initialization_step("Voice Recognizer", True)
            
            return True
            
        except Exception as e:
            ui.show_error(
                "Initialization Error",
                f"Gagal menginisialisasi komponen: {str(e)}",
                [
                    "Pastikan semua dependencies terinstall",
                    "Coba restart program",
                    "Periksa file requirements.txt"
                ]
            )
            return False
    
    def setup_microphone(self):
        """Setup microphone with beautiful UI"""
        
        # Get available devices
        devices = self._get_device_list()
        
        if not devices:
            ui.show_error(
                "❌ Microphone Tidak Terdeteksi",
                "Tidak ada audio input device yang terdeteksi.",
                [
                    "Pastikan microphone terhubung",
                    "Periksa Device Manager di Windows",
                    "Coba gunakan microphone eksternal",
                    "Restart komputer dan coba lagi"
                ]
            )
            return False
        
        # Show setup wizard
        setup_method = ui.show_microphone_setup(devices)
        
        if setup_method == "auto":
            # Auto-detect
            ui.show_auto_detect_progress()
            
            # Get best device
            best_device = self.voice.auto_select_best_microphone()
            
            if best_device is None:
                console.print("[yellow]⚠️  Auto-detect gagal, switching to manual...[/yellow]\n")
                return self._manual_device_selection(devices)
            
            device_name = devices[best_device]['name'] if best_device < len(devices) else "Unknown"
            
            # Show found device
            confirmed = ui.show_device_found(device_name, best_device)
            
            if confirmed:
                self.voice.select_device(best_device)
                return True
            else:
                return self._manual_device_selection(devices)
        
        else:
            # Manual selection
            return self._manual_device_selection(devices)
    
    def _manual_device_selection(self, devices):
        """Manual device selection"""
        
        device_index = ui.show_microphone_list(devices)
        
        if device_index is None:
            return False
        
        self.voice.select_device(device_index)
        console.print(f"[green]✅ Device {device_index} dipilih[/green]\n")
        time.sleep(0.5)
        return True
    
    def _get_device_list(self):
        """Get list of available devices"""
        
        try:
            import pyaudio
            audio = pyaudio.PyAudio()
            devices = []
            
            for i in range(audio.get_device_count()):
                device_info = audio.get_device_info_by_index(i)
                if device_info.get('maxInputChannels') > 0:
                    devices.append({
                        'index': i,
                        'name': device_info.get('name', 'Unknown'),
                        'channels': device_info.get('maxInputChannels', 0)
                    })
            
            audio.terminate()
            return devices
            
        except Exception as e:
            console.print(f"[red]Error getting devices: {e}[/red]")
            return []
    
    def test_microphone(self):
        """Test microphone with UI"""
        
        if not self.voice or not self.voice.microphone:
            ui.show_error(
                "Microphone Belum Disetup",
                "Silakan setup microphone terlebih dahulu.",
                ["Pilih 'Mulai Voice Control' dari menu utama"]
            )
            return
        
        ui.show_microphone_test_start(duration=3)
        ui.show_test_progress(duration=3)
        
        # Actual test
        result = self.voice.test_microphone(duration=3)
        
        if result:
            ui.show_test_result(True, "Microphone berfungsi dengan baik!")
        else:
            ui.show_test_result(
                False, 
                "Test gagal. Coba bicara lebih keras atau periksa koneksi."
            )
    
    def start_voice_control(self):
        """Start voice control loop"""
        
        # Initialize if not done
        if not self.voice:
            if not self.initialize_components():
                return
        
        # Setup microphone
        if not self.setup_microphone():
            console.print("[yellow]⚠️  Setup microphone dibatalkan[/yellow]\n")
            ui.pause()
            return
        
        # Initialize voice system
        ui.show_voice_control_starting()
        
        if not self.voice.initialize():
            ui.show_error(
                "Voice System Error",
                "Gagal menginisialisasi sistem voice recognition.",
                [
                    "Periksa koneksi microphone",
                    "Pastikan microphone tidak digunakan aplikasi lain",
                    "Coba restart program"
                ]
            )
            ui.pause()
            return
        
        # Show active interface
        ui.show_voice_control_active()
        
        # Connect popup to voice for caption
        self.popup.voice_recognizer = self.voice
        
        console.print("[bold green]✅ Sistem siap![/bold green]")
        console.print("[yellow]💡 Buka PowerPoint dan tekan F5 untuk slideshow[/yellow]")
        console.print("[dim]   Kemudian kembali ke window ini untuk kontrol\n[/dim]")
        
        time.sleep(2)
        
        # Main control loop
        self.running = True
        
        try:
            while self.running:
                ui.show_listening()
                
                # Listen for voice
                text = self.voice.listen()
                
                if text is None:
                    ui.show_no_speech()
                    time.sleep(0.3)
                    continue
                
                # Show caption if enabled
                if self.popup.caption_running:
                    try:
                        self.popup.show_caption(text)
                    except:
                        pass
                
                # Detect command
                result = self.detector.detect(text)
                
                if result and result.get("command") != "unknown":
                    # Get confidence
                    confidence = (result.get('score', 0) / result.get('max_score', 10)) * 100
                    
                    # Show detection
                    ui.show_command_detected(
                        result.get("command"),
                        text,
                        confidence
                    )
                    
                    # Execute command
                    feedback = self.ppt.execute_command(result)
                    ui.show_command_feedback(feedback)
                    
                    # Check for stop command
                    if result.get("command") == "stop":
                        console.print("\n[bold yellow]🛑 Menghentikan Voice Control...[/bold yellow]")
                        self.running = False
                        break
                    
                    # Check for help command
                    elif result.get("command") == "help":
                        console.print()
                        self.detector.show_help()
                        ui.pause()
                        ui.show_voice_control_active()
                
                else:
                    # Unknown command
                    ui.show_unknown_command(text)
                
                time.sleep(0.3)
        
        except KeyboardInterrupt:
            console.print("\n\n[yellow]⚠️  Voice Control dihentikan (Ctrl+C)[/yellow]")
            self.running = False
        
        # Show statistics
        console.print("\n" + "="*60)
        console.print("[bold cyan]📊 Session Statistics[/bold cyan]")
        console.print("="*60)
        self.ppt.show_statistics()
        
        ui.pause()
    
    def run(self):
        """Main application loop"""
        
        try:
            # Show welcome
            ui.show_welcome()
            
            # Main menu loop
            while True:
                action = ui.show_main_menu()
                
                if action == "start":
                    self.start_voice_control()
                
                elif action == "test_mic":
                    # Initialize if needed
                    if not self.voice:
                        if not self.initialize_components():
                            continue
                        if not self.setup_microphone():
                            continue
                        if not self.voice.initialize():
                            continue
                    
                    self.test_microphone()
                
                elif action == "tutorial":
                    ui.show_tutorial()
                
                elif action == "about":
                    ui.show_about()
                
                elif action == "exit":
                    break
            
            # Cleanup
            if self.popup:
                try:
                    self.popup.stop()
                except:
                    pass
            
            # Show goodbye
            ui.show_goodbye()
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Program terminated by user[/yellow]")
        
        except Exception as e:
            ui.show_error(
                "Unexpected Error",
                f"Terjadi error: {str(e)}",
                [
                    "Coba restart program",
                    "Periksa log error untuk detail",
                    "Report issue jika error terus terjadi"
                ]
            )


def main():
    """Entry point"""
    
    # Check requirements
    try:
        import pyautogui
    except ImportError:
        console.print("[red]❌ PyAutoGUI tidak terinstall![/red]")
        console.print("   Install dengan: [cyan]pip install pyautogui[/cyan]")
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
    
    try:
        import speech_recognition as sr
    except ImportError:
        console.print("[red]❌ SpeechRecognition tidak terinstall![/red]")
        console.print("   Install dengan: [cyan]pip install SpeechRecognition[/cyan]")
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
    
    try:
        from InquirerPy import inquirer
    except ImportError:
        console.print("[red]❌ InquirerPy tidak terinstall![/red]")
        console.print("   Install dengan: [cyan]pip install InquirerPy[/cyan]")
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
    
    try:
        from rich.console import Console
    except ImportError:
        console.print("[red]❌ Rich tidak terinstall![/red]")
        console.print("   Install dengan: [cyan]pip install rich[/cyan]")
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
    
    # Run application
    app = SlideSenseApp()
    app.run()


if __name__ == "__main__":
    main()
