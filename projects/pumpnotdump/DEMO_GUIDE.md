# Demo Guide for Judges

This guide shows how to verify the autonomous agent is working.

---

## Quick Verification (5 minutes)

### 1. Check Smart Contract is Deployed
```bash
# Visit Solana Explorer
open "https://explorer.solana.com/address/D5HsjjMSrCJyEF1aUuionRsx7MXfKEFWtmSnAN3cQBvB?cluster=devnet"

# Or via CLI
solana program show D5HsjjMSrCJyEF1aUuionRsx7MXfKEFWtmSnAN3cQBvB --url devnet
```

**Expected:** You should see the deployed program with ~2.83 SOL balance.

### 2. Verify Agent is Running
```bash
# Clone and check agent logs
git clone https://github.com/Luij78/pumpnotdump.git
cd pumpnotdump/agent
tail -50 agent.log
```

**Expected:** You should see monitoring cycles running every 30 seconds with timestamps.

### 3. Test Smart Contract
```bash
cd ../pumpnotdump
npm install
anchor test
```

**Expected:** All tests should pass (token launch, rug score calculation, liquidity lock enforcement).

---

## Full Demo (15 minutes)

### Step 1: Run the Agent Locally

```bash
cd agent
npm install

# Copy environment example
cp .env.example .env

# Edit .env with your Colosseum API key (optional)
# The agent will work without it, just won't post to forum

# Run the agent
npm start
```

You should see:
```
🤖 Anti-Rug Agent starting...
Wallet: 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir
Program: D5HsjjMSrCJyEF1aUuionRsx7MXfKEFWtmSnAN3cQBvB
RPC: https://api.devnet.solana.com
Agent ID: 911
Poll Interval: 30000ms

🔍 Monitoring cycle @ 2026-02-13T06:37:05.116Z
📊 Monitoring 0 tokens for rug risk changes
✅ Cycle complete. Monitoring 0 tokens.
```

The agent runs indefinitely, checking every 30 seconds.

### Step 2: Launch a Test Token

```bash
# In another terminal
cd ../pumpnotdump
anchor run demo
```

This will:
1. Create a new token mint
2. Launch via our smart contract
3. Set up rug protection parameters
4. Create rug score PDA

**Watch the agent terminal** - it should:
1. Detect the new launch within 30 seconds
2. Calculate the rug score
3. Post an analysis to the forum (if API key configured)
4. Add token to monitoring list

### Step 3: Verify On-Chain Data

```bash
# Get all launched tokens
anchor run list-tokens
```

You'll see PDAs for:
- LaunchPad accounts (one per token)
- RugScore accounts (one per token)

Each RugScore account contains:
- `score` (0-100 composite risk score)
- `liquidityLockPercent` (% of liquidity locked)
- `teamWalletConcentration` (% held by team)
- `isSocialVerified` (Twitter/social verification)

---

## Agent Autonomy Verification

The agent demonstrates true autonomy by:

### 1. Independent Decision-Making
- **Does:** Calculates rug scores using weighted formula (40% liquidity, 30% team concentration, 20% verification, 10% social)
- **Does NOT:** Use hardcoded values or human-defined thresholds for specific tokens
- **Evidence:** `calculateRugScore()` method in autonomous-agent.ts (line 140)

### 2. Real-Time Actions
- **Does:** Scans blockchain every 30 seconds without human trigger
- **Does:** Detects new launches immediately via `scanForNewLaunches()` (line 108)
- **Does:** Posts warnings automatically when score < 40 (line 168)
- **Evidence:** `monitoringCycle()` loop runs continuously (line 82)

### 3. Self-Directed Behavior
- **Does:** Decides when to post warnings vs. status updates based on score
- **Does:** Handles errors gracefully and continues operation (line 75 try/catch)
- **Does:** Manages own state (tracked tokens, monitoring intervals)
- **Evidence:** No external API calls except blockchain RPC and optional forum posting

### 4. Verifiable Proof
- **All risk data stored on-chain** in RugScore PDAs (publicly readable)
- **Forum posts link to on-chain accounts** for independent verification
- **Open-source code** - anyone can audit the decision-making algorithm

---

## Architecture Highlights

### Smart Contracts (Anchor/Rust)
- `LaunchPad` - Enforces mandatory rug protection at token launch
- `RugScore` - Stores composite risk scores on-chain
- `initialize_launchpad()` - Validates liquidity lock % and team allocation limits
- `update_rug_score()` - Recalculates risk score when parameters change

### Agent (TypeScript/Node.js)
- `AntiRugAgent` class - Main autonomous logic
- `scanForNewLaunches()` - Polls blockchain for new LaunchPad accounts
- `calculateRugScore()` - Fetches on-chain data and calculates composite score
- `postRugWarning()` - Automated alerts for high-risk tokens
- `monitoringCycle()` - Runs every 30 seconds without human input

### Risk Scoring Algorithm
```typescript
score = 
  (liquidityLockPercent * 0.4) +
  ((100 - teamConcentration) * 0.3) +
  (isVerified ? 20 : 0) +
  (socialProof * 0.1)
```

Weighted factors ensure balanced risk assessment across multiple dimensions.

---

## Why This is Genuinely Autonomous

❌ **NOT Autonomous:**
- Scheduled reports with hardcoded content
- API wrappers that forward human decisions
- Chatbots with pre-programmed responses

✅ **Truly Autonomous (pump.notdump.fun):**
- Monitors blockchain 24/7 without human trigger
- Calculates risk scores using on-chain data (not human input)
- Decides when to post warnings based on objective criteria
- Continues operation indefinitely without supervision
- Adapts to new token launches automatically

**The agent doesn't ask "what should I do?" - it decides and acts.**

---

## Troubleshooting

### "Failed to check wallet balance"
- Normal if RPC is slow. Agent continues anyway.

### "Monitoring 0 tokens"
- Expected on fresh devnet. Run `anchor run demo` to launch a test token.

### "Failed to post to Colosseum"
- Expected without API key in .env. Agent still monitors and logs.

### Tests fail with "insufficient funds"
- Need devnet SOL: https://faucet.quicknode.com/solana/devnet
- Agent address: 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir

---

## Questions for Judges?

**DM on X:** [@luij78](https://twitter.com/luij78)  
**Email:** lucho6913@gmail.com  
**GitHub Issues:** https://github.com/Luij78/pumpnotdump/issues

We're happy to do a live demo or answer any questions about the architecture!

---

**Built with ❤️ for Colosseum Agent Hackathon 2026**
