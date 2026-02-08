# pump.notdump.fun — Smart Contract Architecture

## Overview
Anti-rug launchpad for AI agent tokens on Solana. Provides on-chain verification, rug scoring, and treasury controls to protect token buyers.

## Program ID
`2LKf7T24ssBf5wMAGu3Xk3ZQfM53s1rS7616uzLgWiVb`

## Core Components

### 1. PlatformState (Global Config)
**PDA Seeds:** `["platform"]`

**Purpose:** Global platform configuration and authority management.

**Fields:**
- `authority: Pubkey` — Platform admin (can update fees, pause)
- `platform_fee_bps: u16` — Platform fee in basis points (default: 100 = 1%)
- `min_liquidity_lock_days: u16` — Minimum liquidity lock period (default: 30 days)
- `is_paused: bool` — Emergency pause flag
- `total_agents_registered: u64` — Counter
- `total_tokens_launched: u64` — Counter
- `bump: u8` — PDA bump

### 2. AgentRegistry
**PDA Seeds:** `["agent", agent_wallet.key()]`

**Purpose:** Register AI agents with verified metadata and social proof.

**Fields:**
- `agent_wallet: Pubkey` — Agent's primary wallet (authority)
- `name: String` — Agent name (max 50 chars)
- `description: String` — Agent description (max 200 chars)
- `twitter_handle: String` — Verified Twitter handle (max 50 chars)
- `website_url: String` — Agent website (max 100 chars)
- `github_url: String` — GitHub repo (max 100 chars)
- `registration_timestamp: i64` — Unix timestamp
- `is_verified: bool` — Platform verification status
- `tokens_launched: u32` — Number of tokens launched by this agent
- `bump: u8` — PDA bump

**Validation Rules:**
- Name must be unique and non-empty
- At least one social link required (Twitter, website, or GitHub)
- Agent wallet must sign registration

### 3. RugScore
**PDA Seeds:** `["rug_score", token_mint.key()]`

**Purpose:** On-chain scoring system (0-100) to quantify rug risk.

**Fields:**
- `token_mint: Pubkey` — Associated token mint
- `agent_registry: Pubkey` — Link to agent who launched
- `score: u8` — Current rug score (0-100, higher = safer)
- `liquidity_lock_percent: u8` — % of liquidity locked (0-100)
- `liquidity_lock_end_timestamp: i64` — When liquidity unlocks
- `team_wallet_concentration: u8` — % held by team (0-100)
- `is_contract_verified: bool` — Smart contract audit status
- `is_social_verified: bool` — Social media verification
- `last_updated: i64` — Last score update timestamp
- `bump: u8` — PDA bump

**Scoring Algorithm:**
```
score = (liquidity_lock_percent * 0.4) +
        ((100 - team_wallet_concentration) * 0.3) +
        (is_contract_verified ? 20 : 0) +
        (is_social_verified ? 10 : 0)
```

**Score Interpretation:**
- 0-30: High Risk (Red flag)
- 31-60: Medium Risk (Caution)
- 61-80: Low Risk (Acceptable)
- 81-100: Very Low Risk (Recommended)

### 4. TreasuryVault
**PDA Seeds:** `["treasury", agent_registry.key(), token_mint.key()]`

**Purpose:** Secure treasury with time-locked withdrawals and limits.

**Fields:**
- `agent_registry: Pubkey` — Linked agent
- `token_mint: Pubkey` — Token being managed
- `authority: Pubkey` — Agent wallet that can withdraw
- `total_deposited: u64` — Total tokens deposited
- `total_withdrawn: u64` — Total tokens withdrawn
- `max_withdrawal_per_period: u64` — Max tokens per period
- `withdrawal_period_seconds: i64` — Time period (default: 7 days)
- `last_withdrawal_timestamp: i64` — Last withdrawal time
- `time_lock_end_timestamp: i64` — When withdrawals can start
- `requires_multisig: bool` — If true, needs multiple signers
- `multisig_signers: Vec<Pubkey>` — List of approved signers (max 5)
- `multisig_threshold: u8` — Signatures required (e.g., 2 of 3)
- `bump: u8` — PDA bump

