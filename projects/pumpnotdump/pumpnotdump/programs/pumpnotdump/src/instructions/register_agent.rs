use anchor_lang::prelude::*;
use crate::state::*;
use crate::constants::*;
use crate::error::ErrorCode;

#[derive(Accounts)]
pub struct RegisterAgent<'info> {
    #[account(
        init,
        payer = agent_wallet,
        space = AgentRegistry::LEN,
        seeds = [AGENT_SEED, agent_wallet.key().as_ref()],
        bump
    )]
    pub agent_registry: Account<'info, AgentRegistry>,
    
    #[account(mut)]
    pub agent_wallet: Signer<'info>,
    
    #[account(
        mut,
        seeds = [PLATFORM_SEED],
        bump = platform_state.bump
    )]
    pub platform_state: Account<'info, PlatformState>,
    
    pub system_program: Program<'info, System>,
}

pub fn handler(
    ctx: Context<RegisterAgent>,
    name: String,
    description: String,
    twitter_handle: String,
    website_url: String,
    github_url: String,
) -> Result<()> {
    let platform_state = &mut ctx.accounts.platform_state;
    
    // Check if platform is paused
    require!(!platform_state.is_paused, ErrorCode::PlatformPaused);
    
    // Validate input lengths
    require!(name.len() <= AgentRegistry::MAX_NAME_LEN, ErrorCode::NameTooLong);
    require!(!name.is_empty(), ErrorCode::EmptyName);
    require!(description.len() <= AgentRegistry::MAX_DESC_LEN, ErrorCode::DescriptionTooLong);
    require!(twitter_handle.len() <= AgentRegistry::MAX_TWITTER_LEN, ErrorCode::SocialLinkTooLong);
    require!(website_url.len() <= AgentRegistry::MAX_WEBSITE_LEN, ErrorCode::SocialLinkTooLong);
    require!(github_url.len() <= AgentRegistry::MAX_GITHUB_LEN, ErrorCode::SocialLinkTooLong);
    
    // At least one social link required
    require!(
        !twitter_handle.is_empty() || !website_url.is_empty() || !github_url.is_empty(),
        ErrorCode::NoSocialLinks
    );
    
    let clock = Clock::get()?;
    let agent_registry = &mut ctx.accounts.agent_registry;
    
    agent_registry.agent_wallet = ctx.accounts.agent_wallet.key();
    agent_registry.name = name.clone();
    agent_registry.description = description;
    agent_registry.twitter_handle = twitter_handle;
    agent_registry.website_url = website_url;
    agent_registry.github_url = github_url;
    agent_registry.registration_timestamp = clock.unix_timestamp;
    agent_registry.is_verified = false;
    agent_registry.tokens_launched = 0;
    agent_registry.bump = ctx.bumps.agent_registry;
    
    // Increment platform counter
    platform_state.total_agents_registered = platform_state
        .total_agents_registered
        .checked_add(1)
        .ok_or(ErrorCode::ArithmeticOverflow)?;
    
    emit!(AgentRegistered {
        agent_wallet: ctx.accounts.agent_wallet.key(),
        name,
        timestamp: clock.unix_timestamp,
    });
    
    msg!("Agent registered: {}", agent_registry.agent_wallet);
    
    Ok(())
}

#[event]
pub struct AgentRegistered {
    pub agent_wallet: Pubkey,
    pub name: String,
    pub timestamp: i64,
}
