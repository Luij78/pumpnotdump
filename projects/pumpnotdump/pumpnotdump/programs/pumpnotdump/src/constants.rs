use anchor_lang::prelude::*;

// PDA Seeds
#[constant]
pub const PLATFORM_SEED: &[u8] = b"platform";

#[constant]
pub const AGENT_SEED: &[u8] = b"agent";

#[constant]
pub const RUG_SCORE_SEED: &[u8] = b"rug_score";

#[constant]
pub const TREASURY_SEED: &[u8] = b"treasury";

#[constant]
pub const LAUNCH_SEED: &[u8] = b"launch";

// Default values
#[constant]
pub const DEFAULT_PLATFORM_FEE_BPS: u16 = 100; // 1%

#[constant]
pub const DEFAULT_MIN_LIQUIDITY_LOCK_DAYS: u16 = 30;

#[constant]
pub const MIN_LIQUIDITY_PERCENT: u8 = 50; // 50%

#[constant]
pub const MAX_TEAM_PERCENT: u8 = 20; // 20%

#[constant]
pub const MIN_TREASURY_LOCK_DAYS: u16 = 7;

#[constant]
pub const SECONDS_PER_DAY: i64 = 86400;

#[constant]
pub const DEFAULT_WITHDRAWAL_PERIOD_SECONDS: i64 = 604800; // 7 days
