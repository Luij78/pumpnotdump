#!/usr/bin/env python3
"""
Execute Jupiter swap transaction
"""

import json
import subprocess
import base64
import sys
import os
import tempfile
from pathlib import Path

os.environ["PATH"] = f"{Path.home()}/.local/share/solana/install/active_release/bin:" + os.environ.get("PATH", "")

KEYPAIR_PATH = str(Path.home() / ".config/solana/skipper-wallet.json")

def get_quote_and_swap(token_mint: str, sol_amount: float):
    """Get quote and swap transaction"""
    from urllib.request import Request, urlopen
    import json as j
    
    SOL_MINT = "So11111111111111111111111111111111111111112"
    amount = int(sol_amount * 1_000_000_000)
    
    # Get quote
    quote_url = f"https://lite-api.jup.ag/swap/v1/quote?inputMint={SOL_MINT}&outputMint={token_mint}&amount={amount}&slippageBps=100"
    with urlopen(quote_url, timeout=30) as resp:
        quote = j.loads(resp.read())
    
    print(f"📊 Quote: {int(quote['outAmount']):,} tokens for {sol_amount} SOL")
    
    # Get wallet pubkey
    pubkey = subprocess.run(["solana", "address"], capture_output=True, text=True).stdout.strip()
    print(f"📍 Wallet: {pubkey}")
    
    # Get swap transaction
    swap_url = "https://lite-api.jup.ag/swap/v1/swap"
    swap_payload = j.dumps({
        "quoteResponse": quote,
        "userPublicKey": pubkey,
        "wrapAndUnwrapSol": True,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": "auto"
    }).encode()
    
    req = Request(swap_url, data=swap_payload, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=30) as resp:
        swap_result = j.loads(resp.read())
    
    return quote, swap_result, pubkey

def sign_and_send_transaction(swap_tx_b64: str):
    """Sign and send the transaction"""
    
    # Decode base64 transaction
    tx_bytes = base64.b64decode(swap_tx_b64)
    
    # Write to temp file
    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as f:
        f.write(tx_bytes)
        tx_file = f.name
    
    print(f"💾 Transaction saved: {tx_file} ({len(tx_bytes)} bytes)")
    
    # Use solana CLI to sign and send
    # The transaction needs to be signed with our keypair
    # solana doesn't directly support signing raw txns from file
    # We need to use a different approach
    
    # Try using the transfer command approach or RPC directly
    # Actually, the easiest way is to use the send-transaction RPC call
    
    # Convert to base58/base64 for RPC
    tx_b64 = base64.b64encode(tx_bytes).decode()
    
    # Use solana CLI's raw transaction sending if available
    # Or make RPC call
    
    rpc_payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sendTransaction",
        "params": [
            tx_b64,
            {"encoding": "base64", "skipPreflight": False}
        ]
    })
    
    # This won't work without signing first - the tx from Jupiter needs our signature
    print("\n⚠️ Transaction requires signing before broadcast")
    print("The transaction from Jupiter is partially signed (by Jupiter)")
    print("We need to add our signature as the fee payer")
    
    return None

def main():
    if len(sys.argv) < 3:
        print("Usage: python execute_swap.py <token_mint> <sol_amount>")
        print("Example: python execute_swap.py ER8Hgvjk... 0.03")
        sys.exit(1)
    
    token = sys.argv[1]
    amount = float(sys.argv[2])
    
    print("=" * 50)
    print("⚓ SKIPPER SWAP EXECUTOR")
    print("=" * 50)
    
    try:
        quote, swap_result, pubkey = get_quote_and_swap(token, amount)
        
        if swap_result.get("swapTransaction"):
            print("\n✅ Swap transaction received!")
            print(f"🔢 Compute units: {swap_result.get('computeUnitLimit')}")
            print(f"💸 Priority fee: {swap_result.get('prioritizationFeeLamports')} lamports")
            
            # Save for inspection
            with open("/tmp/jupiter_swap.json", "w") as f:
                json.dump({
                    "quote": quote,
                    "swap": swap_result,
                    "pubkey": pubkey,
                    "token": token,
                    "sol_amount": amount
                }, f, indent=2)
            
            print("\n📝 Full response saved to /tmp/jupiter_swap.json")
            
            # Now try to sign and send
            sign_and_send_transaction(swap_result["swapTransaction"])
        else:
            print(f"❌ No swap transaction in response: {swap_result}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
