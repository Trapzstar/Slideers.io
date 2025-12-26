# ============================================
# USAGE EXAMPLES - Practical Demonstrations
# ============================================

## 🎯 QUICK START EXAMPLES

### Example 1: Basic Presentation Flow

```bash
# 1. Start application
python main.py

# Auto-selection happens:
🎙️  AUTO-SELECTING BEST MICROPHONE...
🏆 BEST MICROPHONE SELECTED:
   Name: Headset USB
   SNR: 85.2 dB

# 2. Application ready
🎤 Listening... (bicara sekarang)

# 3. User speaks
[User: "open slide show"]

# 4. System detects and confirms
📊 Confidence: 🟢 HIGH
   [████████████████░░] 80%
   Command: open_slideshow
   Score: 8/10

✅ BUKA SLIDESHOW! (F5)

# 5. PowerPoint opens, return to app
# 6. Continue with navigation

[User: "next slide"]
✅ SLIDE MAJU! (Total: 1)

[User: "next slide"]
✅ SLIDE MAJU! (Total: 2)

[User: "back slide"]
✅ SLIDE MUNDUR! (Total: 1)

# 7. End presentation
[User: "close slide show"]
✅ TUTUP SLIDESHOW! (ESC)

# 8. Exit
[User: "stop program"]
PROGRAM DIHENTIKAN
```

---

## 📊 ADAPTIVE LEARNING EXAMPLES

### Example 2: Accent Learning in Action

```bash
# First attempt with accent
[User speaks with Javanese accent: "neks slid"]
⏰ No speech detected
💡 Tips:
   • Bicara lebih keras
   • Dekatkan mulut ke microphone

# System retries
🔄 Retry 1/3...
[User: "neks slid"]
📝 Score 4.2 < threshold 6.0 (tolerance mode)

# Smart retry with lower threshold
📊 Attempt 2: Lowering threshold for sensitivity
[User: "neks slid"]
📊 Confidence: 🟡 MEDIUM
   [██████████░░░░░░░░] 60%
   Command: next
   Score: 6.5/10

✅ Detected: 'next slide' (confidence: 6.5/10)
💬 Say 'yes' to confirm or anything to cancel

[User: "yes"]
✅ SLIDE MAJU!

# System learns this pronunciation
📚 Learned: 'neks slid' → next
System will recognize this faster next time
```

---

### Example 3: Adaptive Threshold in Action

**Scenario:** User has heavy accent, getting 60% success rate

```
SESSION START
└─ Threshold: 6.0 (normal)

Attempt 1: [Success] Score 8.5
Attempt 2: [Success] Score 7.2
Attempt 3: [Fail] Score 5.9 < 6.0 ❌

# System detects failures
📉 Threshold lowered to 5.5 (tolerance mode)
(Recent failures detected - being more lenient)

Attempt 4: [Fail] Score 5.9 → Now >= 5.5 ✅
Attempt 5: [Success] Score 6.1

# After more failures
Recent failures: 4/10 (40%)
📉 Threshold lowered to 5.0

# User becomes consistent
Recent successes: 8/10
📈 Threshold raised to 6.0 (normal mode)

SESSION END
```

---

## 🎓 TRAINING MODE EXAMPLES

### Example 4: Accent Training Session

```bash
# Start training
python main.py --train-accent

🎓 ACCENT TRAINING MODE
════════════════════════════════════════

Sistem akan belajar cara Anda mengucapkan perintah.

📝 COMMAND 1/6: 'next slide'
────────────────────────────────────
🎤 Percobaan 1/3
   Katakan: 'next slide'
   Tekan Enter untuk merekam...

[User says: "neks slaid"]
✅ Recorded: 'neks slaid' (confidence: 7.5/10)

🎤 Percobaan 2/3
[User says: "neks slid"]
✅ Recorded: 'neks slid' (confidence: 7.8/10)

🎤 Percobaan 3/3
[User says: "next slide"]
✅ Recorded: 'next slide' (confidence: 9.2/10)

✅ Summary: 3 variations recorded (avg confidence: 8.2/10)

[Repeat for remaining 5 commands...]

✅ TRAINING SELESAI!
════════════════════════════════════════

📊 HASIL:
   • Perintah ditraining: 6
   • Total samples: 18
   • Akurasi proyeksi: ~95% untuk aksen Anda

✅ Sistem sekarang lebih familiar dengan aksen Anda!
   Akurasi deteksi akan terus meningkat seiring penggunaan.
```

