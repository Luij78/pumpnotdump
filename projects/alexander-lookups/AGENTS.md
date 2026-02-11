# Alexander Phone Lookups — AGENTS.md

## RULES (NON-NEGOTIABLE)
1. **AUTO-RUN** batches until remaining_owners.json = 0
2. **DO NOT ASK** Luis for permission — just run
3. **USE BROWSER AUTOMATION** (Playwright via browser tool) — NOT curl
4. **When complete:** Email results to Alexander, CC Luis

## Client Info
- **Name:** Alexander Dias
- **Email:** alexanderdrealestater@gmail.com
- **CC:** lucho6913@gmail.com

## Files (VERIFIED)
| File | Path |
|------|------|
| Remaining Owners | `/Users/luisgarcia/Documents/FL Geographic/remaining_owners.json` |
| Results CSV | `/Users/luisgarcia/Documents/FL Geographic/phone_results_browser.csv` |
| Lookup Scripts | `/Users/luisgarcia/Documents/FL Geographic/` |

## Commands
```bash
# Check remaining count
cat "/Users/luisgarcia/Documents/FL Geographic/remaining_owners.json" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))"

# Check results count (subtract 1 for header)
wc -l "/Users/luisgarcia/Documents/FL Geographic/phone_results_browser.csv"
```

## Lookup Method
- **Site:** FastPeopleSearch (https://www.fastpeoplesearch.com)
- **URL Format:** `/name/{first}-{last}_{city}-fl`
- **MUST use browser tool** to bypass Cloudflare
- **Delay:** 5-10 seconds between lookups

## On Completion
1. Email Alexander with results attached
2. CC Luis at lucho6913@gmail.com
3. Update PROJECTS.md status to COMPLETE

---
*Created: 2026-01-28*
