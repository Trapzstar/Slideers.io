# ============================================
# COMPREHENSIVE TROUBLESHOOTING GUIDE
# ============================================

## 📋 TROUBLESHOOTING FLOWCHART

```
Application Issue
    ↓
Is it startup? → Check [Startup Issues](#startup-issues)
    ↓
Is it microphone? → Check [Microphone Issues](#microphone-issues)
    ↓
Is it recognition? → Check [Recognition Issues](#recognition-issues)
    ↓
Is it commands? → Check [Command Issues](#command-issues)
    ↓
Is it performance? → Check [Performance Issues](#performance-issues)
    ↓
Still not working? → Check [Advanced Debugging](#advanced-debugging)
```

---

## 🔧 STARTUP ISSUES

### Issue: "ModuleNotFoundError: No module named 'X'"

**Cause:** Missing Python package

**Solution:**
```bash
# Reinstall all requirements
pip install -r requirements.txt --upgrade

# Or install specific package
pip install speech-recognition
pip install pyaudio
pip install pyautogui
```

**Verify:**
```bash
python -c "import speech_recognition; print('✅ OK')"
python -c "import pyaudio; print('✅ OK')"
python -c "import pyautogui; print('✅ OK')"
```

---

### Issue: "[ERROR] PyAutoGUI belum terinstall"

**Cause:** PyAutoGUI not installed

**Solution:**
```bash
pip install pyautogui
pip install -r requirements.txt
```

**Test:**
```bash
python -c "import pyautogui; pyautogui.press('a'); print('✅ PyAutoGUI works')"
```

---

### Issue: Application starts but crashes immediately

**Cause:** Missing configuration file or initialization error

**Solution:**
```bash
# 1. Create configuration
cp .env.example .env

# 2. Enable debug mode
# Edit .env and set: DEBUG_MODE=True

# 3. Run with error output
python main.py 2>&1 | tee debug.log

# 4. Review debug.log
notepad debug.log
```

---

### Issue: "⚠️ .env file not found"

**Cause:** Configuration file missing

**Solution:**
```bash
# Create from template
cp .env.example .env

# Application will use defaults
# But configure .env for your preferences
notepad .env
```

---

## 🎤 MICROPHONE ISSUES

### Issue: "Microphone setup error"

**Cause:** Microphone not detected or not accessible

**Diagnostics:**
```bash
# 1. Test microphone
python main.py --test-mic

# 2. List available devices
python -c "
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f'{i}: {info[\"name\"]}')"

# 3. Try specific device
python main.py --device 2
```

**Solutions:**
1. **Check Hardware:**
   - ✅ Microphone USB cable connected firmly
   - ✅ Microphone powered (if USB-powered)
   - ✅ Not loose or damaged

2. **Check Software:**
   - ✅ Microphone enabled in Windows Settings
   - ✅ Not muted in Volume Mixer
   - ✅ App has microphone permission
   - ✅ Updated audio drivers

3. **Check System:**
   - ✅ Restart computer
   - ✅ Try different USB port
   - ✅ Disable other audio apps
   - ✅ Check Windows Audio service running

---

### Issue: "⏰ Timeout - tidak ada suara terdeteksi"

**Cause:** Microphone not picking up speech

**Symptoms:**
- Always times out even when speaking
- No audio indicator in Windows
- Microphone appears to work elsewhere

**Diagnostics:**
```bash
# Check if microphone can capture audio
python main.py --test-mic

# Check Windows Volume Mixer
# Settings → Sound → Volume mixer → App volume and device preferences
# (Look for this app, ensure microphone is selected)
```

**Solutions:**
1. **Microphone Muted:**
   - ✅ Check hardware mute button (usually has indicator)
   - ✅ Unmute in Windows Volume Mixer
   - ✅ Check Mute button in Volume Control

2. **Microphone Not Selected:**
   - ✅ Settings → Sound → Input → Select correct device
   - ✅ Settings → Volume mixer → App volume → Select device

3. **Microphone Not Working:**
   - ✅ Test in Windows Sound Settings
   - ✅ Speak and watch mic level indicator
   - ✅ Run microphone troubleshooter
   - ✅ Try different microphone

4. **Audio Settings:**
   - ✅ Increase microphone gain in Sound Settings
   - ✅ Disable noise cancellation temporarily
   - ✅ Disable any voice effects

---

### Issue: "🎤 Suara terdeteksi tapi tidak jelas"

**Cause:** Audio captured but not recognized

**Symptoms:**
- Microphone has levels but no text recognized
- Works sometimes but unreliable

