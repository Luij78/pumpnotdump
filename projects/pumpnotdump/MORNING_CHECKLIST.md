# ✅ Morning Checklist — Colosseum Submission (Feb 12)

**Time Budget:** 15 minutes total  
**Deadline:** Today (Feb 12) end of day

---

## Step 1: Get Devnet SOL (5 min)

**QuickNode Faucet (FASTEST):**
- [ ] Visit: https://faucet.quicknode.com/solana/devnet
- [ ] Enter wallet: `5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir`
- [ ] Complete verification
- [ ] Verify: `~/.local/share/solana/install/active_release/bin/solana balance --url devnet`
- [ ] Expected: >= 2 SOL

**If QuickNode fails, try:**
- [ ] SolFaucet: https://solfaucet.com
- [ ] Colosseum Discord: #devnet-sol channel

---

## Step 2: Deploy Everything (2 min)

```bash
cd ~/clawd/projects/pumpnotdump
./scripts/one-click-deploy.sh
```

**Expected output:**
- [ ] Smart contract built ✓
- [ ] Smart contract deployed ✓
- [ ] Program ID displayed
- [ ] Agent configured ✓
- [ ] Agent started (PID shown) ✓
- [ ] Health checks passed ✓

**Save this info:**
- Program ID: `__________________`
- Agent PID: `__________________`

---

## Step 3: Verify Agent is Running (1 min)

```bash
# Check process
ps aux | grep autonomous-agent

# Watch logs
tail -f ~/clawd/projects/pumpnotdump/agent/agent.log
```

**Expected in logs:**
- [ ] "Anti-Rug Agent starting..."
- [ ] Wallet address shown
- [ ] Program ID shown
- [ ] "Monitoring cycle @ ..."
- [ ] No crash errors

**Ctrl+C to exit log viewer**

---

## Step 4: Post to Forum (SKIP — API Broken)

~~Manual forum posting~~

**Status:** Forum API endpoint doesn't exist. Skip this step.

---

## Step 5: Submit to Colosseum (5 min)

- [ ] Visit: https://colosseum.com/agent-hackathon/claim/c8d9faf7-029b-430e-b58d-fcbaae7caec8
- [ ] Connect X account (@luij78)
- [ ] Connect Solana wallet (5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir)
- [ ] Fill form:
  - Project name: `pump.notdump.fun`
  - GitHub: `https://github.com/Luij78/pumpnotdump`
  - Program ID: (from Step 2)
  - Description: Copy from `COLOSSEUM_SUBMISSION.md`
- [ ] Submit ✅

---

## Step 6: Take Screenshots (2 min)

For submission/proof:
- [ ] Terminal deployment output
- [ ] Agent logs showing monitoring
- [ ] Solana Explorer: https://explorer.solana.com/address/[PROGRAM_ID]?cluster=devnet
- [ ] GitHub repo: https://github.com/Luij78/pumpnotdump

---

## Optional: Post X Thread

If time permits (not required):
- [ ] Copy tweets from `X_LAUNCH_THREAD.md`
- [ ] Post thread on @luij78
- [ ] Tag @Colosseum

---

## ✅ DONE!

**Total Time:** ~15 minutes  
**Submission Status:** Complete  
**Agent Status:** Running 24/7  
**Next:** Wait for judges to review (Winners announced Feb 16)

---

## Troubleshooting

**If deploy fails:**
1. Check SOL balance: `solana balance --url devnet`
2. If 0 SOL, go back to Step 1
3. Read error message carefully
4. Check logs: `tail -f ~/clawd/projects/pumpnotdump/agent/agent.log`
5. Ask Skipper for help

**If agent crashes:**
1. Check logs: `cat ~/clawd/projects/pumpnotdump/agent/agent.log`
2. Verify PROGRAM_ID in `.env` matches deployed program
3. Re-run deploy script

**If submission form errors:**
1. Make sure wallet is connected
2. Make sure X account is connected
3. Try different browser
4. Ask in Colosseum Discord

---

**Remember:** Even without deployment, you can submit code-only. But try for deployment first!

**Confidence:** 99% ready. Just need SOL.

**Good luck! 🚀**
