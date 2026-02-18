# pump.notdump Security Agent — Configuration

## Agent Identity
- **Name:** pump.notdump Security Agent  
- **Platform:** OpenClaw  
- **Mission:** Protect Solana investors from rug pulls through autonomous 24/7 token monitoring  
- **Version:** 1.0.0  
- **Status:** Active

## Skills Loaded
| Skill | Trigger | Frequency |
|-------|---------|-----------|
| `token-scanner` | Cron + manual | Every 5 minutes |
| `rug-detector` | Called by scanner | On demand |
| `alert-sender` | Called by detector | On demand |

## Cron Schedule
```
*/5 * * * *    token-scanner     # Scan new Solana token launches
0 * * * *      alert-sender      # Send hourly summary report
0 6 * * *      daily-brief       # Morning summary to Telegram
```

## API Integrations (No Auth Required)
- **DexScreener:** `https://api.dexscreener.com/latest/dex/tokens/solana`
  - Rate limit: 300 req/min
  - Used for: token data, liquidity, volume, holder info
- **SolScan:** `https://public-api.solscan.io/token/holders`
  - Rate limit: 60 req/min  
  - Used for: detailed holder distribution

## Memory Structure
```
openclaw-agent/
├── skills/
│   ├── token-scanner.skill.md
│   ├── rug-detector.skill.md
│   └── alert-sender.skill.md
├── memory/
│   ├── scan-log.md          # Full scan history
│   ├── flagged-tokens.md    # All medium/high risk flags
│   ├── confirmed-rugs.md    # Confirmed rug pulls (training data)
│   ├── alerts-sent.md       # Alert history
│   ├── accuracy-stats.md    # Agent accuracy metrics
│   └── token-analyses/      # Per-token analysis files
├── agent-config.md          # This file
└── README.md
```

## Risk Thresholds
| Threshold | Score | Action |
|-----------|-------|--------|
| LOW RISK | 0–30 | Log only |
| CAUTION | 31–50 | Monitor |
| MEDIUM RISK | 51–75 | Batch alert |
| HIGH RISK | 76–100 | Immediate alert |

## Alert Channels
- **Primary:** Telegram (`@pumpnotdump_alerts` — configure with `TELEGRAM_BOT_TOKEN`)
- **Secondary:** Discord webhook (optional, configure with `DISCORD_WEBHOOK_URL`)

## Environment Variables
```bash
TELEGRAM_BOT_TOKEN=<your-bot-token>
TELEGRAM_CHAT_ID=<your-channel-id>
DEXSCREENER_POLL_INTERVAL=300    # 5 minutes in seconds
HIGH_RISK_THRESHOLD=75
MEDIUM_RISK_THRESHOLD=50
MAX_ALERTS_PER_HOUR=5
```

## Metrics Tracked
The agent self-reports the following in hourly summaries:
- Tokens scanned (last hour / total)
- High risk flags (last hour / total)
- Confirmed rug pulls caught
- False positive rate
- Estimated funds protected (USD)
- Agent uptime percentage

## Stopping / Pausing
To pause the agent:
```bash
openclaw skill disable token-scanner
```
To resume:
```bash
openclaw skill enable token-scanner
```

## How OpenClaw Powers This Agent
- **Persistent Memory:** Agent maintains scan history, flagged tokens, and accuracy stats across sessions
- **Cron Execution:** Token scanner fires every 5 minutes without human intervention
- **Multi-Tool Chaining:** scanner → detector → alert-sender run as a pipeline
- **Real-World Actions:** Telegram alerts fire automatically when risk thresholds exceeded
- **Web Access:** DexScreener API calls happen live during each scan cycle
- **Self-Improvement:** Agent logs outcomes and updates accuracy stats to improve over time
