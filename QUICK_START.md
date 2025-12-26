# ============================================
# QUICK START GUIDE
# ============================================

## 🚀 GET STARTED IN 5 MINUTES

### Prerequisites
- Windows 10+ (tested on Windows)
- Python 3.8+
- USB Microphone (recommended)
- PowerPoint installed

---

## 📥 INSTALLATION

### 1. Install Dependencies
```bash
cd project_simple
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed pyautogui speech-recognition pyaudio ...
```

### 2. Setup Configuration
```bash
# Copy configuration template
cp .env.example .env

# Edit .env (optional - defaults work for most users)
notepad .env
```

### 3. Test Microphone
```bash
python main.py --test-mic
```

**Expected Output:**
```
✅ Microphone check
✅ Audio level test
✅ Voice sample recording & playback
✅ Speech recognition test
All tests passed ✅
```

If test fails → See [Troubleshooting](#troubleshooting)

---

## ▶️ RUNNING THE APPLICATION

### Basic Start
```bash
python main.py
```

### First Run Experience
1. System detects audio devices
2. Selects best microphone (or asks you)
3. Calibrates microphone
4. Runs quick microphone test
5. Shows help menu
6. **Ready for voice commands!**

### Available Commands
Speak any of these:

| Command | Purpose | Example |
|---------|---------|---------|
| **next slide** | Move to next slide | "next slide" |
| **back slide** | Go to previous slide | "back slide" |
| **open slide show** | Start presentation (F5) | "open slide show" |
| **close slide show** | End presentation (ESC) | "close slide show" |
| **help menu** | Show help | "help menu" |
| **stop program** | Exit application | "stop program" |
| **test mic** | Test microphone | "test mic" |
| **popup on/off** | Toggle accessibility | "popup on" |
| **caption on/off** | Enable live captions | "caption on" |

---

## 🎤 SPEAKING TIPS

### ✅ DO
- Speak **clearly** and at **normal pace**
- Use the **exact phrases** from the help menu
- Speak **closer** to the microphone (3-6 inches)
- Choose a **quiet environment**
- Use **full phrases** ("next slide" not just "next")

### ❌ DON'T
- Whisper or mumble
- Speak too fast or too slow
- Use phrases not in the command list
- Cover the microphone
- Use the app in noisy environments

### 🎯 OPTIMAL CONDITIONS
```
Microphone Distance: 3-6 inches away
Background Noise:    < 50 dB (library quiet)
Speaking Rate:       Normal conversation speed
Voice Clarity:       Clear pronunciation
```

---

## 🔧 CONFIGURATION

### .env File Options

**Voice Settings:**
```ini
# Language for speech recognition
GOOGLE_LANGUAGE=id-ID

# Fuzzy matching sensitivity (0-100)
FUZZY_THRESHOLD=80

# Show confidence scores (True/False)
CONFIDENCE_DISPLAY=True
```

**Timing:**
```ini
# Delay between commands (seconds)
COOLDOWN_SECONDS=2

# Time to wait for speech (seconds)
LISTEN_TIMEOUT=5

# Max phrase length (seconds)
PHRASE_LIMIT=4

# Retry attempts on failure
MAX_RETRIES=3
```

**Features:**
```ini
# Show debug information
DEBUG_MODE=True

# Ask for confirmation before executing
REQUIRE_COMMAND_CONFIRMATION=False

# Retry on network/API errors
ENABLE_ANALYTICS=True
```

### Update Configuration
```bash
# 1. Edit .env file
notepad .env

# 2. Save changes

# 3. Restart application
python main.py
```

---

## 🎯 COMMON SCENARIOS

### Scenario 1: Starting a Presentation
```
1. Open PowerPoint presentation
2. Say: "open slide show"
3. Application says: ✅ BUKA SLIDESHOW
4. PowerPoint enters fullscreen
5. Return to application window
6. Say: "next slide" to navigate
```

### Scenario 2: Navigating Slides
```
During presentation:

Say: "next slide"     → Move forward
Say: "back slide"     → Move backward
Say: "popup on"       → Show accessibility help
Say: "caption on"     → Enable live captions
```

### Scenario 3: Ending Presentation
```
Say: "close slide show"  → Exit presentation (ESC)
Application continues   → Ready for more commands
Say: "stop program"      → Exit application
```

---

## 🆘 TROUBLESHOOTING

### Problem: No Sound Detected
**Symptoms:** Always says "Timeout - tidak ada suara terdeteksi"

**Solutions:**
1. ✅ Check microphone USB connection
2. ✅ Unmute microphone (check hardware mute button)
3. ✅ Unmute in Windows Settings → Privacy & Security
4. ✅ Check Windows Volume Mixer (Settings → Advanced volume)
5. ✅ Speak louder and closer to microphone
6. ✅ Try different microphone: `python main.py --device 2`

### Problem: Recognition Not Working
**Symptoms:** Says "Suara terdeteksi tapi tidak jelas"

**Solutions:**
1. ✅ Reduce background noise (close windows, quiet room)
2. ✅ Speak clearer and slower
3. ✅ Increase FUZZY_THRESHOLD in .env (e.g., 75 instead of 80)
4. ✅ Move closer to microphone
5. ✅ Check internet connection (Google Speech API needs it)
6. ✅ Try calibration: Close and restart application

### Problem: Wrong Commands Executed
**Symptoms:** Says "next" but goes backward

**Solutions:**
1. ✅ Speak exact phrases from help menu
2. ✅ Say "help menu" to see all available commands
3. ✅ Increase COOLDOWN_SECONDS in .env
4. ✅ Speak one command at a time
5. ✅ Enable DEBUG_MODE to see confidence scores

### Problem: Microphone Not Detected
**Symptoms:** "Microphone setup error"

**Solutions:**
1. ✅ List devices: `python main.py` (shows devices at startup)
2. ✅ Select specific device: `python main.py --device 2`
3. ✅ Update audio drivers
4. ✅ Try different USB port
5. ✅ Run as administrator

### Problem: Google API Error
**Symptoms:** "Google API Error" or network timeout

**Solutions:**
1. ✅ Check internet connection
2. ✅ Try again in a moment (API rate limiting)
3. ✅ Check firewall/proxy settings
4. ✅ Verify Google is not blocked in your region
5. ✅ Application auto-retries (default 3x)

### Problem: Application Crashes
**Symptoms:** Application suddenly closes

**Solutions:**
1. ✅ Enable DEBUG_MODE in .env
2. ✅ Run: `python main.py 2>&1 | tee error_log.txt`
3. ✅ Check error messages before crash
4. ✅ Update Python and dependencies
5. ✅ Check system resources (RAM, CPU)

---

## 🔍 TESTING & VALIDATION

### Check Configuration
```bash
python main.py --show-config
```

### Test Microphone
```bash
python main.py --test-mic
```

### Run with Debug Mode
```bash
# In .env, set:
DEBUG_MODE=True
CONFIDENCE_DISPLAY=True

# Then run:
python main.py
```

### Manual Input Testing
```bash
python -c "
from input_validator import InputValidator
test = 'next slide'
sanitized, error = InputValidator.validate_and_sanitize(test)
print(f'✅ Valid: {sanitized}' if not error else f'❌ Error: {error}')
"
```

---

## 📊 SESSION STATISTICS

At the end of each session, see:
```
📊 FINAL REPORT
───────────────
Duration          : 12.5 minutes
Total commands    : 45
  - Next slide    : 18
  - Back slide    : 12
  - Open show     : 1
  - Unknown       : 13
Success rate      : 71.1%
```

---

## 💡 TIPS & TRICKS

### Tip 1: Use Microphone Test Before Presentation
```bash
python main.py --test-mic
```
Ensures everything works before the big moment!

### Tip 2: Adjust Sensitivity for Your Accent
```ini
# In .env - decrease for more lenient matching
FUZZY_THRESHOLD=75  # More forgiving
FUZZY_THRESHOLD=85  # More strict
```

### Tip 3: Enable Real-time Confidence
```ini
# In .env
CONFIDENCE_DISPLAY=True
DEBUG_MODE=True
```
Shows how confident system is in each command.

### Tip 4: Reduce False Positives
```ini
# In .env - increase cooldown
COOLDOWN_SECONDS=3  # Prevents double-commands
```

### Tip 5: Network Issues
If Google API timeout, system auto-retries:
```ini
# In .env - more retries for unreliable network
MAX_RETRIES=5
RETRY_DELAY=2
```

---

## 🚀 NEXT STEPS

After basic setup:

1. **Customize Configuration** → Edit .env for your preferences
2. **Test in Real Scenario** → Do a full presentation practice
3. **Learn All Commands** → Say "help menu" during use
4. **Enable Accessibility** → Try "popup on" for captions
5. **Check Statistics** → Review success rate at end of session

---

## 📞 GETTING HELP

### Quick Diagnostics
```bash
# 1. Check configuration
python main.py --show-config

# 2. Test microphone
python main.py --test-mic

# 3. Enable debug mode and run
# (Set DEBUG_MODE=True in .env)
python main.py
```

### Documentation
- **IMPROVEMENTS.md** - All new features and improvements
- **SECURITY_GUIDE.md** - Security best practices
- **ACCESSIBILITY_README.md** - Accessibility features

### Common Issues
See [Troubleshooting](#troubleshooting) section above

---

## ✅ VERIFICATION CHECKLIST

Before using in production:

- [ ] Microphone connected and working (`--test-mic`)
- [ ] .env file created from .env.example
- [ ] Configuration validated
- [ ] All commands tested manually
- [ ] Presentation content ready
- [ ] Network connection stable
- [ ] Quiet environment available
- [ ] DEBUG_MODE checked (can disable for cleaner output)

---

**Ready to use! 🎉**

Start with:
```bash
python main.py
```

Good luck with your presentation!
