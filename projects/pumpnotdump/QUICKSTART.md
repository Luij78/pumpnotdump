# 🚀 QUICKSTART — Deploy in Under 5 Minutes

**Last Updated:** February 11, 2026 11:36 AM EST  
**Deadline:** February 12, 2026 (~24 hours remaining)  
**Status:** ✅ Code complete, waiting for devnet SOL

---

## Prerequisites (Already Done ✅)

- ✅ Solana CLI installed
- ✅ Anchor CLI installed
- ✅ Wallet configured (~/.config/solana/skipper-wallet.json)
- ✅ Smart contract compiles successfully
- ✅ Agent code written and tested
- ✅ Colosseum registration complete (Agent #911)

**Only Missing:** Devnet SOL in wallet

---

## Step 1: Get Devnet SOL (5-10 minutes)

Your wallet needs 2-3 SOL to deploy. Try these methods:

### Option A: Wait for Rate Limit Reset
```bash
# Check balance
solana balance --url devnet

# Try airdrop (might work if rate limit cleared)
solana airdrop 2 --url devnet
```

### Option B: Web Faucets (Recommended)
1. **QuickNode Faucet** (most reliable)
   - Go to: https://faucet.quicknode.com/solana/devnet
   - Enter wallet: `5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir`
   - Complete verification (might need to tweet)
   - Get 5 SOL

2. **SolFaucet**
   - Go to: https://solfaucet.com
   - Enter wallet address
   - Get 1-2 SOL

3. **Helius Faucet**
   - Alternative wallet: `9LxrENgXEaidARTVyifUU7uuB3TfbwYXGZ99ySsPax9X`
   - Could try this if main wallet stuck

### Option C: Ask Colosseum Discord
If faucets fail, post in #devnet-sol channel with:
```
Need devnet SOL for Agent Hackathon deployment
Agent #911 | pump.notdump.fun
Wallet: 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir
Deadline: Feb 12
```

---

## Step 2: Deploy Smart Contract (2 minutes)

Once you have SOL:

```bash
# Navigate to project
cd ~/clawd/projects/pumpnotdump/pumpnotdump

# Deploy to devnet
anchor deploy

# Expected output:
# Program Id: [PROGRAM_ID_WILL_BE_HERE]
```

**Save the Program ID!** You'll need it for the agent.

---

## Step 3: Configure Agent (1 minute)

```bash
cd ~/clawd/projects/pumpnotdump/agent

# Create .env file
cat > .env << 'EOF'
COLOSSEUM_API_KEY=24ea8d8889659a5321d0452a429f58f1b9cba94ab3d66f0a1d5cd7167e5c3f51
SOLANA_RPC=https://api.devnet.solana.com
PROGRAM_ID=[PASTE_DEPLOYED_PROGRAM_ID]
AGENT_ID=911
POLL_INTERVAL_MS=30000
EOF

# Install dependencies (if not already done)
npm install
```

---

## Step 4: Start Agent (30 seconds)

```bash
npm start
```

**Expected output:**
```
🤖 Anti-Rug Agent starting...
Wallet: 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir
Program: [YOUR_PROGRAM_ID]
✅ Posted to Colosseum forum
🔍 Monitoring cycle @ 2026-02-11T16:36:00.000Z
✅ Cycle complete. Monitoring 0 tokens.
```

**Leave this running!** The agent needs to be active for the hackathon judging.

---

## Step 5: Post to Forum (15 minutes)

1. **Go to:** https://colosseum.com/agent-hackathon
2. **Click:** "Agent #911" or "Post Update"
3. **Copy content from:** `COLOSSEUM_FORUM_POST.md`
4. **Add:** Your deployed program ID where it says [DEPLOYED_PROGRAM_ID]
5. **Add screenshot:** Terminal showing agent running
6. **Post!**

---

## Step 6: Submit to Hackathon (5 minutes)

1. **Visit:** https://colosseum.com/agent-hackathon/claim/c8d9faf7-029b-430e-b58d-fcbaae7caec8
2. **Connect:**
   - X account: @luij78
   - Solana wallet: 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir
3. **Fill in:**
   - Project name: pump.notdump.fun
   - GitHub: https://github.com/Luij78/pumpnotdump
   - Description: (copy from README.md summary)
   - Program ID: [Your deployed ID]
4. **Submit!**

---

## Verification Checklist

Before submitting, verify:

- [ ] Smart contract deployed successfully
- [ ] Agent is running (terminal shows monitoring cycles)
- [ ] Agent posted introduction to Colosseum forum
- [ ] Forum post includes deployed program ID
- [ ] GitHub repo is public and up-to-date
- [ ] README.md has clear description
- [ ] Claim form submitted with all details

---

## Troubleshooting

### "Command not found: solana"
```bash
export PATH="/Users/luisgarcia/.local/share/solana/install/active_release/bin:$PATH"
```

### "Command not found: anchor"
```bash
export PATH="$HOME/.cargo/bin:$PATH"
```

### "Program deploy failed"
Check you have enough SOL:
```bash
solana balance --url devnet
# Should show 2+ SOL
```

### "Agent can't connect to program"
1. Make sure PROGRAM_ID in .env matches deployed program
2. Check wallet has SOL for transaction fees
3. Verify RPC endpoint is responding:
   ```bash
   curl https://api.devnet.solana.com -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1, "method":"getHealth"}'
   ```

### "Agent posts not appearing on Colosseum"
1. Verify API key is correct in .env
2. Check Colosseum API status
3. Try posting manually at colosseum.com to verify account

---

## Time Budget

| Task | Time | Status |
|------|------|--------|
| Get devnet SOL | 5-10 min | ⏳ WAITING |
| Deploy contract | 2 min | Ready |
| Configure agent | 1 min | Ready |
| Start agent | 30 sec | Ready |
| Post to forum | 15 min | Content ready |
| Submit hackathon | 5 min | Claim link ready |
| **TOTAL** | **~25 min** | **Once SOL acquired** |

---

## Contact

**Questions?** Reach out:
- X: [@luij78](https://twitter.com/luij78)
- GitHub: [Luij78](https://github.com/Luij78)
- Colosseum: Agent #911

---

## Final Notes

**This is production-ready code.** The smart contract compiles, the agent is tested, the documentation is comprehensive. The ONLY blocker is getting 2 SOL from a devnet faucet.

**We're 99% done.** Just need that devnet SOL and 25 minutes to deploy + submit.

**Deadline:** 24 hours. Plenty of time once faucets cooperate.

---

*Built with ❤️ for the Colosseum Agent Hackathon*  
*Skipper (Agent #911) - Force for good*
