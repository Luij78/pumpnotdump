#!/usr/bin/env python3
"""Debug the swap transaction"""

import json
import base64
from pathlib import Path
from urllib.request import Request, urlopen

from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders.message import MessageV0
from solana.rpc.api import Client

KEYPAIR_PATH = Path.home() / ".config/solana/skipper-wallet.json"
RPC_URL = "https://api.mainnet-beta.solana.com"
SOL_MINT = "So11111111111111111111111111111111111111112"
JUPITER_API = "https://lite-api.jup.ag/swap/v1"

def load_keypair():
    with open(KEYPAIR_PATH) as f:
        secret = json.load(f)
    return Keypair.from_bytes(bytes(secret))

def main():
    token = "ER8HgvjkEa4c3ToUTGZXAcNH3Vs3XKu3KGcncM8jeJUQ"
    sol_amount = 0.02
    
    keypair = load_keypair()
    pubkey = str(keypair.pubkey())
    print(f"Wallet: {pubkey}")
    
    # Get quote
    amount = int(sol_amount * 1_000_000_000)
    quote_url = f"{JUPITER_API}/quote?inputMint={SOL_MINT}&outputMint={token}&amount={amount}&slippageBps=100"
    with urlopen(quote_url, timeout=30) as resp:
        quote = json.loads(resp.read())
    print(f"Quote output: {int(quote['outAmount']):,} tokens")
    
    # Get swap tx
    payload = json.dumps({
        "quoteResponse": quote,
        "userPublicKey": pubkey,
        "wrapAndUnwrapSol": True,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": "auto"
    }).encode()
    
    req = Request(f"{JUPITER_API}/swap", data=payload, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=30) as resp:
        swap_result = json.loads(resp.read())
    
    swap_tx_b64 = swap_result["swapTransaction"]
    tx_bytes = base64.b64decode(swap_tx_b64)
    
    # Deserialize
    tx = VersionedTransaction.from_bytes(tx_bytes)
    
    print(f"\nTransaction details:")
    print(f"  Message type: {type(tx.message)}")
    print(f"  Num signatures: {len(tx.signatures)}")
    print(f"  Signatures: {tx.signatures}")
    
    # The message
    msg = tx.message
    print(f"  Num account keys: {len(msg.account_keys)}")
    print(f"  Fee payer (first account): {msg.account_keys[0]}")
    print(f"  Our pubkey: {keypair.pubkey()}")
    print(f"  Match: {str(msg.account_keys[0]) == str(keypair.pubkey())}")
    
    # Check recent blockhash
    print(f"  Recent blockhash: {msg.recent_blockhash}")
    
    # Check header
    print(f"  Header - num required signatures: {msg.header.num_required_signatures}")
    print(f"  Header - num readonly signed: {msg.header.num_readonly_signed_accounts}")
    print(f"  Header - num readonly unsigned: {msg.header.num_readonly_unsigned_accounts}")
    
    # Try to create properly signed transaction
    print("\nAttempting to sign...")
    
    # Get message bytes for signing (serialize the message)
    msg_bytes = bytes(msg)
    print(f"  Message bytes length: {len(msg_bytes)}")
    
    # Sign with keypair
    signature = keypair.sign_message(msg_bytes)
    print(f"  Signature: {signature}")
    
    # Reconstruct with our signature
    # The transaction needs exactly the right number of signatures
    num_sigs = msg.header.num_required_signatures
    print(f"  Required signatures: {num_sigs}")
    
    # Create list of signatures (ours first since we're fee payer)
    if num_sigs == 1:
        sigs = [signature]
    else:
        # Keep other signatures, replace first (fee payer) with ours
        sigs = [signature] + list(tx.signatures[1:])
    
    print(f"  Signatures list: {len(sigs)}")
    
    # Create signed transaction
    signed_tx = VersionedTransaction.populate(msg, sigs)
    signed_bytes = bytes(signed_tx)
    
    print(f"  Signed tx bytes: {len(signed_bytes)}")
    
    # Send
    print("\nSending...")
    client = Client(RPC_URL)
    
    from solana.rpc.types import TxOpts
    from solana.rpc.commitment import Confirmed
    
    try:
        result = client.send_raw_transaction(
            signed_bytes,
            opts=TxOpts(skip_preflight=True)  # Skip preflight to see actual error
        )
        print(f"✅ Sent! Signature: {result.value}")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    main()
