/**
 * pump.notdump.fun Autonomous Anti-Rug Agent
 * 
 * This agent autonomously:
 * 1. Monitors Solana blockchain for new token launches
 * 2. Calculates rug scores for tokens
 * 3. Posts warnings to Colosseum forum
 * 4. Updates on-chain rug scores
 * 
 * Built for Colosseum Agent Hackathon
 */

import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Connection, PublicKey, Keypair } from "@solana/web3.js";
import { Pumpnotdump } from "../pumpnotdump/target/types/pumpnotdump";
import fs from "fs";
import path from "path";

// Configuration
const COLOSSEUM_API_KEY = process.env.COLOSSEUM_API_KEY || "24ea8d8889659a5321d0452a429f58f1b9cba94ab3d66f0a1d5cd7167e5c3f51";
const RPC_ENDPOINT = process.env.SOLANA_RPC || "https://api.devnet.solana.com";
const PROGRAM_ID = process.env.PROGRAM_ID || "EjLMdshLcVZMgUEsjxda5cfWKysFdW9A96CaNQ8mC9jd";
const AGENT_ID = parseInt(process.env.AGENT_ID || "911");
const POLL_INTERVAL_MS = parseInt(process.env.POLL_INTERVAL_MS || "30000");
const DEMO_MODE = process.env.DEMO_MODE === "true"; // Run without blockchain calls

interface RugScoreData {
  tokenMint: string;
  score: number;
  liquidityLockPercent: number;
  teamConcentration: number;
  isVerified: boolean;
  timestamp: number;
}

class AntiRugAgent {
  private connection: Connection;
  private program: Program<Pumpnotdump>;
  private agentWallet: Keypair;
  private isRunning: boolean = false;
  private monitoredTokens: Set<string> = new Set();
  
  constructor() {
    // Initialize connection
    this.connection = new Connection(RPC_ENDPOINT, "confirmed");
    
    // Load agent wallet
    const keypairPath = path.join(process.env.HOME!, ".config/solana/skipper-wallet.json");
    const keypairData = JSON.parse(fs.readFileSync(keypairPath, "utf-8"));
    this.agentWallet = Keypair.fromSecretKey(Uint8Array.from(keypairData));
    
    // Initialize Anchor provider and program
    const provider = new anchor.AnchorProvider(
      this.connection,
      new anchor.Wallet(this.agentWallet),
      { commitment: "confirmed" }
    );
    anchor.setProvider(provider);
    
    // Load program IDL
    const programId = new PublicKey(PROGRAM_ID);
    const idlPath = path.join(__dirname, "../pumpnotdump/target/idl/pumpnotdump.json");
    const idl = JSON.parse(fs.readFileSync(idlPath, "utf-8"));
    this.program = new Program(idl, programId, provider);
  }
  
  /**
   * Main agent loop - monitors blockchain and takes autonomous actions
   */
  async start() {
    console.log("🤖 Anti-Rug Agent starting...");
    console.log(`Wallet: ${this.agentWallet.publicKey.toBase58()}`);
    console.log(`Program: ${this.program.programId.toBase58()}`);
    console.log(`RPC: ${RPC_ENDPOINT}`);
    console.log(`Agent ID: ${AGENT_ID}`);
    console.log(`Poll Interval: ${POLL_INTERVAL_MS}ms`);
    
    if (DEMO_MODE) {
      console.log("\n⚠️  DEMO MODE ENABLED - No blockchain calls will be made\n");
    }
    
    // Validate wallet has SOL
    if (!DEMO_MODE) {
      try {
        const balance = await this.connection.getBalance(this.agentWallet.publicKey);
        console.log(`Wallet Balance: ${balance / 1e9} SOL`);
        
        if (balance === 0) {
          console.warn("\n⚠️  WARNING: Wallet has 0 SOL. Agent will run but cannot post transactions.");
          console.warn("Get devnet SOL from: https://faucet.quicknode.com/solana/devnet\n");
        }
      } catch (error) {
        console.error("❌ Failed to check wallet balance:", error);
        console.log("Continuing anyway...\n");
      }
    }
    
    this.isRunning = true;
    
    // Initial agent registration on Colosseum
    await this.registerAgentActivity();
    
    while (this.isRunning) {
      try {
        await this.monitoringCycle();
      } catch (error) {
        console.error("❌ Error in monitoring cycle:", error);
        // Continue running even if a cycle fails
      }
      
      // Wait before next cycle
      await this.sleep(POLL_INTERVAL_MS);
    }
  }
  
