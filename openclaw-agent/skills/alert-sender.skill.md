# Skill: alert-sender

## Purpose
Send formatted, actionable Telegram alerts for high-risk tokens detected by the pump.notdump security agent. Called by `rug-detector` when score > 75.

## Trigger
- Called by: `rug-detector` skill when HIGH RISK token detected
- Called by: `token-scanner` skill for batch summary reports
- Manual: user says "send alert for [token]"

## Tools Required
- `message` — Send Telegram messages to configured alert channel
- `exec` — Run `python3 token-scanner/telegram_alerts.py` for batch sends

## Alert Types

### 🚨 Type 1: IMMEDIATE HIGH RISK ALERT
Fires instantly when a single token scores > 75/100.

**Format:**
```
🚨 HIGH RISK TOKEN DETECTED

Token: [NAME] ($[SYMBOL])
Risk Score: [SCORE]/100 🔴

⚠️ Why this is dangerous:
• [Critical flag 1]
• [Critical flag 2]
• [Critical flag 3]

📊 Stats:
• Liquidity: $[AMOUNT]
• Age: [TIME]
• Mint Authority: [STATUS]
• Top Holder: [PERCENT]%

🔗 Verify: https://dexscreener.com/solana/[ADDRESS]

🛡️ pump.notdump Agent — protecting investors 24/7
```

### ⚠️ Type 2: MEDIUM RISK WATCH ALERT
Sent when a token scores 51–75. Less urgent, but worth monitoring.

**Format:**
```
⚠️ Token Under Monitoring

Token: [NAME] ($[SYMBOL])
Risk Score: [SCORE]/100 🟡

Flagged for: [PRIMARY_REASON]

Will re-scan in 30 minutes.

🔗 https://dexscreener.com/solana/[ADDRESS]
```

### 📊 Type 3: HOURLY SUMMARY REPORT
Sent every hour summarizing all scans since last report.

**Format:**
```
📊 pump.notdump Hourly Report
⏰ [START_TIME] → [END_TIME]

Scanned: [N] tokens
✅ Safe: [N]
⚠️ Monitoring: [N]
🚨 High Risk: [N]

🏆 Safest Token: [NAME] ([SCORE]/100)
☠️ Riskiest: [NAME] ([SCORE]/100)

Funds protected estimate: $[AMOUNT]

🤖 Agent uptime: [UPTIME]%
```

### 🔔 Type 4: PATTERN ALERT
When the agent detects a coordinated attack (multiple related rugs).

**Format:**
```
🔔 COORDINATED RUG PATTERN DETECTED

The agent has identified [N] related tokens
with similar rug pull signatures:

Tokens: [LIST]
Pattern: [PATTERN_TYPE]
Wallets in common: [N]

This may be a coordinated operation.
Avoid all related tokens.

🛡️ pump.notdump Agent
```

## Rate Limiting
- Maximum 1 HIGH RISK alert per token (no duplicates)
- Maximum 5 alerts per hour to avoid spam
- HOURLY SUMMARY always sends, even if 0 high-risk tokens
- If rate limit hit: queue remaining alerts, send in next window

## Configuration
```
TELEGRAM_CHAT_ID: configured in agent environment
ALERT_COOLDOWN_MINUTES: 60 (hourly summaries)
HIGH_RISK_THRESHOLD: 75
MEDIUM_RISK_THRESHOLD: 50
```

## Memory
- Log every sent alert to `memory/alerts-sent.md`
- Track alert→outcome: did flagged tokens actually rug? (for accuracy tracking)
- Update `memory/accuracy-stats.md` monthly

## Success Metrics
The agent tracks its own accuracy:
- True positives: flagged tokens that actually rugged
- False positives: flagged tokens that were actually safe
- Target: > 80% accuracy on HIGH RISK calls
