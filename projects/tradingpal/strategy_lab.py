#!/usr/bin/env python3
"""
Degen Strategy Lab - Paper Trading Simulator
13 strategies running in parallel on BTC 15-min settlement markets
"""
import os
import sys
import json
import time
import requests
from datetime import datetime, timezone, timedelta
from collections import defaultdict

sys.stdout.reconfigure(line_buffering=True)

# Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Files
LAB_DIR = "/tmp/strategy_lab"
TRADES_LOG = f"{LAB_DIR}/trades.json"
RESULTS_LOG = f"{LAB_DIR}/results.json"

os.makedirs(LAB_DIR, exist_ok=True)

# Strategy definitions
STRATEGIES = {
    # Price-based
    "value_hunter": {"desc": "Only ≤35%", "max_price": 0.35},
    "moderate_value": {"desc": "36-45%", "min_price": 0.36, "max_price": 0.45},
    "aggressive": {"desc": "46-55%", "min_price": 0.46, "max_price": 0.55},
    
    # Timing-based
    "early_bird": {"desc": "First 2 min of window", "timing": "early"},
    "last_minute": {"desc": "Final 2 min of window", "timing": "late"},
    
    # Signal-based
    "momentum_rider": {"desc": "Follow BTC momentum", "signal": "momentum"},
    "mean_reversion": {"desc": "Bet on pullback after spike", "signal": "reversion"},
    "ma_divergence": {"desc": "Price vs MA divergence", "signal": "ma_div"},
    
    # Contrarian
    "fade_crowd": {"desc": "Bet against >65% consensus", "contrarian": True, "threshold": 0.65},
    "streak_breaker": {"desc": "After 3+ same outcomes, bet reversal", "signal": "streak"},
    
    # Advanced
    "kelly_sizing": {"desc": "Optimal bet sizing based on edge", "sizing": "kelly"},
    "volatility_filter": {"desc": "Only trade high volatility", "filter": "volatility"},
    "time_of_day": {"desc": "Only trade good hours", "filter": "time"},
}

# Track state
state = {
    "pending_trades": {},  # slug -> {strategy: trade_info, ...}
    "results": defaultdict(lambda: {"wins": 0, "losses": 0, "profit": 0.0, "trades": []}),
    "recent_outcomes": [],  # last 10 market outcomes for streak detection
    "btc_prices": [],  # last 10 BTC prices for momentum
    "hourly_start": None,
    "last_report": None,
    "last_market_slug": None,
}

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        r = requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }, timeout=10)
        return r.ok
    except Exception as e:
        log(f"Telegram error: {e}")
        return False

def get_btc_price():
    """Get current BTC price"""
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=10)
        return r.json()["bitcoin"]["usd"]
    except:
        return None

