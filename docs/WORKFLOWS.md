# WORKFLOWS & HOW-TO GUIDES
**Last Updated:** 2026-01-27

---

## 📧 EMAIL OPERATIONS

### Check Skipper's Inbox
```bash
himalaya envelope list -a skipper
```

### Read a Specific Email
```bash
himalaya message read -a skipper <MESSAGE_ID>
```

### Send an Email
```bash
cat << 'EOF' | himalaya message send -a skipper
From: luis.ai.skipper@gmail.com
To: recipient@example.com
Subject: Your Subject Here

Your message body here.

Best,
Skipper
EOF
```

### Reply to an Email
```bash
himalaya message reply -a skipper <MESSAGE_ID>
```

---

## 🌐 BROWSER AUTOMATION

### 1. Check Available Tabs
```
browser action=tabs profile=chrome
```

### 2. Attach a Tab (Luis must do this)
- Go to the tab in Chrome
- Click the Clawdbot extension icon
- Badge turns ON = attached

### 3. Take a Snapshot
```
browser action=snapshot profile=chrome targetId=<TAB_ID>
```

### 4. Navigate to URL
```
browser action=navigate profile=chrome targetId=<TAB_ID> targetUrl="https://example.com"
```

### 5. Click an Element
```
browser action=act profile=chrome targetId=<TAB_ID> request={"kind":"click","ref":"<REF>"}
```

### 6. Type Text
```
browser action=act profile=chrome targetId=<TAB_ID> request={"kind":"type","ref":"<REF>","text":"hello"}
```

---

## 📞 PHONE NUMBER LOOKUPS

### Process Overview
1. Script reads unprocessed names from CSV
2. Build FastPeopleSearch URL for each
3. Open in browser, extract phone numbers
4. Save to results CSV
5. **IF CAPTCHA → NOTIFY LUIS IMMEDIATELY**

### Files
- **Source:** `/Users/luisgarcia/Documents/FL Geographic/central_fl_4units_detailed.csv`
- **Results:** `/Users/luisgarcia/Documents/FL Geographic/phone_results_browser.csv`
- **Progress:** `/Users/luisgarcia/Documents/FL Geographic/lookup_progress.json`

### Check Progress
```bash
wc -l "/Users/luisgarcia/Documents/FL Geographic/phone_results_browser.csv"
```

### When CAPTCHA Appears
1. **STOP scraping immediately**
2. **Message Luis on Telegram:** "🚨 CAPTCHA hit! Please solve it in the browser window."
3. Wait for Luis to confirm solved
4. Resume processing

---

## 💬 MESSAGING LUIS

### Send a Telegram Message
Use the `message` tool:
```
message action=send target=telegram:5601940168 message="Your message here"
```

Or just reply in the conversation.

### For Urgent Alerts
Start with emoji: 🚨 ⚠️ 📞 📧

---

## ⏰ CRON JOB MANAGEMENT

### List All Jobs
```
cron action=list
```

### Add a New Job
```
cron action=add job={
  "text": "What the job should do",
  "schedule": "0 6 * * *",
  "deliverTo": "telegram:5601940168"
}
```

### Remove a Job
```
cron action=remove jobId=<JOB_ID>
```

### Run a Job Now
```
cron action=run jobId=<JOB_ID>
```

---

## 🗣️ VOICE TRANSCRIPTION

### Transcribe a Voice Message
```bash
# Convert OGG to WAV
ffmpeg -i input.ogg -ar 16000 -ac 1 output.wav

# Transcribe with Whisper
whisper-cli -m ~/.local/share/whisper-cpp/models/ggml-base.en.bin output.wav
```

---

## 💰 MEMECOIN SCANNING

### Manual Scan
```bash
python3 ~/clawd/scripts/memecoin_scanner.py
```

### Check Latest Results
```bash
cat ~/clawd/scripts/latest_scan.json
```

### Criteria for Alerts
- Significant price/volume change
- Social engagement spike
- Pattern matches from @funcry analysis

---

## 🏠 REPAL APP

### Start Development Server
```bash
cd ~/clawd/repal-app && npm run dev
```
Runs at: http://localhost:3001

### Check for Uncommitted Changes
```bash
cd ~/clawd/repal-app && git status
```

### Database Migrations
```bash
cd ~/clawd/repal-app/supabase
# Check migration files
ls migrations/
```

---

## 🗂️ MEMORY MANAGEMENT

### Session Start Protocol
1. Read `SOUL.md` - Who am I
2. Read `USER.md` - Who is Luis
3. Read `memory/YYYY-MM-DD.md` - Today and yesterday
4. Read `MEMORY.md` - Long-term memory (main session only)
5. Read `HEARTBEAT.md` - Active tasks

### Create Daily Memory Log
```markdown
# Memory Log - January 27, 2026

## Session Summary
- What happened
- Decisions made
- Issues encountered

## Tasks Completed
- [ ] Task 1
- [x] Task 2

## Notes
Any important context
```

### Update Long-Term Memory
Edit `~/clawd/MEMORY.md` with:
- Significant learnings
- Important decisions
- New preferences discovered
- Key people/contacts

---

## 🔧 TROUBLESHOOTING

### Gateway Not Responding
```bash
clawdbot gateway status
clawdbot gateway restart  # Ask Luis first!
```

### Browser Tab Not Found
1. Check if tab is attached (extension badge ON)
2. Try `browser action=focus` first
3. Luis may need to reattach

### Email Send Fails
- Check himalaya config: `~/.config/himalaya/config.toml`
- Test with: `himalaya envelope list -a skipper`

### Process Stuck
```bash
# List running exec sessions
process action=list

# Kill a stuck process
process action=kill sessionId=<SESSION_ID>
```

---

*Add new workflows as we discover them!*
