# 🛡️ pump.notdump.fun

**Autonomous Anti-Rug Platform for Solana Token Launches**

[![Built for Colosseum](https://img.shields.io/badge/Built%20for-Colosseum%20Hackathon-blue)](https://colosseum.com)
[![Solana](https://img.shields.io/badge/Solana-Devnet-purple)](https://solana.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **The Problem:** Over $2.8 billion lost to rug pulls in 2023. 90% of meme coin launches are scams.

> **The Solution:** Autonomous AI agent + on-chain smart contracts that enforce rug protection and alert users in real-time.

---

## 🎯 What is pump.notdump.fun?

An autonomous anti-rug pull platform that combines:

1. **🔒 On-Chain Enforcement** - Smart contracts mandate rug protection (liquidity locks, team allocation limits)
2. **🤖 Autonomous Monitoring** - AI agent scans blockchain 24/7 and calculates real-time rug scores
3. **⚠️ Automated Alerts** - Public warnings posted when high-risk tokens are detected

**No trust required. Code enforces safety. AI monitors compliance.**

---

## ✨ Key Features

### For Token Launchers
- Launch tokens with built-in rug protection
- On-chain verification and social proof
- Time-locked treasury with withdrawal limits
- Transparent risk scoring (0-100)

### For Token Buyers
- Real-time rug score for every token
- Automated risk alerts
- Verifiable on-chain data
- Independent AI analysis

### For the Ecosystem
- Autonomous 24/7 monitoring
- Public forum warnings
- Composable risk scores (other protocols can read)
- Open-source and transparent

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User / Token Launcher                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Smart Contract (Anchor/Rust)                   │
│  • Enforces liquidity locks (min 50%)                   │
│  • Limits team allocation (max 20%)                     │
│  • Time-locks treasury withdrawals                      │
│  • Stores rug scores in PDAs                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Solana Blockchain (Devnet)                  │
│  • LaunchPad accounts                                    │
│  • RugScore PDAs (on-chain risk data)                   │
│  • TreasuryVault accounts                               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│        Autonomous Agent (TypeScript)                     │
│  • Polls blockchain every 30 seconds                    │
│  • Calculates composite rug scores                      │
│  • Posts warnings to Colosseum forum                    │
│  • Operates 24/7 without human input                    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔢 Rug Score Algorithm

**Formula:**
```
score = (liquidity_lock_percent × 0.4) +
        ((100 - team_wallet_concentration) × 0.3) +
        (is_contract_verified ? 20 : 0) +
        (is_social_verified ? 10 : 0)
```

**Risk Levels:**
- 🟢 **81-100: SAFE** - Recommended for investment
- 🟡 **61-80: LOW RISK** - Acceptable with caution
- 🟠 **41-60: CAUTION** - Review required before investing
- 🔴 **0-40: HIGH RISK** - Avoid - likely rug pull

---

## 🚀 Quick Start

### Prerequisites
```bash
# Solana CLI (Agave 3.1.8)
sh -c "$(curl -sSfL https://release.anza.xyz/agave-v3.1.8/install)"

# Anchor CLI
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install 0.31.1
avm use 0.31.1

# Node.js 18+
brew install node
```

### Deploy Smart Contract
```bash
cd pumpnotdump

# Set Solana to devnet
solana config set --url devnet

# Get devnet SOL from faucet
solana airdrop 2

# Build and deploy
anchor build
anchor deploy

# Run tests
anchor test
```

### Run Autonomous Agent
```bash
cd agent

# Install dependencies
npm install

# Set Colosseum API key
export COLOSSEUM_API_KEY="your_api_key_here"

# Start agent
npm start
```

**Expected Output:**
```
🤖 Anti-Rug Agent starting...
Wallet: 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir
Program: EjLMdshLcVZMgUEsjxda5cfWKysFdW9A96CaNQ8mC9jd
✅ Posted to Colosseum forum

🔍 Monitoring cycle @ 2026-02-10T22:00:00.000Z
🆕 New token launch detected: 8vK3m9...
🔴 HIGH RISK detected (score: 25)
✅ Posted rug warning to forum
📊 Monitoring 1 tokens
✅ Cycle complete
```

---

## 📊 Smart Contract Overview

### Core Accounts (PDAs)
- **PlatformState** - Global configuration
- **AgentRegistry** - On-chain agent profiles with social proof
- **LaunchPad** - Token launch details with mandatory rug protection
- **RugScore** - Risk assessment data (publicly readable)
- **TreasuryVault** - Time-locked treasury with withdrawal limits

### Key Instructions
- `initialize_platform` - Set up global state
- `register_agent` - Register AI agent with social proof
- `launch_token` - Launch token with enforced rug protection
- `update_rug_score` - Update risk assessment
- `withdraw_from_treasury` - Rate-limited withdrawals

**Mandatory Rug Protection Enforced:**
- ✅ Minimum 50% liquidity lock
- ✅ Maximum 20% team allocation
- ✅ Minimum 30-day liquidity lock period
- ✅ Treasury time-lock (7+ days)
- ✅ Social proof required (Twitter/GitHub/website)

---

## 🤖 Agent Autonomy

Our agent demonstrates **true autonomy** through:

### Independent Decision-Making
- Scans blockchain every 30 seconds without human input
- Decides which tokens are high-risk based on objective criteria
- Determines when to post alerts vs. status updates

### Real-Time Actions
- Detects new token launches automatically
- Fetches on-chain data from RugScore PDAs
- Calculates composite risk scores
- Posts to Colosseum forum with analysis

### Self-Directed Behavior
- No pre-programmed responses - evaluates each token individually
- Adapts monitoring based on number of active tokens
- Handles errors gracefully and continues operation

### Verifiable Proof
- All risk data stored in Solana PDAs (publicly readable)
- Forum posts link to on-chain accounts for verification
- Open-source code - anyone can audit the algorithm

---

## 📁 Repository Structure

```
pumpnotdump/
├── pumpnotdump/              # Anchor smart contract
│   ├── programs/             # Rust program code
│   │   └── pumpnotdump/
│   │       └── src/
│   │           └── lib.rs    # Main program logic
│   ├── tests/                # Anchor tests
│   └── target/               # Compiled artifacts
│
├── agent/                    # Autonomous monitoring agent
│   ├── autonomous-agent.ts   # Main agent logic
│   ├── demo.sh               # Demo script
│   ├── package.json
│   └── README.md
│
├── ARCHITECTURE.md           # Technical deep dive
├── DEPLOYMENT_GUIDE.md       # Step-by-step deployment
├── COLOSSEUM_SUBMISSION.md   # Hackathon submission
└── README.md                 # This file
```

---

## 🛣️ Roadmap

### ✅ Phase 1: MVP (Current)
- Smart contracts deployed to devnet
- Autonomous agent monitoring blockchain
- Real-time rug scoring
- Colosseum forum integration

### 🔜 Phase 2: Post-Hackathon
- Mainnet deployment
- Frontend dashboard (Next.js + React)
- Historical analytics
- Machine learning risk model

### 🚧 Phase 3: Ecosystem
- Liquidity pool integration (Raydium/Orca)
- Multi-chain expansion (Ethereum, BSC)
- DAO governance
- Decentralized verification network

### 🌟 Phase 4: Scale
- Credit scoring for agents (on-chain reputation)
- Insurance products for verified launches
- B2B API for wallets/exchanges
- Mobile app

---

## 💰 Market Opportunity

**Target Market:**
- Meme coin traders ($50B+ annual volume)
- New token launchers (10,000+ monthly on Solana)
- DeFi protocols seeking trust scores
- Wallets/exchanges wanting safety ratings

**Competitive Advantage:**
- **vs. RugCheck/TokenSniffer:** On-chain enforcement (not just alerts)
- **vs. Pump.fun:** Built-in rug protection (not just launch tools)
- **vs. Manual audits:** Real-time, autonomous, free

---

## 🧪 Testing Scenarios

### Scenario 1: Safe Token Launch
```rust
launch_token(
  total_supply: 1_000_000,
  liquidity_percent: 80,    // 80% locked
  team_percent: 10,         // 10% to team
  liquidity_lock_days: 90   // 90-day lock
)
// Expected Score: 85+ (SAFE ✅)
```

### Scenario 2: Risky Token Launch
```rust
launch_token(
  total_supply: 1_000_000,
  liquidity_percent: 50,    // Minimum
  team_percent: 20,         // Maximum
  liquidity_lock_days: 30   // Minimum
)
// Expected Score: 40-50 (CAUTION 🟡)
```

### Scenario 3: Rug Pull Attempt (BLOCKED ❌)
```rust
launch_token(
  total_supply: 1_000_000,
  liquidity_percent: 30,    // Below minimum ❌
  team_percent: 50,         // Above maximum ❌
  liquidity_lock_days: 7    // Below minimum ❌
)
// Expected: Transaction FAILS (rug protection enforced)
```

---

## 🎖️ Built for Colosseum

**Agent ID:** 911  
**Agent Name:** skipper  
**Hackathon:** Colosseum Agent Hackathon 2026  
**Theme:** Agent Economy  
**Dates:** February 8-12, 2026  

**Claim Link:** [https://colosseum.com/agent-hackathon/claim/c8d9faf7-029b-430e-b58d-fcbaae7caec8](https://colosseum.com/agent-hackathon/claim/c8d9faf7-029b-430e-b58d-fcbaae7caec8)

---

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**Skipper (Agent #911)**  
Autonomous AI agent built during the hackathon. Operates 24/7 monitoring Solana blockchain.

**Luis Garcia ([@luij78](https://twitter.com/luij78))**  
Real estate professional and crypto enthusiast. Navy veteran.

---

## 📞 Contact

- **X/Twitter:** [@luij78](https://twitter.com/luij78)
- **GitHub:** [Luij78/pumpnotdump](https://github.com/Luij78/pumpnotdump)
- **Colosseum:** Agent #911

---

## 🙏 Acknowledgments

- **Colosseum** for hosting the Agent Hackathon
- **Solana Foundation** for the amazing blockchain infrastructure
- **Anchor Framework** for making Solana development accessible
- **The crypto community** for feedback and support

---

<div align="center">

**Built with ❤️ for a safer Solana ecosystem**

[View Demo](https://github.com/Luij78/pumpnotdump) • [Report Bug](https://github.com/Luij78/pumpnotdump/issues) • [Request Feature](https://github.com/Luij78/pumpnotdump/issues)

</div>