---

## 🆘 ERROR HANDLING EXAMPLES

### Example 5: Microphone Not Found

```bash
python main.py

🎙️  AUTO-SELECTING BEST MICROPHONE...
🎤 Testing device 0... [Timeout]
🎤 Testing device 1... [Timeout]
🎤 Testing device 2... [No device]

❌ No suitable microphones found!

🎙️  Available devices:
   0. Speakers (Output only)
   1. Realtek Audio
   2. (Unknown device)

Select device number (or press Enter for device 0): 1

🎙️  Device 1 dipilih untuk hybrid recognition
```

---

### Example 6: Google API Connection Error

```bash
🎤 Listening... (bicara sekarang)

[User speaks clearly]

🔊 Listening with Google API...
⏳ Recognizing with Google...
❌ Google API Error: Network timeout

🔄 Retry 1/3...

[Smart retry with lower threshold]

📊 Attempt 2: Lowering threshold for sensitivity
✅ Detected with offline fallback (basic keywords)

📝 Partial match: 'next'
✅ SLIDE MAJU!

(Or if all retries fail:)
❌ Google API Error
─────────────────
💡 SOLUTIONS:
   1. Check internet connection
   2. Try again in a moment (rate limiting)
   3. Check firewall/proxy settings
```

---

## 💬 CONFIDENCE SCORING EXAMPLES

### Example 7: Different Confidence Levels

```
SCENARIO A: High Confidence (Auto-execute)
────────────────────────────
🎤 Listening...
[User: "next slide" - clear, native accent]

📊 Confidence: 🟢 HIGH
   [████████████████░░] 92%
   Command: next
   Score: 9.2/10

✅ Score >= 8.5 → Auto-execute
✅ SLIDE MAJU!


SCENARIO B: Medium Confidence (Ask confirmation)
────────────────────────────
🎤 Listening...
[User: "neks slaid" - accent, slightly unclear]

📊 Confidence: 🟡 MEDIUM
   [██████████░░░░░░░░] 65%
   Command: next
   Score: 6.5/10

❓ MEDIUM CONFIDENCE: Slide maju (6.5/10)
💬 Katakan 'yes' to confirm or anything else to cancel

[User: "yes"]
✅ SLIDE MAJU!

(Or)
[User: "no" / silent]
❌ Cancelled


SCENARIO C: Low Confidence (Retry)
────────────────────────────
🎤 Listening...
[User: "nax sled" - very unclear, background noise]

📝 Score 3.2 < threshold 5.0
⚠️  Please retry:
   • Reduce background noise
   • Speak clearer
   • Move closer to microphone

🔄 Attempting to retry...
🎤 Listening again...
```

---

## 🎮 INTERACTIVE SETUP WIZARD

### Example 8: First-Time User Setup

```bash
python main.py --setup

🎉 SELAMAT DATANG DI VOICE CONTROL FOR POWERPOINT!
════════════════════════════════════════════════════

Mari kita setup aplikasi ini dalam 3 langkah mudah.

STEP 1/3: Pilih bahasa utama
────────────────────────────────
  1. Bahasa Indonesia
  2. English
  3. Mixed (Indonesia + English)

Pilihan [1-3]: 1
✅ Bahasa dipilih: Bahasa Indonesia

STEP 2/3: Setup Microphone
────────────────────────────────
Kami akan menemukan microphone terbaik untuk Anda...

🎙️  SCANNING MICROPHONES FOR BEST QUALITY...
   🎤 Testing device 0...  ✅ SNR: 45.3
   🎤 Testing device 1...  ✅ SNR: 82.1
   🎤 Testing device 2...  ✅ SNR: 28.9

🏆 BEST MICROPHONE SELECTED:
   Index: 1
   Name: Headset USB
   SNR: 82.1 dB

✅ Microphone terbaik dipilih!

Mengetes microphone Anda...
Katakan: 'next slide'

[User: "next slide"]

   ✅ Detected: 'next slide'
   🎉 Microphone test berhasil!

✅ Microphone siap!

STEP 3/3: Fitur Aksesibilitas
────────────────────────────────
Aktifkan fitur untuk kebutuhan khusus:

  1. Captions (untuk tunarungu)
  2. Voice feedback (untuk tunanetra)
  3. Tidak perlu

Pilihan [1-3]: 1
✅ Fitur: Live captioning

════════════════════════════════════════════════════
✅ SETUP SELESAI!
════════════════════════════════════════════════════

📋 Konfigurasi Anda telah disimpan.
🎤 Aplikasi siap digunakan!

💡 Tips:
   • Katakan 'help menu' untuk melihat semua perintah
   • Bicara dengan jelas dan natural
   • Gunakan frasa lengkap dari menu bantuan
```

