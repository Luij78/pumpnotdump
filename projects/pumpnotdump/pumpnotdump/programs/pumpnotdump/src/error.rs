use anchor_lang::prelude::*;

#[error_code]
pub enum ErrorCode {
    #[msg("Platform is currently paused")]
    PlatformPaused,
    
    #[msg("Agent name is too long (max 50 characters)")]
    NameTooLong,
    
    #[msg("Agent description is too long (max 200 characters)")]
    DescriptionTooLong,
    
    #[msg("Social link is too long")]
    SocialLinkTooLong,
    
    #[msg("At least one social link (Twitter, website, or GitHub) is required")]
    NoSocialLinks,
    
    #[msg("Agent name cannot be empty")]
    EmptyName,
    
    #[msg("Liquidity lock percentage must be at least 50%")]
    InsufficientLiquidityLock,
    
    #[msg("Team allocation cannot exceed 20% of total supply")]
    ExcessiveTeamAllocation,
    
    #[msg("Liquidity lock period is below minimum required days")]
    LiquidityLockTooShort,
    
    #[msg("Treasury time lock period is below minimum (7 days)")]
    TreasuryLockTooShort,
    
    #[msg("Treasury time lock has not expired yet")]
    TimeLockActive,
    
    #[msg("Withdrawal amount exceeds period limit")]
    WithdrawalLimitExceeded,
    
    #[msg("Insufficient funds in treasury")]
    InsufficientTreasuryFunds,
    
    #[msg("Multisig threshold cannot be zero")]
    InvalidMultisigThreshold,
    
    #[msg("Multisig threshold exceeds number of signers")]
    ThresholdExceedsSigners,
    
    #[msg("Too many multisig signers (max 5)")]
    TooManySigners,
    
    #[msg("Only platform authority can perform this action")]
    UnauthorizedPlatformAction,
    
    #[msg("Agent is not registered")]
    AgentNotRegistered,
    
    #[msg("Token mint does not match")]
    TokenMintMismatch,
    
    #[msg("Invalid percentage value (must be 0-100)")]
    InvalidPercentage,
    
    #[msg("Arithmetic overflow")]
    ArithmeticOverflow,
    
    #[msg("Invalid withdrawal period (must be positive)")]
    InvalidWithdrawalPeriod,
    
    #[msg("Max withdrawal amount cannot be zero")]
    ZeroWithdrawalLimit,
}
