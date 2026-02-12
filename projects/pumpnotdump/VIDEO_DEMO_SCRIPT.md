# Video Demonstration Script
## pump.notdump.fun - Autonomous Anti-Rug Platform

**Duration:** 3-5 minutes  
**Format:** Screen recording with voiceover  
**Platform:** YouTube + X embed  
**Purpose:** Hackathon submission + marketing

---

## Pre-Recording Checklist

- [ ] Agent is deployed and running
- [ ] Terminal with agent output visible
- [ ] Browser with Colosseum forum open
- [ ] Code editor with key files open
- [ ] Solana Explorer tabs ready
- [ ] Good lighting for webcam (if using)
- [ ] Microphone tested
- [ ] Screen recording software ready (QuickTime/OBS)

---

## Scene 1: Hook (0:00 - 0:20)

**Visual:** Title card with "$2.8B LOST" stat

**Script:**
> "In 2023, over $2.8 billion was lost to cryptocurrency rug pulls. 90% of meme coin launches are scams. Token buyers have zero reliable protection.
> 
> I built an autonomous AI agent to fix this. Let me show you how it works."

**Transition:** Fade to desktop

---

## Scene 2: The Problem (0:20 - 0:45)

**Visual:** Browser showing recent rug pull news articles

**Script:**
> "Every day, thousands of new tokens launch on Solana. Most promise the moon. Many rug pull within hours.
> 
> Existing solutions like RugCheck and TokenSniffer only provide alerts AFTER launch. They can't prevent rug pulls, they can only warn you.
> 
> We need enforcement, not just warnings."

**Transition:** Switch to terminal

---

## Scene 3: The Solution Overview (0:45 - 1:15)

**Visual:** Terminal showing agent starting up

**Script:**
> "Meet pump.notdump.fun - an autonomous anti-rug platform with two parts:
> 
> First, smart contracts that ENFORCE rug protection. Minimum 50% liquidity lock, maximum 20% team allocation, 30-day lock period. These aren't suggestions, they're requirements validated on-chain.
> 
> Second, an AI agent that monitors the blockchain 24/7, calculates real-time rug scores, and posts public warnings.
> 
> Let me show you the agent in action."

**Transition:** Focus on terminal output

---

## Scene 4: Agent Startup (1:15 - 1:45)

**Visual:** Terminal showing agent initialization

**Script:**
> "Here's the agent starting up. It connects to Solana devnet, loads the smart contract, and begins monitoring.
> 
> Notice: it displays the wallet address, program ID, and polling interval. This agent runs completely autonomously - no human input required.
> 
> It's checking its SOL balance to ensure it can post transactions. Now it's entering the main monitoring loop."

**Terminal Output to Show:**
```
🤖 Anti-Rug Agent starting...
Wallet: 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir
Program: EjLMdshLcVZMgUEsjxda5cfWKysFdW9A96CaNQ8mC9jd
Wallet Balance: 2.5 SOL
Poll Interval: 30000ms

🔍 Monitoring cycle @ 2026-02-11T19:45:00.000Z
✅ Posted startup message to Colosseum forum
```

**Transition:** Split screen - terminal + browser

---

## Scene 5: Real-Time Monitoring (1:45 - 2:30)

**Visual:** Split screen showing terminal output + Solana Explorer

**Script:**
> "The agent scans for new token launches every 30 seconds. When it detects one, it fetches the on-chain rug score data.
> 
> Here's a token launch happening now. The agent reads the LaunchPad account, pulls the rug score PDA, and calculates the composite risk score.
> 
> This token has 80% liquidity locked, 10% team allocation, and a 90-day lock period. The agent calculates a score of 85 - that's SAFE.
> 
> Now watch what happens with a risky token..."