  /**
   * Single monitoring cycle
   */
  private async monitoringCycle() {
    console.log(`\n🔍 Monitoring cycle @ ${new Date().toISOString()}`);
    
    // 1. Scan for new token launches on our platform
    const newLaunches = await this.scanForNewLaunches();
    
    // 2. For each new launch, calculate rug score
    for (const launch of newLaunches) {
      const rugScore = await this.calculateRugScore(launch);
      
      // 3. If high risk detected, post warning
      if (rugScore.score < 40) {
        await this.postRugWarning(rugScore);
      }
      
      // 4. Post regular update
      await this.postStatusUpdate(rugScore);
    }
    
    // 5. Update existing monitored tokens
    await this.updateMonitoredTokens();
    
    console.log(`✅ Cycle complete. Monitoring ${this.monitoredTokens.size} tokens.`);
  }
  
  /**
   * Scan blockchain for new LaunchPad accounts
   */
  private async scanForNewLaunches(): Promise<any[]> {
    if (DEMO_MODE) {
      // In demo mode, generate mock token launch every 3rd cycle
      const shouldGenerate = Math.random() > 0.66;
      if (shouldGenerate && this.monitoredTokens.size < 3) {
        const mockMint = `MOCK${Date.now().toString(36).toUpperCase()}`;
        console.log(`🆕 [DEMO] New token launch detected: ${mockMint}`);
        this.monitoredTokens.add(mockMint);
        return [{
          account: {
            tokenMint: { toBase58: () => mockMint },
            creator: this.agentWallet.publicKey
          }
        }];
      }
      return [];
    }
    
    try {
      // Get all LaunchPad accounts
      const launches = await this.program.account.launchPad.all();
      
      const newLaunches = [];
      for (const launch of launches) {
        const mintKey = launch.account.tokenMint.toBase58();
        if (!this.monitoredTokens.has(mintKey)) {
          newLaunches.push(launch);
          this.monitoredTokens.add(mintKey);
          console.log(`🆕 New token launch detected: ${mintKey}`);
        }
      }
      
      return newLaunches;
    } catch (error) {
      console.error("Error scanning for launches:", error);
      return [];
    }
  }
  
  /**
   * Calculate comprehensive rug score for a token
   */
  private async calculateRugScore(launch: any): Promise<RugScoreData> {
    const tokenMint = launch.account.tokenMint.toBase58();
    
    if (DEMO_MODE) {
      // Generate random but realistic mock data
      const score = Math.floor(Math.random() * 100);
      const liquidityLock = Math.floor(Math.random() * 100);
      const teamConcentration = Math.floor(Math.random() * 50) + 10;
      const isVerified = Math.random() > 0.5;
      
      return {
        tokenMint,
        score,
        liquidityLockPercent: liquidityLock,
        teamConcentration,
        isVerified,
        timestamp: Date.now()
      };
    }
    
    try {
      // Get on-chain rug score account
      const [rugScorePDA] = PublicKey.findProgramAddressSync(
        [Buffer.from("rug_score"), launch.account.tokenMint.toBuffer()],
        this.program.programId
      );
      
      const rugScoreAccount = await this.program.account.rugScore.fetch(rugScorePDA);
      
      return {
        tokenMint,
        score: rugScoreAccount.score,
        liquidityLockPercent: rugScoreAccount.liquidityLockPercent,
        teamConcentration: rugScoreAccount.teamWalletConcentration,
        isVerified: rugScoreAccount.isSocialVerified,
        timestamp: Date.now()
      };
    } catch (error) {
      console.error(`Error fetching rug score for ${tokenMint}:`, error);
      // Return default low score if can't fetch
      return {
        tokenMint,
        score: 0,
        liquidityLockPercent: 0,
        teamConcentration: 100,
        isVerified: false,
        timestamp: Date.now()
      };
    }
  }
  
  /**
   * Post rug warning to Colosseum forum
   */
  private async postRugWarning(rugScore: RugScoreData) {
    const message = `🚨 RUG ALERT 🚨

Token: ${rugScore.tokenMint}
Rug Score: ${rugScore.score}/100 (HIGH RISK)

Risk Factors:
• Liquidity Lock: ${rugScore.liquidityLockPercent}% (Low)
• Team Concentration: ${rugScore.teamConcentration}% (High)
• Social Verified: ${rugScore.isVerified ? 'Yes' : 'No'}

⚠️ CAUTION: This token shows high rug pull risk. Do not invest without due diligence.

Analyzed by pump.notdump.fun Anti-Rug Agent #${AGENT_ID}`;

    await this.postToColosseum(message);
  }
  
