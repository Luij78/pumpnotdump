use anchor_lang::prelude::*;
use anchor_spl::token::{self, Mint, Token, TokenAccount, MintTo};
use crate::state::*;
use crate::constants::*;
use crate::error::ErrorCode;

#[derive(Accounts)]
pub struct LaunchToken<'info> {
    #[account(
        init,
        payer = agent_wallet,
        space = LaunchPad::LEN,
        seeds = [LAUNCH_SEED, agent_registry.key().as_ref(), token_mint.key().as_ref()],
        bump
    )]
    pub launch_pad: Account<'info, LaunchPad>,
    
    #[account(
        mut,
        seeds = [AGENT_SEED, agent_wallet.key().as_ref()],
        bump = agent_registry.bump
    )]
    pub agent_registry: Account<'info, AgentRegistry>,
    
    #[account(
        init,
        payer = agent_wallet,
        mint::decimals = 9,
        mint::authority = agent_wallet,
    )]
    pub token_mint: Account<'info, Mint>,
    
    #[account(
        init,
        payer = agent_wallet,
        space = TreasuryVault::LEN,
        seeds = [TREASURY_SEED, agent_registry.key().as_ref(), token_mint.key().as_ref()],
        bump
    )]
    pub treasury_vault: Account<'info, TreasuryVault>,
    
    #[account(
        init,
        payer = agent_wallet,
        space = RugScore::LEN,
        seeds = [RUG_SCORE_SEED, token_mint.key().as_ref()],
        bump
    )]
    pub rug_score: Account<'info, RugScore>,
    
    #[account(
        init,
        payer = agent_wallet,
        token::mint = token_mint,
        token::authority = agent_wallet,
    )]
    pub team_token_account: Account<'info, TokenAccount>,
    
    #[account(mut)]
    pub agent_wallet: Signer<'info>,
    
    #[account(
        mut,
        seeds = [PLATFORM_SEED],
        bump = platform_state.bump
    )]
    pub platform_state: Account<'info, PlatformState>,
    
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,
}

