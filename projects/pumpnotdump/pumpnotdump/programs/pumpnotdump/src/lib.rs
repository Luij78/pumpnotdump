pub mod constants;
pub mod error;
pub mod instructions;
pub mod state;

use anchor_lang::prelude::*;

pub use constants::*;
pub use instructions::*;
pub use state::*;

declare_id!("2LKf7T24ssBf5wMAGu3Xk3ZQfM53s1rS7616uzLgWiVb");

#[program]
pub mod pumpnotdump {
    use super::*;

    /// Initialize the platform with global configuration
    pub fn initialize_platform(
        ctx: Context<InitializePlatform>,
        platform_fee_bps: u16,
        min_liquidity_lock_days: u16,
    ) -> Result<()> {
        instructions::initialize_platform::handler(ctx, platform_fee_bps, min_liquidity_lock_days)
    }

    /// Register an AI agent with metadata and social links
    pub fn register_agent(
        ctx: Context<RegisterAgent>,
        name: String,
        description: String,
        twitter_handle: String,
        website_url: String,
        github_url: String,
    ) -> Result<()> {
        instructions::register_agent::handler(
            ctx,
            name,
            description,
            twitter_handle,
            website_url,
            github_url,
        )
    }

    /// Launch a new token with rug protection parameters
    pub fn launch_token(
        ctx: Context<LaunchToken>,
        total_supply: u64,
        liquidity_percent: u8,
        team_percent: u8,
        liquidity_lock_days: u16,
        treasury_time_lock_days: u16,
        max_withdrawal_per_week: u64,
    ) -> Result<()> {
        instructions::launch_token::handler(
            ctx,
            total_supply,
            liquidity_percent,
            team_percent,
            liquidity_lock_days,
            treasury_time_lock_days,
            max_withdrawal_per_week,
        )
    }

    /// Update the rug score for a token
    pub fn update_rug_score(
        ctx: Context<UpdateRugScore>,
        liquidity_lock_percent: Option<u8>,
        team_wallet_concentration: Option<u8>,
        is_contract_verified: Option<bool>,
        is_social_verified: Option<bool>,
    ) -> Result<()> {
        instructions::update_rug_score::handler(
            ctx,
            liquidity_lock_percent,
            team_wallet_concentration,
            is_contract_verified,
            is_social_verified,
        )
    }

    /// Create a treasury vault with time locks and withdrawal limits
    pub fn create_treasury(
        ctx: Context<CreateTreasury>,
        time_lock_days: u16,
        max_withdrawal_per_period: u64,
        withdrawal_period_seconds: i64,
        multisig_signers: Vec<Pubkey>,
        multisig_threshold: u8,
    ) -> Result<()> {
        instructions::create_treasury::handler(
            ctx,
            time_lock_days,
            max_withdrawal_per_period,
            withdrawal_period_seconds,
            multisig_signers,
            multisig_threshold,
        )
    }

    /// Withdraw tokens from treasury vault
    pub fn withdraw_from_treasury(ctx: Context<WithdrawFromTreasury>, amount: u64) -> Result<()> {
        instructions::withdraw_from_treasury::handler(ctx, amount)
    }

    /// Platform admin verifies an agent
    pub fn verify_agent(ctx: Context<VerifyAgent>) -> Result<()> {
        instructions::verify_agent::handler(ctx)
    }
}
