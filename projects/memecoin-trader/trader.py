#!/usr/bin/env python3
"""
Skipper's Memecoin Trader 🚀
Solana memecoin trading bot using Jupiter API
"""

import json
import subprocess
import base64
import sys
import os
from pathlib import Path

# Add solana path
os.environ["PATH"] = f"{Path.home()}/.local/share/solana/install/active_release/bin:" + os.environ.get("PATH", "")

JUPITER_LITE_API = "https://lite-api.jup.ag/swap/v1"
SOL_MINT = "So11111111111111111111111111111111111111112"
KEYPAIR_PATH = Path.home() / ".config/solana/skipper-wallet.json"

def run_cmd(cmd):
    """Run shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_wallet_pubkey():
    return run_cmd("solana address")

def get_balance():
    return run_cmd("solana balance")

def sol_to_lamports(sol: float) -> int:
    return int(sol * 1_000_000_000)

def lamports_to_sol(lamports: int) -> float:
    return lamports / 1_000_000_000

def get_quote(output_mint: str, sol_amount: float):
    """Get swap quote using curl (more reliable than Python requests in some envs)"""
    amount = sol_to_lamports(sol_amount)
    url = f"{JUPITER_LITE_API}/quote?inputMint={SOL_MINT}&outputMint={output_mint}&amount={amount}&slippageBps=100"
    result = run_cmd(f'curl -s "{url}"')
    try:
        return json.loads(result)
    except:
        return None

def get_swap_tx(quote: dict, user_pubkey: str):
    """Get swap transaction"""
    payload = json.dumps({
        "quoteResponse": quote,
        "userPublicKey": user_pubkey,
        "wrapAndUnwrapSol": True,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": "auto"
    })
    
    url = f"{JUPITER_LITE_API}/swap"
    result = run_cmd(f"curl -s -X POST '{url}' -H 'Content-Type: application/json' -d '{payload}'")
    try:
        return json.loads(result)
    except:
        print(f"Failed to parse swap response: {result[:200]}")
        return None

def sign_and_send(swap_tx_base64: str):
    """Sign and send transaction using solana CLI"""
    # Decode base64 to raw transaction
    tx_bytes = base64.b64decode(swap_tx_base64)
    
    # Write to temp file
    tx_path = "/tmp/swap_tx.bin"
    with open(tx_path, "wb") as f:
        f.write(tx_bytes)
    
    # Use solana CLI to sign and send
    # Note: This requires proper setup - the transaction from Jupiter is already serialized
    # We need to sign it with our keypair
    
    print("⚠️ Transaction ready but needs signing...")
    print(f"TX bytes: {len(tx_bytes)} bytes")
    return None

def buy_token(token_mint: str, sol_amount: float):
    """Buy a token with SOL"""
    print(f"\n🎯 BUYING {token_mint[:8]}... with {sol_amount} SOL")
    
    pubkey = get_wallet_pubkey()
    print(f"📍 Wallet: {pubkey}")
    print(f"💰 Balance: {get_balance()}")
    
    # Get quote
    print("📊 Getting quote...")
    quote = get_quote(token_mint, sol_amount)
    
    if not quote or "error" in str(quote).lower():
        print(f"❌ Quote failed: {quote}")
        return None
    
    out_amount = int(quote.get("outAmount", 0))
    price_impact = float(quote.get("priceImpactPct", 0))
    
    print(f"✅ Quote received:")
    print(f"   Output: {out_amount:,} tokens")
    print(f"   Price Impact: {price_impact:.4f}%")
    print(f"   Route: {quote.get('routePlan', [{}])[0].get('swapInfo', {}).get('label', 'Unknown')}")
    
    # Get swap transaction
    print("🔄 Getting swap transaction...")
    swap_response = get_swap_tx(quote, pubkey)
    
    if not swap_response or "error" in str(swap_response).lower():
        print(f"❌ Swap TX failed: {swap_response}")
        return None
    
    swap_tx = swap_response.get("swapTransaction")
    if swap_tx:
        print(f"✅ Swap TX received ({len(swap_tx)} chars)")
        
        # For now, save the transaction for manual execution
        with open("/tmp/last_swap.json", "w") as f:
            json.dump({
                "quote": quote,
                "swapTransaction": swap_tx,
                "pubkey": pubkey,
                "token": token_mint,
                "amount": sol_amount
            }, f, indent=2)
        
        print("💾 Transaction saved to /tmp/last_swap.json")
        return swap_response
    
    return None

def main():
    print("=" * 50)
    print("⚓ SKIPPER MEMECOIN TRADER")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python trader.py quote <token_mint> <sol_amount>")
        print("  python trader.py buy <token_mint> <sol_amount>")
        print("  python trader.py balance")
        print("\nExample:")
        print("  python trader.py quote ER8Hgvjk... 0.05")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "balance":
        print(f"📍 Wallet: {get_wallet_pubkey()}")
        print(f"💰 Balance: {get_balance()}")
    
    elif action == "quote":
        if len(sys.argv) < 4:
            print("Usage: trader.py quote <token_mint> <sol_amount>")
            sys.exit(1)
        token = sys.argv[2]
        amount = float(sys.argv[3])
        quote = get_quote(token, amount)
        print(json.dumps(quote, indent=2))
    
    elif action == "buy":
        if len(sys.argv) < 4:
            print("Usage: trader.py buy <token_mint> <sol_amount>")
            sys.exit(1)
        token = sys.argv[2]
        amount = float(sys.argv[3])
        buy_token(token, amount)
    
    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
