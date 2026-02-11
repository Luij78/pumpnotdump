#!/usr/bin/env python3
"""
Skipper's Solana Swap Bot 🚀
Actually executes swaps using Jupiter + Solana Python SDK
"""

import json
import base64
import sys
import os
from pathlib import Path
from urllib.request import Request, urlopen

# Solana imports
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed

# Config
KEYPAIR_PATH = Path.home() / ".config/solana/skipper-wallet.json"
RPC_URL = "https://api.mainnet-beta.solana.com"
SOL_MINT = "So11111111111111111111111111111111111111112"
JUPITER_API = "https://lite-api.jup.ag/swap/v1"

def load_keypair():
    """Load keypair from JSON file"""
    with open(KEYPAIR_PATH) as f:
        secret = json.load(f)
    return Keypair.from_bytes(bytes(secret))

def get_quote(token_mint: str, sol_amount: float):
    """Get Jupiter quote"""
    amount = int(sol_amount * 1_000_000_000)
    url = f"{JUPITER_API}/quote?inputMint={SOL_MINT}&outputMint={token_mint}&amount={amount}&slippageBps=100"
    
    with urlopen(url, timeout=30) as resp:
        return json.loads(resp.read())

def get_swap_transaction(quote: dict, pubkey: str):
    """Get swap transaction from Jupiter"""
    payload = json.dumps({
        "quoteResponse": quote,
        "userPublicKey": pubkey,
        "wrapAndUnwrapSol": True,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": "auto"
    }).encode()
    
    req = Request(f"{JUPITER_API}/swap", data=payload, headers={"Content-Type": "application/json"})
    
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def execute_swap(token_mint: str, sol_amount: float):
    """Execute a swap from SOL to token"""
    print("=" * 50)
    print("⚓ SKIPPER SWAP BOT")
    print("=" * 50)
    
    # Load keypair
    print("🔑 Loading wallet...")
    keypair = load_keypair()
    pubkey = str(keypair.pubkey())
    print(f"📍 Wallet: {pubkey}")
    
    # Check balance
    client = Client(RPC_URL)
    balance = client.get_balance(keypair.pubkey())
    sol_balance = balance.value / 1_000_000_000
    print(f"💰 Balance: {sol_balance:.4f} SOL")
    
    if sol_balance < sol_amount + 0.01:  # Need buffer for fees
        print(f"❌ Insufficient balance! Need at least {sol_amount + 0.01} SOL")
        return None
    
    # Get quote
    print(f"\n📊 Getting quote for {sol_amount} SOL → {token_mint[:8]}...")
    quote = get_quote(token_mint, sol_amount)
    
    out_amount = int(quote["outAmount"])
    price_impact = float(quote.get("priceImpactPct", 0))
    route = quote.get("routePlan", [{}])[0].get("swapInfo", {}).get("label", "Unknown")
    
    print(f"✅ Quote received:")
    print(f"   Output: {out_amount:,} tokens")
    print(f"   Price Impact: {price_impact:.4f}%")
    print(f"   Route: {route}")
    
    if price_impact > 5:
        print(f"⚠️ WARNING: High price impact ({price_impact:.2f}%)!")
        # Could add confirmation prompt here
    
    # Get swap transaction
    print("\n🔄 Getting swap transaction...")
    swap_result = get_swap_transaction(quote, pubkey)
    
    if not swap_result.get("swapTransaction"):
        print(f"❌ Failed to get swap transaction: {swap_result}")
        return None
    
    print(f"✅ Transaction received")
    print(f"   Compute units: {swap_result.get('computeUnitLimit')}")
    print(f"   Priority fee: {swap_result.get('prioritizationFeeLamports')} lamports")
    
    # Decode and sign transaction
    print("\n✍️ Signing transaction...")
    swap_tx_b64 = swap_result["swapTransaction"]
    tx_bytes = base64.b64decode(swap_tx_b64)
    
    # Deserialize the versioned transaction
    tx = VersionedTransaction.from_bytes(tx_bytes)
    
    # For versioned transactions, we need to create a new signed transaction
    # Get the message and sign it
    from solders.presigner import Presigner
    from solders.signature import Signature
    
    # Sign the message
    message_bytes = bytes(tx.message)
    signature = keypair.sign_message(message_bytes)
    
    # Create new transaction with signature
    signed_tx = VersionedTransaction.populate(tx.message, [signature])
    
    # Serialize signed transaction
    signed_tx_bytes = bytes(signed_tx)
    
    # Send transaction
    print("🚀 Sending transaction...")
    try:
        from solana.rpc.types import TxOpts
        result = client.send_raw_transaction(
            signed_tx_bytes,
            opts=TxOpts(skip_preflight=False, preflight_commitment=Confirmed)
        )
        
        tx_sig = str(result.value)
        print(f"\n✅ TRANSACTION SENT!")
        print(f"🔗 Signature: {tx_sig}")
        print(f"🔍 Explorer: https://solscan.io/tx/{tx_sig}")
        
        # Wait for confirmation
        print("\n⏳ Waiting for confirmation...")
        client.confirm_transaction(result.value, commitment="confirmed")
        print("✅ CONFIRMED!")
        
        return tx_sig
        
    except Exception as e:
        print(f"❌ Transaction failed: {e}")
        return None

def main():
    if len(sys.argv) < 3:
        print("Usage: python swap.py <token_mint> <sol_amount>")
        print("\nExamples:")
        print("  python swap.py ER8HgvjkEa4c3ToUTGZXAcNH3Vs3XKu3KGcncM8jeJUQ 0.03")
        print("\nThis will swap SOL for the specified token using Jupiter.")
        sys.exit(1)
    
    token_mint = sys.argv[1]
    sol_amount = float(sys.argv[2])
    
    if sol_amount < 0.001:
        print("❌ Minimum swap amount is 0.001 SOL")
        sys.exit(1)
    
    if sol_amount > 0.1:
        print(f"⚠️ Large swap amount: {sol_amount} SOL")
        print("Press Ctrl+C to cancel, or wait 3 seconds...")
        import time
        time.sleep(3)
    
    execute_swap(token_mint, sol_amount)

if __name__ == "__main__":
    main()
