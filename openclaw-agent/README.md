# pump.notdump Security Agent

> Autonomous 24/7 Solana token security monitoring, powered by OpenClaw.

## What This Agent Does

The pump.notdump security agent runs continuously on OpenClaw, scanning every new Solana token launch for rug pull signals. When it finds a high-risk token, it sends an immediate Telegram alert — before investors lose money.

**In the last 24h (example output):**
```
🤖 Agent Scan #2847
Tokens scanned: 847
✅ Low risk: 801
⚠️ Monitoring: 23
🚨 High risk flagged: 23
Estimated funds protected: ~$126K
```

## How It Works

```
[DexScreener API] ──▶ [token-scanner skill]
                              │
                    Every new token found
                              │
                              ▼
                    [rug-detector skill]
                      Scores 0–100 on:
                      • Liquidity depth
                      • Holder concentration  
                      • Mint/Freeze authority
                      • Token age
                      • Volume patterns
                              │
                    Score > 75? HIGH RISK
                              │
                              ▼
                    [alert-sender skill]
                    → Telegram alert fires
```

## Quick Start

### Prerequisites
- Python 3.8+
- OpenClaw installed and configured
- Telegram bot token (for alerts)

### Install
```bash
cd pumpnotdump/token-scanner
pip3 install -r requirements.txt
```

### Configure
```bash
cp .env.example .env
# Edit .env with your Telegram credentials
```

### Run Scanner Manually
```bash
python3 token-scanner/scanner.py
```

### Run with OpenClaw (Automated)
```bash
# Load the skills into OpenClaw
openclaw skill load openclaw-agent/skills/token-scanner.skill.md
openclaw skill load openclaw-agent/skills/rug-detector.skill.md
openclaw skill load openclaw-agent/skills/alert-sender.skill.md

# Start the agent
openclaw agent start
```

The agent will now:
- Scan new tokens every 5 minutes automatically
- Send Telegram alerts for high-risk tokens
- Generate hourly summary reports
- Maintain persistent memory of all scans

## Skill Files

| File | Purpose |
|------|---------|
| `skills/token-scanner.skill.md` | Main scan loop — fetches + scores new tokens |
| `skills/rug-detector.skill.md` | Deep analysis — 10 detection patterns |
| `skills/alert-sender.skill.md` | Telegram alerts — 4 alert types |
| `agent-config.md` | Full configuration + memory structure |

## Risk Scoring

The agent scores each token 0–100 based on:

| Factor | Weight | Safe Signal |
|--------|--------|-------------|
| Mint authority | 40pts | Revoked |
| Liquidity depth | 25pts | > $10K |
| Holder concentration | 20pts | Top holder < 20% |
| Token age | 15pts | > 24h old |
| Volume/Liquidity ratio | 15pts | < 10x |
| Freeze authority | 35pts | Revoked |

**Score interpretation:**
- 0–30: ✅ Low Risk — safe to trade
- 31–50: 🟡 Caution — monitor
- 51–75: ⚠️ Medium Risk — batch alert
- 76–100: 🚨 High Risk — immediate alert

## Why OpenClaw?

Traditional token scanners are passive dashboards. This agent is **active** — it:
1. Runs without human intervention (OpenClaw cron)
2. Chains multiple tools (web fetch → analysis → alert)
3. Maintains memory across sessions (knows which tokens it's seen before)
4. Acts on findings (sends real Telegram messages)
5. Self-improves (tracks its own accuracy over time)

That's the difference between a tool and an agent.

## Project Links
- **Live Demo:** https://pumpnotdump-landing.vercel.app
- **GitHub:** https://github.com/Luij78/pump-not-dump
- **Hackathon:** SURGE × OpenClaw on lablab.ai (deadline March 1, 2026)
