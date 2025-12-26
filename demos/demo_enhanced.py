# ============================================
# DEMO ENHANCED ACCESSIBILITY FEATURES
# ============================================
import time
import threading
from accessibility_popup import AccessibilityPopup
from hybrid_voice_recognizer import HybridVoiceRecognizer

def demo_enhanced_features():
    """Demonstrate enhanced accessibility features"""

    # Create popup instance
    popup = AccessibilityPopup()
    popup.update_settings({
        'position': 'bottom-right',
        'size': (400, 200),
        'transparency': 0.9,
        'font_size': 16,
        'theme': 'dark'
    })

    # Create voice recognizer for captioning demo
    voice_recognizer = HybridVoiceRecognizer()
    voice_recognizer.initialize()

    # Connect voice recognizer to popup
    popup.voice_recognizer = voice_recognizer

    # Start popup system
    popup.start()

    print("🚀 Enhanced Accessibility Features Demo")
    print("=" * 50)
    print("Fitur yang akan didemonstrasikan:")
    print("1. Real-time Captioning")
    print("2. Multi-language Support")
    print("3. Analytics & Statistics")
    print("Tekan Ctrl+C untuk berhenti demo")
    print()

    try:
        # Demo 1: Basic popup functionality
        print("1️⃣ Menampilkan popup dasar...")
        popup.show_slide_info(1, 10, "Pendahuluan")
        time.sleep(3)

        # Demo 2: Multi-language support
        print("2️⃣ Mendemonstrasikan multi-language support...")
        available_langs = popup.get_available_languages()
        print(f"   Bahasa tersedia: {list(available_langs.values())}")

        # Change to English
        popup.set_caption_language("en")
        popup.show_caption("Hello! This is a test caption in English")
        time.sleep(3)

        # Change to Spanish
        popup.set_caption_language("es")
        popup.show_caption("¡Hola! Esta es una prueba de subtítulo en español")
        time.sleep(3)

        # Back to Indonesian
        popup.set_caption_language("id")
        popup.show_caption("Halo! Ini adalah contoh teks caption dalam bahasa Indonesia")
        time.sleep(3)

        # Demo 3: Analytics
        print("3️⃣ Menampilkan analytics...")
        popup.show_analytics_popup()
        time.sleep(4)

        # Demo 4: Real-time captioning (simulated)
        print("4️⃣ Memulai real-time captioning...")
        print("   Coba katakan sesuatu ke microphone...")

        # Start captioning
        popup.start_real_time_captioning(voice_recognizer)
        time.sleep(8)  # Listen for 8 seconds

        # Stop captioning
        popup.stop_real_time_captioning()
        print("   Real-time captioning dihentikan")

        # Show final analytics
        print("5️⃣ Menampilkan analytics akhir...")
        popup.show_analytics_popup()
        time.sleep(4)

        print("✅ Demo selesai!")

    except KeyboardInterrupt:
        print("\n⏹️  Demo dihentikan oleh user")

    finally:
        # Save analytics
        popup.save_analytics()

        # Cleanup
        popup.stop_real_time_captioning()
        popup.stop()
        print("🧹 Cleanup selesai")

if __name__ == "__main__":
    demo_enhanced_features()