use anchor_lang::prelude::*;
use crate::state::*;
use crate::constants::*;
use crate::error::ErrorCode;

#[derive(Accounts)]
pub struct CreateTreasury<'info> {
    #[account(
        init,
        payer = agent_wallet,
        space = TreasuryVault::LEN,
        seeds = [TREASURY_SEED, agent_registry.key().as_ref(), token_mint.key().as_ref()],
        bump
    )]
    pub treasury_vault: Account<'info, TreasuryVault>,
    
    #[account(
        seeds = [AGENT_SEED, agent_wallet.key().as_ref()],
        bump = agent_registry.bump
    )]
    pub agent_registry: Account<'info, AgentRegistry>,
    
    /// CHECK: Token mint account, validated by caller
    pub token_mint: AccountInfo<'info>,
    
    #[account(mut)]
    pub agent_wallet: Signer<'info>,
    
    pub system_program: Program<'info, System>,
}

pub fn handler(
    ctx: Context<CreateTreasury>,
    time_lock_days: u16,
    max_withdrawal_per_period: u64,
    withdrawal_period_seconds: i64,
    multisig_signers: Vec<Pubkey>,
    multisig_threshold: u8,
) -> Result<()> {
    // Validate inputs
    require!(time_lock_days >= MIN_TREASURY_LOCK_DAYS, ErrorCode::TreasuryLockTooShort);
    require!(withdrawal_period_seconds > 0, ErrorCode::InvalidWithdrawalPeriod);
    require!(max_withdrawal_per_period > 0, ErrorCode::ZeroWithdrawalLimit);
    
    // Validate multisig configuration
    if !multisig_signers.is_empty() {
        require!(multisig_signers.len() <= TreasuryVault::MAX_SIGNERS, ErrorCode::TooManySigners);
        require!(multisig_threshold > 0, ErrorCode::InvalidMultisigThreshold);
        require!(
            multisig_threshold as usize <= multisig_signers.len(),
            ErrorCode::ThresholdExceedsSigners
        );
    }
    
    let clock = Clock::get()?;
    let time_lock_end = clock.unix_timestamp
        .checked_add(time_lock_days as i64 * SECONDS_PER_DAY)
        .ok_or(ErrorCode::ArithmeticOverflow)?;
    
    let treasury_vault = &mut ctx.accounts.treasury_vault;
    
    treasury_vault.agent_registry = ctx.accounts.agent_registry.key();
    treasury_vault.token_mint = ctx.accounts.token_mint.key();
    treasury_vault.authority = ctx.accounts.agent_wallet.key();
    treasury_vault.total_deposited = 0;
    treasury_vault.total_withdrawn = 0;
    treasury_vault.max_withdrawal_per_period = max_withdrawal_per_period;
    treasury_vault.withdrawal_period_seconds = withdrawal_period_seconds;
    treasury_vault.last_withdrawal_timestamp = 0;
    treasury_vault.time_lock_end_timestamp = time_lock_end;
    treasury_vault.requires_multisig = !multisig_signers.is_empty();
    treasury_vault.multisig_signers = multisig_signers;
    treasury_vault.multisig_threshold = multisig_threshold;
    treasury_vault.bump = ctx.bumps.treasury_vault;
    
    msg!("Treasury created with time lock until: {}", time_lock_end);
    
    Ok(())
}
