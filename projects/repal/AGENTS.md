# Repal CRM — AGENTS.md

## RULES
1. **Goal:** Get CRM working for Luis's real estate business
2. **Stack:** Next.js 14, Supabase, Clerk, Tailwind
3. **Don't deploy** without Luis testing locally first

## Repository
- **GitHub:** https://github.com/Luij78/repal-app
- **Local:** ~/clawd/repal-app

## Commands
```bash
# Navigate to project
cd ~/clawd/repal-app

# Install deps
pnpm install

# Run dev server
pnpm dev

# Run migrations
# (Need Supabase connection first)
```

## Pending Migration
- **File:** `001_add_lead_fields.sql`
- **Purpose:** Add lead tracking fields
- **Status:** Ready, needs Supabase setup

## TODO
- [ ] Run Supabase migration
- [ ] Test lead entry flow
- [ ] Connect to Luis's workflow
- [ ] Deploy to Vercel

## Status: 40% — UI done, needs backend work

---
*Created: 2026-01-28*
