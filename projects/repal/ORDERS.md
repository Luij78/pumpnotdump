# REPal (Real Estate Pal) — ORDERS.md

## 🚨 PRIORITY: MAIN PROJECT

## 🎯 VISION
An AI-powered relationship intelligence platform for real estate agents. Not just a CRM — a **Super App** that watches, learns, and surfaces opportunities before you even know to look.

**Tagline:** "Your unfair advantage in real estate."

**Business Model:** SaaS subscription via App Store
**Goal:** Replace Brivity → Launch publicly → Recurring revenue

---

## 📍 CURRENT SITUATION

- **Now:** Using Brivity (partner pays)
- **Building:** REPal as personal CRM replacement
- **Future:** Offer REPal as subscription product for other agents
- **Exit:** Move off Brivity entirely when REPal is ready

**Why this matters:** Luis uses Brivity daily = built-in product research. Every pain point, every workaround, every "I wish it did X" = REPal feature spec.

---

## 🧠 CORE CONCEPT: Relationship Intelligence

Traditional CRM: Stores contacts, reminds you to follow up.
REPal: Tracks everything, finds connections, surfaces value opportunities.

**The Rebecca Example:**
- She viewed a property months ago
- That property just dropped $23K
- REPal catches it → drafts a text → you look like a hero
- She thinks you've been watching the market just for her. You have.

---

## 🔥 FEATURE SET

### Phase 1: Smart Follow-Ups (NOW)
- [ ] Track lead preferences (price, beds, areas, property types)
- [ ] Monitor MLS for matches → auto-alert
- [ ] Price drop detection on viewed/saved properties
- [ ] Draft personalized follow-up texts/emails with actual listings
- [ ] "Days since contact" intelligence

### Phase 2: Relationship Graph
- [ ] Build connection map between all contacts
- [ ] Surface hidden relationships ("John's sister-in-law knows your past client")
- [ ] Track interactions across channels (text, email, call, social)
- [ ] Identify warm intro opportunities

### Phase 3: Market Intelligence
- [ ] Monitor competitor agents (new listings, price changes)
- [ ] Underpriced listing alerts (Zillow estimate vs actual)
- [ ] Pocket listing hunter (wholesaler groups, auctions, estate sales)
- [ ] Pre-call dossiers (LinkedIn, socials, property records)

### Phase 4: Automation Layer
- [ ] AI receptionist (qualify leads, book appointments)
- [ ] Voice clone for initial outreach (disclosed as AI)
- [ ] Auto-apply for awards, speaking gigs, bonuses
- [ ] Content army (trend monitoring, draft posts)

### Phase 5: Prediction Engine
- [ ] Analyze past deals → identify winning patterns
- [ ] Best times to call by lead type
- [ ] Lead scoring based on historical conversion
- [ ] "Who to call today" daily briefing

---

## 🏗️ TECHNICAL STACK

**Existing (repal-crm):**
- Next.js 14 + App Router
- Supabase (Postgres + Auth)
- Clerk (if keeping)
- Tailwind CSS
- GitHub: https://github.com/Luij78/repal-app
- Local: ~/clawd/repal-app

**To Add:**
- MLS API integration (or scraping fallback)
- OpenAI/Claude for draft generation
- ElevenLabs for voice features
- Social media APIs (LinkedIn, Facebook, X)
- Property data APIs (Zillow, Redfin, PropStream)

---

## 📊 CURRENT STATE

**What exists:**
- Basic UI built (40%)
- Lead entry flow started
- Supabase schema ready for migration

**What we're doing NOW (manual):**
- Working through Brivity overdue tasks
- Drafting personalized follow-ups with real listings
- Building the "muscle memory" for what REPal should automate

**Gap:** The manual work we're doing IS the product spec. Every draft we write teaches us what REPal should do automatically.

---

## 🚀 NEXT STEPS

