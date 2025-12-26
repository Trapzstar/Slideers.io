# ============================================
# INTERACTIVE SETUP WIZARD
# ============================================

class InteractiveSetupWizard:
    """First-time user setup wizard"""
    
    def __init__(self, voice_recognizer, detector, config):
        self.voice = voice_recognizer
        self.detector = detector
        self.config = config
    
    def run_full_setup(self):
        """Run complete setup wizard"""
        self._show_welcome()
        self._setup_language()
        self._setup_microphone()
        self._setup_accessibility()
        self._save_and_complete()
    
    def _show_welcome(self):
        """Show welcome message"""
        print("\n" + "="*60)
        print("🎉 SELAMAT DATANG DI VOICE CONTROL FOR POWERPOINT!")
        print("="*60)
        print("\nMari kita setup aplikasi ini dalam 3 langkah mudah.\n")
    
    def _setup_language(self):
        """Language preference"""
        print("STEP 1/3: Pilih bahasa utama")
        print("─" * 40)
        print("  1. Bahasa Indonesia")
        print("  2. English")
        print("  3. Mixed (Indonesia + English)")
        
        choice = input("\nPilihan [1-3]: ").strip()
        
        language_map = {
            '1': ('id-ID', 'Bahasa Indonesia'),
            '2': ('en-US', 'English'),
            '3': ('mixed', 'Mixed')
        }
        
        lang_code, lang_name = language_map.get(choice, ('id-ID', 'Bahasa Indonesia'))
        
        self.config.set('GOOGLE_LANGUAGE', lang_code)
        print(f"✅ Bahasa dipilih: {lang_name}\n")
    
    def _setup_microphone(self):
        """Microphone calibration"""
        print("\nSTEP 2/3: Setup Microphone")
        print("─" * 40)
        print("Kami akan menemukan microphone terbaik untuk Anda...\n")
        
        best_device = self.voice.auto_select_best_device()
        
        if best_device is not None:
            print(f"✅ Microphone terbaik dipilih!\n")
        else:
            print("⚠️  Tidak bisa auto-select. Pilih manual:\n")
            self.voice.list_audio_devices()
            device = input("Device index: ").strip()
            self.voice.select_device(int(device))
        
        # Quick test
        print("\nMengetes microphone Anda...")
        print("Katakan: 'next slide'\n")
        
        result = self.voice.test_microphone(duration=3)
        
        if result:
            print("✅ Microphone siap!\n")
        else:
            print("⚠️  Microphone memerlukan adjustment")
            self._adjust_microphone_settings()
    
    def _adjust_microphone_settings(self):
        """Help user adjust microphone"""
        print("\n💡 Tips penyesuaian:")
        print("   • Bicara lebih keras")
        print("   • Dekatkan mulut ke microphone")
        print("   • Kurangi background noise")
        print("   • Pastikan microphone tidak mute\n")
        
        retry = input("Coba lagi? (y/n): ").strip().lower()
        if retry == 'y':
            self.voice.test_microphone(duration=3)
    
    def _setup_accessibility(self):
        """Accessibility features"""
        print("\nSTEP 3/3: Fitur Aksesibilitas")
        print("─" * 40)
        print("Aktifkan fitur untuk kebutuhan khusus:\n")
        print("  1. Captions (untuk tunarungu)")
        print("  2. Voice feedback (untuk tunanetra)")
        print("  3. Tidak perlu")
        
        choice = input("\nPilihan [1-3]: ").strip()
        
        features = {
            '1': ('captions', 'Live captioning'),
            '2': ('voice_feedback', 'Voice feedback'),
            '3': ('none', 'No special features')
        }
        
        feature, name = features.get(choice, ('none', 'No special features'))
        print(f"✅ Fitur: {name}\n")
    
    def _save_and_complete(self):
        """Save configuration and show completion message"""
        self.config.save_env()
        
        print("\n" + "="*60)
        print("✅ SETUP SELESAI!")
        print("="*60)
        print("\n📋 Konfigurasi Anda telah disimpan.")
        print("🎤 Aplikasi siap digunakan!")
        print("\n💡 Tips:")
        print("   • Katakan 'help menu' untuk melihat semua perintah")
        print("   • Bicara dengan jelas dan natural")
        print("   • Gunakan frasa lengkap dari menu bantuan\n")
        
        input("Tekan Enter untuk mulai...")

# Quick setup runner
def run_interactive_setup(voice, detector, config):
    """Run setup wizard"""
    wizard = InteractiveSetupWizard(voice, detector, config)
    wizard.run_full_setup()
