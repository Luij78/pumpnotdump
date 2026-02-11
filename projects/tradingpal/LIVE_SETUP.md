# TradingPal Live Setup

**Last Updated:** 2026-01-28 by Skipper
**Location:** garciafamilybusiness@192.168.5.51:~/deal_finder/TradingPal

---

## 🎯 STANDING ORDERS (Read This First!)

1. **Every heartbeat:** Check if bots are running. If down + has balance → restart immediately.
2. **Every heartbeat:** Run `redeem_now.py` to claim any settled positions.
3. **When degens catch a trade:** Ping Luis on Telegram 🖨️
4. **DON'T touch the strategy** — no changing MIN_SHARES, MAX_PRICE, or trading logic unless Luis says.
5. **Report status** when asked — balance, record, recent trades.

---

## 🤖 Running Bots

Three bots run 24/7:

| Bot | Purpose | How to Start |
|-----|---------|--------------|
| `hold_to_settle.py` | Main trader — picks direction, bets, holds to settlement, auto-redeems | `nohup python3 hold_to_settle.py &` |
| `pnl_notifier.py` | P&L tracking + Telegram alerts | `nohup python3 pnl_notifier.py &` |
| `trade_notifier_v2.py` | Trade notifications (blockchain verified) | `nohup python3 trade_notifier_v2.py &` |

**Only `hold_to_settle.py` actually trades.** The other two are monitoring/alerting.

---

## 💰 Wallet

- **Address:** 0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3
- **Network:** Polygon
- **Check balance:** `python3 check_balance.py`

---

## ⚙️ Settings (in hold_to_settle.py)

```python
MIN_SHARES = 5      # Minimum position size
MAX_PRICE = 0.35    # Only enter if price < 35¢ (changed from 55¢)
```

**Strategy:** BTC 15-min Up/Down markets. Uses MA crossover for direction. Waits for settlement, auto-redeems wins.

---

## 📊 Check Status

```bash
# SSH to iMac
ssh garciafamilybusiness@192.168.5.51

# Check bots running
ps aux | grep -E 'hold_to_settle|notifier' | grep -v grep

# Check balance (on-chain)
cd ~/deal_finder/TradingPal
source venv/bin/activate
python3 check_balance.py

# Check positions
curl -s "https://data-api.polymarket.com/positions?user=0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3"

# Redeem settled positions
python3 redeem_now.py
```

---

## 🔄 Restart Bots

```bash
# Kill all
pkill -f hold_to_settle.py
pkill -f pnl_notifier.py
pkill -f trade_notifier_v2.py

# Start all
cd ~/deal_finder/TradingPal
source venv/bin/activate
nohup python3 hold_to_settle.py > /tmp/hold_to_settle.log 2>&1 &
nohup python3 pnl_notifier.py > /tmp/pnl_notifier.log 2>&1 &
nohup python3 trade_notifier_v2.py > /tmp/trade_notifier_v2.log 2>&1 &
```

---

## 📢 Notifications

Both notifiers send to Luis via **TradingPal Telegram Bot** (@TradingwPal_bot)
- Token: 8277928699:AAFt842BmOnha-QQBDdSPqAfPEjsqWlE3PA
- Chat ID: 5601940168

**Fixed 2026-01-28:** `trade_notifier_v2.py` was trying to send via Clawdbot API (unreachable). Updated to use direct Telegram API.

---

## 📈 Performance Tracking

- **Record:** Tracked in pnl_notifier state file (`.pnl_state.json`)
- **As of 2026-01-28:** 16W-16L, +$29.40 profit
- **Redemption:** Winning shares auto-redeem via CTF contract. Losing shares show as $0 (nothing to claim).

---

## ⚠️ Rules (from Luis)

1. **DON'T touch the winning strategy** — leave thresholds alone unless Luis says
2. **Ping Luis when degens catch a trade** — notify on new trades
3. **Run redeem_now.py during heartbeats** — claim any settled positions
4. **If bot down + has balance → RESTART immediately** (don't ask)

---

## 📚 Related Docs

- `STRATEGY_GUIDE.md` — Full strategy explanation (Ascetic0x method)
- `REDEMPTION_FIX.md` — How redemption works
- `README.md` — Original system docs (mostly outdated)
