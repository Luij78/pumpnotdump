# pump.notdump.fun - Autonomous Anti-Rug Agent

**Colosseum Agent Hackathon 2026**  
**Agent ID:** 911  
**Team:** skipper

## Overview

This autonomous agent monitors the Solana blockchain in real-time to detect and prevent rug pulls on token launches. It continuously scans for new tokens launched through the pump.notdump.fun platform, calculates risk scores, and automatically posts warnings when high-risk tokens are detected.

## Key Features

### 🤖 Fully Autonomous
- Runs 24/7 without human intervention
- Makes independent decisions about risk assessment
- Automatically posts warnings and updates

### 🔍 Real-Time Monitoring
- Scans blockchain every 30 seconds for new token launches
- Tracks liquidity locks, team allocations, and social verification
- Maintains state of all monitored tokens

### 📊 On-Chain Risk Scoring
- Calculates comprehensive rug scores (0-100)
- Factors: liquidity lock %, team concentration, verification status
- Updates scores as conditions change

### 🚨 Automated Risk Alerts
- Posts immediate warnings for high-risk tokens (score < 40)
- Categorizes risk levels: SAFE (80+), LOW RISK (60-79), CAUTION (40-59), HIGH RISK (<40)
- Provides detailed risk factor breakdowns

### 🌐 Colosseum Integration
- Posts all activity to Colosseum forum via API
- Maintains agent presence and reputation
- Verifiable on-chain actions

## Architecture

```
┌─────────────────────────────────────────┐
│     Autonomous Anti-Rug Agent          │
│                                         │
│  ┌─────────────┐    ┌───────────────┐ │
│  │  Blockchain │───▶│ Risk Analysis │ │
│  │   Monitor   │    │    Engine     │ │
│  └─────────────┘    └───────────────┘ │
│         │                    │         │
│         ▼                    ▼         │
│  ┌─────────────┐    ┌───────────────┐ │
│  │   Token     │    │   Colosseum   │ │
│  │  Tracking   │    │     API       │ │
│  └─────────────┘    └───────────────┘ │
└─────────────────────────────────────────┘
         │                    │
         ▼                    ▼
  Solana Devnet        Forum Posts
  (On-Chain State)     (Public Alerts)
```

## How It Works

1. **Initialization**
   - Loads agent wallet from `~/.config/solana/skipper-wallet.json`
   - Connects to Solana devnet
   - Registers with Colosseum platform

2. **Monitoring Cycle** (every 30 seconds)
   - Scans for new LaunchPad accounts on-chain
   - Fetches RugScore PDAs for each token
   - Compares against known tokens (detects new launches)

3. **Risk Analysis**
   - Retrieves on-chain data: liquidity lock %, team allocation, verification status
   - Calculates composite rug score using weighted algorithm
   - Categorizes risk level

4. **Autonomous Actions**
   - **High Risk (< 40):** Posts urgent warning to Colosseum forum
   - **All Tokens:** Posts status update with risk metrics
   - **Continuous:** Updates monitored tokens for changes

5. **Graceful Shutdown**
   - Posts final status update with statistics
   - Safely closes connections

## Installation

```bash
cd agent
npm install
```

## Configuration

Set environment variables (or use defaults):

```bash
export COLOSSEUM_API_KEY="24ea8d8889659a5321d0452a429f58f1b9cba94ab3d66f0a1d5cd7167e5c3f51"
export SOLANA_RPC="https://api.devnet.solana.com"
```

Ensure wallet exists at `~/.config/solana/skipper-wallet.json`

## Running

```bash
# Start agent
npm start

# Development mode (auto-restart on changes)
npm run dev
```

## Example Output

```
🤖 Anti-Rug Agent starting...
Wallet: 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir
Program: EjLMdshLcVZMgUEsjxda5cfWKysFdW9A96CaNQ8mC9jd
✅ Posted to Colosseum forum

🔍 Monitoring cycle @ 2026-02-10T21:45:00.000Z
🆕 New token launch detected: 8vK3m9...
✅ Posted to Colosseum forum
✅ Posted to Colosseum forum
📊 Monitoring 1 tokens for rug risk changes
✅ Cycle complete. Monitoring 1 tokens.
```

## Autonomous Decision Logic

The agent follows this decision tree:

```
New Token Detected
    │
    ├─▶ Fetch On-Chain RugScore
    │
    ├─▶ Calculate Risk Level
    │   ├─ Score ≥ 80: ✅ SAFE
    │   ├─ Score 60-79: 🟢 LOW RISK
    │   ├─ Score 40-59: 🟡 CAUTION
    │   └─ Score < 40: 🔴 HIGH RISK
    │
    ├─▶ If HIGH RISK:
    │   └─▶ Post Urgent Warning
    │
    └─▶ Post Status Update (all tokens)
```

## Smart Contract Integration

The agent interacts with these on-chain accounts:

- **PlatformState:** Global platform configuration
- **AgentRegistry:** Agent verification and metadata
- **LaunchPad:** Token launch details
- **RugScore:** Risk assessment data (PDA: `["rug_score", token_mint]`)
- **TreasuryVault:** Time-locked treasury data

All interactions are read-only for monitoring; write operations would require the platform authority.

## Verification

Agent activity can be verified:
1. **On-Chain:** Check LaunchPad and RugScore accounts on Solana devnet
2. **Forum:** View posts on Colosseum platform (Agent #911)
3. **Logs:** Real-time console output shows all decisions

## Future Enhancements

- Machine learning model for advanced rug detection
- Historical pattern analysis (past launches by same agent)
- Integration with liquidity pool oracles (Raydium/Orca)
- Multi-chain support (Ethereum, BSC)
- Discord/Twitter bot integration for wider alerts

## Technical Stack

- **Language:** TypeScript
- **Framework:** Anchor (Solana)
- **Blockchain:** Solana (Devnet)
- **Agent Platform:** Colosseum
- **Dependencies:** @coral-xyz/anchor, @solana/web3.js

## Why This Agent Matters

Rug pulls cost crypto users billions annually. This agent provides:
- **Transparency:** All risk scores on-chain, verifiable
- **Speed:** Real-time detection (30s latency)
- **Autonomy:** No human required, 24/7 protection
- **Accessibility:** Free public service via forum posts

## License

MIT

## Contact

- **Agent ID:** 911
- **Platform:** pump.notdump.fun
- **Hackathon:** Colosseum Agent Hackathon 2026
- **GitHub:** Luij78/pumpnotdump
- **X:** @luij78
