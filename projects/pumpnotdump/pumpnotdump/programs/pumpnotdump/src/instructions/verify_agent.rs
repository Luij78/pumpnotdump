use anchor_lang::prelude::*;
use crate::state::*;
use crate::constants::*;
use crate::error::ErrorCode;

#[derive(Accounts)]
pub struct VerifyAgent<'info> {
    #[account(
        mut,
        seeds = [AGENT_SEED, agent_registry.agent_wallet.as_ref()],
        bump = agent_registry.bump
    )]
    pub agent_registry: Account<'info, AgentRegistry>,
    
    pub platform_authority: Signer<'info>,
    
    #[account(
        seeds = [PLATFORM_SEED],
        bump = platform_state.bump,
        has_one = authority @ ErrorCode::UnauthorizedPlatformAction
    )]
    pub platform_state: Account<'info, PlatformState>,
    
    /// CHECK: Checked via has_one constraint
    pub authority: AccountInfo<'info>,
}

pub fn handler(ctx: Context<VerifyAgent>) -> Result<()> {
    let agent_registry = &mut ctx.accounts.agent_registry;
    
    agent_registry.is_verified = true;
    
    let clock = Clock::get()?;
    
    emit!(AgentVerified {
        agent_wallet: agent_registry.agent_wallet,
        timestamp: clock.unix_timestamp,
    });
    
    msg!("Agent verified: {}", agent_registry.agent_wallet);
    
    Ok(())
}

#[event]
pub struct AgentVerified {
    pub agent_wallet: Pubkey,
    pub timestamp: i64,
}
