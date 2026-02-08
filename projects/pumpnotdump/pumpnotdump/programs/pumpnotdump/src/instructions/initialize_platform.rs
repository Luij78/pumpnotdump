use anchor_lang::prelude::*;
use crate::state::*;
use crate::constants::*;

#[derive(Accounts)]
pub struct InitializePlatform<'info> {
    #[account(
        init,
        payer = authority,
        space = PlatformState::LEN,
        seeds = [PLATFORM_SEED],
        bump
    )]
    pub platform_state: Account<'info, PlatformState>,
    
    #[account(mut)]
    pub authority: Signer<'info>,
    
    pub system_program: Program<'info, System>,
}

pub fn handler(
    ctx: Context<InitializePlatform>,
    platform_fee_bps: u16,
    min_liquidity_lock_days: u16,
) -> Result<()> {
    let platform_state = &mut ctx.accounts.platform_state;
    
    platform_state.authority = ctx.accounts.authority.key();
    platform_state.platform_fee_bps = platform_fee_bps;
    platform_state.min_liquidity_lock_days = min_liquidity_lock_days;
    platform_state.is_paused = false;
    platform_state.total_agents_registered = 0;
    platform_state.total_tokens_launched = 0;
    platform_state.bump = ctx.bumps.platform_state;
    
    msg!("Platform initialized with fee: {} bps, min lock: {} days", 
        platform_fee_bps, min_liquidity_lock_days);
    
    Ok(())
}
