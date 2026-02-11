#!/usr/bin/env python3
"""
Smart BTC 15-min Trader
Strategy: Follow market consensus when odds > 55%
"""
import os
import sys
import json
import time
import requests
from datetime import datetime, timezone, timedelta

sys.path.insert(0, '/Users/garciafamilybusiness/deal_finder/TradingPal')
os.chdir('/Users/garciafamilybusiness/deal_finder/TradingPal')

from dotenv import load_dotenv
load_dotenv()

import cloudflare_bypass
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType

LOG_FILE = '/tmp/smart_trader.log'
RESULTS_FILE = '/tmp/smart_results.json'

MIN_EDGE = 0.55  # Only bet when one side has >55% odds
MAX_PRICE = 0.60  # Don't pay more than 60 cents
MIN_SHARES = 5

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def load_results():
    try:
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'trades': [], 'wins': 0, 'losses': 0, 'pending': 0}

def save_results(data):
    with open(RESULTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_market():
    et = timezone(timedelta(hours=-5))
    now = datetime.now(et)
    curr_min = 15 * (now.minute // 15)
    window_start = now.replace(minute=curr_min, second=0, microsecond=0)
    ts = int(window_start.timestamp())
    slug = f'btc-updown-15m-{ts}'
    
    try:
        r = requests.get(f'https://gamma-api.polymarket.com/events?slug={slug}', timeout=10)
        events = r.json()
        if events:
            e = events[0]
            m = e['markets'][0]
            if not m.get('closed') and m.get('acceptingOrders'):
                prices = json.loads(m.get('outcomePrices', '["0.5","0.5"]'))
                return {
                    'slug': slug,
                    'title': e['title'],
                    'tokens': json.loads(m['clobTokenIds']),
                    'up': float(prices[0]),
                    'down': float(prices[1])
                }
    except Exception as e:
        log(f"Market error: {e}")
    return None

def check_winner(slug):
    try:
        r = requests.get(f'https://gamma-api.polymarket.com/events?slug={slug}', timeout=10)
        events = r.json()
        if events:
            m = events[0]['markets'][0]
            if m.get('closed'):
                prices = json.loads(m.get('outcomePrices', '["0","0"]'))
                if float(prices[0]) == 1:
                    return 'UP'
                elif float(prices[1]) == 1:
                    return 'DOWN'
    except:
        pass
    return None

def resolve_pending(data):
    for trade in data['trades']:
        if trade.get('result') == 'pending':
            winner = check_winner(trade['market'])
            if winner:
                if trade['direction'] == winner:
                    trade['result'] = 'WIN'
                    data['wins'] += 1
                    log(f"✅ WON: {trade['market'][-10:]} - bet {trade['direction']}")
                else:
                    trade['result'] = 'LOSS'
                    data['losses'] += 1
                    log(f"❌ LOST: {trade['market'][-10:]} - bet {trade['direction']}, {winner} won")
                data['pending'] -= 1
                save_results(data)
    return data

def place_trade(client, market, direction):
    token_idx = 0 if direction == 'UP' else 1
    token_id = market['tokens'][token_idx]
    price = market['up'] if direction == 'UP' else market['down']
    
    if price > MAX_PRICE:
        log(f"⏭️ Price too high: {price:.0%}")
        return None
    
    order_price = min(price + 0.02, MAX_PRICE)
    
    log(f"💰 Placing {direction}: {MIN_SHARES} shares @ ${order_price:.2f}")
    
    order_args = OrderArgs(price=order_price, size=MIN_SHARES, side='BUY', token_id=token_id)
    signed = client.create_order(order_args)
    return client.post_order(signed, OrderType.GTC)

def main():
    log("=" * 60)
    log("🧠 SMART TRADER - Follow the Crowd (>55% edge)")
    log("=" * 60)
    
    cloudflare_bypass.apply_cloudflare_bypass()
    key = os.getenv('PRIVATE_KEY')
    client = ClobClient('https://clob.polymarket.com', key=key, chain_id=137)
    creds = client.create_or_derive_api_creds()
    client.set_api_creds(creds)
    log("✅ Connected!")
    
    data = load_results()
    traded = set(t['market'] for t in data['trades'])
    
    while True:
        try:
            data = resolve_pending(data)
            
            market = get_market()
            if not market:
                log("No market, waiting...")
                time.sleep(30)
                continue
            
            if market['slug'] in traded:
                time.sleep(30)
                continue
            
            up_odds = market['up']
            down_odds = market['down']
            
            # Determine if there's an edge
            if up_odds >= MIN_EDGE:
                direction = 'UP'
                edge = up_odds
            elif down_odds >= MIN_EDGE:
                direction = 'DOWN'
                edge = down_odds
            else:
                log(f"⏸️ No edge: UP {up_odds:.0%} / DOWN {down_odds:.0%}")
                traded.add(market['slug'])  # Skip this window
                time.sleep(30)
                continue
            
            log(f"\n📊 {market['title']}")
            log(f"   Odds: UP {up_odds:.0%} | DOWN {down_odds:.0%}")
            log(f"   Edge: {direction} @ {edge:.0%}")
            
            result = place_trade(client, market, direction)
            
            if result and result.get('success'):
                log(f"✅ TRADE PLACED!")
                traded.add(market['slug'])
                data['trades'].append({
                    'time': datetime.now().isoformat(),
                    'market': market['slug'],
                    'direction': direction,
                    'odds': edge,
                    'result': 'pending'
                })
                data['pending'] += 1
                save_results(data)
            else:
                log(f"❌ Failed: {result}")
            
            time.sleep(60)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            log(f"Error: {e}")
            time.sleep(30)

if __name__ == '__main__':
    main()
