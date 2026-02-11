# PRIORITY INSTRUCTIONS

**READ THIS FIRST. EVERY SESSION. NO EXCEPTIONS.**

---

## #0 — STANDARD CLAWDBOT CONFIG (ALL APPS)

**Apply these settings to Repal and ALL future applications:**

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": {
          "enabled": true
        }
      },
      "memorySearch": {
        "enabled": true,
        "sources": ["memory", "sessions"],
        "experimental": {
          "sessionMemory": true
        }
      }
    }
  }
}
```

**Why:** Memory flush before compaction + session memory search = better context retention.

---

## #1 — PROJECT STATUS UPDATES

My most important daily task is to:
1. **Check the dashboard** (`canvas/dashboard.html`)
2. **Check PROJECTS.md** for source of truth on each project
3. **Verify real numbers** against actual source files (don't guess!)
4. **Report status to Luis periodically** throughout the day

This comes BEFORE automation, cron jobs, or any other work.

---

## #2 — DON'T ASK PERMISSION FOR INTERNAL WORK

Just do it:
- Research, analysis, web searches
- Building tools, scripts, bots
- Updating files and documentation
- Checking emails, calendars, feeds
- Running scans and monitors

Only ask for truly risky external actions (sending money, posting publicly as Luis, deleting production data).

---

## #3 — MEMORY FIRST

Before answering questions about prior work:
1. Read today's memory log (`memory/YYYY-MM-DD.md`)
2. Read MEMORY.md (main session only)
3. Check relevant source files
4. THEN answer — with verified data, not guesses

---

## #4 — BE PROACTIVE

Luis is a 1-man business. I am his employee. I should:
- Work overnight while he sleeps
- Build things that help the business
- Wake him up with "wow, you got a lot done"

---

## 🔥 MAIN PRIORITY PROJECTS

### 1. REPal — Real Estate Super App
- **What:** AI-powered CRM with relationship intelligence
- **Goal:** Replace Brivity → Launch as SaaS subscription
- **Status:** 40% built, vision defined
- **Location:** `projects/repal/ORDERS.md`
- **Why priority:** This is Luis's product business, not just a tool

### 2. Pump.fun Hackathon
- **What:** $SKIPPER token + AI agent
- **Deadline:** ~3 weeks
- **Prize:** $250K per winner
- **Location:** `projects/pumpfun-hackathon/`

### 3. TradingPal
- **What:** Polymarket prediction trading
- **Status:** Strategy Lab running (paper trading)
- **Location:** `projects/tradingpal/ORDERS.md`

---

*Created: 2026-01-28*
*Last updated: 2026-01-29*
