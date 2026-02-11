#!/usr/bin/env python3
"""
Hold to Settlement Bot
- Picks direction using MA crossover (same as original)
- Places bet
- WAITS for market to settle
- AUTO-REDEEMS winnings

This is what the original bot SHOULD have done.
"""
import os
import sys
import json
import time
import requests
from datetime import datetime, timezone, timedelta
from web3 import Web3

sys.path.insert(0, '/Users/garciafamilybusiness/deal_finder/TradingPal')
os.chdir('/Users/garciafamilybusiness/deal_finder/TradingPal')

from dotenv import load_dotenv
load_dotenv()

import cloudflare_bypass
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType

LOG_FILE = '/tmp/hold_to_settle.log'
RESULTS_FILE = '/tmp/hold_results.json'

MIN_SHARES = 5
MAX_PRICE = 0.55  # Only enter at reasonable prices

# Redemption contracts
USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
CTF_ADDRESS = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045"

REDEEM_ABI = [{
    "constant": False,
    "inputs": [
        {"name": "collateralToken", "type": "address"},
        {"name": "parentCollectionId", "type": "bytes32"},
        {"name": "conditionId", "type": "bytes32"},
        {"name": "indexSets", "type": "uint256[]"}
    ],
    "name": "redeemPositions",
    "outputs": [],
    "type": "function"
}]

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
        return {'trades': [], 'wins': 0, 'losses': 0, 'redeemed': 0, 'total_profit': 0}

def save_results(data):
    with open(RESULTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_btc_trend():
    """MA crossover - same as original bot"""
    try:
        r = requests.get('https://api.binance.us/api/v3/klines?symbol=BTCUSDT&interval=5m&limit=10', timeout=10)
        data = r.json()
        closes = [float(k[4]) for k in data]
        current = closes[-1]
        ma5 = sum(closes[-5:]) / 5
        direction = 'DOWN' if current < ma5 else 'UP'
        return direction, current, ma5
    except:
        return 'UP', 0, 0

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
                    'condition_id': m['conditionId'],
                    'up': float(prices[0]),
                    'down': float(prices[1]),
                    'end_time': m['endDate']
                }
    except Exception as e:
        log(f"Market error: {e}")
    return None

def check_market_resolved(slug):
    """Check if market resolved and who won"""
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

def redeem_position(condition_id, pk):
    """Redeem winning shares"""
    try:
        w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
        account = w3.eth.account.from_key(pk)
        
        ctf = w3.eth.contract(
            address=Web3.to_checksum_address(CTF_ADDRESS),
            abi=REDEEM_ABI
        )
        
        tx = ctf.functions.redeemPositions(
            Web3.to_checksum_address(USDC_ADDRESS),
            bytes.fromhex('00' * 32),
            bytes.fromhex(condition_id[2:]),
            [1, 2]
        ).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 300000,
            'gasPrice': w3.eth.gas_price,
            'chainId': 137
        })
        
        signed = w3.eth.account.sign_transaction(tx, pk)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
        return receipt.status == 1
    except Exception as e:
        log(f"Redeem error: {e}")
        return False

def place_trade(client, market, direction):
    token_idx = 0 if direction == 'UP' else 1
    token_id = market['tokens'][token_idx]
    price = market['up'] if direction == 'UP' else market['down']
    
    if price > MAX_PRICE:
        log(f"⏭️ Price too high: {price:.0%}")
        return None
    
    order_price = min(price + 0.02, MAX_PRICE + 0.05)
    cost = MIN_SHARES * order_price
    
    log(f"💰 Placing {direction}: {MIN_SHARES} shares @ ${order_price:.2f} (${cost:.2f})")
    
    order_args = OrderArgs(price=order_price, size=MIN_SHARES, side='BUY', token_id=token_id)
    signed = client.create_order(order_args)
    return client.post_order(signed, OrderType.GTC)

def main():
    log("=" * 60)
    log("🎯 HOLD TO SETTLEMENT BOT")
    log("   Strategy: MA crossover + Wait for settle + Auto-redeem")
    log("=" * 60)
    
    cloudflare_bypass.apply_cloudflare_bypass()
    pk = os.getenv('PRIVATE_KEY')
    client = ClobClient('https://clob.polymarket.com', key=pk, chain_id=137)
    creds = client.create_or_derive_api_creds()
    client.set_api_creds(creds)
    log("✅ Connected!")
    
    data = load_results()
    traded = set(t['market'] for t in data['trades'])
    pending_trades = [t for t in data['trades'] if t.get('result') == 'pending']
    
    while True:
        try:
            # First, check pending trades for resolution
            for trade in pending_trades[:]:
                winner = check_market_resolved(trade['market'])
                if winner:
                    if trade['direction'] == winner:
                        log(f"✅ WON: {trade['market'][-10:]} - Redeeming...")
                        if redeem_position(trade['condition_id'], pk):
                            trade['result'] = 'WIN'
                            trade['redeemed'] = True
                            data['wins'] += 1
                            data['redeemed'] += 1
                            profit = MIN_SHARES * 1.0 - trade['cost']
                            data['total_profit'] += profit
                            log(f"   💵 Redeemed! Profit: ${profit:.2f}")
                        else:
                            trade['result'] = 'WIN'
                            trade['redeemed'] = False
                            data['wins'] += 1
                            log(f"   ⚠️ Won but redeem failed")
                    else:
                        trade['result'] = 'LOSS'
                        data['losses'] += 1
                        log(f"❌ LOST: {trade['market'][-10:]}")
                    
                    pending_trades.remove(trade)
                    save_results(data)
                    log(f"📊 Record: {data['wins']}W / {data['losses']}L | Profit: ${data['total_profit']:.2f}")
            
            # Look for new trade
            market = get_market()
            if not market:
                time.sleep(30)
                continue
            
            if market['slug'] in traded:
                time.sleep(30)
                continue
            
            # Get direction from MA crossover
            direction, btc_now, ma5 = get_btc_trend()
            
            log(f"\n📊 {market['title']}")
            log(f"   BTC: ${btc_now:,.0f} | MA5: ${ma5:,.0f}")
            log(f"   Signal: {direction}")
            log(f"   Odds: UP {market['up']:.0%} | DOWN {market['down']:.0%}")
            
            result = place_trade(client, market, direction)
            
            if result and result.get('success'):
                price = market['up'] if direction == 'UP' else market['down']
                cost = MIN_SHARES * min(price + 0.02, MAX_PRICE + 0.05)
                
                trade = {
                    'time': datetime.now().isoformat(),
                    'market': market['slug'],
                    'condition_id': market['condition_id'],
                    'direction': direction,
                    'btc': btc_now,
                    'ma5': ma5,
                    'cost': cost,
                    'result': 'pending'
                }
                
                data['trades'].append(trade)
                traded.add(market['slug'])
                pending_trades.append(trade)
                save_results(data)
                
                log(f"✅ TRADE PLACED! Waiting for settlement...")
            else:
                log(f"❌ Trade failed: {result}")
                traded.add(market['slug'])  # Skip this window
            
            time.sleep(60)
            
        except KeyboardInterrupt:
            log("Stopped!")
            break
        except Exception as e:
            log(f"Error: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(30)

if __name__ == '__main__':
    main()
