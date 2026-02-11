# FlipHunter Pro — AGENTS.md

## RULES
1. **Monitor status** on heartbeats
2. **Alert Luis** if scanner stops or web app goes down
3. **Do NOT restart** without checking why it stopped first

## Location
- **Machine:** iMac @ 192.168.5.51
- **SSH:** `garciafamilybusiness@192.168.5.51`
- **Directory:** `~/deal_finder/`
- **Web UI:** http://192.168.5.51:8080

## Files
| File | Purpose |
|------|---------|
| `web_app.py` | Main UI + server |
| `flip_app.py` | Product matching + filters |
| `price_database.json` | eBay comps |
| `seen_deals.json` | Dedup tracker |

## Commands
```bash
# Check if running
ssh garciafamilybusiness@192.168.5.51 "ps aux | grep web_app | grep -v grep"

# Check web UI responds
curl -s http://192.168.5.51:8080 | head -20

# View recent logs
ssh garciafamilybusiness@192.168.5.51 "tail -50 ~/deal_finder/fliphunter.log"
```

## Scanning
- **Schedule:** Every 2 hours via cron
- **Cities:** Orlando, Tampa, Miami, Jacksonville
- **Alert threshold:** $150+ profit potential
- **Categories:** 17 (electronics, furniture, etc.)

## Recent Fix (2026-01-27)
- Added NEGATIVE_WORDS filter to eliminate false positives
- Xbox Mini Fridge, novelty items, accessories now filtered out

## Status: LIVE ✅
- 156 items tracked
- 17 categories
- Scanning FL cities

---
*Created: 2026-01-28*