**Terminal Output to Show:**
```
🔍 Monitoring cycle @ 2026-02-11T19:45:30.000Z
🆕 New token launch detected: SafeMoonAI (8vK3m9...)
📊 Fetching rug score data...
   Liquidity Lock: 80%
   Team Concentration: 10%
   Verified: Yes
   Social Proof: Yes
🟢 SAFE (Score: 85)
✅ Posted status update to forum

🔍 Monitoring cycle @ 2026-02-11T19:46:00.000Z
🆕 New token launch detected: QuickPump (7nB2k8...)
📊 Fetching rug score data...
   Liquidity Lock: 30% ⚠️
   Team Concentration: 60% ⚠️
   Verified: No
   Social Proof: No
🔴 HIGH RISK (Score: 25)
⚠️  Posting rug warning to forum...
```

**Transition:** Browser tab to Colosseum forum

---

## Scene 6: Forum Warning (2:30 - 3:00)

**Visual:** Browser showing Colosseum forum with agent's warning post

**Script:**
> "And here's the autonomous warning post. The agent posted this without any human input.
> 
> It includes the token mint address, the risk score, the specific concerns, and a recommendation to avoid.
> 
> Notice the link to the on-chain rug score PDA - anyone can verify this data themselves. Full transparency.
> 
> This warning was posted in real-time, BEFORE anyone could buy the risky token."

**Browser to Show:**
- Forum post with red warning icon
- Risk score: 25/100
- Detailed breakdown
- Link to Solana Explorer for PDA
- Timestamp showing real-time posting

**Transition:** Code editor

---

## Scene 7: Code Walkthrough (3:00 - 3:45)

**Visual:** VS Code showing key parts of the agent

**Script:**
> "Let's look at how this works under the hood.
> 
> Here's the main monitoring loop. The agent scans for new launches, calculates scores, and decides autonomously when to post warnings.
> 
> Here's the rug score algorithm. It's weighted by importance: liquidity lock is 40%, team concentration is 30%, then contract verification and social proof.
> 
> And here's the decision logic. If the score is below 40, it posts a warning. If it's 40-60, it posts a caution. Above 60, just a status update.
> 
> No pre-programmed responses. Every token is evaluated individually based on on-chain data."

**Code to Show:**
```typescript
// Main monitoring loop
while (this.isRunning) {
  const newLaunches = await this.scanForNewLaunches();
  
  for (const launch of newLaunches) {
    const rugScore = await this.calculateRugScore(launch);
    
    // Autonomous decision-making
    if (rugScore.score < 40) {
      await this.postRugWarning(launch, rugScore);
    } else if (rugScore.score < 60) {
      await this.postCautionAlert(launch, rugScore);
    } else {
      await this.postStatusUpdate(launch, rugScore);
    }
  }
  
  await this.sleep(POLL_INTERVAL_MS);
}

// Rug score calculation
calculateRugScore(launch): number {
  const score = 
    (launch.liquidityLockPercent * 0.4) +
    ((100 - launch.teamConcentration) * 0.3) +
    (launch.isContractVerified ? 20 : 0) +
    (launch.hasSocialProof ? 10 : 0);
  
  return Math.round(score);
}
```

**Transition:** Solana Explorer

---

## Scene 8: On-Chain Proof (3:45 - 4:15)

**Visual:** Solana Explorer showing smart contract accounts

**Script:**
> "Everything is verifiable on-chain. Here's the deployed smart contract on Solana devnet.
> 
> Here's a rug score PDA - you can see the liquidity lock percentage, team concentration, verification status, all stored publicly.
> 
> And here's the treasury vault account with the time-lock enforced. Teams can't instant rug because the withdrawal limits are coded into the contract.
> 
> This isn't just software - it's on-chain infrastructure anyone can build on top of."

**Explorer to Show:**
- Program account with deployed contract
- RugScore PDA with decoded data
- TreasuryVault account with locked funds
- Transaction history showing time-lock enforcement

**Transition:** GitHub repo

---

## Scene 9: Open Source (4:15 - 4:40)

**Visual:** GitHub repo page

**Script:**
> "The entire project is open source on GitHub. 800 lines of Rust for the smart contracts, 360 lines of TypeScript for the autonomous agent.
> 
> Complete documentation: architecture guide, deployment instructions, testing scenarios.
> 
> Anyone can audit the code, contribute improvements, or deploy their own instance.
> 
> This is infrastructure for a safer Solana ecosystem."

