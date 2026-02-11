# TradingPal (Polymarket Bot) — AGENTS.md

## RULES (NON-NEGOTIABLE)
1. **AUTO-REDEEM** settled positions on EVERY heartbeat — don't wait for Luis
2. **AUTO-RESTART** traders if balance > $1 and not running
3. **Check status** on heartbeats (ps aux + redeem check)
4. **VPN Required** — Dubai server via Mullvad must be active on iMac

## Location
- **Machine:** iMac @ 192.168.5.51
- **SSH:** `garciafamilybusiness@192.168.5.51`
- **Directory:** `~/deal_finder/TradingPal/`

## Wallet
- **Address:** 0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3
- **Network:** Polygon (Polymarket)

## Bots — LIVE vs MONITORING

| Bot | Type | Real Trades? | Notes |
|-----|------|--------------|-------|
| `time_decay_trader.py` | ⛔ DISABLED | ❌ No | Scalper — Luis doesn't want scalping |
| `hold_to_settle.py` | **LIVE TRADER** | ✅ YES | ONLY bot that trades — holds to settlement |
| `pnl_notifier.py` | Monitor | ❌ No | Tracks P&L, no trades |
| `trade_notifier_v2.py` | Monitor | ❌ No | Sends Telegram alerts |

**Strategy:** Predictions ONLY — no scalping. Bot picks UP/DOWN, holds until 15-min market settles, auto-redeems.

**Log file:** `/tmp/hold_to_settle.log`

## Files
| File | Purpose |
|------|---------|
| `time_decay_trader.py` | LIVE trader — makes real trades |
| `hold_to_settle.py` | LIVE trader — makes real trades |
| `pnl_notifier.py` | P&L monitoring |
| `trade_notifier_v2.py` | Telegram trade alerts |
| `redeem_now.py` | Claim settled positions |
| `time_decay_live.log` | Trade history log |

## Commands
```bash
# 1. CHECK & REDEEM (run on every heartbeat!)
ssh garciafamilybusiness@192.168.5.51 "cd ~/deal_finder/TradingPal && python3 redeem_now.py"

# 2. Check what's running
ssh garciafamilybusiness@192.168.5.51 "ps aux | grep -E 'time_decay|hold_to_settle|notifier' | grep -v grep"

# 3. Check trade history
ssh garciafamilybusiness@192.168.5.51 "cd ~/deal_finder/TradingPal && grep 'Order filled' time_decay_live.log"

# 4. Restart time_decay_trader (if balance > $1)
ssh garciafamilybusiness@192.168.5.51 "cd ~/deal_finder/TradingPal && nohup python3 time_decay_trader.py >> time_decay_live.log 2>&1 &"

# 5. Restart hold_to_settle (if balance > $1)
ssh garciafamilybusiness@192.168.5.51 "cd ~/deal_finder/TradingPal && source venv/bin/activate && nohup python3 hold_to_settle.py >> /tmp/hold_to_settle.log 2>&1 &"
```

## Strategy
- Binary UP/DOWN prediction on BTC/ETH/SOL price
- Entry: $0.30-$0.35 range only
- Hold to market close (15-min windows)
- **Check frequency: Every 1 second** (catch brief price dips)

## Current Status (Updated Jan 28, 2026)
- **time_decay_trader.py:** 🟢 RUNNING — but wallet too low for new trades
- **hold_to_settle.py:** 🟢 RUNNING — but wallet too low for new trades
- **pnl_notifier.py:** 🟢 RUNNING
- **trade_notifier_v2.py:** 🟢 RUNNING
- **Wallet Balance:** $0.83 USDC (needs top-up to trade)
- **Redeemable Positions:** 0

## Trade History (Jan 27, 2026)
```
[21:47:52] Order filled at $0.470
[21:51:35] Order filled at $0.530
[22:05:07] Order filled at $0.290
```

---
*Last updated: 2026-01-28 06:49 AM EST*
