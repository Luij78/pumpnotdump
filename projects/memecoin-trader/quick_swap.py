#!/usr/bin/env python3
"""
Quick Jupiter Swap Script for Solana memecoins
Uses Jupiter V6 API
"""

import json
import subprocess
import requests
import sys
from pathlib import Path

# Constants
JUPITER_API = "https://quote-api.jup.ag/v6"
SOL_MINT = "So11111111111111111111111111111111111111112"  # Wrapped SOL
KEYPAIR_PATH = Path.home() / ".config/solana/skipper-wallet.json"

def get_wallet_pubkey():
    """Get pubkey from solana CLI"""
    result = subprocess.run(
        ["solana", "address"],
        capture_output=True, text=True,
        env={**dict(__import__('os').environ), 
             "PATH": f"{Path.home()}/.local/share/solana/install/active_release/bin:" + __import__('os').environ.get('PATH', '')}
    )
    return result.stdout.strip()

def get_quote(input_mint: str, output_mint: str, amount: int, slippage_bps: int = 100):
    """Get swap quote from Jupiter"""
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": str(amount),
        "slippageBps": slippage_bps,
    }
    response = requests.get(f"{JUPITER_API}/quote", params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Quote error: {response.text}")
        return None

def get_swap_transaction(quote: dict, user_pubkey: str):
    """Get swap transaction from Jupiter"""
    payload = {
        "quoteResponse": quote,
        "userPublicKey": user_pubkey,
        "wrapAndUnwrapSol": True,
    }
    response = requests.post(f"{JUPITER_API}/swap", json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Swap error: {response.text}")
        return None

def lamports_to_sol(lamports: int) -> float:
    return lamports / 1_000_000_000

def sol_to_lamports(sol: float) -> int:
    return int(sol * 1_000_000_000)

def main():
    if len(sys.argv) < 3:
        print("Usage: python quick_swap.py <token_mint> <sol_amount>")
        print("Example: python quick_swap.py ER8HgvjkEa4c3ToUTGZXAcNH3Vs3XKu3KGcncM8jeJUQ 0.05")
        sys.exit(1)
    
    token_mint = sys.argv[1]
    sol_amount = float(sys.argv[2])
    
    print(f"🔍 Getting quote for {sol_amount} SOL -> {token_mint[:8]}...")
    
    pubkey = get_wallet_pubkey()
    print(f"📍 Wallet: {pubkey}")
    
    amount_lamports = sol_to_lamports(sol_amount)
    quote = get_quote(SOL_MINT, token_mint, amount_lamports)
    
    if not quote:
        print("❌ Failed to get quote")
        sys.exit(1)
    
    out_amount = int(quote.get("outAmount", 0))
    price_impact = quote.get("priceImpactPct", "0")
    
    print(f"💰 You'll receive: {out_amount:,} tokens")
    print(f"📊 Price impact: {float(price_impact)*100:.2f}%")
    print(f"🔄 Route: {' -> '.join([r['swapInfo']['label'] for r in quote.get('routePlan', [])])}")
    
    # For now, just show the quote - actual execution needs more setup
    print("\n⚠️  Quote only - transaction signing requires additional setup")
    print(json.dumps(quote, indent=2)[:500] + "...")

if __name__ == "__main__":
    main()
