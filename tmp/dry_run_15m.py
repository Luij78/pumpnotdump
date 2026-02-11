#!/usr/bin/env python3
"""
Dry Run Tracker for BTC 15-min markets
Tracks: Price to beat, our prediction, actual outcome
"""
import json
import time
import requests
from datetime import datetime, timezone, timedelta

LOG_FILE = '/tmp/dry_run_15m.json'

def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f'[{ts}] {msg}', flush=True)

def load_log():
    try:
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'trades': [], 'wins': 0, 'losses': 0, 'pending': 0}

def save_log(data):
    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_current_btc():
    """Get current BTC price from Binance"""
    try:
        r = requests.get('https://api.binance.us/api/v3/ticker/price?symbol=BTCUSDT', timeout=5)
        return float(r.json()['price'])
    except:
        return 0

def get_market_info(slug):
    """Get market info including price to beat"""
    try:
        r = requests.get(f'https://gamma-api.polymarket.com/events?slug={slug}', timeout=10)
        events = r.json()
        if events:
            e = events[0]
            m = e['markets'][0]
            prices = json.loads(m.get('outcomePrices', '["0.5", "0.5"]'))
            return {
                'title': e['title'],
                'closed': m.get('closed', False),
                'up_price': float(prices[0]),
                'down_price': float(prices[1]),
                'accepting': m.get('acceptingOrders', False),
                'end_time': m.get('endDate')
            }
    except Exception as e:
        log(f'Market error: {e}')
    return None

def get_window_times():
    """Get current and next window timestamps"""
    et = timezone(timedelta(hours=-5))
    now = datetime.now(et)
    curr_min = 15 * (now.minute // 15)
    
    window_start = now.replace(minute=curr_min, second=0, microsecond=0)
    window_end = window_start + timedelta(minutes=15)
    next_window = window_end
    
    return {
        'now': now,
        'window_start': window_start,
        'window_end': window_end,
        'window_ts': int(window_start.timestamp()),
        'next_ts': int(next_window.timestamp()),
        'mins_left': (window_end - now).seconds // 60,
        'secs_left': (window_end - now).seconds % 60
    }

def check_and_resolve_pending(data):
    """Check if any pending trades can be resolved"""
    for trade in data['trades']:
        if trade.get('result') == 'pending':
            slug = trade['market']
            market = get_market_info(slug)
            
            if market and market['closed']:
                # Market resolved - check outcome
                if market['down_price'] == 1:
                    winner = 'DOWN'
                elif market['up_price'] == 1:
                    winner = 'UP'
                else:
                    continue
                
                if trade['prediction'] == winner:
                    trade['result'] = 'WIN'
                    data['wins'] += 1
                    log(f"✅ RESOLVED WIN: {trade['market'][-10:]} - Predicted {trade['prediction']}, Won!")
                else:
                    trade['result'] = 'LOSS'
                    data['losses'] += 1
                    log(f"❌ RESOLVED LOSS: {trade['market'][-10:]} - Predicted {trade['prediction']}, {winner} won")
                
                data['pending'] -= 1
                trade['actual_winner'] = winner
                save_log(data)
    
    return data

def main():
    log('=' * 60)
    log('🧪 DRY RUN TRACKER - BTC 15-min Markets')
    log('=' * 60)
    
    data = load_log()
    traded_markets = set(t['market'] for t in data['trades'])
    
    log(f"Loaded {len(data['trades'])} previous trades")
    log(f"Record: {data['wins']}W / {data['losses']}L / {data['pending']} pending")
    
    while True:
        try:
            # Check pending trades first
            data = check_and_resolve_pending(data)
            
            times = get_window_times()
            slug = f'btc-updown-15m-{times["window_ts"]}'
            
            # Skip if already traded this window
            if slug in traded_markets:
                log(f"Already logged {slug[-10:]}, waiting... ({times['mins_left']}m {times['secs_left']}s left)")
                time.sleep(30)
                continue
            
            market = get_market_info(slug)
            
            if not market or not market['accepting']:
                log(f"Market {slug[-10:]} not ready, waiting...")
                time.sleep(15)
                continue
            
            # Get current BTC price
            btc_now = get_current_btc()
            
            # Determine prediction based on current momentum
            # If UP is favored (>50%), predict UP. If DOWN favored, predict DOWN.
            if market['down_price'] > market['up_price']:
                prediction = 'DOWN'
            else:
                prediction = 'UP'
            
            # Log the dry run trade
            trade = {
                'time': datetime.now().isoformat(),
                'market': slug,
                'title': market['title'],
                'btc_at_entry': btc_now,
                'up_odds': market['up_price'],
                'down_odds': market['down_price'],
                'prediction': prediction,
                'result': 'pending',
                'mins_into_window': 15 - times['mins_left']
            }
            
            data['trades'].append(trade)
            data['pending'] += 1
            traded_markets.add(slug)
            save_log(data)
            
            log(f"")
            log(f"📊 DRY RUN TRADE LOGGED")
            log(f"   Market: {market['title']}")
            log(f"   BTC Now: ${btc_now:,.2f}")
            log(f"   Odds: Up {market['up_price']:.0%} | Down {market['down_price']:.0%}")
            log(f"   Prediction: {prediction}")
            log(f"   Entry: {trade['mins_into_window']} min into window")
            log(f"   Record: {data['wins']}W / {data['losses']}L / {data['pending']}P")
            log(f"")
            
            time.sleep(30)
            
        except KeyboardInterrupt:
            log("Stopped by user")
            break
        except Exception as e:
            log(f"Error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(30)

if __name__ == '__main__':
    main()
