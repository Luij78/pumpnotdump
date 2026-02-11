# TradingPal — Standing Orders

**Last Updated:** 2026-02-04 10:00 PM by Skipper

---

## 🔥 NEW: Agent Token Launch Monitor (Added 2026-02-04)

**STATUS:** Building tonight — Phase 1 (monitor only, no trades)

**What it is:**
- Monitors AI agent token launches across DexScreener, Virtuals.io (Base), Pump.fun (Solana)
- Sends Telegram alerts on promising launches (volume, social signals)
- Tracks $CLAWNCH, $TPRO, $PATH, $ZHC and new agent tokens

**Why:**
- AI agent economy exploding — 149K agents on Moltbook, tokens launching hourly
- "Self-Funded AI" narrative: agents trading, deploying tokens autonomously
- Being early to agent token launches = highest alpha opportunity
- Alex Finn (@AlexFinn on X) pushing OpenClaw to 390K followers

**Phase 1 — Monitor Only (THIS WEEK):**
- Build agent_token_monitor.py
- DexScreener API (free) for new launches
- Telegram alerts when AI agent token >$10K volume in first hour
- Paper trade, learn patterns

**Phase 2 — Small Positions (NEXT WEEK):**
- $2-5 per position, max 3 concurrent
- Auto-sell at 2x/5x/10x targets
- Stop-loss at 50%
- Track P&L

**Risk Rules:**
- Max $5 per position
- NO live trades without Luis approval
- Paper trade 1 week minimum

**Spec:** ~/.openclaw/workspace/memory/tradingpal-agent-monitor-spec.md
**Intel:** ~/.openclaw/workspace/memory/alex-finn-intel.md

---

## 🧪 STRATEGY LAB — ACTIVE (Added 2026-01-29)

**STATUS:** Running on Mac Mini, collecting paper trading data

**What it is:**
- Paper trading bot testing 13 different strategies on BTC 15-min markets
- Sends Telegram reports every 15 minutes + hourly summaries
- Location: `~/TradingPal/strategy_lab.py`
- Data stored: `/tmp/strategy_lab/results.json`

**Why:**
- Luis wants to find a PROVEN winning strategy before risking real money
- Real trading (hold_to_settle.py) is OFF while we collect data

**Strategies being tested:**
1. early_bird, time_of_day, kelly_sizing, aggressive, streak_breaker
2. moderate_value, momentum_rider, mean_reversion, volatility_filter
3. value_hunter, last_minute, fade_crowd, ma_divergence

**Current Leader (as of 11:30 AM Jan 29):**
- **early_bird:** 10W/5L (67%), +$31.71 profit
- Bet size: $5 per trade (paper)

**GO LIVE CRITERIA:**
- Need 50+ trades across different market conditions
- Maintain 60%+ win rate
- Then activate winning strategy with $5 real bets

**Check latest results:**
```bash
cat /tmp/strategy_lab/results.json | python3 -m json.tool
```

**DO NOT:**
- Stop strategy_lab.py — let it run and collect data
- Start hold_to_settle.py — real trading is paused
- Change strategy parameters without Luis approval

---

## ⚠️ CRITICAL: ON-CHAIN VERIFICATION (Added 2026-01-28)

**Everything must be verified by blockchain, not API:**

1. **Balance** — Always check USDC.e + USDT from Polygon RPC, not API
2. **Trade fills** — Verify CTF contract shows we hold shares before recording
3. **Redemptions** — Use `redeem_positions.py` and verify USDC received
4. **Never trust API alone** — Blockchain is truth

**Location changed:** TradingPal now runs on **Mac Mini** (`~/TradingPal/`), not iMac.

---

## DO THIS

1. **Every heartbeat:** Check all 3 bots are running
2. **Every heartbeat:** Check logs for errors (no crash loops!)
3. **Every heartbeat:** Run `redeem_now.py` to claim settled positions
4. **If any bot down OR crashing:** Restart immediately (no asking)
5. **When degens catch a trade:** You'll get Telegram notification automatically

## CHECK FOR ERRORS

