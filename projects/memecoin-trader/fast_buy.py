#!/usr/bin/env python3
"""
Fast memecoin buy - uses curl for RPC for speed
"""

import json
import base64
import sys
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen

from solders.keypair import Keypair
from solders.transaction import VersionedTransaction

KEYPAIR_PATH = Path.home() / ".config/solana/skipper-wallet.json"
SOL_MINT = "So11111111111111111111111111111111111111112"
JUPITER_API = "https://lite-api.jup.ag/swap/v1"
RPC_URL = "https://api.mainnet-beta.solana.com"

def load_keypair():
    with open(KEYPAIR_PATH) as f:
        return Keypair.from_bytes(bytes(json.load(f)))

def send_tx_via_curl(tx_base64: str):
    """Send transaction using curl for speed"""
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sendTransaction",
        "params": [tx_base64, {"encoding": "base64", "skipPreflight": True, "maxRetries": 3}]
    })
    
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", RPC_URL, "-H", "Content-Type: application/json", "-d", payload],
        capture_output=True, text=True, timeout=30
    )
    return json.loads(result.stdout)

def check_tx_via_curl(sig: str):
    """Check transaction status using curl"""
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignatureStatuses",
        "params": [[sig], {"searchTransactionHistory": True}]
    })
    
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", RPC_URL, "-H", "Content-Type: application/json", "-d", payload],
        capture_output=True, text=True, timeout=10
    )
    return json.loads(result.stdout)

def buy(token_mint: str, sol_amount: float):
    print(f"⚡ FAST BUY: {token_mint[:12]}... with {sol_amount} SOL")
    
    keypair = load_keypair()
    pubkey = str(keypair.pubkey())
    print(f"📍 Wallet: {pubkey}")
    
    # Get quote via urllib (fast)
    amount = int(sol_amount * 1e9)
    quote_url = f"{JUPITER_API}/quote?inputMint={SOL_MINT}&outputMint={token_mint}&amount={amount}&slippageBps=200"
    
    print("📊 Getting quote...")
    with urlopen(quote_url, timeout=10) as resp:
        quote = json.loads(resp.read())
    
    out_tokens = int(quote['outAmount'])
    print(f"   Output: {out_tokens:,} tokens")
    
    # Get swap transaction
    print("🔄 Getting swap tx...")
    payload = json.dumps({
        "quoteResponse": quote,
        "userPublicKey": pubkey,
        "wrapAndUnwrapSol": True,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": 5000000  # 0.005 SOL priority fee - aggressive
    }).encode()
    
    req = Request(f"{JUPITER_API}/swap", data=payload, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=15) as resp:
        swap_result = json.loads(resp.read())
    
    # Sign transaction
    print("✍️ Signing...")
    tx_bytes = base64.b64decode(swap_result["swapTransaction"])
    tx = VersionedTransaction.from_bytes(tx_bytes)
    
    msg_bytes = bytes(tx.message)
    signature = keypair.sign_message(msg_bytes)
    signed_tx = VersionedTransaction.populate(tx.message, [signature])
    signed_b64 = base64.b64encode(bytes(signed_tx)).decode()
    
    # Send via curl (faster than Python RPC client)
    print("🚀 Sending...")
    result = send_tx_via_curl(signed_b64)
    
    if "error" in result:
        print(f"❌ RPC Error: {result['error']}")
        return None
    
    tx_sig = result["result"]
    print(f"✅ TX Sent: {tx_sig}")
    print(f"🔗 https://solscan.io/tx/{tx_sig}")
    
    # Quick confirmation check
    import time
    for i in range(15):
        time.sleep(2)
        status = check_tx_via_curl(tx_sig)
        val = status.get("result", {}).get("value", [None])[0]
        if val:
            if val.get("err"):
                print(f"❌ TX Failed: {val['err']}")
                return None
            else:
                print(f"✅ CONFIRMED! Slot: {val['slot']}")
                return tx_sig
        print(f"⏳ Confirming... ({i+1}/15)")
    
    print("⚠️ TX may still be processing...")
    return tx_sig

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python fast_buy.py <token_mint> <sol_amount>")
        sys.exit(1)
    
    buy(sys.argv[1], float(sys.argv[2]))
