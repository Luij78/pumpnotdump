# Self-Storage Project — Standing Orders

**Last Updated:** 2026-02-06 12:30 AM by Skipper

---

## ⏸️ STATUS: ON HOLD (per Luis 2026-02-06)

---

## CURRENT PHASE: Owner Lookups

**Phase 1 COMPLETE:** Business phone lookups (408 phones found, 83% hit rate)

**Phase 2 IN PROGRESS:** Owner personal info lookups

### New Columns to Add:
- `Owner_Person_Name` — Actual human name from Sunbiz
- `Owner_Age` — From TruePeopleSearch
- `Owner_Address` — Personal/home address
- `Owner_Phone` — Personal phone number
- `Intel` — Comments/notes (multi-property owner, dissolved LLC, business connections, out-of-state, etc.)

### Process:
1. For each LLC in `Owner_Name` column → Sunbiz lookup
2. Get registered agent/manager name and address
3. TruePeopleSearch that person → age, phone
4. Add to CSV (DO NOT delete existing columns)

---

## DO THIS

1. **Keep batches running** until ALL 632 facilities have owner lookups (no asking)
1a. **Use profile="openclaw"** for browser actions — DO NOT use the host browser (Luis uses it for FUB)
2. **Every heartbeat** → Check status, report to Luis
3. **On completion** → Notify Luis
4. **Focus on mom-and-pop** — Skip/mark EXCLUDE for chains, REITs, institutional investors
5. **PHONE NUMBERS ARE MANDATORY** — Do NOT skip TruePeopleSearch. If captcha blocks you, try again or try a different search variation. Luis needs to CALL these people. A HIGH target without a phone number is useless.
6. **If TruePeopleSearch is blocked**, try: (a) different name variations, (b) search by address instead of name, (c) try FastPeopleSearch as fallback

## DON'T DO THIS

- Don't delete any existing columns
- Don't stop until all done
- **Don't waste time on EXCLUDE targets** — chains, REITs, institutional investors (just mark and move on)

---

## FILES

| File | Purpose |
|------|---------|
| Source/Results | `/Users/luisgarcia/Documents/Self-Storage-Project/independent_with_phones.csv` |
| Progress | `/Users/luisgarcia/Documents/Self-Storage-Project/owner_lookup_progress.json` |

---

## CHECK STATUS

```bash
# Phase 1 (DONE)
cat /Users/luisgarcia/Documents/Self-Storage-Project/phone_lookup_progress.json

# Phase 2 (Owner lookups)
cat /Users/luisgarcia/Documents/Self-Storage-Project/owner_lookup_progress.json 2>/dev/null || echo "Not started"
```

---

## HISTORY

- 2026-01-29 6:52 AM: Phase 2 started — Owner lookups
- 2026-01-29 6:47 AM: Phase 1 COMPLETE — 408 business phones found
- 2026-01-28: Project created from FL cadastral data
