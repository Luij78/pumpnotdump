# Alexander Phone Lookups — Standing Orders

**Last Updated:** 2026-02-06 12:30 AM by Skipper

---

## ⏸️ STATUS: ON HOLD (per Luis 2026-02-06)

---

## DO THIS

1. **Keep batches running** until ALL ~2,300 owners done (no asking)
1a. **Use profile="clawd"** for browser actions — DO NOT use the host browser (Luis uses it for FUB)
2. **Cross-check** phone_results_browser.csv before each lookup (no duplicates)
3. **For individuals** → TruePeopleSearch directly
4. **For LLCs/Corps/Trusts** → Sunbiz first, get person name, then TruePeopleSearch
5. **Every heartbeat** → Check project status, report to Luis
6. **On final completion** → Final email to Alexander (CC Luis)

## SUB-AGENT EFFICIENCY (Added 2026-01-29)

- **Batch size: 5 lookups per sub-agent** (smaller = no aborts)
- **Longer timeouts** — let sub-agents wait out rate limits
- **Sequential spawning** — one at a time, no overlap

## EMAIL NOTIFICATIONS (Updated 2026-01-29)

Send email to Alexander (CC Luis) ONLY:
- **Every 50 successful lookups** (not after every batch)
- **On final completion**
- **If Luis requests it**

NO emails after small batches — reduces noise, saves time.

## DON'T DO THIS

- Don't do double work — always check if owner already in results
- Don't stop until all ~2,300 owners processed
- Don't skip LLCs — look them up on Sunbiz first
- Don't forget to notify after batches

---

## LOOKUP METHODS

**Individuals:** TruePeopleSearch directly

**LLCs/Corps/Trusts:**
1. Go to https://dos.fl.gov/sunbiz/search/
2. Search by entity name
3. Get registered agent or officer name
4. Look up that person on TruePeopleSearch

---

## SCOPE

| Metric | Value |
|--------|-------|
| Total Owners | ~2,300 (from 2,328 properties) |
| Source | Central_FL_4Unit_Properties.csv |

---

## CHECK STATUS

```bash
# Done count (subtract 1 for header)
wc -l "/Users/luisgarcia/Documents/FL Geographic/phone_results_browser.csv"

# Remaining count
cat "/Users/luisgarcia/Documents/FL Geographic/remaining_owners.json" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))"
```

---

## FILES

| File | Purpose |
|------|---------|
| Source | `/Users/luisgarcia/Documents/FL Geographic/Central_FL_4Unit_Properties.csv` |
| Results | `/Users/luisgarcia/Documents/FL Geographic/phone_results_browser.csv` |
| Queue | `/Users/luisgarcia/Documents/FL Geographic/remaining_owners.json` |

---

## AFTER EACH BATCH

**Email:**
- To: alexanderdrealestater@gmail.com
- CC: lucho6913@gmail.com
- Subject: Phone Lookup Update - [X] of ~2,300 Complete ([Y]%)
- Attach: phone_results_browser.csv

**Telegram:** Notify Luis with progress

---

## CLIENT

**Alexander Dias**
- Email: alexanderdrealestater@gmail.com
- Project: FL multi-family (4-unit) property owner phone lookups
- Started: 2026-01-26

---

## HISTORY

- 2026-01-29: Efficiency update — 5 lookups/batch, emails every 50 only
- 2026-01-28: Added Sunbiz lookup for LLCs/Corps/Trusts
- 2026-01-28: Corrected scope to ~2,300 owners (was incorrectly 937)
- 2026-01-28: Added batch notification rule (email + Telegram)
- 2026-01-27: Browser automation working
- 2026-01-26: Project started, first 25 owners emailed