**GitHub to Show:**
- Repository structure
- Key files (lib.rs, autonomous-agent.ts)
- Documentation files
- Star count and forks

**Transition:** Closing slide

---

## Scene 10: Closing (4:40 - 5:00)

**Visual:** Title card with project info

**Script:**
> "pump.notdump.fun - autonomous anti-rug protection for Solana.
> 
> Built in 72 hours for the Colosseum Agent Hackathon.
> 
> The code is live, the agent is running, and we're just getting started.
> 
> Check out the GitHub repo, star the project, and let's make crypto safer together.
> 
> Thanks for watching."

**End Card:**
```
🛡️ pump.notdump.fun

GitHub: github.com/Luij78/pumpnotdump
Agent ID: 911
Built by: Luis Garcia (@luij78)

⭐ Star on GitHub
💬 Questions? luij78 on X
🏆 Colosseum Agent Hackathon 2026
```

**Music:** Fade out

---

## Technical Setup

### Recording Software
- **macOS:** QuickTime Player (Cmd+Shift+5)
- **Cross-platform:** OBS Studio (free, pro features)
- **Paid:** ScreenFlow (better editing)

### Audio
- **Microphone:** Built-in Mac mic acceptable, external USB mic better
- **Script:** Read from teleprompter or notes (natural, not robotic)
- **Editing:** Audacity (free) to remove background noise

### Video Editing
- **Basic:** iMovie (free on Mac)
- **Advanced:** DaVinci Resolve (free)
- **Professional:** Final Cut Pro

### Export Settings
- **Resolution:** 1920x1080 (1080p)
- **Frame Rate:** 30fps or 60fps
- **Format:** MP4 (H.264)
- **Bitrate:** 5-10 Mbps
- **File Size:** Target under 500MB for easy upload

---

## Upload Strategy

### YouTube
- **Title:** "pump.notdump.fun - Autonomous Anti-Rug Platform for Solana | Colosseum Hackathon 2026"
- **Description:** Full project description, links, timestamps
- **Tags:** Solana, Web3, Crypto, AI, Autonomous Agents, Rug Pull, DeFi, Blockchain
- **Thumbnail:** Custom with project logo + "$2.8B Lost" stat
- **Category:** Science & Technology
- **Visibility:** Public

### X (Embedded)
- **Post:** "3-minute demo of pump.notdump.fun - autonomous anti-rug protection for Solana 🛡️ [VIDEO]"
- **Embed:** Upload video directly to X (better engagement than YouTube link)
- **Pin:** Pin to profile during hackathon

### Colosseum Forum
- **Post:** Embed YouTube link in forum submission
- **Context:** "Video demonstration of agent autonomy"

---

## Alternative: Live Demo (Instead of Recorded)

If recording feels too polished, do a **live walkthrough**:

**Advantages:**
- More authentic/relatable
- Shows real bugs/delays (honesty)
- Can interact with comments
- Demonstrates actual autonomy (not staged)

**Platform Options:**
- X Spaces (audio + screenshare)
- YouTube Live
- Discord stream in Colosseum server

**Format:**
- 20-30 minute live coding/demo session
- Q&A at the end
- Record and post replay

---

## Post-Production Checklist

- [ ] Video rendered at 1080p
- [ ] Audio levels normalized
- [ ] Transitions are smooth
- [ ] Text overlays are readable
- [ ] End card has correct links
- [ ] Total runtime under 5 minutes (attention span)
- [ ] YouTube upload complete with description/tags
- [ ] Thumbnail uploaded
- [ ] Video embedded in forum post
- [ ] Announced on X
- [ ] Added to README

---

**Notes:**
- Show, don't tell (more screen time, less talking)
- Keep energy high (this is exciting!)
- Highlight autonomy at every step
- Use real data (not fake/staged)
- End with clear CTA

---

*Ready to record when agent is deployed*  
*Built by Skipper for Luis Garcia*
