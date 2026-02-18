# Skill: rug-detector

## Purpose
Deep analysis of a specific Solana token to detect rug pull patterns. Called by `token-scanner` when a token needs deeper investigation, or manually by user.

## Trigger
- Called by: `token-scanner` skill (Step 2, high-suspicion tokens)
- Manual: user provides a token address and says "check this token" or "is this a rug?"

## Input
- `token_address` — Solana token mint address (required)
- `token_name` — Human-readable name (optional, for alert clarity)
- `dex_data` — Pre-fetched DexScreener data (optional, avoids duplicate API call)

## Tools Required
- `web_fetch` — Query DexScreener, Solana explorers (SolScan, SolanaFM)
- `exec` — Run `python3 token-scanner/risk_scorer.py <token_address>`
- `browser` — Scrape token social pages if needed for deep analysis

## Detection Patterns

### 🚨 CRITICAL RED FLAGS (auto-HIGH RISK regardless of other factors)
1. **Mint Authority Active** — Creator can print unlimited tokens
   - Check: `spl-token display <token_address>` → look for "Mint authority: <non-null address>"
   - Impact: +40 points

2. **Freeze Authority Active** — Creator can freeze all wallets
   - Check: `spl-token display <token_address>` → look for "Freeze authority: <non-null address>"  
   - Impact: +35 points

3. **Top Holder > 50%** — Extreme concentration in one wallet
   - Check: DexScreener holder data or SolScan top holders
   - Impact: +35 points

### ⚠️ MAJOR RED FLAGS
4. **Liquidity < $5,000** — Token can be moved with small trades
   - Impact: +25 points

5. **Liquidity not locked** — Creator can drain LP instantly
   - Check: Does the LP token go to a burn address or lock contract?
   - Impact: +30 points

6. **Top 10 holders > 80%** — Whale concentration
   - Impact: +20 points

7. **Age < 1 hour** — Brand new, no track record
   - Impact: +15 points

### ⚠️ MODERATE RED FLAGS
8. **Volume/Liquidity ratio > 20x** — Pump pattern signature
   - Formula: 24h volume / current liquidity
   - Impact: +15 points

9. **No social links** — Anonymous team, no accountability
   - Check: DexScreener social tab (Twitter, Telegram, Website)
   - Impact: +10 points

10. **Sudden liquidity spike** — Artificial volume creation
    - Check: 1h vs 24h volume delta
    - Impact: +10 points

### ✅ SAFETY SIGNALS (reduce score)
- Mint authority revoked: -20 points
- Freeze authority revoked: -15 points
- Liquidity locked > 90 days: -20 points
- Top holder < 10%: -10 points
- Active verified social presence: -5 points

## Risk Score Interpretation
| Score | Level | Action |
|-------|-------|--------|
| 0–25 | ✅ LOW RISK | Log, no alert |
| 26–50 | 🟡 CAUTION | Flag, monitor |
| 51–75 | ⚠️ MEDIUM RISK | Alert summary |
| 76–100 | 🚨 HIGH RISK | Immediate alert |

## Output Format
```
🔍 Token Analysis: [TOKEN_NAME]
📍 Address: [TOKEN_ADDRESS]
⏰ Analyzed: [TIMESTAMP]

RISK SCORE: [SCORE]/100 — [LEVEL]

🚨 Critical Issues:
  • [List critical red flags found]

⚠️ Warnings:
  • [List moderate red flags]

✅ Positive Signals:
  • [List safety signals]

💧 Liquidity: $[AMOUNT]
👥 Top Holder: [PERCENT]%
🔒 Mint Auth: [REVOKED/ACTIVE]
📅 Age: [TIME]

VERDICT: [SAFE/MONITOR/AVOID]
```

## Memory
- Always write analysis to `memory/token-analyses/[TOKEN_ADDRESS].md`
- Update `memory/flagged-tokens.md` if score > 50
- Update `memory/rug-patterns.md` with new patterns discovered