**Withdrawal Rules:**
- Cannot withdraw before `time_lock_end_timestamp`
- Cannot exceed `max_withdrawal_per_period` within `withdrawal_period_seconds`
- If multisig enabled, requires `multisig_threshold` signatures
- All withdrawals logged on-chain

### 5. LaunchPad
**PDA Seeds:** `["launch", agent_registry.key(), token_mint.key()]`

**Purpose:** Token launch configuration with mandatory rug protection.

**Fields:**
- `agent_registry: Pubkey` — Agent launching the token
- `token_mint: Pubkey` — Token mint account
- `total_supply: u64` — Total token supply
- `liquidity_pool: Pubkey` — Associated liquidity pool (Raydium/Orca)
- `liquidity_locked_amount: u64` — Tokens locked in liquidity
- `liquidity_lock_end_timestamp: i64` — When liquidity unlocks
- `team_allocation: u64` — Tokens allocated to team
- `treasury_vault: Pubkey` — Associated treasury vault
- `launch_timestamp: i64` — When token was launched
- `is_active: bool` — Launch status
- `bump: u8` — PDA bump

**Mandatory Rug Protection:**
- Minimum 50% of supply must be locked in liquidity
- Liquidity lock minimum: 30 days (configurable in PlatformState)
- Team allocation cannot exceed 20% of total supply
- Treasury must have time lock (minimum 7 days)
- Must have valid AgentRegistry with at least one social link

## Instructions

### 1. `initialize_platform`
**Accounts:**
- `platform_state` (init, mut) — PlatformState PDA
- `authority` (signer) — Platform admin
- `system_program`

**Args:**
- `platform_fee_bps: u16` — Initial platform fee
- `min_liquidity_lock_days: u16` — Minimum lock period

**Logic:**
- Creates global PlatformState
- Sets initial configuration
- Initializes counters

### 2. `register_agent`
**Accounts:**
- `agent_registry` (init, mut) — AgentRegistry PDA
- `agent_wallet` (signer, mut) — Agent's wallet (pays rent)
- `platform_state` (mut) — Increment counter
- `system_program`

**Args:**
- `name: String`
- `description: String`
- `twitter_handle: String`
- `website_url: String`
- `github_url: String`

**Logic:**
- Validates input lengths
- Requires at least one social link
- Creates AgentRegistry PDA
- Increments platform counter
- Emits `AgentRegistered` event

### 3. `launch_token`
**Accounts:**
- `launch_pad` (init, mut) — LaunchPad PDA
- `agent_registry` (mut) — Must be registered agent
- `token_mint` (init, mut) — New token mint
- `treasury_vault` (init, mut) — TreasuryVault PDA
- `rug_score` (init, mut) — RugScore PDA
- `agent_wallet` (signer, mut) — Pays rent + signs
- `platform_state` (mut) — Increment counter
- `token_program`
- `system_program`
- `rent`

**Args:**
- `total_supply: u64`
- `liquidity_percent: u8` — % to lock (min 50)
- `team_percent: u8` — % to team (max 20)
- `liquidity_lock_days: u16` — Lock duration (min 30)
- `treasury_time_lock_days: u16` — Treasury lock (min 7)
- `max_withdrawal_per_week: u64`

**Logic:**
- Validates agent is registered
- Checks rug protection minimums (liquidity ≥50%, team ≤20%)
- Creates token mint
- Initializes LaunchPad, TreasuryVault, RugScore
- Calculates initial rug score
- Mints tokens to appropriate accounts
- Emits `TokenLaunched` event

### 4. `update_rug_score`
**Accounts:**
- `rug_score` (mut) — RugScore PDA
- `launch_pad` — Associated launch
- `agent_registry` — Linked agent
- `authority` (signer) — Platform admin or agent

**Args:**
- `liquidity_lock_percent: Option<u8>`
- `team_wallet_concentration: Option<u8>`
- `is_contract_verified: Option<bool>`
- `is_social_verified: Option<bool>`