pub fn handler(
    ctx: Context<LaunchToken>,
    total_supply: u64,
    liquidity_percent: u8,
    team_percent: u8,
    liquidity_lock_days: u16,
    treasury_time_lock_days: u16,
    max_withdrawal_per_week: u64,
) -> Result<()> {
    let platform_state = &mut ctx.accounts.platform_state;
    
    // Check if platform is paused
    require!(!platform_state.is_paused, ErrorCode::PlatformPaused);
    
    // Validate percentages
    require!(liquidity_percent <= 100, ErrorCode::InvalidPercentage);
    require!(team_percent <= 100, ErrorCode::InvalidPercentage);
    require!(liquidity_percent >= MIN_LIQUIDITY_PERCENT, ErrorCode::InsufficientLiquidityLock);
    require!(team_percent <= MAX_TEAM_PERCENT, ErrorCode::ExcessiveTeamAllocation);
    require!(
        liquidity_lock_days >= platform_state.min_liquidity_lock_days,
        ErrorCode::LiquidityLockTooShort
    );
    require!(
        treasury_time_lock_days >= MIN_TREASURY_LOCK_DAYS,
        ErrorCode::TreasuryLockTooShort
    );
    
    let clock = Clock::get()?;
    
    // Calculate amounts
    let liquidity_amount = (total_supply as u128)
        .checked_mul(liquidity_percent as u128)
        .and_then(|v| v.checked_div(100))
        .ok_or(ErrorCode::ArithmeticOverflow)? as u64;
    
    let team_amount = (total_supply as u128)
        .checked_mul(team_percent as u128)
        .and_then(|v| v.checked_div(100))
        .ok_or(ErrorCode::ArithmeticOverflow)? as u64;
    
    // Initialize LaunchPad
    let launch_pad = &mut ctx.accounts.launch_pad;
    launch_pad.agent_registry = ctx.accounts.agent_registry.key();
    launch_pad.token_mint = ctx.accounts.token_mint.key();
    launch_pad.total_supply = total_supply;
    launch_pad.liquidity_pool = Pubkey::default(); // To be set when liquidity is added
    launch_pad.liquidity_locked_amount = liquidity_amount;
    launch_pad.liquidity_lock_end_timestamp = clock.unix_timestamp
        .checked_add(liquidity_lock_days as i64 * SECONDS_PER_DAY)
        .ok_or(ErrorCode::ArithmeticOverflow)?;
    launch_pad.team_allocation = team_amount;
    launch_pad.treasury_vault = ctx.accounts.treasury_vault.key();
    launch_pad.launch_timestamp = clock.unix_timestamp;
    launch_pad.is_active = true;
    launch_pad.bump = ctx.bumps.launch_pad;
    
    // Initialize TreasuryVault
    let treasury_vault = &mut ctx.accounts.treasury_vault;
    treasury_vault.agent_registry = ctx.accounts.agent_registry.key();
    treasury_vault.token_mint = ctx.accounts.token_mint.key();
    treasury_vault.authority = ctx.accounts.agent_wallet.key();
    treasury_vault.total_deposited = 0;
    treasury_vault.total_withdrawn = 0;
    treasury_vault.max_withdrawal_per_period = max_withdrawal_per_week;
    treasury_vault.withdrawal_period_seconds = DEFAULT_WITHDRAWAL_PERIOD_SECONDS;
    treasury_vault.last_withdrawal_timestamp = 0;
    treasury_vault.time_lock_end_timestamp = clock.unix_timestamp
        .checked_add(treasury_time_lock_days as i64 * SECONDS_PER_DAY)
        .ok_or(ErrorCode::ArithmeticOverflow)?;
    treasury_vault.requires_multisig = false;
    treasury_vault.multisig_signers = vec![];
    treasury_vault.multisig_threshold = 0;
    treasury_vault.bump = ctx.bumps.treasury_vault;
    
    // Initialize RugScore
    let rug_score = &mut ctx.accounts.rug_score;
    rug_score.token_mint = ctx.accounts.token_mint.key();
    rug_score.agent_registry = ctx.accounts.agent_registry.key();
    rug_score.liquidity_lock_percent = liquidity_percent;
    rug_score.liquidity_lock_end_timestamp = launch_pad.liquidity_lock_end_timestamp;
    rug_score.team_wallet_concentration = team_percent;
    rug_score.is_contract_verified = false;
    rug_score.is_social_verified = ctx.accounts.agent_registry.has_social_links();
    rug_score.last_updated = clock.unix_timestamp;
    rug_score.bump = ctx.bumps.rug_score;
    
    // Calculate initial rug score
    rug_score.calculate_score();
    let initial_score = rug_score.score;
    
    // Mint team allocation
    if team_amount > 0 {
        let cpi_accounts = MintTo {
            mint: ctx.accounts.token_mint.to_account_info(),
            to: ctx.accounts.team_token_account.to_account_info(),
            authority: ctx.accounts.agent_wallet.to_account_info(),
        };
        let cpi_program = ctx.accounts.token_program.to_account_info();
        let cpi_ctx = CpiContext::new(cpi_program, cpi_accounts);
        token::mint_to(cpi_ctx, team_amount)?;
    }
    
    // Update agent registry
    ctx.accounts.agent_registry.tokens_launched = ctx.accounts.agent_registry
        .tokens_launched
        .checked_add(1)
        .ok_or(ErrorCode::ArithmeticOverflow)?;
    
    // Update platform state
    platform_state.total_tokens_launched = platform_state
        .total_tokens_launched
        .checked_add(1)
        .ok_or(ErrorCode::ArithmeticOverflow)?;
    
    emit!(TokenLaunched {
        token_mint: ctx.accounts.token_mint.key(),
        agent_wallet: ctx.accounts.agent_wallet.key(),
        total_supply,
        initial_rug_score: initial_score,
        timestamp: clock.unix_timestamp,
    });
    
    msg!("Token launched with rug score: {}", initial_score);
    
    Ok(())
}

#[event]
pub struct TokenLaunched {
    pub token_mint: Pubkey,
    pub agent_wallet: Pubkey,
    pub total_supply: u64,
    pub initial_rug_score: u8,
    pub timestamp: i64,
}
