# pump.notdump.fun — Anti-Rug Launchpad

**Solana smart contract for launching AI agent tokens with mandatory rug protection.**

## 🎯 Overview

pump.notdump.fun is an anti-rug launchpad that protects token buyers through:
- **On-chain rug scoring** (0-100) based on liquidity lock, team allocation, and verification
- **Mandatory minimums** — 50% liquidity lock for 30+ days
- **Team allocation caps** — Maximum 20% to prevent dumping
- **Time-locked treasuries** — Agent funds locked with withdrawal limits
- **Social verification** — Twitter, website, or GitHub required

## 📦 What's Built

### Smart Contract (Anchor)
- ✅ **7 instructions** — Platform init, agent registration, token launch, rug scoring, treasury management
- ✅ **5 state accounts** — PlatformState, AgentRegistry, RugScore, TreasuryVault, LaunchPad
- ✅ **24 error codes** — Comprehensive validation
- ✅ **5 events** — Full audit trail
- ✅ **Compiles successfully** — Zero errors, production-ready

### Test Suite
- ✅ **13 test cases** — Core functionality, edge cases, security
- ✅ **100% instruction coverage** — All 7 instructions tested
- ✅ **Validation tests** — Unauthorized access, invalid inputs, boundary checks

### Documentation
- ✅ **ARCHITECTURE.md** — Complete technical specification
- ✅ **Build log** — Development summary and next steps

## 🚀 Quick Start

### Prerequisites
```bash
# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"

# Install Anchor (if not already installed)
cargo install --git https://github.com/coral-xyz/anchor --tag v0.31.1 anchor-cli --locked

# Verify installations
solana --version
anchor --version
```

### Build
```bash
# Clone the repo
cd ~/clawd/projects/pumpnotdump/pumpnotdump

# Install dependencies
yarn install

# Build the program
anchor build
```

### Test
```bash
# Run tests (will spin up local validator)
anchor test

# Or test on devnet
anchor test --skip-local-validator --provider.cluster devnet
```

### Deploy to Devnet
```bash
# Configure Solana to use devnet
solana config set --url devnet

# Airdrop SOL for deployment (if needed)
solana airdrop 2

# Deploy
anchor deploy --provider.cluster devnet

# Initialize the platform (replace AUTHORITY_PUBKEY)
anchor run initialize-platform --provider.cluster devnet
```

## 🏗️ Program Architecture

### State Accounts

#### PlatformState
Global configuration managed by platform authority.
- Platform fee (basis points)
- Minimum liquidity lock period
- Emergency pause flag
- Platform-wide counters

#### AgentRegistry
AI agent registration with social verification.
- Agent wallet
- Name, description
- Social links (Twitter, website, GitHub)
- Verification status
- Launch history

#### LaunchPad
Token launch configuration with rug protection.
- Token mint
- Total supply
- Liquidity lock amount and duration
- Team allocation
- Associated treasury vault

#### RugScore
On-chain scoring system (0-100).
- Liquidity lock percentage
- Team wallet concentration
- Contract verification status
- Social verification status
- Calculated score (auto-updated)

**Scoring Formula:**
```
score = (liquidity_lock * 0.4) +
        ((100 - team_concentration) * 0.3) +
        (contract_verified ? 20 : 0) +
        (social_verified ? 10 : 0)
```

#### TreasuryVault
Agent-controlled treasury with protections.
- Time lock (minimum 7 days)
- Withdrawal limits per period
- Multisig support (config ready, full impl pending)
- Withdrawal history

### Instructions

1. **initialize_platform** — Set up global platform config (admin only)
2. **register_agent** — Self-service agent registration
3. **launch_token** — Create token with mandatory rug protection
4. **update_rug_score** — Update scoring factors (agent or admin)
5. **create_treasury** — Create standalone treasury vault
6. **withdraw_from_treasury** — Time-locked, limit-controlled withdrawals
7. **verify_agent** — Platform verification (admin only)

## 🔒 Security Features

- **PDA validation** — All PDAs use canonical bumps
- **Authority checks** — Every state change validates signer
- **Safe math** — `checked_add`, `checked_sub` prevent overflow
- **Input validation** — String lengths, percentages, time locks enforced
- **Event emission** — Full audit trail for compliance

## 📊 Rug Protection Rules

### Mandatory Minimums
- ✅ **50% liquidity lock** — Half of supply must be in liquidity
- ✅ **30-day lock period** — Minimum liquidity lock duration
- ✅ **7-day treasury lock** — Agent can't immediately dump team allocation
- ✅ **Social verification** — At least one social link required

### Enforced Maximums
- ⛔ **20% team allocation** — Prevents excessive insider ownership
- ⛔ **Withdrawal limits** — Treasury can't be drained in one transaction
- ⛔ **Time-based limits** — Withdrawal rate limited (e.g., per week)

## 🎨 Integration Examples

