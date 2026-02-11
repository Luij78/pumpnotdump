#!/usr/bin/env python3
"""Test with httpx HTTP/2"""
import httpx
import json

print("Testing with httpx HTTP/2...")

client = httpx.Client(
    http2=True,
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://polymarket.com',
        'Referer': 'https://polymarket.com/',
    },
    timeout=30
)

# Test GET
r = client.get('https://clob.polymarket.com/time')
print(f"GET /time: {r.status_code} - HTTP/{r.http_version}")

# Test POST  
r2 = client.post('https://clob.polymarket.com/order', json={'test': True})
print(f"POST /order: {r2.status_code} - HTTP/{r2.http_version}")

if r2.status_code != 200:
    print(f"Response: {r2.text[:200]}")

client.close()