**Solutions:**
1. **Speak Better:**
   - ✅ Speak **clearer** (enunciate)
   - ✅ Speak at **normal pace** (not too fast)
   - ✅ Speak **louder** (3-6 inches from mic)
   - ✅ Complete your phrase (don't pause mid-word)

2. **Reduce Noise:**
   - ✅ Close windows/doors
   - ✅ Turn off fans/AC
   - ✅ Minimize background conversation
   - ✅ Use microphone in quieter room

3. **Adjust Sensitivity:**
   ```ini
   # In .env - less strict fuzzy matching
   FUZZY_THRESHOLD=75  # More lenient (was 80)
   ```

4. **Recalibrate:**
   - ✅ Close and restart application (recalibrates automatically)
   - ✅ Let it calibrate in the environment where you'll use it

---

### Issue: Microphone works but then suddenly stops

**Cause:** Microphone driver issue or system resource problem

**Solutions:**
```bash
# 1. Restart application
# (Ctrl+C then python main.py)

# 2. Restart audio service
net stop "Windows Audio"
net start "Windows Audio"

# 3. Restart computer

# 4. Update audio drivers
# Device Manager → Audio inputs → Right-click → Update driver
```

---

## 🔍 RECOGNITION ISSUES

### Issue: "❌ Google API Error"

**Cause:** Google Speech API communication problem

**Network Issues:**
```bash
# Test internet connection
ping google.com

# Check firewall allows access
# Windows Firewall → Allow app through firewall
# Ensure Python (python.exe) is allowed
```

**Solutions:**
1. **Network:**
   - ✅ Check internet connection (ping google.com)
   - ✅ Check firewall settings
   - ✅ Disable VPN temporarily (if using)
   - ✅ Try different network (mobile hotspot)

2. **API Rate Limiting:**
   - ✅ Wait a moment and retry
   - ✅ Increase RETRY_DELAY in .env:
     ```ini
     MAX_RETRIES=5
     RETRY_DELAY=2  # Wait 2 seconds between retries
     ```

3. **Configuration:**
   - ✅ Verify GOOGLE_LANGUAGE in .env:
     ```ini
     GOOGLE_LANGUAGE=id-ID  # For Indonesian
     GOOGLE_LANGUAGE=en-US  # For English
     ```

---

### Issue: "Both recognition methods failed"

**Cause:** Google API failed and offline fallback not available

**Current Limitation:**
This version doesn't have offline speech recognition. It requires:
- Google Speech API access
- Internet connection
- Network connectivity to Google servers

**Solutions:**
1. **Short-term:**
   - ✅ Check internet connection
   - ✅ Verify network is stable
   - ✅ Try again in a moment
   - ✅ Check Windows can access Google

2. **Long-term:**
   - ✅ Consider backup internet (mobile hotspot)
   - ✅ Plan for offline mode in future version (Vosk integration)

---

## 💬 COMMAND ISSUES

### Issue: "⚠️ PERINTAH TIDAK DIKENALI" (Unknown Command)

**Cause:** Voice input didn't match any recognized command

**Diagnostics:**
```bash
# Enable confidence display
# In .env, set:
DEBUG_MODE=True
CONFIDENCE_DISPLAY=True

# Run and observe scores
python main.py
```

**Solutions:**
1. **Exact Phrase:**
   - ❌ Say: "next"
   - ✅ Say: "next slide"
   - ✅ Say: "slide next"
   (Use exact phrases from help menu)

2. **Pronunciation:**
   - ❌ Say: "neks slid"
   - ✅ Say: "next slide" clearly
   (Enunciate clearly)

3. **Reduce Strictness:**
   ```ini
   # In .env - be more lenient
   FUZZY_THRESHOLD=75  # Was 80
   ```

4. **Increase Cooldown:**
   ```ini
   # In .env - prevent double-execution
   COOLDOWN_SECONDS=3  # Was 2
   ```

5. **View All Commands:**
   Say: "help menu" to see all valid commands

---

### Issue: Wrong Command Executed

**Cause:** Voice matched a different command than intended

**Example:**
- Say: "back slide"
- Executed: "next slide" ❌

**Diagnostics:**
```bash
# Enable debug to see scores
DEBUG_MODE=True
CONFIDENCE_DISPLAY=True
```

**Solutions:**
1. **Speak Different:**
   - ✅ Articulate more clearly
   - ✅ Use different similar phrase:
     - "back slide" or "slide back" or "previous slide"

2. **Increase Threshold:**
   ```ini
   # In .env - more strict matching
   FUZZY_THRESHOLD=85  # Was 80
   ```

3. **Increase Cooldown:**
   ```ini
   # In .env - prevent rapid re-execution
   COOLDOWN_SECONDS=3
   ```

---

### Issue: Command Confirmation Not Working

**Cause:** Feature requires specific setup

**Note:** Command confirmation is optional feature
```ini
# In .env - to enable
REQUIRE_COMMAND_CONFIRMATION=True
```

**Current Behavior:** 
- Shows confirmation request
- But doesn't actually wait for voice response yet
- This is planned for future enhancement

---

## ⚡ PERFORMANCE ISSUES

### Issue: Application is slow/laggy

**Cause:** System resources or configuration

**Diagnostics:**
```bash
# Check system resources
# Task Manager → Performance tab
# Look for: CPU, Memory, Disk usage

# Monitor while running
python main.py  # Watch Task Manager while speaking
```

**Solutions:**
1. **System Resources:**
   - ✅ Close other heavy applications
   - ✅ Free up RAM (restart computer)
   - ✅ Disable background apps
   - ✅ Check disk space (need ~500MB free)

2. **Configuration:**
   - ✅ Reduce DEBUG_MODE if enabled
   - ✅ Disable CONFIDENCE_DISPLAY if slow
   - ✅ Reduce MAX_RETRIES
   - ✅ Reduce LISTEN_TIMEOUT

3. **Network:**
   - ✅ Check internet speed (minimum 1 Mbps)
   - ✅ Close bandwidth-heavy apps
   - ✅ Use wired connection if possible

---

### Issue: High CPU Usage

**Cause:** Background processing or infinite loops

**Check:**
```bash
# Monitor CPU in Task Manager
# Python.exe should be < 20% idle, ~30-50% when listening/processing

# Enable debug to see what's happening
DEBUG_MODE=True
python main.py
```

**Solutions:**
```bash
# 1. Reduce processing
# In .env
DEBUG_MODE=False
CONFIDENCE_DISPLAY=False

# 2. Reduce retries
MAX_RETRIES=2

# 3. Lower timeouts
LISTEN_TIMEOUT=4

# 4. Restart if stuck
# Ctrl+C to stop
# Then: python main.py
```

---

## 🛡️ SECURITY ISSUES

### Issue: "⚠️ Input validation error"

**Cause:** Voice input contains dangerous characters

**Example:**
- Say: "next; delete files"
- Detected: "Potential injection attempt" ✓ (Blocked correctly!)

**This is GOOD - security working!**

**Solutions:**
- ✅ Speak normal command (no special chars)
- ✅ Use exact phrases from help menu
- ✅ Don't try to exploit with voice

---

## 🐛 ADVANCED DEBUGGING

### Enable Full Debug Mode
```bash
# In .env
DEBUG_MODE=True
CONFIDENCE_DISPLAY=True

# Run and collect output
python main.py > debug_output.txt 2>&1
```

### Test Individual Components
```bash
# Test config manager
python -c "from config_manager import get_config; c = get_config(); c.show_config()"

# Test input validator
python -c "from input_validator import InputValidator; print(InputValidator.validate_and_sanitize('next slide'))"

# Test error handler
python -c "from error_handler import get_error_handler; e = get_error_handler(); e.handle_error('microphone_not_found')"

# Test voice detector
python -c "from voice_detector import SmartVoiceDetector; d = SmartVoiceDetector(); print(d.detect('next slide'))"
```

### Check File Permissions
```bash
# Windows - check file ownership
icacls .env

# Should show: (current_user):(F) - Full Control
# If wrong: run as administrator to fix

icacls ".env" /inheritance:r /grant:r "$env:username`:F"
```

### Review Error Logs
```bash
# If error log created
type error_log.txt

# Or run with logging
python main.py 2>&1 | tee full_log.txt
notepad full_log.txt
```

---

## 🆘 WHEN ALL ELSE FAILS

### Nuclear Reset
```bash
# 1. Stop the application
# (Ctrl+C)

# 2. Remove generated files
del speech_history.txt
del __pycache__\*.*

# 3. Reset configuration
del .env
copy .env.example .env

# 4. Restart computer

# 5. Test again
python main.py --test-mic
python main.py
```

### Collect Diagnostic Info
```bash
# Gather all diagnostic data
python main.py --show-config > diagnostics.txt
python main.py --test-mic >> diagnostics.txt 2>&1
systeminfo >> diagnostics.txt
ipconfig >> diagnostics.txt

# Review and share diagnostics.txt if asking for help
```

### Ask for Help
When posting for help, provide:
1. **Output from:** `python main.py --show-config`
2. **Output from:** `python main.py --test-mic`
3. **Error message** from screen
4. **Steps to reproduce** the issue
5. **System info** (Windows version, Python version)

---

## 📊 DIAGNOSTIC COMMANDS REFERENCE

```bash
# Show configuration
python main.py --show-config

# Test microphone
python main.py --test-mic

# Run with debug enabled
DEBUG_MODE=True python main.py

# Check specific module
python -c "from [module] import [class]; print('✅ OK')"

# List audio devices
python main.py | head -20

# Test specific device
python main.py --device 2

# Save full output
python main.py > output.log 2>&1
```

---

## 🎯 QUICK FIXES BY SYMPTOM

| Symptom | Quick Fix |
|---------|-----------|
| No sound detected | Unmute microphone, speak louder |
| Wrong command | Speak exact phrase from help menu |
| Crashes | `cp .env.example .env` then restart |
| API error | Check internet, wait moment, retry |
| Slow response | Close other apps, reduce debug mode |
| Confidence low | Speak clearer, reduce FUZZY_THRESHOLD |
| Always timeout | Enable microphone in Windows Settings |
| Nothing happens | Enable DEBUG_MODE to see what's happening |

---

**Last Updated:** 2025-12-23
**Version:** 1.1