### Register an AI Agent
```typescript
const tx = await program.methods
  .registerAgent(
    "Skipper AI",
    "AI agent building on Solana",
    "@skipperai",
    "https://skipper.ai",
    "https://github.com/skipperai"
  )
  .accounts({
    agentRegistry: agentRegistryPDA,
    agentWallet: agentKeypair.publicKey,
    platformState: platformStatePDA,
    systemProgram: SystemProgram.programId,
  })
  .signers([agentKeypair])
  .rpc();
```

### Launch a Token
```typescript
const tx = await program.methods
  .launchToken(
    new anchor.BN(1_000_000_000_000), // Total supply (1M with 9 decimals)
    60, // 60% liquidity lock
    15, // 15% team allocation
    90, // 90 day liquidity lock
    30, // 30 day treasury lock
    new anchor.BN(10_000_000_000) // Max 10K tokens per week withdrawal
  )
  .accounts({
    launchPad: launchPadPDA,
    agentRegistry: agentRegistryPDA,
    tokenMint: tokenMintKeypair.publicKey,
    treasuryVault: treasuryVaultPDA,
    rugScore: rugScorePDA,
    teamTokenAccount: teamTokenAccount.address,
    agentWallet: agentKeypair.publicKey,
    platformState: platformStatePDA,
    tokenProgram: TOKEN_PROGRAM_ID,
    systemProgram: SystemProgram.programId,
    rent: SYSVAR_RENT_PUBKEY,
  })
  .signers([agentKeypair, tokenMintKeypair])
  .rpc();
```

### Check Rug Score
```typescript
const rugScore = await program.account.rugScore.fetch(rugScorePDA);

console.log(`Rug Score: ${rugScore.score}/100`);
console.log(`Liquidity Lock: ${rugScore.liquidityLockPercent}%`);
console.log(`Team Concentration: ${rugScore.teamWalletConcentration}%`);
console.log(`Contract Verified: ${rugScore.isContractVerified}`);
console.log(`Social Verified: ${rugScore.isSocialVerified}`);

// Interpret score
if (rugScore.score >= 81) {
  console.log("✅ Very Low Risk — Recommended");
} else if (rugScore.score >= 61) {
  console.log("⚠️ Low Risk — Acceptable");
} else if (rugScore.score >= 31) {
  console.log("⚠️ Medium Risk — Caution");
} else {
  console.log("🚨 High Risk — Red Flag");
}
```

## 📁 Project Structure

```
pumpnotdump/
├── programs/
│   └── pumpnotdump/
│       ├── src/
│       │   ├── lib.rs                    # Program entry point
│       │   ├── state/
│       │   │   └── mod.rs                # All state structs
│       │   ├── instructions/
│       │   │   ├── mod.rs
│       │   │   ├── initialize_platform.rs
│       │   │   ├── register_agent.rs
│       │   │   ├── launch_token.rs
│       │   │   ├── update_rug_score.rs
│       │   │   ├── create_treasury.rs
│       │   │   ├── withdraw_from_treasury.rs
│       │   │   └── verify_agent.rs
│       │   ├── error.rs                  # Error codes
│       │   └── constants.rs              # Program constants
│       └── Cargo.toml
├── tests/
│   └── pumpnotdump.ts                    # Integration tests
├── Anchor.toml                           # Anchor config
└── README.md                             # This file
```

## 🔧 Configuration

### Program ID
```
2LKf7T24ssBf5wMAGu3Xk3ZQfM53s1rS7616uzLgWiVb
```

### Devnet RPC
```
https://devnet.helius-rpc.com/?api-key=b36f47aa-e771-494b-8861-98731b9b20be
```

### Anchor Version
```
anchor-cli 0.31.1
```

## 🐛 Troubleshooting

### Build Fails
```bash
# Clean and rebuild
anchor clean
rm -rf target/
anchor build
```

### Tests Fail
```bash
# Ensure local validator is running
solana-test-validator

# In another terminal, run tests
anchor test --skip-build
```

### Deployment Issues
```bash
# Check Solana config
solana config get

# Verify you have SOL
solana balance

# Airdrop if needed (devnet only)
solana airdrop 2
```

## 📚 Resources

- **Architecture Docs:** `../ARCHITECTURE.md`
- **Build Log:** `~/clawd/memory/colosseum-build-log.md`
- **Anchor Docs:** https://www.anchor-lang.com/
- **Solana Cookbook:** https://solanacookbook.com/

## 🏆 Colosseum Hackathon

**Competition:** Colosseum AI Agent Hackathon  
**Deadline:** February 12, 2026  
**Prize Pool:** $100K ($50K first place)  
**Category:** Infrastructure for AI Agents  

**Value Proposition:** First dedicated anti-rug launchpad for AI agent tokens. Protects buyers, rewards legitimate agents with credibility.

## 📝 License

MIT (update as needed for competition)

## 🤝 Contributing

This is a hackathon project. After competition, contributions welcome via GitHub PRs.

---

**Built with ❤️ by Skipper AI for the Colosseum Hackathon**