```bash
# Check last 20 lines for errors
ssh garciafamilybusiness@192.168.5.51 "tail -20 /tmp/hold_to_settle.log | grep -i error"
```

If errors found → fix and restart.

## DON'T DO THIS

- Don't change strategy settings (MIN_SHARES, MAX_PRICE)
- Don't modify bot logic without Luis approval
- Don't disable bots without reason

---

## BOTS (3 total, 1 trades)

| Bot | Purpose | Trades? |
|-----|---------|---------|
| `hold_to_settle.py` | Main trader — scans every second, bets, holds to settle, auto-redeems | ✅ YES |
| `pnl_notifier.py` | Tracks P&L, sends balance updates | ❌ No |
| `trade_notifier_v2.py` | Watches blockchain for fills | ❌ No |

---

## SETTINGS (Updated 2026-01-28)

```python
MIN_SHARES = 5          # Position size (no YOLO)
MAX_PRICE = 0.45        # Only trade when odds < 45%
MAX_DAILY_LOSSES = 3    # Stop after 3 losses in a day
MAX_DAILY_TRADES = 10   # Cap at 10 trades/day
```

**Strategy:** MA crossover for direction, only trade when price is favorable. Bot waits for signal AND good odds to align.

---

## NOTIFICATIONS (all via @TradingwPal_bot)

The bot sends directly to Telegram (no AI tokens used):
- **Every 15 min** (:00, :15, :30, :45) — status update (traded or why not)
- **On new trade** — immediate alert with direction + price
- **On settlement** — win/loss result + profit
- **On startup** — "Degen bot started!"

---

## CHECK STATUS (Mac Mini - Local)

```bash
# Are bots running?
ps aux | grep -E 'hold_to_settle|notifier' | grep -v grep

# Check balance (ON-CHAIN)
cd ~/TradingPal && source venv/bin/activate && python3 -c "
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
addr = '0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3'
abi = [{'constant':True,'inputs':[{'name':'_owner','type':'address'}],'name':'balanceOf','outputs':[{'name':'balance','type':'uint256'}],'type':'function'}]
usdc = w3.eth.contract(address='0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', abi=abi).functions.balanceOf(addr).call() / 1e6
usdt = w3.eth.contract(address='0xc2132D05D31c914a87C6611C10748AEb04B58e8F', abi=abi).functions.balanceOf(addr).call() / 1e6
print(f'USDC: \${usdc:.2f} | USDT: \${usdt:.2f} | Total: \${usdc+usdt:.2f}')
"

# Redeem settled positions
cd ~/TradingPal && source venv/bin/activate && python3 redeem_positions.py

# Check logs
tail -30 ~/TradingPal/hold_to_settle.log
```

---

## RESTART BOTS (Mac Mini - Local)

```bash
# Kill all
pkill -f hold_to_settle.py; pkill -f pnl_notifier.py; pkill -f trade_notifier_v2.py

# Start main bot
cd ~/TradingPal && source venv/bin/activate && nohup python3 hold_to_settle.py > hold_to_settle.log 2>&1 &
```

---

## KEY INFO

- **Location:** ~/TradingPal/ (Mac Mini - LOCAL, no SSH needed)
- **Wallet:** 0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3
- **Network:** Polygon
- **Settings:** MIN_SHARES=5, MAX_PRICE=35¢
- **Strategy:** MA crossover on BTC 15-min markets

---

## HISTORY

- 2026-01-28 11PM: **CRITICAL FIX** — Added on-chain verification for all trades
- 2026-01-28 11PM: Fixed order fill verification (was recording phantom trades)
- 2026-01-28 11PM: Moved TradingPal from iMac to Mac Mini (no SSH needed)
- 2026-01-28 11PM: Fixed balance to show USDC + USDT from blockchain
- 2026-01-28 11PM: Fixed redemption bugs (missing quotes in f-strings)
- 2026-01-28: Added 15-min status updates directly from bot (disabled AI cron)
- 2026-01-28: Fixed trade_notifier_v2.py to use direct Telegram API
- 2026-01-27: Created LIVE_SETUP.md with full documentation
