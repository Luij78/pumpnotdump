#!/usr/bin/env python3
"""Test stealth Playwright bypass"""
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import time
import json
import requests

print("Starting stealth browser...")

stealth = Stealth()

with stealth.use_sync(sync_playwright()) as p:
    browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
    context = browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = context.new_page()
    
    print("Loading Polymarket CLOB...")
    page.goto("https://clob.polymarket.com/time", timeout=30000, wait_until="domcontentloaded")
    time.sleep(2)
    content = page.content()
    print("Content:", content[:400])
    
    cookies = context.cookies()
    print("Cookies:", [c['name'] for c in cookies])
    
    cf_cookies = {c['name']: c['value'] for c in cookies}
    
    browser.close()

# Test with cookies
print("\nTesting API with cookies...")
session = requests.Session()
session.cookies.update(cf_cookies)
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Origin': 'https://polymarket.com',
    'Referer': 'https://polymarket.com/',
})

r = session.get('https://clob.polymarket.com/time')
print(f"GET /time: {r.status_code}")

r2 = session.post('https://clob.polymarket.com/order', json={'test': True})
print(f"POST /order: {r2.status_code}")

print("Done!")
