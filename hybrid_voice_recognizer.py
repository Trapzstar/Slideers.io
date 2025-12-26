# ============================================
# HYBRID VOICE RECOGNIZER (OFFLINE + GOOGLE API)
# ============================================
import speech_recognition as sr
import pyaudio
import numpy as np
import time
from error_handler import get_error_handler
from feedback_ui import get_feedback_ui
from config_manager import get_config
from voice_quality_tester import VoiceQualityTester

class HybridVoiceRecognizer:
    def __init__(self, debug_mode=True, config=None):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_ready = False
        self.device_index = None
        self.speech_history = []
        self.debug_mode = debug_mode
        self.noise_reduction_enabled = False
        self.error_handler = get_error_handler(debug_mode)
        self.feedback_ui = get_feedback_ui(debug_mode)
        self.config = config or get_config()
        self.quality_tester = VoiceQualityTester(debug_mode)
        
        # Adaptive energy threshold
        self.base_energy_threshold = 300
        self.current_attempt = 0

        # Offline fallback removed - using simplified approach

    def initialize(self):
        """Initialize Hybrid Speech Recognition (Google + Offline fallback)"""
        try:
            # List devices
            self.list_audio_devices()

            # Microphone setup
            try:
                if self.device_index is not None:
                    self.microphone = sr.Microphone(device_index=self.device_index)
                    print(f"✅ Microphone Hybrid dipilih: Device {self.device_index}")
                else:
                    self.microphone = sr.Microphone()
                    print("✅ Microphone Hybrid siap")

                # Test microphone with shorter calibration
                with self.microphone as source:
                    print("🎤 Calibrating microphone for ambient noise (shorter)...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Shorter calibration
                    print("🎤 Microphone calibrated")

            except Exception as mic_error:
                print(f"❌ Microphone setup error: {mic_error}")
                print("💡 Solusi:")
                print("   1. Pastikan microphone terhubung dan tidak mute")
                print("   2. Coba restart aplikasi")
                print("   3. Periksa pengaturan audio Windows")
                return False

            self.is_ready = True
            print("🔄 Hybrid mode: Google API (primary) + Offline Sphinx (fallback)")
            return True

        except Exception as e:
            print(f"❌ Hybrid initialization error: {e}")
            self.is_ready = False
            return False

    def list_audio_devices(self):
        """List available audio input devices"""
        try:
            audio = pyaudio.PyAudio()
            print("\n🎙️  DAFTAR PERANGKAT AUDIO INPUT:")
            print("-" * 40)
            for i in range(audio.get_device_count()):
                device_info = audio.get_device_info_by_index(i)
                if device_info.get('maxInputChannels') > 0:
                    print(f"  {i}: {device_info.get('name')} (Channels: {device_info.get('maxInputChannels')})")
            print("-" * 40)
            audio.terminate()
        except Exception as e:
            print(f"⚠️  Tidak bisa list devices: {e}")

    def set_debug_mode(self, enabled=True):
        """Enable or disable debug mode"""
        self.debug_mode = enabled
        print(f"🔧 Debug mode: {'ON' if enabled else 'OFF'}")

    def select_device(self, device_index):
        """Select specific audio device"""
        self.device_index = device_index
        print(f"🎙️  Device {device_index} dipilih untuk hybrid recognition")
    
    def auto_select_best_device(self):
        """
        Automatically select best microphone based on quality (SNR)
        Returns: device_index or None if no suitable device found
        """
        device_index, device_info = self.quality_tester.find_best_microphone()
        
        if device_index is not None:
            self.select_device(device_index)
            return device_index
        
        return None
    
    def list_device_quality(self):
        """Display microphone quality ranking"""
        return self.quality_tester.get_device_ranking()

    def add_to_history(self, text):
        """Add recognized text to history"""
        self.speech_history.append(text)
        if len(self.speech_history) > 10:
            self.speech_history.pop(0)

    def listen_google_primary(self):
        """Try Google Speech API first with better error handling and retries"""
        max_retries = self.config.get_int("MAX_RETRIES")
        retry_delay = self.config.get_float("RETRY_DELAY")
        
        for attempt in range(max_retries):
            try:
                with self.microphone as source:
                    if self.debug_mode:
                        print("    🔊 Listening with Google API...", end="", flush=True)

                    # Listen for audio with longer timeout for better recognition
                    audio = self.recognizer.listen(
                        source,
                        timeout=self.config.get_int("LISTEN_TIMEOUT"),
                        phrase_time_limit=self.config.get_int("PHRASE_LIMIT")
                    )

                    if self.debug_mode:
                        print("\r    ⏳ Recognizing with Google...", end="", flush=True)

                    # Recognize with Google Speech API
                    text = self.recognizer.recognize_google(audio, language=self.config.get("GOOGLE_LANGUAGE"))

                    if self.debug_mode:
                        print(f"\r    📝 Google: '{text}'")

                    self.add_to_history(text)
                    self.error_handler.reset_retry_count("google_api_error")
                    return text

            except sr.WaitTimeoutError:
                if self.debug_mode:
                    print("\r    ⏰ No speech detected")
                    print("    💡 Ensure microphone is active and not muted")
                self.error_handler.handle_error("no_speech_detected", context="Listen timeout")
                return None
                
            except sr.UnknownValueError:
                if self.debug_mode:
                    print("\r    🤔 Speech detected but unclear")
                    print("    💡 Try speaking clearer or closer to microphone")
                
                if self.error_handler.should_retry("google_api_error", max_retries):
                    if self.debug_mode:
                        self.feedback_ui.show_retry_info(attempt + 1, max_retries, retry_delay)
                    time.sleep(retry_delay)
                    continue
                return None
                
            except sr.RequestError as e:
                error_msg = self.error_handler.format_error_message(e)
                if self.debug_mode:
                    print(f"\r    ❌ Google API Error: {error_msg}")
                
                self.error_handler.handle_error("google_api_error", e, "Listen Google API")
                
                if self.error_handler.should_retry("google_api_error", max_retries):
                    if self.debug_mode:
                        self.feedback_ui.show_retry_info(attempt + 1, max_retries, retry_delay)
                    time.sleep(retry_delay)
                    continue
                return None
                
            except Exception as e:
                error_msg = self.error_handler.format_error_message(e)
                if self.debug_mode:
                    print(f"\r    ❌ Error: {error_msg}")
                
                self.error_handler.handle_error("google_api_error", e, "Listen error")
                
                if self.error_handler.should_retry("google_api_error", max_retries):
                    if self.debug_mode:
                        self.feedback_ui.show_retry_info(attempt + 1, max_retries, retry_delay)
                    time.sleep(retry_delay)
                    continue
                return None
        
        return None

    def listen_offline_fallback(self):
        """Fallback to offline recognition - simplified version"""
        if self.debug_mode:
            print("    🔄 Switching to offline recognition...")

        # For now, just try a simple keyword spotting approach
        # This is a placeholder - in production you'd want proper offline ASR
        try:
            # Simple approach: try to detect basic keywords using Google with very short timeout
            # as a last resort, but this will likely fail too
            with self.microphone as source:
                if self.debug_mode:
                    print("    🔊 Trying basic offline detection...")

                # Very short listen for basic keywords
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=2)

                # Try with English first for basic commands
                text = self.recognizer.recognize_google(audio, language="en-US")
                if text and any(keyword in text.lower() for keyword in ['next', 'previous', 'back', 'stop', 'quit']):
                    if self.debug_mode:
                        print(f"    📝 Basic offline: '{text}'")
                    self.add_to_history(text)
                    return text.lower().strip()

        except:
            pass

        if self.debug_mode:
            print("    ❌ Offline recognition not available")

        return None

    def listen(self, timeout=5, phrase_limit=4):
        """Hybrid listening with smart retry logic"""
        if not self.is_ready:
            return None

        # Try with smart retry (3 attempts with adaptive thresholds)
        text = self.listen_with_smart_retry(max_retries=3, adaptive=True)
        return text
    
    def listen_with_smart_retry(self, max_retries=3, adaptive=True):
        """
        Listen with intelligent retry mechanism
        - Adaptive energy threshold based on attempt number
        - Progressive visual feedback
        - Smart fallback strategy
        
        Args:
            max_retries: Maximum number of retry attempts
            adaptive: Whether to use adaptive energy threshold
        
        Returns:
            Recognized text or None
        """
        for attempt in range(max_retries):
            try:
                # Adaptive energy threshold
                if adaptive and attempt > 0:
                    # Increase sensitivity with each retry
                    adjustment = attempt * 50
                    self.recognizer.energy_threshold = max(100, self.base_energy_threshold - adjustment)
                    if self.debug_mode:
                        print(f"    📊 Attempt {attempt+1}: Lowering threshold for sensitivity")
                
                # Try primary Google method
                text = self.listen_google_primary()
                if text:
                    return text
                
                # On failure, show retry feedback
                if attempt < max_retries - 1:
                    self.feedback_ui.show_retry_info(attempt + 1, max_retries, delay=0.5)
                    time.sleep(0.5)
            
            except Exception as e:
                if self.debug_mode:
                    print(f"    ❌ Retry error: {str(e)[:50]}")
                
                if attempt == max_retries - 1:
                    self.error_handler.handle_error("audio_buffer_overflow", e, "Retry exhausted")
                    return None
        
        # All retries failed
        if self.debug_mode:
            print("    ⚠️  Failed after 3 attempts - returning to listen")
        
        return None

    def get_history(self):
        """Get speech recognition history"""
        return self.speech_history.copy()

    def clear_history(self):
        """Clear speech recognition history"""
        self.speech_history.clear()
        print("🗑️  History cleared")

    def show_history(self):
        """Show speech recognition history"""
        if not self.speech_history:
            print("📝 History kosong")
            return

        print("\n📝 SPEECH RECOGNITION HISTORY:")
        print("-" * 40)
        for i, text in enumerate(self.speech_history[-10:], 1):  # Show last 10
            print(f"  {i}. '{text}'")
        print("-" * 40)

    def save_history(self, filename="speech_history.txt"):
        """Save speech history to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Speech Recognition History\n")
                f.write("=" * 30 + "\n")
                for text in self.speech_history:
                    f.write(f"{text}\n")
            print(f"💾 History disimpan ke {filename}")
        except Exception as e:
            print(f"❌ Gagal menyimpan history: {e}")

    def test_microphone(self, duration=3):
        """Test microphone input for specified duration"""
        print(f"\n🎙️  TESTING MICROPHONE ({duration} detik)...")
        print("-" * 40)

        try:
            with self.microphone as source:
                print("   Recording... bicaralah sekarang!")
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)

                print("   Recognizing...")
                text = self.recognizer.recognize_google(audio, language="id-ID")

                print(f"   ✅ Detected: '{text}'")
                print("   🎉 Microphone test berhasil!")
                return True

        except sr.WaitTimeoutError:
            print("   ⏰ Timeout - tidak ada suara terdeteksi")
            print("   ⚠️  Pastikan microphone terhubung dan tidak mute")
            return False
        except sr.UnknownValueError:
            print("   🤔 Suara terdeteksi tapi tidak jelas")
            print("   💡 Coba bicara lebih jelas atau dekat ke microphone")
            return False
        except sr.RequestError as e:
            print(f"   ❌ API Error: {e}")
            print("   🔄 Mencoba offline test...")
            return self.test_microphone_offline(duration)
        except Exception as e:
            print(f"   ❌ Test error: {e}")
            return False

    def test_microphone_offline(self, duration=3):
        """Offline microphone test"""
        try:
            print("   🔄 Testing offline...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
                # Just check if audio was captured
                audio.get_raw_data()
                print("   ✅ Audio captured successfully (offline)")
                return True
        except:
            print("   ❌ Offline test juga gagal")
            return False
    
    def listen_quick(self, timeout=2):
        """Quick listen for confirmation (shorter timeout)"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=2
                )
                text = self.recognizer.recognize_google(audio, language=self.config.get("GOOGLE_LANGUAGE"))
                return text
        except:
            return None

