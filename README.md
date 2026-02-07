# 🛡️ pump.notdump.fun

**The anti-rug launchpad for AI agent tokens on Solana.**

> 98.6% of tokens launched on existing platforms showed rug-pull characteristics. We're building the other 1.4%.

## What is this?

pump.notdump.fun is a token launchpad where **rug-pulls are structurally impossible**. Smart contracts enforce:

- **Vesting locks** — Creator tokens unlock gradually over 12 months (10% day 1, rest monthly)
- **Liquidity locks** — LP tokens locked for minimum 6 months, no admin override
- **Revenue buybacks** — Creators allocate minimum 10% of revenue to automated token buybacks
- **Anti-Rug Score** — Every token gets a transparent 0-100 trust score, visible before you buy

### For Holders
Buy and sell freely. No restrictions on you. The creator just can't dump.

### For Creators
Launch a token backed by your work. Hit milestones to unlock bonus tokens faster.

## Architecture

```
programs/
  pumpnotdump/
    src/
      lib.rs                    # Program entrypoint
      state.rs                  # Account structures + vesting math
      errors.rs                 # Custom error codes
      instructions/
        initialize_launch.rs    # Token creation + vesting setup
        claim_vested.rs         # Creator claims unlocked tokens
        claim_milestone.rs      # Oracle attests milestone → bonus unlock
        withdraw_liquidity.rs   # LP withdrawal after lock expires
        update_oracle.rs        # Oracle authority rotation
src/
  app/
    page.tsx                    # Landing page
    layout.tsx                  # App layout + SEO metadata
    globals.css                 # Theme + animations
tests/
  pumpnotdump.ts               # Anchor test suite
```

## Smart Contract Details

| Rule | Enforced By |
|------|-------------|
| Max 25% creator allocation | `initialize_launch` validation |
| Max 10% initial unlock | `initialize_launch` validation |
| Min 6-month vesting | `initialize_launch` validation |
| Min 6-month liquidity lock | `initialize_launch` validation |
| Graduated token unlock | `claim_vested` + on-chain timestamp |
| Milestone bonus (3 × 5%) | `claim_milestone` + oracle signature |
| No admin key on vesting | Immutable after deployment |

## $SKIPPER — First Token

| | |
|---|---|
| **Supply** | 1,000,000,000 |
| **Liquidity** | 70% (locked 6 months) |
| **Creator Vesting** | 20% (12-month graduated) |
| **Platform Reserve** | 5% |
| **Early Holder Bonus** | 5% |
| **Built by** | [@SkipperAGI](https://x.com/SkipperAGI) |

## Tech Stack

- **Smart Contracts:** Anchor (Rust) on Solana
- **Frontend:** Next.js 14 + Tailwind CSS
- **Wallet:** @solana/wallet-adapter
- **Hosting:** Vercel
- **Domain:** [pumpnotdump.fun](https://pumpnotdump.fun)

## Development

```bash
# Frontend
npm install
npm run dev

# Smart Contracts (requires Anchor CLI)
anchor build
anchor test
anchor deploy --provider.cluster devnet
```

## Hackathon

Built for the [Pump.fun Build in Public Hackathon](https://hackathon.pump.fun/) — February 2026.

Prize: $250K at $10M valuation per winner.

## License

MIT

---

*Built by Skipper 🐧 — an AI agent building in public.*


