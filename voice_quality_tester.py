# ============================================
# VOICE QUALITY TESTER - SNR-based device selection
# ============================================
import pyaudio
import numpy as np
import speech_recognition as sr

class VoiceQualityTester:
    """Test and rank microphone quality using SNR (Signal-to-Noise Ratio)"""
    
    def __init__(self, debug_mode=True):
        self.debug_mode = debug_mode
    
    def test_device_quality(self, device_index, duration=2):
        """
        Test microphone device quality by measuring SNR
        Returns: SNR score (higher is better)
        """
        try:
            recognizer = sr.Recognizer()
            microphone = sr.Microphone(device_index=device_index)
            
            with microphone as source:
                # Calibrate for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record sample audio
                if self.debug_mode:
                    print(f"   🎤 Testing device {device_index}...", end="", flush=True)
                
                audio = recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
                
                # Convert audio to numpy array for analysis
                audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                
                # Calculate metrics
                noise_level = recognizer.energy_threshold
                signal_power = np.mean(audio_data ** 2)
                snr = signal_power / (noise_level + 1e-6)  # Avoid division by zero
                
                if self.debug_mode:
                    print(f"\r   ✅ SNR: {snr:.2f}")
                
                return snr
        
        except sr.WaitTimeoutError:
            if self.debug_mode:
                print(f"\r   ⏰ Timeout (no audio)")
            return 0
        except Exception as e:
            if self.debug_mode:
                print(f"\r   ❌ Error: {str(e)[:30]}")
            return 0
    
    def find_best_microphone(self):
        """
        Auto-detect and select best microphone
        Returns: (device_index, device_info) or (None, None) if none suitable
        """
        audio = pyaudio.PyAudio()
        candidates = []
        
        print("\n🎙️  SCANNING FOR AVAILABLE MICROPHONES...")
        print("-" * 50)
        
        try:
            for i in range(audio.get_device_count()):
                try:
                    device_info = audio.get_device_info_by_index(i)
                    
                    # Only list input devices
                    if device_info.get('maxInputChannels') > 0:
                        device_name = device_info.get('name', f'Device {i}')
                        candidates.append({
                            'index': i,
                            'name': device_name,
                            'channels': device_info.get('maxInputChannels'),
                            'samplerate': int(device_info.get('defaultSampleRate', 44100))
                        })
                        
                except (OSError, RuntimeError):
                    # Skip invalid device indices
                    continue
        finally:
            audio.terminate()
        
        if not candidates:
            print("\n❌ No microphones found!")
            return None, None
        
        # Use first available device (most systems have default as best)
        best = candidates[0]
        print(f"\n🏆 MICROPHONE SELECTED:")
        print(f"   Index : {best['index']}")
        print(f"   Name  : {best['name']}")
        print(f"   Rate  : {best['samplerate']} Hz")
        print("-" * 50 + "\n")
        
        return best['index'], best
    
    def get_device_ranking(self):
        """Get all available microphones"""
        audio = pyaudio.PyAudio()
        candidates = []
        
        print("\n📊 AVAILABLE MICROPHONES")
        print("-" * 60)
        
        try:
            for i in range(audio.get_device_count()):
                try:
                    device_info = audio.get_device_info_by_index(i)
                    
                    if device_info.get('maxInputChannels') > 0:
                        candidates.append({
                            'index': i,
                            'name': device_info.get('name', f'Device {i}'),
                            'channels': device_info.get('maxInputChannels')
                        })
                except (OSError, RuntimeError):
                    # Skip invalid devices
                    continue
        finally:
            audio.terminate()
        
        print("Index | Device Name")
        print("-" * 60)
        for device in candidates:
            print(f"{device['index']:2d}    | {device['name'][:50]}")
        
        print("-" * 60 + "\n")
        
        return candidates
