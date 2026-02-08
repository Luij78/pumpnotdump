use anchor_lang::prelude::*;

/// Global platform configuration
#[account]
pub struct PlatformState {
    pub authority: Pubkey,
    pub platform_fee_bps: u16,
    pub min_liquidity_lock_days: u16,
    pub is_paused: bool,
    pub total_agents_registered: u64,
    pub total_tokens_launched: u64,
    pub bump: u8,
}

impl PlatformState {
    pub const LEN: usize = 8 + // discriminator
        32 + // authority
        2 +  // platform_fee_bps
        2 +  // min_liquidity_lock_days
        1 +  // is_paused
        8 +  // total_agents_registered
        8 +  // total_tokens_launched
        1;   // bump
}

/// AI Agent registration with metadata
#[account]
pub struct AgentRegistry {
    pub agent_wallet: Pubkey,
    pub name: String,
    pub description: String,
    pub twitter_handle: String,
    pub website_url: String,
    pub github_url: String,
    pub registration_timestamp: i64,
    pub is_verified: bool,
    pub tokens_launched: u32,
    pub bump: u8,
}

impl AgentRegistry {
    pub const MAX_NAME_LEN: usize = 50;
    pub const MAX_DESC_LEN: usize = 200;
    pub const MAX_TWITTER_LEN: usize = 50;
    pub const MAX_WEBSITE_LEN: usize = 100;
    pub const MAX_GITHUB_LEN: usize = 100;

    pub const LEN: usize = 8 + // discriminator
        32 + // agent_wallet
        4 + Self::MAX_NAME_LEN + // name (string length + data)
        4 + Self::MAX_DESC_LEN + // description
        4 + Self::MAX_TWITTER_LEN + // twitter_handle
        4 + Self::MAX_WEBSITE_LEN + // website_url
        4 + Self::MAX_GITHUB_LEN + // github_url
        8 + // registration_timestamp
        1 + // is_verified
        4 + // tokens_launched
        1;  // bump

    /// Validate that at least one social link is provided
    pub fn has_social_links(&self) -> bool {
        !self.twitter_handle.is_empty() || 
        !self.website_url.is_empty() || 
        !self.github_url.is_empty()
    }
}

/// On-chain rug risk scoring (0-100)
#[account]
pub struct RugScore {
    pub token_mint: Pubkey,
    pub agent_registry: Pubkey,
    pub score: u8,
    pub liquidity_lock_percent: u8,
    pub liquidity_lock_end_timestamp: i64,
    pub team_wallet_concentration: u8,
    pub is_contract_verified: bool,
    pub is_social_verified: bool,
    pub last_updated: i64,
    pub bump: u8,
}

impl RugScore {
    pub const LEN: usize = 8 + // discriminator
        32 + // token_mint
        32 + // agent_registry
        1 +  // score
        1 +  // liquidity_lock_percent
        8 +  // liquidity_lock_end_timestamp
        1 +  // team_wallet_concentration
        1 +  // is_contract_verified
        1 +  // is_social_verified
        8 +  // last_updated
        1;   // bump

    /// Calculate rug score based on multiple factors
    /// Formula: (liquidity_lock * 0.4) + ((100 - team_concentration) * 0.3) + 
    ///          (contract_verified ? 20 : 0) + (social_verified ? 10 : 0)
    pub fn calculate_score(&mut self) {
        let liquidity_score = (self.liquidity_lock_percent as u16 * 40) / 100;
        let team_score = ((100 - self.team_wallet_concentration as u16) * 30) / 100;
        let contract_score = if self.is_contract_verified { 20 } else { 0 };
        let social_score = if self.is_social_verified { 10 } else { 0 };

        self.score = (liquidity_score + team_score + contract_score + social_score)
            .min(100) as u8;
    }
}

/// Agent-controlled treasury with time locks and limits
#[account]
pub struct TreasuryVault {
    pub agent_registry: Pubkey,
    pub token_mint: Pubkey,
    pub authority: Pubkey,
    pub total_deposited: u64,
    pub total_withdrawn: u64,
    pub max_withdrawal_per_period: u64,
    pub withdrawal_period_seconds: i64,
    pub last_withdrawal_timestamp: i64,
    pub time_lock_end_timestamp: i64,
    pub requires_multisig: bool,
    pub multisig_signers: Vec<Pubkey>,
    pub multisig_threshold: u8,
    pub bump: u8,
}

impl TreasuryVault {
    pub const MAX_SIGNERS: usize = 5;

    pub const LEN: usize = 8 + // discriminator
        32 + // agent_registry
        32 + // token_mint
        32 + // authority
        8 +  // total_deposited
        8 +  // total_withdrawn
        8 +  // max_withdrawal_per_period
        8 +  // withdrawal_period_seconds
        8 +  // last_withdrawal_timestamp
        8 +  // time_lock_end_timestamp
        1 +  // requires_multisig
        4 + (32 * Self::MAX_SIGNERS) + // multisig_signers vec
        1 +  // multisig_threshold
        1;   // bump

    /// Check if withdrawal is allowed based on time lock and limits
    pub fn can_withdraw(&self, amount: u64, current_time: i64) -> bool {
        // Check time lock
        if current_time < self.time_lock_end_timestamp {
            return false;
        }

        // Check period-based withdrawal limit
        let time_since_last = current_time - self.last_withdrawal_timestamp;
        if time_since_last < self.withdrawal_period_seconds {
            // Still within the same period, check if limit exceeded
            return amount <= self.max_withdrawal_per_period;
        }

        // New period, withdrawal is allowed
        true
    }
}

/// Token launch configuration with rug protection
#[account]
pub struct LaunchPad {
    pub agent_registry: Pubkey,
    pub token_mint: Pubkey,
    pub total_supply: u64,
    pub liquidity_pool: Pubkey,
    pub liquidity_locked_amount: u64,
    pub liquidity_lock_end_timestamp: i64,
    pub team_allocation: u64,
    pub treasury_vault: Pubkey,
    pub launch_timestamp: i64,
    pub is_active: bool,
    pub bump: u8,
}

impl LaunchPad {
    pub const LEN: usize = 8 + // discriminator
        32 + // agent_registry
        32 + // token_mint
        8 +  // total_supply
        32 + // liquidity_pool
        8 +  // liquidity_locked_amount
        8 +  // liquidity_lock_end_timestamp
        8 +  // team_allocation
        32 + // treasury_vault
        8 +  // launch_timestamp
        1 +  // is_active
        1;   // bump

    /// Validate rug protection minimums
    pub fn validate_rug_protection(&self, min_liquidity_percent: u8, max_team_percent: u8) -> bool {
        let liquidity_percent = (self.liquidity_locked_amount * 100) / self.total_supply;
        let team_percent = (self.team_allocation * 100) / self.total_supply;

        liquidity_percent >= min_liquidity_percent as u64 && 
        team_percent <= max_team_percent as u64
    }
}
