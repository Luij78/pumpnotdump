# Skill: token-scanner

## Purpose
Scan new Solana token launches via DexScreener API and analyze them for rug pull risk factors. Runs autonomously every 5 minutes.

## Trigger
- Cron: every 5 minutes (`*/5 * * * *`)
- Manual: user says "scan tokens" or "check new launches"
- Event: new token launch detected on Solana

## Tools Required
- `web_fetch` — Call DexScreener API for new token data
- `exec` — Run `python3 token-scanner/scanner.py` for detailed analysis
- `message` — Send alerts to Telegram when high-risk tokens found

## Steps

### Step 1: Fetch New Tokens
```
GET https://api.dexscreener.com/latest/dex/tokens/solana
```
Filter for tokens created in the last 10 minutes.

### Step 2: Score Each Token
Run `risk_scorer.py` on each token. Look for:
- Liquidity < $10K → RISKY (score += 25)
- Token age < 24h → CAUTION (score += 15)
- Volume/Liquidity ratio > 10x → SUSPICIOUS (score += 20)
- Mint authority NOT revoked → RISKY (score += 30)
- Top holder > 20% → RISKY (score += 20)

### Step 3: Classify
- Score 0–30: ✅ LOW RISK — mention in summary
- Score 31–60: ⚠️ MEDIUM RISK — flag for monitoring
- Score 61–100: 🚨 HIGH RISK — send immediate alert

### Step 4: Send Alerts
For HIGH RISK tokens, call `alert-sender` skill immediately.
For MEDIUM RISK tokens, log and include in next summary report.

### Step 5: Update Memory
Append scan results to agent memory:
```
memory/scan-log.md
memory/flagged-tokens.md
```

## Output Format
```
🤖 pump.notdump Agent Scan #[N]
⏰ [timestamp]

Tokens scanned: [N]
✅ Low risk: [N]
⚠️ Medium risk: [N]  
🚨 High risk: [N]

[If high risk tokens found, list them with scores]
```

## Error Handling
- If DexScreener API times out: retry once after 30 seconds
- If no new tokens found: log "No new launches in last 10 min" and exit cleanly
- If score calculation fails: default to MEDIUM RISK and flag for manual review

## Memory
This skill maintains:
- `memory/scan-log.md` — Full scan history with timestamps
- `memory/flagged-tokens.md` — All high/medium risk flags
- `memory/confirmed-rugs.md` — Tokens later confirmed as rug pulls (for ML training)