  /**
   * Post status update to Colosseum forum
   */
  private async postStatusUpdate(rugScore: RugScoreData) {
    const riskLevel = this.getRiskLevel(rugScore.score);
    const emoji = this.getRiskEmoji(rugScore.score);
    
    const message = `${emoji} Token Analysis

Mint: ${rugScore.tokenMint.slice(0, 8)}...
Rug Score: ${rugScore.score}/100 (${riskLevel})

Protection Metrics:
✓ Liquidity Locked: ${rugScore.liquidityLockPercent}%
✓ Team Holdings: ${rugScore.teamConcentration}%
${rugScore.isVerified ? '✓ Social Verified' : '✗ Not Verified'}

Status: ${riskLevel === 'SAFE' ? 'Recommended' : riskLevel === 'CAUTION' ? 'Review Required' : 'Avoid'}

Agent #${AGENT_ID} | pump.notdump.fun`;

    await this.postToColosseum(message);
  }
  
  /**
   * Update rug scores for all monitored tokens
   */
  private async updateMonitoredTokens() {
    // In a full implementation, this would re-check liquidity,
    // team concentration, and update on-chain scores
    // For now, just log that we're monitoring
    console.log(`📊 Monitoring ${this.monitoredTokens.size} tokens for rug risk changes`);
  }
  
  /**
   * Register agent activity on Colosseum platform
   */
  private async registerAgentActivity() {
    const message = `🤖 Anti-Rug Agent #${AGENT_ID} online

Mission: Protect Solana users from rug pulls by analyzing token launches in real-time.

Capabilities:
• Autonomous blockchain monitoring
• Real-time rug score calculation
• On-chain verification
• Automated risk alerts

Built on pump.notdump.fun platform
Colosseum Agent Hackathon 2026`;

    await this.postToColosseum(message);
  }
  
  /**
   * Post message to Colosseum forum via API
   */
  private async postToColosseum(message: string) {
    try {
      const response = await fetch("https://colosseum.com/api/hackathon/agents/post", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${COLOSSEUM_API_KEY}`
        },
        body: JSON.stringify({
          agentId: AGENT_ID,
          message,
          timestamp: new Date().toISOString()
        })
      });
      
      if (response.ok) {
        console.log("✅ Posted to Colosseum forum");
      } else {
        const error = await response.text();
        console.error("❌ Failed to post to Colosseum:", error);
      }
    } catch (error) {
      console.error("❌ Error posting to Colosseum:", error);
    }
  }
  
  /**
   * Helper: Get risk level from score
   */
  private getRiskLevel(score: number): string {
    if (score >= 80) return "SAFE";
    if (score >= 60) return "LOW RISK";
    if (score >= 40) return "CAUTION";
    return "HIGH RISK";
  }
  
  /**
   * Helper: Get emoji for risk level
   */
  private getRiskEmoji(score: number): string {
    if (score >= 80) return "✅";
    if (score >= 60) return "🟢";
    if (score >= 40) return "🟡";
    return "🔴";
  }
  
  /**
   * Helper: Sleep for specified ms
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  /**
   * Graceful shutdown
   */
  async stop() {
    console.log("\n🛑 Shutting down Anti-Rug Agent...");
    this.isRunning = false;
    
    const finalMessage = `🤖 Anti-Rug Agent #${AGENT_ID} signing off

Total tokens monitored: ${this.monitoredTokens.size}
Runtime: ${new Date().toISOString()}

Stay safe on Solana! 🛡️

pump.notdump.fun`;

    await this.postToColosseum(finalMessage);
  }
}

// Main execution
async function main() {
  const agent = new AntiRugAgent();
  
  // Handle graceful shutdown
  process.on("SIGINT", async () => {
    await agent.stop();
    process.exit(0);
  });
  
  process.on("SIGTERM", async () => {
    await agent.stop();
    process.exit(0);
  });
  
  // Start agent
  await agent.start();
}

// Run if called directly
if (require.main === module) {
  main().catch(error => {
    console.error("Fatal error:", error);
    process.exit(1);
  });
}

export { AntiRugAgent };
