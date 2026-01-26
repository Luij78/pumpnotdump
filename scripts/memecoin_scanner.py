#!/usr/bin/env python3
"""
Memecoin Scanner - Finds runners before they moon
Checks for: Volume spikes, holder growth, price pumps
"""

import requests
import json
from datetime import datetime

def scan_trending_memecoins():
    """Scan DexScreener for trending Solana memecoins"""
    
    findings = []
    
    try:
        # Get trending tokens from DexScreener
        resp = requests.get(
            'https://api.dexscreener.com/latest/dex/tokens/trending',
            timeout=30
        )
        
        if resp.status_code == 200:
            data = resp.json()
            tokens = data if isinstance(data, list) else data.get('tokens', [])
            
            for token in tokens[:20]:
                try:
                    price_change_24h = float(token.get('priceChange', {}).get('h24', 0) or 0)
                    volume_24h = float(token.get('volume', {}).get('h24', 0) or 0)
                    liquidity = float(token.get('liquidity', {}).get('usd', 0) or 0)
                    
                    # Alert criteria: >50% gain, >$100k volume, >$20k liquidity
                    if price_change_24h > 50 and volume_24h > 100000 and liquidity > 20000:
                        findings.append({
                            'name': token.get('baseToken', {}).get('name', 'Unknown'),
                            'symbol': token.get('baseToken', {}).get('symbol', '???'),
                            'price': token.get('priceUsd', 'N/A'),
                            'change_24h': price_change_24h,
                            'volume_24h': volume_24h,
                            'liquidity': liquidity,
                            'chain': token.get('chainId', 'unknown'),
                            'address': token.get('baseToken', {}).get('address', 'N/A')
                        })
                except:
                    continue
    except Exception as e:
        print(f"DexScreener error: {e}")
    
    # Also check Solana specific
    try:
        resp = requests.get(
            'https://api.dexscreener.com/latest/dex/search?q=solana',
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            pairs = data.get('pairs', [])
            
            for pair in pairs[:30]:
                try:
                    price_change_24h = float(pair.get('priceChange', {}).get('h24', 0) or 0)
                    volume_24h = float(pair.get('volume', {}).get('h24', 0) or 0)
                    liquidity = float(pair.get('liquidity', {}).get('usd', 0) or 0)
                    txns_24h = pair.get('txns', {}).get('h24', {})
                    buys = txns_24h.get('buys', 0)
                    sells = txns_24h.get('sells', 0)
                    
                    # Runner criteria: >100% pump, high volume, more buys than sells
                    if price_change_24h > 100 and volume_24h > 50000 and buys > sells:
                        findings.append({
                            'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                            'symbol': pair.get('baseToken', {}).get('symbol', '???'),
                            'price': pair.get('priceUsd', 'N/A'),
                            'change_24h': price_change_24h,
                            'volume_24h': volume_24h,
                            'liquidity': liquidity,
                            'buys': buys,
                            'sells': sells,
                            'chain': 'solana',
                            'address': pair.get('baseToken', {}).get('address', 'N/A')
                        })
                except:
                    continue
    except Exception as e:
        print(f"Solana scan error: {e}")
    
    # Deduplicate by address
    seen = set()
    unique_findings = []
    for f in findings:
        if f['address'] not in seen:
            seen.add(f['address'])
            unique_findings.append(f)
    
    # Sort by 24h change
    unique_findings.sort(key=lambda x: x.get('change_24h', 0), reverse=True)
    
    return unique_findings[:5]  # Top 5 runners

def format_alert(findings):
    """Format findings into alert message"""
    if not findings:
        return None
    
    msg = "🚨 **MEMECOIN RUNNER ALERT** 🚨\n\n"
    
    for i, coin in enumerate(findings, 1):
        msg += f"**{i}. {coin['symbol']}** ({coin['name'][:20]})\n"
        msg += f"   💰 Price: ${coin['price']}\n"
        msg += f"   📈 24h: +{coin['change_24h']:.1f}%\n"
        msg += f"   📊 Volume: ${coin['volume_24h']:,.0f}\n"
        msg += f"   💧 Liquidity: ${coin['liquidity']:,.0f}\n"
        if coin.get('buys') and coin.get('sells'):
            msg += f"   🟢 Buys/Sells: {coin['buys']}/{coin['sells']}\n"
        msg += f"   📍 CA: `{coin['address'][:20]}...`\n\n"
    
    msg += "⚠️ DYOR - Not financial advice!"
    
    return msg

if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Scanning for memecoin runners...")
    findings = scan_trending_memecoins()
    
    if findings:
        alert = format_alert(findings)
        print(alert)
        
        # Save to file for cron job to pick up
        with open('/Users/luisgarcia/clawd/scripts/latest_scan.json', 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'findings': findings
            }, f, indent=2)
    else:
        print("No runners detected this scan.")
