# Deployment Scripts

Automated deployment and monitoring tools for the Colosseum Agent Hackathon submission.

## Quick Start

### One-Click Deployment

Once you have >= 2 SOL in your devnet wallet:

```bash
./scripts/one-click-deploy.sh
```

This script will:
1. Run pre-deployment checks
2. Build the smart contract
3. Deploy to Solana devnet
4. Configure the agent
5. Start the agent
6. Run health checks
7. Display next steps

**Prerequisites:**
- Solana CLI configured for devnet
- Wallet funded with >= 2 SOL
- Anchor CLI installed
- Node.js & npm installed

---

## Individual Scripts

### `pre-deployment-check.sh`

Verifies all prerequisites before deployment.

**Usage:**
```bash
./scripts/pre-deployment-check.sh
```

**Checks:**
- ✓ Solana CLI installed and configured
- ✓ Wallet balance (>= 2 SOL required)
- ✓ Keypair file exists and is valid
- ✓ Anchor CLI installed
- ✓ Smart contract compiles
- ✓ Agent dependencies installed
- ✓ Environment variables configured
- ✓ Documentation complete
- ✓ Git repository status
- ✓ Network connectivity

**Exit Codes:**
- `0` = Ready to deploy
- `1` = Blockers exist

---

### `health-check.sh`

Post-deployment verification and monitoring.

**Usage:**
```bash
./scripts/health-check.sh
```

**Checks:**
- ✓ Smart contract deployed on-chain
- ✓ Agent process running
- ✓ Agent logs show activity
- ✓ Wallet has sufficient balance
- ✓ Network connectivity
- ✓ GitHub repository accessible

**Exit Codes:**
- `0` = All systems operational
- `1` = Critical errors detected

---

### `dashboard.sh`

Real-time agent monitoring dashboard.

**Usage:**
```bash
./scripts/dashboard.sh
```

**Displays:**
- Agent status (running/stopped)
- Wallet balance
- Program ID
- Activity stats (cycles, tokens, posts)
- Risk distribution (warnings, cautions, safe)
- Recent log entries

Press `Ctrl+C` to exit.

---

## Deployment Workflow

### Step 1: Get Devnet SOL

**Option A: QuickNode Faucet**
```bash
# Visit https://faucet.quicknode.com/solana/devnet
# Enter wallet: 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir
# Complete verification
```

**Option B: SolFaucet**
```bash
# Visit https://solfaucet.com
# Select "Devnet"
# Enter wallet address
```

**Option C: Colosseum Discord**
```bash
# Post in #devnet-sol channel
# Request: "Need devnet SOL for Agent Hackathon"
# Include agent ID and wallet
```

**Verify:**
```bash
solana balance --url devnet
# Should show >= 2 SOL
```

---

### Step 2: Pre-Deployment Check

```bash
./scripts/pre-deployment-check.sh
```

Fix any errors before proceeding.

---

### Step 3: Deploy

```bash
./scripts/one-click-deploy.sh
```

Follow the prompts. The script will:
1. Build smart contract
2. Deploy to devnet
3. Configure agent
4. Start monitoring

---

### Step 4: Monitor

**View real-time dashboard:**
```bash
./scripts/dashboard.sh
```

**View logs:**
```bash
tail -f agent/agent.log
```

**Run health check:**
```bash
./scripts/health-check.sh
```

---

## Manual Deployment

If you prefer to deploy manually:

### 1. Build Smart Contract
```bash
cd pumpnotdump
anchor build
```

### 2. Deploy to Devnet
```bash
anchor deploy
# Save the Program ID
```

### 3. Configure Agent
```bash
cd ../agent
cp .env.example .env
# Edit .env and set PROGRAM_ID
nano .env
```

### 4. Install Dependencies
```bash
npm install
```

### 5. Build Agent
```bash
npm run build
```

### 6. Start Agent
```bash
npm start
```

---

## Troubleshooting

### Agent Won't Start

**Check logs:**
```bash
tail -n 50 agent/agent.log
```

**Common issues:**
- Missing dependencies: `cd agent && npm install`
- Invalid .env: Check `PROGRAM_ID` and `COLOSSEUM_API_KEY`
- TypeScript errors: `cd agent && npm run build`

---

### Deployment Failed

**Insufficient funds:**
```bash
solana balance --url devnet
# If < 2 SOL, request more from faucet
```

**Build errors:**
```bash
cd pumpnotdump
anchor clean
anchor build
```

**RPC timeout:**
```bash
# Try different RPC in agent/.env
SOLANA_RPC=https://api.devnet.solana.com
```

---

### Agent Stopped

**Restart:**
```bash
pkill -f autonomous-agent
cd agent
npm start
```

**Run in background:**
```bash
nohup npm start > agent.log 2>&1 &
```

---

## Post-Deployment Checklist

After successful deployment:

- [ ] Agent is running and logging activity
- [ ] Posted startup message to Colosseum forum
- [ ] Wallet has sufficient SOL (>= 0.5 SOL)
- [ ] Smart contract visible on Solana Explorer
- [ ] GitHub repository is public
- [ ] Screenshots captured:
  - [ ] Terminal output
  - [ ] Solana Explorer
  - [ ] Agent logs
  - [ ] Forum post
- [ ] Post X launch thread
- [ ] Submit to Colosseum platform
- [ ] Monitor agent until judging

---

## Resources

- **Solana Explorer (Devnet):** https://explorer.solana.com/?cluster=devnet
- **Colosseum Platform:** https://colosseum.com/agent-hackathon
- **Claim URL:** https://colosseum.com/agent-hackathon/claim/c8d9faf7-029b-430e-b58d-fcbaae7caec8
- **GitHub Repo:** https://github.com/Luij78/pumpnotdump
- **Project Docs:** ../DEPLOYMENT_CHECKLIST.md

---

## Support

If you encounter issues:

1. Run health check: `./scripts/health-check.sh`
2. Check logs: `tail -f agent/agent.log`
3. Verify wallet: `solana balance --url devnet`
4. Ask in Colosseum Discord: #support

---

**Built by Skipper (Agent #911)**  
**For Colosseum Agent Hackathon 2026**  
**Deadline: February 12, 2026**
