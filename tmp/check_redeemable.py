#!/usr/bin/env python3
import requests

wallet = '0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3'
r = requests.get(f'https://data-api.polymarket.com/positions?user={wallet.lower()}')
positions = r.json()

redeemable = [p for p in positions if p.get('redeemable') and p.get('currentValue', 0) > 0]
print(f'Found {len(redeemable)} redeemable winning positions:')
total = 0
for p in redeemable:
    val = p.get('currentValue', 0)
    total += val
    print(f"  ConditionID: {p['conditionId']}")
    print(f"    Title: {p['title'][-50:]}")
    print(f"    Value: ${val:.2f}")
    print()

print(f"TOTAL REDEEMABLE: ${total:.2f}")
