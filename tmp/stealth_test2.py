#!/usr/bin/env python3
"""Capture browser headers for POST requests"""
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import time
import json
import os
import sys

sys.path.insert(0, '/Users/garciafamilybusiness/deal_finder/TradingPal')
os.chdir('/Users/garciafamilybusiness/deal_finder/TradingPal')
from dotenv import load_dotenv
load_dotenv()

print("Starting stealth browser...")

stealth = Stealth()
captured_headers = {}

with stealth.use_sync(sync_playwright()) as p:
    browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    
    # Capture requests
    def handle_request(request):
        if 'clob.polymarket.com' in request.url:
            print(f"  {request.method} {request.url}")
            captured_headers[request.url] = dict(request.headers)
    
    page.on('request', handle_request)
    
    print("Loading Polymarket CLOB...")
    page.goto("https://clob.polymarket.com/time", timeout=30000, wait_until="domcontentloaded")
    time.sleep(2)
    
    # Try making a POST via browser
    print("\nTrying POST via page.evaluate...")
    result = page.evaluate('''async () => {
        try {
            const resp = await fetch('https://clob.polymarket.com/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({test: true})
            });
            return {status: resp.status, text: await resp.text()};
        } catch(e) {
            return {error: e.toString()};
        }
    }''')
    print(f"Browser POST result: {result}")
    
    cookies = context.cookies()
    cf_cookies = {c['name']: c['value'] for c in cookies}
    
    browser.close()

print("\nCaptured headers:")
for url, headers in captured_headers.items():
    print(f"\n{url}:")
    for k, v in headers.items():
        print(f"  {k}: {v[:50]}..." if len(v) > 50 else f"  {k}: {v}")

print("\nCookies:", list(cf_cookies.keys()))