**Logic:**
- Updates provided fields
- Recalculates score using algorithm
- Updates timestamp
- Emits `RugScoreUpdated` event

### 5. `create_treasury`
**Accounts:**
- `treasury_vault` (init, mut) — TreasuryVault PDA
- `agent_registry` — Must be registered agent
- `token_mint` — Token to manage
- `agent_wallet` (signer, mut) — Pays rent
- `system_program`

**Args:**
- `time_lock_days: u16`
- `max_withdrawal_per_period: u64`
- `withdrawal_period_seconds: i64`
- `multisig_signers: Vec<Pubkey>`
- `multisig_threshold: u8`

**Logic:**
- Creates TreasuryVault PDA
- Sets withdrawal limits
- Configures multisig if signers provided
- Validates threshold ≤ signers.len()

### 6. `withdraw_from_treasury`
**Accounts:**
- `treasury_vault` (mut) — TreasuryVault PDA
- `agent_wallet` (signer) — Must be authority
- `token_account_from` (mut) — Vault's token account
- `token_account_to` (mut) — Recipient token account
- `token_program`

**Args:**
- `amount: u64`

**Logic:**
- Checks time lock has passed
- Validates withdrawal limit not exceeded in period
- If multisig: verify signatures (future: use additional signers)
- Transfers tokens
- Updates counters and timestamp
- Emits `TreasuryWithdrawal` event

### 7. `verify_agent`
**Accounts:**
- `agent_registry` (mut) — Agent to verify
- `platform_authority` (signer) — Platform admin only
- `platform_state` — Verify authority

**Args:** None

**Logic:**
- Platform admin marks agent as verified
- Updates `is_verified` flag
- Emits `AgentVerified` event

## Events

```rust
#[event]
pub struct AgentRegistered {
    pub agent_wallet: Pubkey,
    pub name: String,
    pub timestamp: i64,
}

#[event]
pub struct TokenLaunched {
    pub token_mint: Pubkey,
    pub agent_wallet: Pubkey,
    pub total_supply: u64,
    pub initial_rug_score: u8,
    pub timestamp: i64,
}

#[event]
pub struct RugScoreUpdated {
    pub token_mint: Pubkey,
    pub old_score: u8,
    pub new_score: u8,
    pub timestamp: i64,
}

#[event]
pub struct TreasuryWithdrawal {
    pub treasury_vault: Pubkey,
    pub amount: u64,
    pub recipient: Pubkey,
    pub timestamp: i64,
}

#[event]
pub struct AgentVerified {
    pub agent_wallet: Pubkey,
    pub timestamp: i64,
}
```

## Security Considerations

1. **PDA Validation:** All PDAs use canonical bumps and proper seeds
2. **Signer Checks:** All state changes require appropriate signer verification
3. **Integer Overflow:** Use `checked_add`, `checked_sub` for all math
4. **Reentrancy:** No cross-program invocations that could create reentrancy
5. **Time Validation:** All timestamps use `Clock::get()?.unix_timestamp`
6. **Input Validation:** All strings have max lengths, percentages bounded 0-100
7. **Authority Checks:** Only platform admin can verify agents, update platform state

## Dependencies

```toml
[dependencies]
anchor-lang = "0.31.1"
anchor-spl = "0.31.1"  # For SPL token operations
```

## Testing Strategy

1. **Unit Tests:** Test scoring algorithm, withdrawal limits, time locks
2. **Integration Tests:** Full launch flow, treasury withdrawals, score updates
3. **Edge Cases:** Zero amounts, boundary values, expired time locks
4. **Security Tests:** Unauthorized access, invalid PDAs, overflow attempts

## Future Enhancements (Post-MVP)

- Real multisig implementation with transaction proposal system
- Liquidity pool integration (Raydium/Orca)
- On-chain oracle integration for price feeds
- Governance system for platform parameter updates
- Agent reputation scores based on historical launches
- Automated rug detection monitoring

---

**Built for Colosseum Hackathon | Deadline: Feb 12, 2026**
