#!/usr/bin/env python3
"""
Quick memecoin buy script - Skipper's Trading Bot
"""

import json
import base64
import sys
from pathlib import Path
from urllib.request import Request, urlopen

from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solana.rpc.api import Client
from solana.rpc.types import TxOpts

KEYPAIR_PATH = Path.home() / ".config/solana/skipper-wallet.json"
RPC_URL = "https://api.mainnet-beta.solana.com"
SOL_MINT = "So11111111111111111111111111111111111111112"
JUPITER_API = "https://lite-api.jup.ag/swap/v1"

def load_keypair():
    with open(KEYPAIR_PATH) as f:
        return Keypair.from_bytes(bytes(json.load(f)))

def buy(token_mint: str, sol_amount: float):
    print(f"🎯 Buying {token_mint[:12]}... with {sol_amount} SOL")
    
    keypair = load_keypair()
    pubkey = str(keypair.pubkey())
    client = Client(RPC_URL)
    
    # Check balance
    balance = client.get_balance(keypair.pubkey()).value / 1e9
    print(f"💰 Balance: {balance:.4f} SOL")
    
    if balance < sol_amount + 0.005:
        print("❌ Insufficient balance")
        return None
    
    # Get quote
    amount = int(sol_amount * 1e9)
    quote_url = f"{JUPITER_API}/quote?inputMint={SOL_MINT}&outputMint={token_mint}&amount={amount}&slippageBps=150"
    
    with urlopen(quote_url, timeout=30) as resp:
        quote = json.loads(resp.read())
    
    out_tokens = int(quote['outAmount'])
    print(f"📊 Quote: {out_tokens:,} tokens")
    
    # Get swap transaction
    payload = json.dumps({
        "quoteResponse": quote,
        "userPublicKey": pubkey,
        "wrapAndUnwrapSol": True,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": 500000  # Higher priority fee
    }).encode()
    
    req = Request(f"{JUPITER_API}/swap", data=payload, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=30) as resp:
        swap_result = json.loads(resp.read())
    
    # Decode and sign
    tx_bytes = base64.b64decode(swap_result["swapTransaction"])
    tx = VersionedTransaction.from_bytes(tx_bytes)
    
    msg_bytes = bytes(tx.message)
    signature = keypair.sign_message(msg_bytes)
    signed_tx = VersionedTransaction.populate(tx.message, [signature])
    
    # Send immediately
    print("🚀 Sending...")
    result = client.send_raw_transaction(bytes(signed_tx), opts=TxOpts(skip_preflight=True))
    
    tx_sig = str(result.value)
    print(f"✅ TX: {tx_sig}")
    print(f"🔗 https://solscan.io/tx/{tx_sig}")
    
    # Quick confirm check
    import time
    for i in range(10):
        time.sleep(2)
        status = client.get_signature_statuses([result.value])
        if status.value[0]:
            if status.value[0].err:
                print(f"❌ Failed: {status.value[0].err}")
            else:
                print(f"✅ CONFIRMED! Slot: {status.value[0].slot}")
            break
        print(f"⏳ Waiting... ({i+1}/10)")
    
    return tx_sig

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python buy.py <token_mint> <sol_amount>")
        sys.exit(1)
    
    buy(sys.argv[1], float(sys.argv[2]))
