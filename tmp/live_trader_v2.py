#!/usr/bin/env python3
"""
Live Trader v2 - Improved market detection
Auto-switches to next active market when current closes
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
MIN_SHARES = 5  # Polymarket minimum shares
MAX_PRICE = 0.55  # Only enter if price ≤ 55¢ (keeps cost ~$2.75)
TRADE_LOG = 'live_trades_v2.json'

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line, flush=True)
    with open('/tmp/live_trader_v2.log', 'a') as f:
        f.write(line + '\n')

def load_trades():
    try:
        with open(TRADE_LOG, 'r') as f:
            return json.load(f)
    except:
        return {'trades': [], 'wins': 0, 'losses': 0, 'pending': 0}

def save_trades(data):
    with open(TRADE_LOG, 'w') as f:
        json.dump(data, f, indent=2)

def get_next_active_market(asset='btc'):
    """Find the next active 15-min market - checks multiple windows"""
    et = timezone(timedelta(hours=-5))
    now = datetime.now(et)
    
    for offset in range(4):
        total_minutes = now.hour * 60 + now.minute + (offset * 15)
        window_hour = total_minutes // 60
        window_min = 15 * ((total_minutes % 60) // 15)
        
        check_time = now.replace(hour=window_hour % 24, minute=window_min, second=0, microsecond=0)
        if window_hour >= 24:
            check_time += timedelta(days=1)
            check_time = check_time.replace(hour=window_hour % 24)
        
        ts = int(check_time.timestamp())
        slug = f'{asset}-updown-15m-{ts}'
        
        try:
            r = requests.get(f'https://gamma-api.polymarket.com/events?slug={slug}', timeout=10)
            events = r.json()
            
            if events:
                e = events[0]
                m = e['markets'][0]
                
                if not m.get('closed') and m.get('acceptingOrders'):
                    prices = json.loads(m.get('outcomePrices', '["0.5", "0.5"]'))
                    return {
                        'slug': slug,
                        'title': e['title'],
                        'tokens': json.loads(m['clobTokenIds']),
                        'prices': {'up': float(prices[0]), 'down': float(prices[1])},
                        'end_time': m['endDate'],
                        'offset': offset
                    }
        except Exception as e:
            continue
    return None

def get_btc_direction():
    """Compare current price to 15-min window start"""
    et = timezone(timedelta(hours=-5))
    now = datetime.now(et)
    curr_min = 15 * (now.minute // 15)
    window_start = now.replace(minute=curr_min, second=0, microsecond=0)
    start_ts = int(window_start.timestamp() * 1000)
    
    try:
        r = requests.get('https://api.binance.us/api/v3/klines', params={
            'symbol': 'BTCUSDT', 'interval': '1m', 'startTime': start_ts, 'limit': 20
        }, timeout=10)
        data = r.json()
        
        if not data:
            return 'UP', 0, 0
        
        start_price = float(data[0][1])
        current_price = float(data[-1][4])
        direction = 'UP' if current_price >= start_price else 'DOWN'
        return direction, current_price, start_price
    except:
        return 'UP', 0, 0

def place_trade(client, market, direction):
    """Place a trade - minimum size, skip if too expensive"""
    token_idx = 0 if direction == 'UP' else 1
    token_id = market['tokens'][token_idx]
    market_price = market['prices']['up' if direction == 'UP' else 'down']
    
    # Skip if market already too expensive (odds too skewed)
    if market_price > MAX_PRICE:
        log(f'⏭️ Skipping - price {market_price:.0%} > max {MAX_PRICE:.0%}')
        return {'success': False, 'reason': 'too_expensive'}
    
    price = min(market_price + 0.02, MAX_PRICE + 0.05)  # Small buffer above market
    shares = MIN_SHARES  # Always minimum
    cost = shares * price
    
    log(f'Placing {direction}: {shares} shares @ ${price:.2f} (${cost:.2f} total)')
    
    order_args = OrderArgs(price=price, size=shares, side='BUY', token_id=token_id)
    signed = client.create_order(order_args)
    return client.post_order(signed, OrderType.GTC)

def main():
    log('=' * 60)
    log('🚀 LIVE TRADER V2 - Skipper at the helm!')
    log('=' * 60)
    
    cloudflare_bypass.apply_cloudflare_bypass()
    key = os.getenv('PRIVATE_KEY')
    client = ClobClient('https://clob.polymarket.com', key=key, chain_id=137)
    creds = client.create_or_derive_api_creds()
    client.set_api_creds(creds)
    log('✅ Client connected!')
    
    trades_data = load_trades()
    traded_markets = set(t.get('market') for t in trades_data['trades'])
    
    while True:
        try:
            market = get_next_active_market('btc')
            
            if not market:
                log('No active market, waiting 30s...')
                time.sleep(30)
                continue
            
            if market['slug'] in traded_markets:
                log(f"Already traded {market['slug'][-10:]}, waiting...")
                time.sleep(30)
                continue
            
            direction, curr_price, start_price = get_btc_direction()
            diff = curr_price - start_price
            
            log(f"Market: {market['title']}")
            log(f'BTC Start: ${start_price:,.0f} | Now: ${curr_price:,.0f} | Diff: ${diff:+,.0f}')
            log(f"Odds: Up {market['prices']['up']:.1%} | Down {market['prices']['down']:.1%}")
            log(f'Betting: {direction}')
            
            result = place_trade(client, market, direction)
            
            if result.get('success'):
                log(f"✅ TRADE PLACED! Order: {result['orderID'][:20]}...")
                traded_markets.add(market['slug'])
                trades_data['trades'].append({
                    'time': datetime.now().isoformat(),
                    'market': market['slug'],
                    'direction': direction,
                    'btc_start': start_price,
                    'btc_entry': curr_price,
                    'order_id': result['orderID']
                })
                trades_data['pending'] += 1
                save_trades(trades_data)
            else:
                log(f'❌ Failed: {result}')
            
            time.sleep(60)
            
        except KeyboardInterrupt:
            log('Stopped by captain!')
            break
        except Exception as e:
            log(f'Error: {e}')
            import traceback
            traceback.print_exc()
            time.sleep(30)

if __name__ == '__main__':
    main()
