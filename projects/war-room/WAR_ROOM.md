# 🕵️ Competitive Intelligence War Room

**Created:** 2026-01-29
**Territory:** Clermont, Winter Garden, Central Florida
**MLS:** Stellar MLS (Luis has access)

---

## 🎯 WATCH LIST

### Content Creators to Study

| Name | Platform | Handle | Notes |
|------|----------|--------|-------|
| **Ken Pozek** | YouTube/TikTok | @kenpozek | Winter Garden-based, 2000+ deals, "The Orlando Real", huge YouTube presence, does $30M+ luxury tours |
| **Tu Realtor** | Instagram | @turealtorenflorida | Verified since May 2023, joined April 2020, consistent content |

### Ken Pozek Intel
- **Team:** Pozek Group / The Orlando Real
- **Brokerage:** Real Broker, LLC (BK3313335)
- **Office:** 270 Plant Street Suite 230, Winter Garden, FL
- **Website:** theorlandoreal.com
- **Strategy:** YouTube content marketing, property tours, luxury market focus
- **Note:** He's in YOUR backyard (Winter Garden). Study his content playbook.

---

## 📍 TERRITORY

**Primary:** Clermont, FL
**Secondary:** Winter Garden, FL
**Region:** Central Florida / Greater Orlando

### Clermont Zip Codes:
- 34711 (Clermont proper)
- 34714 (Clermont/Four Corners)
- 34715 (Clermont)

### Winter Garden Zip Codes:
- 34787 (Winter Garden / Horizon West)
- 34786 (Windermere area)

---

## 🚨 ALERT TRIGGERS (Dream Alerts)

### 1. Underpriced Deals
- Property listed >10% below Zillow Zestimate
- Recent price drop >5%
- Days on market >45 (motivated seller)
- Estate sales, foreclosures, REO

### 2. Lead-Property Matching
- New listing matches a lead's saved search criteria
- Price drop on property a lead previously viewed
- New listing in neighborhood where lead showed interest

### 3. FSBO Opportunities
- All FSBOs in Clermont/Winter Garden
- Especially those >30 days on market (getting desperate)
- Price drops on FSBOs (really desperate)

---

## 📋 FSBO HUNTING STRATEGY

### Sources to Scrape:
1. **Zillow** - FSBO filter
2. **Realtor.com** - FSBO listings
3. **Craigslist** - Real estate by owner
4. **Facebook Marketplace** - Homes for sale
5. **ForSaleByOwner.com**
6. **Fizber.com**
7. **FSBO.com**
8. **HomeFinder.com**

### Data to Capture:
- Address
- Price
- Beds/Baths/Sqft
- Days on market
- Owner name (from property records)
- Phone number (via lookup)
- Photos
- Listing URL

### Output:
Daily CSV: `fsbo_central_florida_YYYY-MM-DD.csv`

---

## 🔄 DAILY WAR ROOM ROUTINE

**6:30 AM - Morning Intel Brief**

1. **New Listings** in Clermont/Winter Garden
   - Any underpriced vs Zestimate?
   - Any matching lead criteria?

2. **Price Changes**
   - Drops >$10k
   - Properties sitting >30 DOM

3. **FSBO Update**
   - New FSBOs in territory
   - FSBO price drops

4. **Competitor Watch**
   - Ken Pozek new videos?
   - Tu Realtor new posts?
   - What are they promoting?

5. **Market Snapshot**
   - Active listings count
   - Median price trend
   - Days on market average

---

## 🛠️ IMPLEMENTATION PLAN

### Phase 1: FSBO Scraper (This Week)
- [ ] Build scraper for Zillow FSBOs
- [ ] Build scraper for Craigslist
- [ ] Cross-reference with property records for owner info
- [ ] Phone lookup integration
- [ ] Daily cron job

### Phase 2: MLS Integration (Next Week)
- [ ] Figure out Stellar MLS API or export
- [ ] Build listing tracker
- [ ] Price change alerts
- [ ] DOM monitoring

### Phase 3: Lead Matching (Week 3)
- [ ] Export Brivity lead preferences
- [ ] Build matching algorithm
- [ ] Auto-alert when match found

### Phase 4: Competitor Monitoring (Ongoing)
- [ ] YouTube RSS for Ken Pozek
- [ ] Instagram scraper for Tu Realtor
- [ ] Weekly competitor digest

---

## 📊 SUCCESS METRICS

- FSBOs contacted per week
- Listing appointments from FSBO outreach
- Underpriced deals identified
- Lead-property matches made
- Time saved vs manual searching

---

*The War Room is being built. Intel flows in. Opportunities don't slip by.*
