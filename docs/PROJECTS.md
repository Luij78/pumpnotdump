# PROJECTS
**Last Updated:** 2026-01-27

---

## 🏠 ACTIVE PROJECTS

### 1. REPal CRM
**Status:** Active Development
**Priority:** HIGH

**Description:** Real estate CRM built for Luis's agent business

**Tech Stack:**
- Next.js 14
- Supabase (database)
- Clerk (authentication)
- Tailwind CSS

**Location:** `~/clawd/repal-app`
**GitHub:** https://github.com/Luij78/repal-app
**Running at:** http://localhost:3001

**Features Implemented:**
- Lead Manager with priority scoring (1-10)
- Notes Log with timestamped entries
- AI Follow-up, AI Rewrite, Voice buttons
- Birthday and Home Anniversary tracking
- Quick message generation
- Status workflow (New → Contacted → Qualified → etc.)

**Known Issues:**
- Clerk auth may have key mismatch (infinite redirect warning)
- Some Supabase migrations pending

**Recent Changes (2026-01-27):**
- Added Notes Log section matching tiiny.site design
- Added "Add Timestamped Entry" teal button
- Made Lead Detail modal wider
- Added auto-scroll to latest note

---

### 2. Phone Number Lookups (Real Estate Leads)
**Status:** IN PROGRESS - BLOCKED BY CAPTCHA
**Priority:** HIGH

**Description:** Scraping phone numbers for property owners in Central FL

**Data Location:** `/Users/luisgarcia/Documents/FL Geographic/`

**Files:**
- `central_fl_4units_detailed.csv` - Source data (property owners)
- `phone_results_browser.csv` - Results with phone numbers
- `lookup_progress.json` - Processing state
- `browser_phone_lookup.py` - Main script

**Progress:**
- Total individual owners: ~1,098
- Completed: 112 (with phone numbers found)
- Remaining: ~986

**Website:** FastPeopleSearch.com

**Issue:** CAPTCHA triggers after ~30-40 lookups. Need human to solve checkbox CAPTCHA.

**Process:**
1. Open FastPeopleSearch URL for each owner
2. Extract phone numbers from results
3. Save to CSV with Name, City, Address, Phone1, Phone2, Phone3, Status
4. When CAPTCHA appears → IMMEDIATELY NOTIFY LUIS

---

### 3. Pump.fun Hackathon 🏆
**Status:** Planning
**Priority:** MEDIUM

**Description:** $3M prize pool hackathon - 12 winners get $250k each

**Deadline:** February 18, 2026

**Concept Ideas:**
- $REPAL token
- $SKIPPER token
- Veteran-themed token
- Meme play

**Solana Wallet:** `5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir`
**Keypair:** `~/.config/solana/skipper-wallet.json`

---

### 4. TradingPal (Polymarket Bot)
**Status:** Needs Fix
**Priority:** LOW

**Description:** Automated trading bot for Polymarket prediction markets

**Location:** Desktop iMac `~/deal_finder/TradingPal/`
**Wallet:** `0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3`

**Issue:** Sell orders failing on expired markets - needs proper redemption logic for resolved markets

---

### 5. Memecoin Scanner
**Status:** Running
**Priority:** MEDIUM

**Description:** Automated scanner for pumping memecoins

**Script:** `~/clawd/scripts/memecoin_scanner.py`
**Schedule:** Every 30 minutes (cron job)
**Output:** `~/clawd/scripts/latest_scan.json`

**Criteria:**
- Price/volume changes
- Social engagement spikes
- @funcry timeline patterns (blocked - bird CLI times out)

---

### 6. X/Twitter Revival (@luij78)
**Status:** Blocked
**Priority:** MEDIUM

**Description:** Revive Luis's Twitter account for monetization

**Account:** @luij78 (4k followers, currently dormant)
**Goal:** Build following, post consistently, X Premium payouts

**Issue:** Bird CLI times out on GraphQL requests. Need alternative approach or debug cookies.

---

### 7. Voice Chat Interface
**Status:** Testing
**Priority:** LOW

**Description:** Web-based voice interface to talk to Skipper

**Location:** `~/clawd/voice-chat/`
**URL:** http://localhost:8888
**Server:** `node server.js`

**Features:**
- Push-to-talk or click-to-toggle
- Web Speech API for recognition
- TTS for responses
- Proxies to Clawdbot API

**Issue:** Some users having trouble with microphone permissions

---

## 📦 COMPLETED PROJECTS

### Central FL Property Data Collection
**Completed:** 2026-01-26

**Description:** Collected 4-unit property data for Central FL

**Output:** 2,328 properties in `central_fl_4units_detailed.csv`

**Shared with:** Alexander Dias (alexanderdias@kw.com)

---

## 📋 PROJECT TEMPLATE

When adding new projects:

```markdown
### Project Name
**Status:** Planning | Active | Blocked | Completed
**Priority:** HIGH | MEDIUM | LOW

**Description:** What is this project?

**Location:** Where are the files?

**Tech/Tools:** What's used?

**Current State:** What's done? What's left?

**Blockers:** Any issues?

**Next Steps:** What needs to happen next?
```

---

*Keep this updated as projects progress!*
