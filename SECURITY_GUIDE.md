# ============================================
# SECURITY GUIDE FOR VOICE CONTROL
# ============================================

## 🔒 SECURITY ARCHITECTURE

This application implements multiple layers of security to protect your system and data:

```
┌─────────────────────────────────────────────┐
│  SECURITY LAYERS                            │
├─────────────────────────────────────────────┤
│ 1. Input Validation                         │
│    ├─ Sanitization (remove dangerous chars) │
│    ├─ Injection detection                   │
│    └─ Whitelist validation                  │
├─────────────────────────────────────────────┤
│ 2. Command Execution Control                │
│    ├─ Whitelist-only commands               │
│    ├─ pyautogui event validation            │
│    └─ Rate limiting                         │
├─────────────────────────────────────────────┤
│ 3. Credential Management                    │
│    ├─ Environment variables (.env)          │
│    ├─ No hardcoded secrets                  │
│    └─ Git-ignored configuration             │
├─────────────────────────────────────────────┤
│ 4. Data Protection                          │
│    ├─ File permissions (mode 600)           │
│    ├─ Secure logging                        │
│    └─ No sensitive data in logs             │
└─────────────────────────────────────────────┘
```

---

## 🛡️ THREAT MITIGATION

### 1. COMMAND INJECTION ATTACKS

**Threat:** Attacker uses voice to inject system commands
```
Voice Input: "next slide; rm -rf ~"
→ System attempts: press_key('right'); rm -rf ~
→ Dangerous! 🔴
```

**Mitigation:**
- ✅ Input sanitization removes `;`, `|`, `&`, etc.
- ✅ Whitelist validation (only safe commands allowed)
- ✅ No shell execution (only keyboard events)
- ✅ pyautogui limited to safe key presses

**Safe Commands:**
```python
SAFE_COMMANDS = {
    "next", "previous", "stop", "help", "test",
    "open_slideshow", "close_slideshow", "noise",
    "popup_on", "popup_off", "caption_on", "caption_off",
    "change_language", "show_analytics"
}
```

### 2. PATH TRAVERSAL ATTACKS

**Threat:** Attacker tries to access sensitive files
```
Voice Input: "../../sensitive_file"
→ Attempts to read outside allowed directory
→ Dangerous! 🔴
```

**Mitigation:**
- ✅ Path validation prevents `..` sequences
- ✅ Only whitelisted directories allowed
- ✅ File operations checked against safe paths

### 3. CODE INJECTION

**Threat:** Malicious code embedded in voice input
```
Voice Input: "exec(import os; os.system('rm -rf'))"
→ Dangerous! 🔴
```

**Mitigation:**
- ✅ Keyword blocking (exec, eval, import, etc.)
- ✅ Input length limits (max 200 chars)
- ✅ Character restrictions (alphanumeric + spaces only)
- ✅ No dynamic code execution

### 4. API KEY EXPOSURE

**Threat:** Credentials visible in source code
```python
# DANGEROUS! 🔴
GOOGLE_API_KEY = "sk-1234567890abcdef"
```

**Mitigation:**
- ✅ Environment variables (.env file)
- ✅ .env in .gitignore (never committed)
- ✅ Separate configs for dev/prod
- ✅ Credentials passed via environment only

### 5. DATA LEAKAGE

**Threat:** Sensitive data in logs or files
```
Log: "User said: 'next' from device 192.168.1.100"
→ Tracks user location!
```

**Mitigation:**
- ✅ Logging without sensitive data
- ✅ File permissions (600 - read by owner only)
- ✅ No IP addresses in logs
- ✅ No user voice samples recorded
- ✅ History file is local-only

---

## 🔐 SETUP SECURITY

### Step 1: Create .env File
```bash
# Copy from template (NEVER commit .env!)
cp .env.example .env
```

### Step 2: Add to .gitignore
```bash
# Ensure .env is ignored
echo ".env" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__/" >> .gitignore
```

### Step 3: Restrict File Permissions

**Windows (PowerShell - Admin):**
```powershell
# Restrict to current user only
icacls ".env" /inheritance:r /grant:r "$env:username`:F"
icacls "speech_history.txt" /inheritance:r /grant:r "$env:username`:F"
```

**Linux/Mac:**
```bash
# Owner read/write only
chmod 600 .env
chmod 600 speech_history.txt
```

### Step 4: Validate Configuration
```bash
# Check configuration is valid
python -c "from config_manager import get_config; c = get_config(); print('✅ Valid' if c.validate() else '❌ Invalid')"
```

---

## 🚨 INPUT VALIDATION FLOW

```
Voice Input (from microphone)
    ↓
Length Check (2-200 characters)
    ↓
Special Character Removal
    ├─ Remove: `;`, `|`, `&`, `$`, `(`, `)`, etc.
    └─ Keep: letters, numbers, spaces
    ↓
