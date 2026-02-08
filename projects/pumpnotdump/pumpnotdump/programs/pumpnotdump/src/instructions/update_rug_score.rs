use anchor_lang::prelude::*;
use crate::state::*;
use crate::constants::*;
use crate::error::ErrorCode;

#[derive(Accounts)]
pub struct UpdateRugScore<'info> {
    #[account(
        mut,
        seeds = [RUG_SCORE_SEED, token_mint.key().as_ref()],
        bump = rug_score.bump
    )]
    pub rug_score: Account<'info, RugScore>,
    
    /// CHECK: Token mint, validated by PDA seeds
    pub token_mint: AccountInfo<'info>,
    
    #[account(
        seeds = [LAUNCH_SEED, agent_registry.key().as_ref(), token_mint.key().as_ref()],
        bump = launch_pad.bump
    )]
    pub launch_pad: Account<'info, LaunchPad>,
    
    #[account(
        seeds = [AGENT_SEED, agent_wallet.key().as_ref()],
        bump = agent_registry.bump
    )]
    pub agent_registry: Account<'info, AgentRegistry>,
    
    pub agent_wallet: Signer<'info>,
    
    #[account(
        seeds = [PLATFORM_SEED],
        bump = platform_state.bump
    )]
    pub platform_state: Account<'info, PlatformState>,
}

pub fn handler(
    ctx: Context<UpdateRugScore>,
    liquidity_lock_percent: Option<u8>,
    team_wallet_concentration: Option<u8>,
    is_contract_verified: Option<bool>,
    is_social_verified: Option<bool>,
) -> Result<()> {
    let rug_score = &mut ctx.accounts.rug_score;
    let old_score = rug_score.score;
    
    // Validate authority (either agent or platform admin)
    let is_agent = ctx.accounts.agent_wallet.key() == ctx.accounts.agent_registry.agent_wallet;
    let is_platform_admin = ctx.accounts.agent_wallet.key() == ctx.accounts.platform_state.authority;
    require!(is_agent || is_platform_admin, ErrorCode::UnauthorizedPlatformAction);
    
    // Update fields if provided
    if let Some(percent) = liquidity_lock_percent {
        require!(percent <= 100, ErrorCode::InvalidPercentage);
        rug_score.liquidity_lock_percent = percent;
    }
    
    if let Some(concentration) = team_wallet_concentration {
        require!(concentration <= 100, ErrorCode::InvalidPercentage);
        rug_score.team_wallet_concentration = concentration;
    }
    
    if let Some(verified) = is_contract_verified {
        rug_score.is_contract_verified = verified;
    }
    
    if let Some(verified) = is_social_verified {
        rug_score.is_social_verified = verified;
    }
    
    // Recalculate score
    rug_score.calculate_score();
    
    let clock = Clock::get()?;
    rug_score.last_updated = clock.unix_timestamp;
    
    emit!(RugScoreUpdated {
        token_mint: ctx.accounts.token_mint.key(),
        old_score,
        new_score: rug_score.score,
        timestamp: clock.unix_timestamp,
    });
    
    msg!("Rug score updated: {} -> {}", old_score, rug_score.score);
    
    Ok(())
}

#[event]
pub struct RugScoreUpdated {
    pub token_mint: Pubkey,
    pub old_score: u8,
    pub new_score: u8,
    pub timestamp: i64,
}