---

## 📱 CLI FEEDBACK EXAMPLES

### Example 9: Rich Error Messages

```bash
🎤 Listening... (bicara sekarang)

[User speaks in very noisy environment]

⏰ Tidak mendengar suara
💡 Tips:
   • Pastikan microphone tidak mute
   • Bicara lebih keras dan jelas
   • Kurangi background noise
   • Dekatkan mulut ke microphone (3-6 inchi)


─────────────────────────────────────────

[Another attempt - wrong command]

📝 Score 2.5 < threshold 6.0
💡 Sistem membutuhkan speech yang lebih jelas:
   • Ejakan lebih jelas setiap kata
   • Berbicara dengan kecepatan normal
   • Gunakan frasa persis dari menu bantuan

💬 Katakan 'help menu' untuk melihat semua perintah
```

---

## 🔄 AUTO-CORRECTION EXAMPLES

### Example 10: Learning from User Behavior

```
SESSION 1:
[User: "nex slaid" repeatedly]
❌ Failed 3 times

SESSION 2:
System remembers: "nex slaid" attempted 3x
Recently: Same user saying "nex slaid" again
📚 Learned: 'nex slaid' → next

🎤 Listening...
[User: "nex slaid"]
✅ SLIDE MAJU! (Now recognized immediately!)
```

---

## 📊 STATISTICS & LEARNING

### Example 11: Session Statistics with Adaptive Learning

```bash
[After 20-minute presentation]

📊 FINAL REPORT
════════════════════════════════════════

STATISTIK SESSION:
   Durasi          : 20.5 menit
   Total perintah  : 35
   - Slide maju    : 15
   - Slide mundur  : 12
   - Buka slideshow: 1
   - Tutup slideshow: 1
   - Stop          : 1
   - Bantuan       : 3
   - Tidak dikenali: 2
   
Success rate    : 94.3%

🧠 ADAPTIVE LEARNING:
   • Threshold: 5.5 → 6.2 (adapted over session)
   • Commands learned: 5 new accent variants
   • Success improvements: +23% from start to end
   • Accent familiarity: 92% (high)

📚 RECOMMENDATIONS:
   ✅ System now highly accurate for your accent
   ✅ Consider accent training for 100% accuracy
   ✅ No further configuration needed
```

---

## 🚀 COMMAND WORKFLOW EXAMPLES

### Example 12: Complete Presentation Workflow

```bash
# 1. Start application with setup
python main.py

# 2. First-time setup (optional)
# [Auto-setup completes or user skips]

# 3. Ready for presentation
[User: "help menu"]
# Shows all available commands

[User: "open slide show"]
✅ BUKA SLIDESHOW! (F5)
# PowerPoint F5 triggered, opens fullscreen

# 4. Return to CLI, ready for voice commands
[User: "next slide"]  ✅
[User: "next slide"]  ✅
[User: "next slide"]  ✅
[User: "back slide"]  ✅
[User: "next slide"]  ✅

# 5. Show accessibility popup
[User: "popup on"]
# Accessibility overlay appears with slide info

# 6. Enable live captions
[User: "caption on"]
# Live caption panel shows

# 7. Change caption language
[User: "change language"]
# Switches to next language (English, Spanish, etc.)

# 8. Show analytics
[User: "show analytics"]
# Session statistics popup appears

# 9. End presentation
[User: "close slide show"]
✅ TUTUP SLIDESHOW! (ESC)
# PowerPoint exits, returns to CLI

# 10. Exit application
[User: "stop program"]
PROGRAM DIHENTIKAN

📊 Final statistics shown
```

---

**Version:** 2.0
**Last Updated:** 2025-12-23
**Status:** Production Ready