Injection Pattern Detection
    ├─ Shell patterns: `exec`, `eval`, `system`
    ├─ Keywords: `import`, `subprocess`, `bash`
    └─ Symbols: `..`, `/`, `>`, `<`
    ↓
Whitelist Command Validation
    ├─ Is command in safe list?
    └─ YES → Continue | NO → Reject
    ↓
Safe Execution
    └─ Execute validated command only
```

---

## 📊 VALIDATION EXAMPLES

### ✅ VALID INPUT
```
"next slide"          → ✅ Allowed (sanitized to "next slide")
"back slide"          → ✅ Allowed (sanitized to "back slide")
"stop program"        → ✅ Allowed
"help menu"           → ✅ Allowed
```

### ❌ INVALID INPUT
```
"next; rm -rf /"      → ❌ Blocked (shell injection)
"../../passwords"     → ❌ Blocked (path traversal)
"exec(malicious)"     → ❌ Blocked (code injection)
"next|next|next"      → ❌ Blocked (pipe characters)
"$(dangerous)"        → ❌ Blocked (variable expansion)
"test`command`here"   → ❌ Blocked (command substitution)
```

---

## 🔍 MONITORING & LOGGING

### Safe Logging Practices
```python
# ✅ SAFE: Only log command type
print("Command: next_slide")

# ❌ UNSAFE: Logs user voice (PII)
print(f"User said: {voice_input}")

# ✅ SAFE: Log error type without details
print("Google API Error")

# ❌ UNSAFE: Logs API response with secrets
print(f"API Response: {api_response}")
```

### What Gets Logged
- Command types (next, previous, etc.)
- Success/failure status
- Generic error types
- System state changes

### What Never Gets Logged
- User's voice/speech input
- API responses
- Credentials
- System paths
- IP addresses
- Personal information

---

## 🚀 DEPLOYMENT SECURITY

### Before Going Live
- [ ] .env file configured with secure values
- [ ] .env added to .gitignore
- [ ] File permissions set (chmod 600)
- [ ] Dependencies updated (`pip install --upgrade -r requirements.txt`)
- [ ] Security validation passed
- [ ] Test with --test-mic option
- [ ] Review error_handler output in debug mode

### Production Checklist
```bash
# Verify security
python -c "from input_validator import InputValidator as IV; \
  tests = ['next slide', 'next; rm -rf', '../sensitive']; \
  [print(f'{t}: {\"✅\" if IV.validate_and_sanitize(t)[0] else \"❌\"}') for t in tests]"

# Check configuration
python main.py --show-config

# Test microphone
python main.py --test-mic

# Verify file permissions
ls -la .env speech_history.txt
```

### Hardening Tips
1. **Network:** Run on localhost only (no network exposure)
2. **Process:** Run with minimum required privileges
3. **Filesystem:** Use full-disk encryption (BitLocker/FileVault)
4. **Updates:** Keep OS and Python libraries updated
5. **Monitoring:** Review logs regularly for anomalies

---

## 🎯 BEST PRACTICES

### Daily Usage
1. Keep .env file secure (never share)
2. Don't speak credentials or sensitive info
3. Monitor error messages for anomalies
4. Review speech_history.txt periodically
5. Report any unexpected behavior

### Regular Maintenance
```bash
# Weekly: Update dependencies
pip install --upgrade -r requirements.txt

# Monthly: Review logs
tail -50 speech_history.txt

# Quarterly: Security audit
python main.py --show-config
python main.py --test-mic
```

### Incident Response
If you suspect a security issue:
1. Stop the application
2. Review recent logs
3. Check .env file integrity
4. Verify file permissions
5. Restart application
6. Enable DEBUG_MODE for investigation

---

## 🔗 SECURITY RESOURCES

### Input Validation
- OWASP Input Validation Cheat Sheet
- Python Security Best Practices
- Voice Interface Security Patterns

### Credential Management
- 12-Factor App Configuration
- Environment Variables Best Practices
- Secret Management Tools (HashiCorp Vault, etc.)

### Secure Coding
- OWASP Top 10
- CWE Top 25 Most Dangerous Software Weaknesses
- Python Security in Depth

---

## 📞 REPORTING SECURITY ISSUES

If you discover a security vulnerability:
1. **DO NOT** post on public forums
2. **DO** contact developers directly
3. **DO** provide:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (optional)

---

## ✅ SECURITY VALIDATION CHECKLIST

### Startup Validation
```
[✓] Load .env file
[✓] Validate configuration
[✓] Check file permissions
[✓] Initialize error handler
[✓] Initialize input validator
[✓] Start voice recognizer
```

### Runtime Validation
```
[✓] Sanitize voice input
[✓] Detect injection patterns
[✓] Validate command whitelist
[✓] Execute safely
[✓] Log safely (no PII)
```

### Shutdown Validation
```
[✓] Close microphone safely
[✓] Save history securely
[✓] Clear sensitive data
[✓] Close all files
```

---

**Version:** 1.1
**Last Updated:** 2025-12-23
**Status:** Production Ready
