#!/usr/bin/env python3
"""
Live $1 Trader - One trade every 15 minutes on BTC Up/Down
CORRECT LOGIC: Compare current price to window start price
"""
import os
import sys
import json
import time
import requests
from datetime import datetime, timezone, timedelta

sys.path.insert(0, '.')
os.chdir('/Users/garciafamilybusiness/deal_finder/TradingPal')
from dotenv import load_dotenv
load_dotenv()

import cloudflare_bypass
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType

# Config
MIN_SHARES = 5  # Polymarket minimum
TRADE_AMOUNT = 3.0  # ~$3 per trade to ensure 5+ shares
TRADE_LOG = 'live_trades.json'

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line, flush=True)
    with open('/tmp/live_trader.log', 'a') as f:
        f.write(line + '\n')

def load_trades():
    try:
        with open(TRADE_LOG, 'r') as f:
            return json.load(f)
    except:
        return {'trades': [], 'wins': 0, 'losses': 0, 'pending': 0, 'total_pnl': 0}

def save_trades(data):
    with open(TRADE_LOG, 'w') as f:
        json.dump(data, f, indent=2)

def get_window_start_time():
    """Get the timestamp for the start of current 15-min window"""
    et = timezone(timedelta(hours=-5))
    now = datetime.now(et)
    curr_min = 15 * (now.minute // 15)
    window_start = now.replace(minute=curr_min, second=0, microsecond=0)
    return window_start

def get_btc_direction():
    """
    CORRECT LOGIC: Compare current price to price at window start
    Returns: direction, current_price, start_price
    """
    try:
        window_start = get_window_start_time()
        start_ts = int(window_start.timestamp() * 1000)
        
        # Get candles from window start to now
        r = requests.get('https://api.binance.us/api/v3/klines', params={
            'symbol': 'BTCUSDT',
            'interval': '1m',
            'startTime': start_ts,
            'limit': 20
        }, timeout=10)
        data = r.json()
        
        if not data:
            log('No price data!')
            return 'UP', 0, 0
        
        start_price = float(data[0][1])  # Open of first candle
        current_price = float(data[-1][4])  # Close of last candle
        
        direction = 'UP' if current_price >= start_price else 'DOWN'
        return direction, current_price, start_price
        
    except Exception as e:
        log(f'Price error: {e}')
        return 'UP', 0, 0

def get_current_market():
    """Get the current 15-min BTC market"""
    window_start = get_window_start_time()
    ts = int(window_start.timestamp())
    slug = f'btc-updown-15m-{ts}'
    
    try:
        r = requests.get(f'https://gamma-api.polymarket.com/events?slug={slug}', timeout=10)
        events = r.json()
        if events:
            e = events[0]
            m = e['markets'][0]
            if not m.get('closed'):
                return {
                    'slug': slug,
                    'title': e['title'],
                    'tokens': json.loads(m['clobTokenIds']),
                    'odds': json.loads(m['outcomePrices']),
                    'end_time': m['endDate']
                }
    except Exception as e:
        log(f'Market error: {e}')
    return None

def place_trade(client, market, direction):
    """Place a trade"""
    token_idx = 0 if direction == 'UP' else 1
    token_id = market['tokens'][token_idx]
    odds = float(market['odds'][token_idx])
    
    # Calculate shares - must be at least 5
    price = min(odds + 0.02, 0.95)  # Pay slightly above market, max 95c
    shares = max(MIN_SHARES, round(TRADE_AMOUNT / price, 2))
    
    log(f'Placing {direction} bet: {shares} shares @ ${price:.2f}')
    
    order_args = OrderArgs(
        price=price,
        size=shares,
        side='BUY',
        token_id=token_id
    )
    
    signed = client.create_order(order_args)
    result = client.post_order(signed, OrderType.GTC)
    return result

def main():
    log('=' * 60)
    log('LIVE TRADER STARTED')
    log('Strategy: Bet direction based on window start vs current price')
    log('=' * 60)
    
    # Setup client
    cloudflare_bypass.apply_cloudflare_bypass()
    key = os.getenv('PRIVATE_KEY')
    client = ClobClient('https://clob.polymarket.com', key=key, chain_id=137)
    creds = client.create_or_derive_api_creds()
    client.set_api_creds(creds)
    log('Client connected!')
    
    trades_data = load_trades()
    
    # Check if we already traded the current market (handles restarts)
    last_market = None
    if trades_data['trades']:
        last_trade = trades_data['trades'][-1]
        last_market = last_trade.get('market')
        log(f'Last traded market: {last_market[-10:] if last_market else "None"}')
    
    while True:
        try:
            market = get_current_market()
            
            if not market:
                log('No active market, waiting...')
                time.sleep(30)
                continue
            
            # Only trade once per market - check trade log too
            already_traded = any(t.get('market') == market['slug'] for t in trades_data['trades'])
            if market['slug'] == last_market or already_traded:
                now = datetime.now()
                curr_min = 15 * (now.minute // 15)
                next_min = curr_min + 15
                if next_min >= 60:
                    wait_secs = (60 - now.minute) * 60 + 5 - now.second
                else:
                    wait_secs = (next_min - now.minute) * 60 + 5 - now.second
                wait_secs = max(wait_secs, 10)
                log(f'Already traded {market["slug"][-10:]}. Next in {wait_secs}s')
                time.sleep(min(wait_secs, 60))
                continue
            
            # Get direction based on window start vs current price
            direction, current_price, start_price = get_btc_direction()
            diff = current_price - start_price
            
            log(f'Market: {market["title"]}')
            log(f'Start: ${start_price:,.0f} | Now: ${current_price:,.0f} | Diff: ${diff:+,.0f}')
            log(f'Betting: {direction}')
            
            result = place_trade(client, market, direction)
            
            if result.get('success'):
                log(f'✅ TRADE PLACED!')
                log(f'   Order ID: {result["orderID"][:20]}...')
                log(f'   Status: {result["status"]}')
                
                trade_record = {
                    'time': datetime.now().isoformat(),
                    'market': market['slug'],
                    'direction': direction,
                    'start_price': start_price,
                    'entry_price': current_price,
                    'diff': diff,
                    'order_id': result['orderID'],
                    'status': result['status'],
                    'result': 'pending'
                }
                trades_data['trades'].append(trade_record)
                trades_data['pending'] += 1
                save_trades(trades_data)
                
                last_market = market['slug']
            else:
                log(f'❌ Trade failed: {result}')
            
            time.sleep(30)
            
        except KeyboardInterrupt:
            log('Stopped by user')
            break
        except Exception as e:
            log(f'Error: {e}')
            import traceback
            traceback.print_exc()
            time.sleep(30)
    
    log('Trader stopped')

if __name__ == '__main__':
    main()
