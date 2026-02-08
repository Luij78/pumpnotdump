use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount, Transfer};
use crate::state::*;
use crate::constants::*;
use crate::error::ErrorCode;

#[derive(Accounts)]
pub struct WithdrawFromTreasury<'info> {
    #[account(
        mut,
        seeds = [TREASURY_SEED, agent_registry.key().as_ref(), token_mint.key().as_ref()],
        bump = treasury_vault.bump,
    )]
    pub treasury_vault: Account<'info, TreasuryVault>,
    
    #[account(
        seeds = [AGENT_SEED, agent_wallet.key().as_ref()],
        bump = agent_registry.bump
    )]
    pub agent_registry: Account<'info, AgentRegistry>,
    
    /// CHECK: Token mint, validated by PDA seeds
    pub token_mint: AccountInfo<'info>,
    
    #[account(mut)]
    pub agent_wallet: Signer<'info>,
    
    #[account(
        mut,
        token::mint = token_mint,
        token::authority = treasury_vault,
    )]
    pub vault_token_account: Account<'info, TokenAccount>,
    
    #[account(
        mut,
        token::mint = token_mint,
    )]
    pub recipient_token_account: Account<'info, TokenAccount>,
    
    pub token_program: Program<'info, Token>,
}

pub fn handler(ctx: Context<WithdrawFromTreasury>, amount: u64) -> Result<()> {
    let treasury_vault = &mut ctx.accounts.treasury_vault;
    let clock = Clock::get()?;
    let current_time = clock.unix_timestamp;
    
    // Check authority
    require!(
        treasury_vault.authority == ctx.accounts.agent_wallet.key(),
        ErrorCode::UnauthorizedPlatformAction
    );
    
    // Check time lock
    require!(
        current_time >= treasury_vault.time_lock_end_timestamp,
        ErrorCode::TimeLockActive
    );
    
    // Check withdrawal limits
    require!(
        treasury_vault.can_withdraw(amount, current_time),
        ErrorCode::WithdrawalLimitExceeded
    );
    
    // Check sufficient funds
    require!(
        ctx.accounts.vault_token_account.amount >= amount,
        ErrorCode::InsufficientTreasuryFunds
    );
    
    // Note: Full multisig implementation would require additional signers
    // For MVP, we just check if multisig is required and warn
    if treasury_vault.requires_multisig {
        msg!("Warning: Multisig required but not fully implemented in MVP");
        // In production, would verify additional signers here
    }
    
    // Perform transfer using PDA as authority
    let agent_registry_key = ctx.accounts.agent_registry.key();
    let token_mint_key = ctx.accounts.token_mint.key();
    let seeds = &[
        TREASURY_SEED,
        agent_registry_key.as_ref(),
        token_mint_key.as_ref(),
        &[treasury_vault.bump],
    ];
    let signer_seeds = &[&seeds[..]];
    
    let cpi_accounts = Transfer {
        from: ctx.accounts.vault_token_account.to_account_info(),
        to: ctx.accounts.recipient_token_account.to_account_info(),
        authority: treasury_vault.to_account_info(),
    };
    let cpi_program = ctx.accounts.token_program.to_account_info();
    let cpi_ctx = CpiContext::new_with_signer(cpi_program, cpi_accounts, signer_seeds);
    token::transfer(cpi_ctx, amount)?;
    
    // Update treasury state
    treasury_vault.total_withdrawn = treasury_vault
        .total_withdrawn
        .checked_add(amount)
        .ok_or(ErrorCode::ArithmeticOverflow)?;
    treasury_vault.last_withdrawal_timestamp = current_time;
    
    emit!(TreasuryWithdrawal {
        treasury_vault: ctx.accounts.treasury_vault.key(),
        amount,
        recipient: ctx.accounts.recipient_token_account.key(),
        timestamp: current_time,
    });
    
    msg!("Withdrew {} tokens from treasury", amount);
    
    Ok(())
}

#[event]
pub struct TreasuryWithdrawal {
    pub treasury_vault: Pubkey,
    pub amount: u64,
    pub recipient: Pubkey,
    pub timestamp: i64,
}
