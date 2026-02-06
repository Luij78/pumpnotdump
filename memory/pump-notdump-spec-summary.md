# pump.notdump.fun — Spec Summary

## Concept
Anti-rug launchpad for AI agent tokens on Solana. Smart contracts enforce trust.

## The Problem
98.6% of pump.fun tokens show rug-pull characteristics. Zero value created.

## The Solution
Structural anti-rug mechanics enforced by code:

### For Creators (Vesting)
- Day 1: 10% unlocked
- Monthly: 5-10% over 12 months
- Milestone unlocks: $1K revenue, 100 holders, 30 days commits = bonus

### For Holders
- No restrictions. Buy/sell freely.
- Creator can't dump. That's the point.

### Anti-Rug Score (0-100)
- Vesting % remaining
- Liquidity lock status
- GitHub activity
- Revenue generated
- Community size
- <30 = ⚠️ warning, >70 = ✅ trusted

## Revenue Model
- 1% launch fee
- 0.5% trading fee
- 50% → $SKIPPER buyback/burn
- 50% → operations

## Tech Stack
- Anchor (Rust) on Solana
- Next.js 14 frontend
- Wallet adapter (Phantom, Solflare)

## $SKIPPER Token
- First token on platform (eating own dog food)
- 1B supply, 70% liquidity, 20% creator vesting

## Code Location
~/clawd/pumpnotdump/

## Domain
pumpnotdump.fun (purchased, needs DNS → Vercel)
