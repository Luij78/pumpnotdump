# INFRASTRUCTURE & SYSTEM SETUP
**Last Updated:** 2026-01-27

---

## ⚠️ IMPORTANT: CLAWDBOT → MOLTBOT TRANSITION

**Status:** Clawdbot has been renamed to **Moltbot** due to Anthropic trademark C&D.

- **Current package:** `clawdbot` (npm) — still works, version 2026.1.24-3
- **New package:** `moltbot` (npm) — will be the future
- **Website:** https://molt.bot
- **GitHub:** https://github.com/moltbot/moltbot

**Migration plan:**
1. Monitor `moltbot` npm package for stable release
2. When ready: `npm uninstall -g clawdbot && npm install -g moltbot`
3. Config files likely stay the same (same codebase)
4. Update commands from `clawdbot` to `moltbot`

**No action needed yet** — current setup works fine.

---

## 🖥️ HARDWARE

### Mac Mini (Primary Server)
- **User:** luisgarcia
- **OS:** macOS (Darwin 24.6.0, arm64)
- **Node.js:** v25.4.0
- **Role:** Main Clawdbot gateway, all primary operations
- **Location:** Luis's home

### iMac (Desktop)
- **User:** garciafamilybusiness
- **IP:** 192.168.5.51
- **Role:** Secondary compute, TradingPal bot
- **Access:** SSH from Mac Mini

---

## 🤖 CLAWDBOT GATEWAY

### Service Details
- **Type:** LaunchAgent (auto-starts on login)
- **Plist:** `~/Library/LaunchAgents/com.clawdbot.gateway.plist`
- **Logs:** `/tmp/clawdbot/clawdbot-YYYY-MM-DD.log`
- **Port:** 18789
- **Bind:** loopback (127.0.0.1) - local only for security

### Config Location
- **File:** `~/.clawdbot/clawdbot.json`
- **Service Config:** Same file

### Commands
```bash
# Check status
clawdbot gateway status

# Start/stop/restart
clawdbot gateway start
clawdbot gateway stop
clawdbot gateway restart

# View logs
tail -f /tmp/clawdbot/clawdbot-$(date +%Y-%m-%d).log
```

### ⚠️ IMPORTANT
**NEVER restart the gateway without asking Luis first** - it disconnects all active sessions!

---

## 🌐 BROWSER CONTROL

### Chrome Extension (Browser Relay)
- **Extension Location:** `/opt/homebrew/lib/node_modules/clawdbot/assets/chrome-extension`
- **Desktop Copy:** `~/Desktop/clawdbot-chrome-extension`
- **Relay Port:** 18792
- **Profile:** `chrome` (for browser tool)

### How to Load Extension
1. Go to `chrome://extensions`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select the chrome-extension folder

### How to Attach a Tab
1. Navigate to the tab you want to control
2. Click the Clawdbot extension icon in toolbar
3. Badge should turn ON

### Using Browser Tool
```javascript
// Check tabs
browser action=tabs profile=chrome

// Take snapshot
browser action=snapshot profile=chrome targetId=<TAB_ID>

// Navigate
browser action=navigate profile=chrome targetId=<TAB_ID> targetUrl="https://..."
```

---

## 📱 TELEGRAM CHANNEL

### Configuration
- **Channel:** telegram
- **Luis's Chat ID:** 5601940168
- **Username:** @luij78
- **Bot configured in:** `~/.clawdbot/clawdbot.json`

### Capabilities
- Inline buttons
- Reactions (MINIMAL mode)
- Voice message transcription
- Image/media handling

---

## ⏰ SCHEDULED JOBS (CRON)

### Active Cron Jobs
| Job | Schedule | Purpose |
|-----|----------|---------|
| Morning Brief | 6:00 AM EST | Weather, tasks, daily update |
| Overnight Work | 11:00 PM EST | Proactive tasks while Luis sleeps |
| Memecoin Scanner | Every 30 min | Check for pumping coins |

### Managing Cron
```bash
# List jobs
cron action=list

# Add job
cron action=add job={...}

# Remove job
cron action=remove jobId=<ID>
```

---

## 📂 KEY DIRECTORIES

```
~/.clawdbot/                 # Clawdbot config and data
├── clawdbot.json            # Main config
├── agents/                  # Agent data
├── media/                   # Media files (inbound/outbound)
└── sessions/                # Session transcripts

~/.config/himalaya/          # Email CLI config
└── config.toml

~/.config/bird/              # Twitter CLI config
└── config.json5

~/.config/solana/            # Solana wallet
└── skipper-wallet.json

~/clawd/                     # Main workspace
~/Documents/FL Geographic/   # Real estate data files
```

---

## 🔧 INSTALLED TOOLS

### CLI Tools
- **himalaya** - Email (IMAP/SMTP)
- **bird** - Twitter/X CLI
- **whisper-cli** - Voice transcription
- **ffmpeg** - Audio/video processing
- **solana** - Solana CLI for crypto

### Whisper Transcription
- **Model:** `~/.local/share/whisper-cpp/models/ggml-base.en.bin`
- **Workflow:** ffmpeg (ogg→wav) → whisper-cli → text

---

## 🚀 SERVICES RUNNING

| Service | Port | Purpose |
|---------|------|---------|
| Clawdbot Gateway | 18789 | Main AI agent gateway |
| Browser Relay | 18792 | Chrome extension relay |
| REPal App | 3001 | Real estate CRM |
| Voice Chat | 8888 | Web voice interface |

### Check Running Services
```bash
# List listening ports
lsof -i -P | grep LISTEN

# Check specific port
lsof -i :18789
```

---

## 🔄 STARTUP SEQUENCE

When the Mac Mini boots:
1. LaunchAgent starts Clawdbot gateway automatically
2. Gateway connects to Anthropic API
3. Telegram bot comes online
4. Cron jobs resume

If REPal needs to run:
```bash
cd ~/clawd/repal-app && npm run dev
```

If Voice Chat needs to run:
```bash
cd ~/clawd/voice-chat && node server.js
```

---

*Keep infrastructure docs updated when systems change!*
