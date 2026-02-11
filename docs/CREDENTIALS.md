# CREDENTIALS & API KEYS
**Last Updated:** 2026-01-27
**⚠️ SENSITIVE - Do not share publicly**

---

## 📧 EMAIL (Skipper's Account)

### Gmail Account
- **Email:** luis.ai.skipper@gmail.com
- **Purpose:** Skipper's dedicated email for sending/receiving
- **Created:** 2026-01-25

### Himalaya Email CLI
- **Config File:** `~/.config/himalaya/config.toml`
- **Account Name:** `skipper`
- **Protocol:** IMAP/SMTP with Gmail

**How to use:**
```bash
# List inbox
himalaya envelope list -a skipper

# Read message (by ID)
himalaya message read -a skipper <ID>

# Send email
echo "message body" | himalaya message send -a skipper
```

---

## 🤖 CLAWDBOT GATEWAY

### Gateway Configuration
- **Config File:** `~/.clawdbot/clawdbot.json`
- **Port:** 18789
- **Bind:** loopback (127.0.0.1)
- **Auth Mode:** token

### Gateway Token
- **Token:** `d393c3ce17a9add5233ef964e262bf271edd3167dc9ad790`
- **Used for:** API calls to gateway, browser extension

### Browser Extension
- **Location:** `/opt/homebrew/lib/node_modules/clawdbot/assets/chrome-extension`
- **Backup copy:** `~/Desktop/clawdbot-chrome-extension`
- **Relay Port:** 18792

---

## 🐦 X/TWITTER (@luij78)

### Bird CLI Cookies
- **Config:** `~/.config/bird/config.json5`
- **auth_token:** `f43e830764a4a60500e73b21079c442f5e12be9f`
- **ct0:** (stored in config file)

**Status:** Timing out on GraphQL - needs debugging

---

## 💰 CRYPTO WALLETS

### Polymarket (Ethereum/Polygon)
- **Wallet:** `0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3`
- **Platform:** Polymarket (Polygon network)
- **Bot Location:** `~/deal_finder/TradingPal/` (on Desktop/iMac)

### Solana (Memecoin Trading)
- **Pubkey:** `5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir`
- **Keypair File:** `~/.config/solana/skipper-wallet.json`
- **Created:** 2026-01-26
- **Network:** mainnet-beta
- **Purpose:** Pump.fun hackathon + memecoin trading

---

## 🔐 TELEGRAM BOT

### Clawdbot Telegram Integration
- **Chat with Luis:** Telegram @luij78 (ID: 5601940168)
- **Token:** Stored in `~/.clawdbot/clawdbot.json` under `channels.telegram`

---

## 📊 SUPABASE (REPal Database)

### Project Details
- **Project:** REPal CRM
- **Location:** `~/clawd/repal-app/.env.local`
- **Contains:** NEXT_PUBLIC_SUPABASE_URL, SUPABASE_ANON_KEY, etc.

---

## 🔑 CLERK (REPal Auth)

### Configuration
- **Location:** `~/clawd/repal-app/.env.local`
- **Contains:** NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY

**Note:** May have key mismatch causing infinite redirect - needs debugging

---

## 🗣️ ELEVENLABS (TTS)

### Voice Synthesis
- **CLI Tool:** `sag` (if installed)
- **Used for:** Converting text to speech for voice responses
- **API Key:** Check `~/.config/sag/` or environment variables

---

## 🌐 BRAVE SEARCH

### Web Search API
- **Used by:** Clawdbot's web_search tool
- **Plan:** Free tier (rate limited)
- **Limits:** 2000 queries/month, 1 req/sec

---

## 🖥️ SSH CONNECTIONS

### Desktop (iMac)
- **Host:** `garciafamilybusiness@192.168.5.51`
- **Purpose:** TradingPal bot, additional compute

### Mac Mini (Main Server)
- **Host:** `luisgarcia@Luiss-Mac-mini-2.local`
- **Purpose:** Clawdbot gateway, main operations

---

## 📝 HOW TO ADD NEW CREDENTIALS

When adding new API keys or credentials:
1. Add to this file with clear labeling
2. Note the config file location
3. Include usage examples
4. Update MASTER.md if it's a major service

---

*Keep this file updated whenever credentials change!*