1. **Document the patterns** — Every good follow-up becomes a template
2. **Run Supabase migration** — Get the backend working
3. **Build lead import** — Pull from Brivity export
4. **Add preference tracking** — What each lead wants
5. **MLS monitoring** — Price drops, new listings matching preferences
6. **Auto-draft engine** — Generate follow-ups like we do manually

---

## 💡 THE INSIGHT

The manual CRM work we're doing right now isn't busywork — it's PRODUCT RESEARCH.

Every Rebecca-style follow-up teaches us:
- What data to track
- What triggers matter
- How to personalize at scale

Build the system that does what we're doing manually, but for 500 leads at once.

---

## 🎖️ VETERAN ANGLE

Luis is a Navy vet. REPal can lean into:
- VA loan expertise positioning
- Military relocation specialization  
- Veteran homebuyer targeting
- "Navy vet helping fellow veterans find home" brand

---

## 💰 BUSINESS MODEL

**Pricing Tiers (Draft):**
- **Solo Agent:** $49/mo — Core CRM + AI follow-ups
- **Team:** $99/mo — Multi-user + shared leads
- **Brokerage:** $299/mo — White-label + analytics

**Competitive Edge:**
- Brivity, Follow Up Boss, LionDesk = dumb CRMs (store data, send reminders)
- REPal = intelligent CRM (watches market, finds opportunities, drafts value)
- First real estate CRM with **relationship intelligence** built-in

**App Store Strategy:**
- iOS + Android apps (React Native or Flutter)
- Web dashboard for full features
- Mobile-first for agents on the go

---

## 🛣️ ROADMAP

**Phase 1 — Personal Use (NOW → 2 months)**
- Build what Luis needs daily
- Replace Brivity functions one by one
- Document every pain point

**Phase 2 — Beta (2-4 months)**
- Invite 5-10 agent friends to test
- Iterate on feedback
- Polish core workflows

**Phase 3 — Launch (4-6 months)**
- App Store submission
- Landing page + waitlist
- Content marketing (Luis as the face)

**Phase 4 — Scale**
- Paid ads to real estate agents
- Affiliate program (agents refer agents)
- Brokerage partnerships

---

## 📝 BRIVITY PAIN POINTS (Capture these!)

*Every frustration with Brivity = REPal feature opportunity*

- [ ] (Add pain points as Luis encounters them)

---

## 🧠 CRM RULES (Learned from Brivity Work)

*These rules apply to drafting follow-ups. REPal should enforce/automate these.*

### 1. VERIFY BEFORE CLAIMING
Never say "I have properties" or "there are options" without:
- Actually searching and finding listings first
- Having specific addresses and prices ready
- Being able to send links immediately

**REPal should:** Auto-search MLS before drafting, only suggest if matches exist.

### 2. INCLUDE SPECIFIC ADDRESSES
Every property mention needs:
- Full street address
- Price
- Bed/bath count

**REPal should:** Auto-populate property details in draft templates.

### 3. USE COMMAS, NOT DASHES
In text/email drafts: use "," instead of "—"

**REPal should:** Enforce formatting rules in draft generation.

### 4. VALUE-DRIVEN FOLLOW-UPS
Don't "check in" — deliver value:
- Price drops on viewed properties
- New listings matching saved criteria
- Relevant market intel

**REPal should:** Track what each lead viewed, alert on price drops, auto-draft with value hooks.

### 5. MATCH LANGUAGE PREFERENCE
If lead speaks Spanish → draft in Spanish

**REPal should:** Store language preference, generate drafts in correct language.

### 6. NEVER ASSUME STR/RENTAL STATUS
Don't claim a property is "STR-friendly" or "vacation rental zone" unless:
- Listing description explicitly states it
- HOA docs confirm short-term rentals allowed
- Zoning is verified

**Why:** If buyer purchases based on STR claim and it's wrong = legal liability.

**REPal should:** Flag STR status as "Verified" or "Unverified", pull from listing description or HOA data.

---

*Created: 2026-01-29*
*Status: MAIN PRIORITY — Vision defined, building*