def get_market():
    """Get current BTC 15-min market using gamma API (same as hold_to_settle)"""
    et = timezone(timedelta(hours=-5))
    now = datetime.now(et)
    curr_min = 15 * (now.minute // 15)
    window_start = now.replace(minute=curr_min, second=0, microsecond=0)
    ts = int(window_start.timestamp())
    slug = f"btc-updown-15m-{ts}"
    
    # Calculate time left in window
    window_end = window_start + timedelta(minutes=15)
    time_left = (window_end - now).total_seconds()
    
    try:
        r = requests.get(f"https://gamma-api.polymarket.com/events?slug={slug}", timeout=10)
        events = r.json()
        if events:
            e = events[0]
            m = e["markets"][0]
            if not m.get("closed") and m.get("acceptingOrders"):
                prices = json.loads(m.get("outcomePrices", "[\"0.5\",\"0.5\"]"))
                return {
                    "slug": slug,
                    "title": e["title"],
                    "up_price": float(prices[0]),
                    "down_price": float(prices[1]),
                    "time_left": time_left,
                    "window_start": window_start,
                    "condition_id": m["conditionId"],
                }
        return None
    except Exception as e:
        log(f"Market fetch error: {e}")
        return None

def check_market_resolved(slug):
    """Check if market resolved and get outcome"""
    try:
        r = requests.get(f"https://gamma-api.polymarket.com/events?slug={slug}", timeout=10)
        events = r.json()
        if events:
            m = events[0]["markets"][0]
            if m.get("closed"):
                prices = json.loads(m.get("outcomePrices", "[\"0.5\",\"0.5\"]"))
                up_final = float(prices[0])
                # If UP settled at 1.0 (or close), UP won
                if up_final > 0.9:
                    return "UP"
                elif up_final < 0.1:
                    return "DOWN"
        return None
    except:
        return None

def calculate_momentum():
    """Calculate BTC momentum from recent prices"""
    if len(state["btc_prices"]) < 2:
        return 0
    return state["btc_prices"][-1] - state["btc_prices"][-2]

def calculate_volatility():
    """Calculate recent volatility"""
    if len(state["btc_prices"]) < 5:
        return 0
    prices = state["btc_prices"][-5:]
    avg = sum(prices) / len(prices)
    variance = sum((p - avg) ** 2 for p in prices) / len(prices)
    return variance ** 0.5

def get_streak():
    """Get current outcome streak"""
    if not state["recent_outcomes"]:
        return None, 0
    last = state["recent_outcomes"][-1]
    count = 0
    for outcome in reversed(state["recent_outcomes"]):
        if outcome == last:
            count += 1
        else:
            break
    return last, count

def is_good_trading_hour():
    """Check if current hour is historically good"""
    hour = datetime.now().hour
    good_hours = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    return hour in good_hours

def evaluate_strategies(market, btc_price):
    """Evaluate all strategies and return paper trades"""
    trades = {}
    
    up_price = market["up_price"]
    down_price = market["down_price"]
    time_left = market["time_left"]
    
    momentum = calculate_momentum()
    volatility = calculate_volatility()
    streak_dir, streak_count = get_streak()
    
    for name, config in STRATEGIES.items():
        direction = None
        bet_size = 5.0  # Default $5 paper bet
        reason = ""
        
        # Price-based strategies
        if "max_price" in config and "min_price" not in config:
            max_p = config["max_price"]
            if up_price <= max_p:
                direction = "UP"
                reason = f"UP at {up_price:.0%} ≤ {max_p:.0%}"
            elif down_price <= max_p:
                direction = "DOWN"
                reason = f"DOWN at {down_price:.0%} ≤ {max_p:.0%}"
        
        elif "max_price" in config and "min_price" in config:
            min_p = config["min_price"]
            max_p = config["max_price"]
            if min_p <= up_price <= max_p:
                direction = "UP"
                reason = f"UP at {up_price:.0%} in [{min_p:.0%}-{max_p:.0%}]"
            elif min_p <= down_price <= max_p:
                direction = "DOWN"
                reason = f"DOWN at {down_price:.0%} in [{min_p:.0%}-{max_p:.0%}]"
        
        # Timing-based
        elif config.get("timing") == "early":
            if time_left > 780:  # > 13 min left (first 2 min of window)
                direction = "UP" if up_price < down_price else "DOWN"
                reason = f"Early entry ({time_left/60:.1f}m left)"
        
        elif config.get("timing") == "late":
            if time_left < 120:  # < 2 min left
                direction = "UP" if up_price < down_price else "DOWN"
                reason = f"Last minute ({time_left:.0f}s left)"
        
        # Signal-based
        elif config.get("signal") == "momentum":
            if abs(momentum) > 50:
                direction = "UP" if momentum > 0 else "DOWN"
                reason = f"Momentum {'+'if momentum>0 else ''}{momentum:.0f}"
        
        elif config.get("signal") == "reversion":
            if momentum > 100:
                direction = "DOWN"
                reason = f"Mean reversion (spike +{momentum:.0f})"
            elif momentum < -100:
                direction = "UP"
                reason = f"Mean reversion (drop {momentum:.0f})"
        
        elif config.get("signal") == "ma_div":
            if up_price < 0.35 and momentum > 0:
                direction = "UP"
                reason = f"MA div: cheap UP + momentum"
            elif down_price < 0.35 and momentum < 0:
                direction = "DOWN"
                reason = f"MA div: cheap DOWN + momentum"
        
        elif config.get("signal") == "streak":
            if streak_count >= 3:
                direction = "DOWN" if streak_dir == "UP" else "UP"
                reason = f"Break {streak_count}x {streak_dir} streak"
        
        # Contrarian
        elif config.get("contrarian"):
            threshold = config["threshold"]
            if up_price > threshold:
                direction = "DOWN"
                reason = f"Fade crowd (UP at {up_price:.0%})"
            elif down_price > threshold:
                direction = "UP"
                reason = f"Fade crowd (DOWN at {down_price:.0%})"
        
        # Advanced filters/sizing
        elif config.get("sizing") == "kelly":
            cheaper = "UP" if up_price < down_price else "DOWN"
            price = min(up_price, down_price)
            if price < 0.50:
                direction = cheaper
                edge = 0.5 - price
                bet_size = max(1, min(20, edge * 100))
                reason = f"Kelly: {cheaper} at {price:.0%}, bet ${bet_size:.0f}"
        
        elif config.get("filter") == "volatility":
            if volatility > 50:
                direction = "UP" if momentum > 0 else "DOWN"
                reason = f"High vol ({volatility:.0f})"
        
        elif config.get("filter") == "time":
            if is_good_trading_hour():
                cheaper = "UP" if up_price < down_price else "DOWN"
                price = min(up_price, down_price)
                if price < 0.50:
                    direction = cheaper
                    reason = f"Good hour, {cheaper} at {price:.0%}"
        
        if direction:
            trades[name] = {
                "direction": direction,
                "price": up_price if direction == "UP" else down_price,
                "bet_size": bet_size,
                "reason": reason,
            }
    
    return trades

def record_trades(slug, market, trades):
    """Record paper trades for settlement tracking"""
    state["pending_trades"][slug] = {
        "market": {
            "slug": slug,
            "title": market["title"],
            "up_price": market["up_price"],
            "down_price": market["down_price"],
        },
        "trades": trades,
        "placed_at": datetime.now().isoformat(),
    }
    
    try:
        with open(TRADES_LOG, "w") as f:
            json.dump(state["pending_trades"], f, indent=2, default=str)
    except:
        pass

def settle_trades(slug, outcome):
    """Settle trades for a resolved market"""
    if slug not in state["pending_trades"]:
        return
    
    pending = state["pending_trades"][slug]
    trades = pending["trades"]
    settled_count = 0
    
    for strategy, trade in trades.items():
        won = trade["direction"] == outcome
        price = trade["price"]
        bet_size = trade["bet_size"]
        
        if won:
            profit = bet_size * (1 - price) / price
            state["results"][strategy]["wins"] += 1
        else:
            profit = -bet_size
            state["results"][strategy]["losses"] += 1
        
        state["results"][strategy]["profit"] += profit
        state["results"][strategy]["trades"].append({
            "slug": slug,
            "direction": trade["direction"],
            "outcome": outcome,
            "won": won,
            "profit": round(profit, 2),
            "price": price,
        })
        settled_count += 1
    
    state["recent_outcomes"].append(outcome)
    if len(state["recent_outcomes"]) > 10:
        state["recent_outcomes"] = state["recent_outcomes"][-10:]
    
    del state["pending_trades"][slug]
    
    try:
        with open(RESULTS_LOG, "w") as f:
            json.dump(dict(state["results"]), f, indent=2, default=str)
    except:
        pass
    
    return settled_count

def generate_15min_report():
    """Generate detailed 15-min report"""
    lines = ["🧪 *15-Min Strategy Report*"]
    lines.append(f"_{datetime.now().strftime('%I:%M %p EST')}_\n")
    
    sorted_strats = sorted(
        [(k, v) for k, v in state["results"].items() if v["wins"] + v["losses"] > 0],
        key=lambda x: x[1]["profit"],
        reverse=True
    )
    
    if not sorted_strats:
        lines.append("⏳ No completed trades yet.")
    else:
        # Overall stats
        total_profit = sum(d["profit"] for d in state["results"].values())
        total_wins = sum(d["wins"] for d in state["results"].values())
        total_losses = sum(d["losses"] for d in state["results"].values())
        total_trades = total_wins + total_losses
        
        lines.append(f"*📊 Overall: {total_wins}W/{total_losses}L | ${total_profit:+.2f}*\n")
        
        # Winners
        winners = [(k, v) for k, v in sorted_strats if v["profit"] > 0]
        losers = [(k, v) for k, v in sorted_strats if v["profit"] < 0]
        
        if winners:
            lines.append("*✅ WORKING:*")
            for name, data in winners[:5]:
                wr = (data["wins"]/(data["wins"]+data["losses"])*100)
                lines.append(f"  {name}: {data['wins']}W/{data['losses']}L ({wr:.0f}%) ${data['profit']:+.2f}")
        
        if losers:
            lines.append("\n*❌ NOT WORKING:*")
            for name, data in losers[-3:]:
                wr = (data["wins"]/(data["wins"]+data["losses"])*100) if (data["wins"]+data["losses"]) > 0 else 0
                lines.append(f"  {name}: {data['wins']}W/{data['losses']}L ({wr:.0f}%) ${data['profit']:+.2f}")
    
    # Pending trades
    pending_count = sum(len(p["trades"]) for p in state["pending_trades"].values())
    if pending_count:
        lines.append(f"\n⏳ {pending_count} bets pending")
        # Show what's pending
        for slug, pending in state["pending_trades"].items():
            market_time = slug.split("-")[-1]
            bets = ", ".join([f"{t['direction']}" for t in pending["trades"].values()])
            lines.append(f"  {len(pending['trades'])} strategies: {bets}")
    
    return "\n".join(lines)

def generate_hourly_report():
    """Generate comprehensive hourly report"""
    lines = ["📊 *HOURLY STRATEGY LAB REPORT*"]
    lines.append(f"_{datetime.now().strftime('%I:%M %p EST')}_\n")
    
    sorted_strats = sorted(
        [(k, v) for k, v in state["results"].items() if v["wins"] + v["losses"] > 0],
        key=lambda x: x[1]["profit"],
        reverse=True
    )
    
    if not sorted_strats:
        lines.append("No completed trades this hour.")
        return "\n".join(lines)
    
    # Overall summary
    total_profit = sum(d["profit"] for d in state["results"].values())
    total_trades = sum(d["wins"] + d["losses"] for d in state["results"].values())
    total_wins = sum(d["wins"] for d in state["results"].values())
    wr = (total_wins/total_trades*100) if total_trades else 0
    
    lines.append(f"*💰 NET P&L: ${total_profit:+.2f}*")
    lines.append(f"*📈 {total_wins}W/{total_trades-total_wins}L ({wr:.0f}% win rate)*\n")
    
    # All strategies ranked
    lines.append("*🏆 STRATEGY RANKINGS:*")
    for i, (name, data) in enumerate(sorted_strats, 1):
        w, l = data["wins"], data["losses"]
        total = w + l
        wr = (w/total*100) if total else 0
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        profit_emoji = "🟢" if data["profit"] > 0 else "🔴" if data["profit"] < 0 else "⚪"
        lines.append(f"{emoji} {i}. {name}")
        lines.append(f"   {profit_emoji} {w}W/{l}L ({wr:.0f}%) ${data['profit']:+.2f}")
    
    # Strategies that haven't triggered
    active = set(k for k, v in state["results"].items() if v["wins"] + v["losses"] > 0)
    inactive = set(STRATEGIES.keys()) - active
    if inactive:
        lines.append(f"\n*😴 NOT TRIGGERED:* {', '.join(inactive)}")
    
    # Recommendations
    lines.append("\n*💡 INSIGHTS:*")
    if sorted_strats:
        best = sorted_strats[0]
        if best[1]["profit"] > 0:
            lines.append(f"  Best performer: {best[0]} (+${best[1]['profit']:.2f})")
        if len(sorted_strats) > 1:
            worst = sorted_strats[-1]
            if worst[1]["profit"] < 0:
                lines.append(f"  Worst performer: {worst[0]} (${worst[1]['profit']:.2f})")
    
    return "\n".join(lines)

def main():
    log("🧪 Degen Strategy Lab Starting...")
    log(f"📊 {len(STRATEGIES)} strategies loaded")
    
    send_telegram("🧪 *Strategy Lab ONLINE!*\n\n13 strategies paper trading BTC 15-min markets.\n\n⏰ Reports every 15 min\n📊 Hourly summaries\n\nFirst report at :45")
    
    state["hourly_start"] = datetime.now()
    state["last_report"] = datetime.now()
    
    while True:
        try:
            # Get BTC price for momentum tracking
            btc = get_btc_price()
            if btc:
                state["btc_prices"].append(btc)
                if len(state["btc_prices"]) > 20:
                    state["btc_prices"] = state["btc_prices"][-20:]
            
            # Get current market
            market = get_market()
            
            if market:
                slug = market["slug"]
                
                # Only place new trades once per market
                if slug != state["last_market_slug"]:
                    state["last_market_slug"] = slug
                    log(f"\n📈 NEW MARKET: {market['title']}")
                    log(f"   UP: {market['up_price']:.0%} | DOWN: {market['down_price']:.0%}")
                    
                    # Evaluate all strategies
                    trades = evaluate_strategies(market, btc)
                    
                    if trades:
                        record_trades(slug, market, trades)
                        log(f"   📝 {len(trades)} strategies placed paper bets:")
                        for name, t in list(trades.items())[:5]:
                            log(f"      {name}: {t['direction']} @ {t['price']:.0%} ({t['reason']})")
                        if len(trades) > 5:
                            log(f"      ...and {len(trades)-5} more")
                    else:
                        log("   ⏭️ No strategies triggered")
            
            # Check for settled markets (check every cycle)
            for slug in list(state["pending_trades"].keys()):
                outcome = check_market_resolved(slug)
                if outcome:
                    count = settle_trades(slug, outcome)
                    log(f"⚖️ SETTLED {slug[-15:]}: {outcome} ({count} strategies)")
                    # Send quick update
                    winners = [s for s,t in state["pending_trades"].get(slug, {}).get("trades", {}).items() if t["direction"] == outcome]
                    send_telegram(f"⚖️ *Market Settled: {outcome}*\n{count} strategies bet, check next 15-min report for details")
            
            # Check if time for reports
            now = datetime.now()
            
            # 15-min report (at :00, :15, :30, :45)
            if now.minute % 15 == 0 and (now - state["last_report"]).total_seconds() > 60:
                report = generate_15min_report()
                send_telegram(report)
                state["last_report"] = now
                log("📨 Sent 15-min report")
            
            # Hourly report
            if now.minute == 0 and (now - state["hourly_start"]).total_seconds() > 3000:
                report = generate_hourly_report()
                send_telegram(report)
                state["hourly_start"] = now
                log("📨 Sent hourly report")
            
            time.sleep(10)  # Check every 10 seconds
            
        except KeyboardInterrupt:
            log("🛑 Shutting down...")
            break
        except Exception as e:
            log(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(30)

if __name__ == "__main__":
    main()
