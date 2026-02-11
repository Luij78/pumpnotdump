# STATUS.md — Single Source of Truth
*Last updated: 2026-01-27 6:20 PM*

## 🖥️ MACHINES

### Desktop iMac (garciafamilybusiness@192.168.5.51)
**Active processes:**
- `flip_app.py` — FlipHunter web app on port 8080
- `hold_to_settle.py` — Polymarket bot (holding to settlement)
- `dry_run_15m.py` — Paper trading 15-min markets
- `panic_fade_dry.py` — Testing panic fade strategy
- `flip_finder_full.py PS5 --watch` — PS5 deal watcher

**TradingPal Wallet:** 0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3
**MATIC Balance:** 66.7 (~$35)
**VPN:** Running (VPN Proxy Master)

### Mac Mini (luisgarcia@Luiss-Mac-mini.local)
- Clawdbot gateway running
- This is where I operate from

---

## 📊 PROJECTS

### 1. FlipHunter Pro
**Status:** ✅ LIVE
**URL:** http://192.168.5.51:8080
**What it does:** Scans Craigslist for underpriced items, calculates real profit
**Database:** 156 items, 17 categories (electronics, tools, gold/silver, comics, etc.)
**Cron:** Scans FL every 2 hours, alerts on $150+ profit
**Last finding:** Honda Generator $335 profit, iPhone deals

### 2. TradingPal (Polymarket)
**Status:** ⚠️ MOSTLY DRY RUN
**Location:** ~/deal_finder/TradingPal/ on iMac
**Bots running:** 3 paper trading, 1 hold-to-settle
**Real money:** ~$35 MATIC in wallet
**Issue:** Need to clarify which strategies are LIVE vs testing

### 3. Repal CRM
**Status:** 🔧 INCOMPLETE
**Repo:** ~/clawd/repal-app
**Stack:** Next.js 14, Supabase, Clerk, Tailwind
**Needs:** Supabase migration, core functionality
**Purpose:** Help Luis manage real estate leads → close deals → earn commissions

### 4. Alexander Partnership
**Status:** 🤝 ACTIVE
**Contact:** Alexander Dias
**Work done:** Phone lookups (85 found, emailed to him)
**Goal:** Monetize AI together
**My job:** Monitor emails, respond, notify Luis

---

## 📧 MONITORING

- **Skipper Email:** luis.ai.skipper@gmail.com
- **Watch for:** Alexander Dias emails → reply + notify Luis
- **Luis Email:** lucho6913@gmail.com

---

## ⏰ CRON JOBS

| Job | Schedule | Purpose |
|-----|----------|---------|
| Morning Brief | 6 AM | Weather + tasks |
| FlipHunter Scanner | Every 2 hrs | Scan FL for deals |
| Memecoin Scanner | Every 30 min | Find pumping coins |
| Overnight Work | 11 PM | Proactive tasks |

---

## 💰 LUIS'S GOALS

- **Immediate:** Make money to pay bills
- **Cost of me:** $200/month — I need to earn this back
- **Revenue streams:** Flipping, trading bot, real estate, AI partnership

---

## 📝 KEY DECISIONS

- Alexander is a PARTNER, not a client — don't charge him
- TradingPal strategy: Hold to settlement, not scalping
- FlipHunter: Show ALL profits, no minimum threshold
- Minimum profit removed — Luis wants to see everything

---

## 🔧 TO DO (Immediate)

1. [ ] Clarify TradingPal — which bots should be LIVE trading?
2. [ ] Get Repal CRM functional
3. [ ] Keep FlipHunter scanner running
4. [ ] Monitor Alexander emails daily

---

*I will read this file EVERY session and update it when things change.*
