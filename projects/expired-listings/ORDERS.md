# Expired Listings — Standing Orders

**Last Updated:** 2026-01-28 9:35 PM by Skipper + Luis

---

## DO THIS

1. **Keep owner lookup batches running** until all 1,309 done (no asking)
1a. **Use profile="clawd"** for browser actions — DO NOT use the host browser (Luis uses it for FUB)
2. **Check MLS status first** — skip if property is back on market
3. **Look up owners** on Property Appraiser sites by county
4. **After each batch** → Email Luis + Alexander
5. **Every heartbeat** → Check status, report to Luis
6. **Phone lookups WAIT** until Alexander project is complete
7. **On completion** → Notify Luis

## DON'T DO THIS

- Don't do phone lookups yet — wait for Alexander to finish
- Don't look up properties that are back on market
- Don't stop until all 1,309 owners found

---

## LOOKUP METHODS

**Step 1: Check if still expired**
- Search address on Zillow/Realtor.com
- If "For Sale" or "Active" → SKIP
- If "Off market" → Proceed

**Step 2: Owner lookup by county**
- **O-prefix MLS#** → Orange County PA: https://ocpaweb.ocpafl.org/parcelsearch
- **G-prefix MLS#** → Lake County PA: https://lakecopropappr.com/property-search.aspx

**Step 3 (AFTER Alexander done): Phone lookup**
- Use TruePeopleSearch for owner names
- For LLCs → Sunbiz first, then TruePeopleSearch

---

## SCOPE

| Metric | Value |
|--------|-------|
| Total | 1,309 properties |
| Counties | Orange (O-prefix) and Lake (G-prefix) |
| Price Range | $300K+ |
| Status | Expired MLS listings |

---

## CHECK STATUS

```bash
python3 -c "import csv; f=open('/Users/luisgarcia/Documents/Expired-Listings/expired_listings_with_owners.csv'); r=csv.DictReader(f); rows=list(r); done=len([x for x in rows if x.get('Owner_Name','').strip()]); print(f'Done: {done}/1309, Remaining: {1309-done}')"
```

---

## FILES

| File | Purpose |
|------|---------|
| Results | `/Users/luisgarcia/Documents/Expired-Listings/expired_listings_with_owners.csv` |
| Source PDF | `/Users/luisgarcia/.clawdbot/media/inbound/61395846-2334-4beb-81b9-ff8d44df5fdb.pdf` |

---

## AFTER EACH BATCH

**Email:**
- To: lucho6913@gmail.com, alexanderdrealestater@gmail.com
- Subject: Expired Listings Update - [X] of 1,309 Owners Found
- Attach: expired_listings_with_owners.csv

**Telegram:** Notify Luis with progress

---

## CSV COLUMNS

`MLS_ID, Address, Beds, Baths, SqFt, Market_Date, ADOM, Orig_Price, List_Price, Owner_Name, Mailing_Address, Phone, Notes`

---

## HISTORY

- 2026-01-28: Created ORDERS.md, moved to Documents/Expired-Listings/
- 2026-01-28: 20 done, 1,289 remaining
- 2026-01-28: Project started from expired MLS PDF
