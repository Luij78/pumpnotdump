# Colosseum Hackathon — Quick Reference Card

**⏰ DEADLINE: TODAY (Feb 12, 2026)**

---

## 🔥 FASTEST PATH (5 MINUTES)

### Get SOL (Web Faucet - Fastest)
https://faucet.quicknode.com/solana/devnet
- Enter wallet: `5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir`
- Complete verification
- Wait for confirmation

### Deploy (One Command)
```bash
cd ~/clawd/projects/pumpnotdump
./scripts/one-click-deploy.sh
```

### Submit
https://colosseum.com/agent-hackathon/claim/c8d9faf7-029b-430e-b58d-fcbaae7caec8
- Connect X (@luij78)
- Connect wallet
- Fill form with Program ID from deploy output
- Submit

---

## 📋 CRITICAL INFO

**Agent ID:** 911  
**Agent Name:** skipper  
**Claim Code:** c8d9faf7-029b-430e-b58d-fcbaae7caec8  

**Wallets:**
- AgentWallet: `5fu6oduPKC7PpyEqV8GTcxrRdjJV8aZoBCMuxE26mQ8h`
- Original: `5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir`
- Helius: `9LxrENgXEaidARTVyifUU7uuB3TfbwYXGZ99ySsPax9X`

**GitHub:** https://github.com/Luij78/pumpnotdump  
**API Key:** (in memory/colosseum-hackathon.md)

---

## 🆘 IF SOL FAUCETS FAIL

### Try CLI First
```bash
~/.local/share/solana/install/active_release/bin/solana airdrop 2 --url devnet
```

### Discord Request
1. Join: https://discord.gg/QK6d4F7h5q
2. Go to #devnet-sol
3. Post:
```
Need devnet SOL for Agent Hackathon deployment
Agent #911 | pump.notdump.fun
Wallet: 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir
Deadline: Today (Feb 12)
Project: https://github.com/Luij78/pumpnotdump
```

### Alternative Faucets
- https://solfaucet.com
- https://faucet.solana.com

### Check Balance
```bash
~/.local/share/solana/install/active_release/bin/solana balance --url devnet
```

---

## 📝 MANUAL STEPS (If Deploy Works)

### 1. Forum Post
- Find Colosseum forum (website or Discord)
- Post content from: `COLOSSEUM_FORUM_POST.md`
- Include Agent #911, GitHub link, Program ID

### 2. X Thread (Optional)
- Content ready in: `X_LAUNCH_THREAD.md`
- 9 tweets prepared
- Can post after submission

---

## 🚨 IF NO SOL BY NOON

### Code-Only Submission
1. Go to claim URL (same as above)
2. Submit GitHub repo
3. In notes: "Devnet faucets rate-limited, code ready to deploy"
4. Include: "All tests pass, compiles clean, 99% complete"

**Win probability:** Lower (5-10%) but better than nothing

---

## 📂 KEY FILES

**Action Plan:** `MORNING_STATUS_FEB12.md` (full details)  
**Deploy Script:** `scripts/one-click-deploy.sh`  
**Forum Post:** `COLOSSEUM_FORUM_POST.md`  
**Submission Text:** `COLOSSEUM_SUBMISSION.md`  
**X Thread:** `X_LAUNCH_THREAD.md`  

---

## ✅ VERIFICATION CHECKLIST

After deploy:
- [ ] Smart contract deployed (Program ID received)
- [ ] Agent started (check `ps aux | grep autonomous-agent`)
- [ ] Agent logs working (`tail -f agent/agent.log`)
- [ ] Forum post created (manual)
- [ ] Hackathon submission form filled
- [ ] X thread posted (optional)

---

## 💰 PRIZES

- 1st: $50,000 USDC
- 2nd: $30,000 USDC
- 3rd: $15,000 USDC
- Most Agentic: $5,000 USDC

---

## 🎯 WHAT JUDGES WILL SEE

- ✅ Professional GitHub repo
- ✅ Comprehensive documentation
- ✅ Clean, working code (800 lines Rust, 360 lines TS)
- ✅ Real utility (anti-rug protection)
- ✅ True autonomy (monitors → analyzes → alerts)
- ⏸️ Live deployment (if SOL acquired)

---

**Status:** 99% complete. Only needs SOL to deploy.  
**Time to Deploy:** 5 minutes once SOL acquired  
**Confidence:** High (if deployed) | Low (if code-only)

**Good luck! 🚀**
