#!/usr/bin/env python3
import requests
from datetime import datetime

# Get the BTC price at start of current 15-min window
r = requests.get('https://api.binance.us/api/v3/klines', params={
    'symbol': 'BTCUSDT',
    'interval': '1m',
    'limit': 15  # Last 15 minutes
}, timeout=10)
data = r.json()

# First candle is ~15 mins ago (window start)
start_candle = data[0]
current_candle = data[-1]

start_price = float(start_candle[1])  # Open price
current_price = float(current_candle[4])  # Close price

print(f'Window start price: ${start_price:,.2f}')
print(f'Current price: ${current_price:,.2f}')
print(f'Difference: ${current_price - start_price:+,.2f}')
print(f'Should bet: {"UP" if current_price >= start_price else "DOWN"}')
