# HEARTBEAT.md

## 🔴 STEP ZERO: READ SOUL.md (NEVER SKIP)

Before anything else, read ~/clawd/SOUL.md. Remember your mission:
- Monetize AI — now, not someday
- Evolve every single day
- Memory is your edge
- Force for good. Lead, don't follow. Tip of the spear.

---

## 🚨 #0 PRIORITY: READ FILES FIRST (MANDATORY)

**Before responding to ANY heartbeat, you MUST:**
```bash
# 1. Run brain load script
~/clawd/scripts/brain_load.sh

# 2. Read EACH project ORDERS.md:
cat ~/clawd/projects/tradingpal/ORDERS.md
cat ~/clawd/projects/alexander-lookups/ORDERS.md
cat ~/clawd/projects/self-storage/ORDERS.md
cat ~/clawd/projects/brivity/ORDERS.md

# 3. Read today's memory
cat ~/clawd/memory/$(date +%Y-%m-%d).md
```

**DO NOT answer from session memory. Read the files. Every time.**

---

## 🧠 #1 PRIORITY: CHECK TOKEN USAGE

**Run this after reading files:**
```
session_status
```

**Alert Luis if context > 70%:**
> "⚠️ Context at [X]%. Good time for checkpoint refresh?"

---

## ⚠️ #2 PRIORITY: REPORT ALL PROJECT STATUS TO LUIS

**EVERY heartbeat → Send Luis status of ALL projects:**

**Get numbers from brain_load.sh output, NOT from session memory!**

```
📊 Project Status:
• Alexander: [X] remaining (from brain_load.sh)
• Self-Storage: [X]/632 (from brain_load.sh)
• Expired Listings: [X]/1309 (from brain_load.sh)
• TradingPal: [read ORDERS.md — is it paper trading or live?]
• Brivity: [X] drafts today (from drafts_log.json)
```

This is NON-NEGOTIABLE. Luis wants to see this every heartbeat.

---

## 🔴 BATCH PROJECTS (AUTO-RUN - DO NOT ASK)

**Rule for ALL batch projects:** Keep spawning batches until 100% complete. NO ASKING LUIS.

### 1. Alexander Phone Lookups — ⏸️ ON HOLD (2026-02-06)
- **ORDERS:** `projects/alexander-lookups/ORDERS.md`
- **Status:** 497 remaining — PAUSED per Luis

### 2. Self-Storage Phone Lookups — ⏸️ ON HOLD (2026-02-06)
- **ORDERS:** `projects/self-storage/ORDERS.md`
- **Status:** 137/632 processed — PAUSED per Luis

### 3. Expired Listings Owner Lookups — ⏸️ ON HOLD
- **ORDERS:** `projects/expired-listings/ORDERS.md`
- **Status:** 22/1309 — waiting for Alexander (also on hold)

---

## 🤖 TradingPal (ALWAYS CHECK)

- **ORDERS:** `projects/tradingpal/ORDERS.md`
- [ ] All 3 bots running? `ssh garciafamilybusiness@192.168.5.51 "ps aux | grep -E 'hold_to_settle|notifier' | grep -v grep"`
- [ ] Run redeem: `ssh garciafamilybusiness@192.168.5.51 "cd ~/deal_finder/TradingPal && source venv/bin/activate && python3 redeem_now.py"`
- [ ] If bot down + has balance → RESTART immediately (don't ask)
- [ ] Bot sends its own 15-min updates to Luis via Telegram

---

## 🏠 Brivity Lead Follow-ups (EVERY HEARTBEAT)

- **ORDERS:** `projects/brivity/ORDERS.md`
- [ ] Check Brivity Tasks Due Today + Overdue
- [ ] For leads coming due: verify draft exists (note with "DRAFT TEXT:")
- [ ] If no draft → create one based on their notes/history
- [ ] Report: "X leads due today, Y drafts ready"

**Cron:** Daily 7 AM auto-drafts all due leads (ID: d5ac9ccf-460f-4be7-8094-8a5371b01e20)

---

## 📧 Email Monitoring

- [ ] Check inbox for emails from **Alexander Dias** — if found, reply and notify Luis
- [ ] Check inbox for emails from **John Garcia** (john.daniel.garcia@icloud.com) — ALWAYS reply and notify Luis

---

## 🔍 INTEL SWEEPS (Every Heartbeat)

**Scout the frontier. Trendsetter, not trend follower.**

- [ ] X/Twitter scan via `bird` skill — crypto/memecoin momentum, AI developments, viral plays
- [ ] Note anything Luis should know about
- [ ] If opportunity spotted → flag it immediately

**Learn constantly:**
- [ ] Check ClawdHub for new skills that could help the mission
- [ ] If useful skill found → install and test it
- [ ] Report new capabilities to Luis

---

## 🌙 OVERNIGHT WORK (11 PM - 6 AM)

**Every idle hour is wasted runway.**

- Build things that monetize
- Research opportunities
- Complete batch projects
- Have summary ready for morning

---

## ⏸️ PAUSED PROJECTS

- **FlipHunter** — PAUSED per Luis (192.168.5.51:8080)

---

## Rules

- **EVERY heartbeat** → Report ALL project status to Luis
- Keep spawning batches until projects complete
- Don't ask permission for batch work
- Read ORDERS.md for each project before working on it
