#!/usr/bin/env python3
"""
Improved market finder that automatically finds the next active BTC 15-min market
"""
import requests
import json
from datetime import datetime, timezone, timedelta

def get_next_active_market(asset='btc'):
    """
    Find the next active 15-min market for the given asset.
    Checks current window, then next window if current is closed.
    """
    et = timezone(timedelta(hours=-5))
    now = datetime.now(et)
    
    # Try current window first, then next 3 windows
    for offset in range(4):
        # Calculate window start time
        total_minutes = now.hour * 60 + now.minute + (offset * 15)
        window_hour = total_minutes // 60
        window_min = 15 * ((total_minutes % 60) // 15)
        
        # Handle day rollover
        check_time = now.replace(hour=window_hour % 24, minute=window_min, second=0, microsecond=0)
        if offset > 0 and window_hour >= 24:
            check_time += timedelta(days=1)
            check_time = check_time.replace(hour=window_hour % 24)
        
        ts = int(check_time.timestamp())
        slug = f'{asset}-updown-15m-{ts}'
        
        try:
            r = requests.get(f'https://gamma-api.polymarket.com/events?slug={slug}', timeout=10)
            events = r.json()
            
            if events and len(events) > 0:
                e = events[0]
                m = e['markets'][0]
                
                # Check if market is active and accepting orders
                if not m.get('closed') and m.get('acceptingOrders'):
                    # Parse current prices
                    prices = json.loads(m.get('outcomePrices', '["0.5", "0.5"]'))
                    
                    return {
                        'slug': slug,
                        'title': e['title'],
                        'tokens': json.loads(m['clobTokenIds']),
                        'prices': {
                            'up': float(prices[0]),
                            'down': float(prices[1])
                        },
                        'end_time': m['endDate'],
                        'event_start': e.get('startTime'),
                        'window_offset': offset,
                        'accepting_orders': m.get('acceptingOrders', False)
                    }
        except Exception as e:
            print(f"Error checking {slug}: {e}")
            continue
    
    return None

def get_all_active_15m_markets():
    """Get all active 15-minute Up/Down markets"""
    try:
        # Query series for 15-minute markets
        r = requests.get(
            'https://gamma-api.polymarket.com/events',
            params={
                'tag_slug': '15M',
                'active': 'true',
                'closed': 'false',
                'limit': 20
            },
            timeout=10
        )
        events = r.json()
        
        active_markets = []
        for e in events:
            if 'markets' in e and len(e['markets']) > 0:
                m = e['markets'][0]
                if m.get('acceptingOrders') and not m.get('closed'):
                    prices = json.loads(m.get('outcomePrices', '["0.5", "0.5"]'))
                    active_markets.append({
                        'slug': e['slug'],
                        'title': e['title'],
                        'asset': e['slug'].split('-')[0].upper(),
                        'prices': {
                            'up': float(prices[0]),
                            'down': float(prices[1])
                        },
                        'end_time': m['endDate'],
                        'volume': m.get('volumeNum', 0),
                        'liquidity': m.get('liquidityNum', 0)
                    })
        
        return active_markets
    except Exception as e:
        print(f"Error fetching markets: {e}")
        return []

if __name__ == '__main__':
    print("=" * 60)
    print("NEXT ACTIVE BTC 15-MIN MARKET")
    print("=" * 60)
    
    market = get_next_active_market('btc')
    if market:
        print(f"\n✅ Found: {market['title']}")
        print(f"   Slug: {market['slug']}")
        print(f"   Up: {market['prices']['up']:.1%}")
        print(f"   Down: {market['prices']['down']:.1%}")
        print(f"   End: {market['end_time']}")
        print(f"   Window offset: {market['window_offset']} (0=current, 1=next, etc)")
    else:
        print("\n❌ No active market found")
    
    print("\n" + "=" * 60)
    print("ALL ACTIVE 15-MIN MARKETS")
    print("=" * 60)
    
    all_markets = get_all_active_15m_markets()
    for m in all_markets[:10]:
        print(f"\n📊 {m['title']}")
        print(f"   Up: {m['prices']['up']:.1%} | Down: {m['prices']['down']:.1%}")
