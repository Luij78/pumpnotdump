#!/usr/bin/env python3
"""Quick redemption script for winning positions"""
import os
import requests
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Contract addresses
USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
CTF_ADDRESS = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045"

REDEEM_ABI = [{
    "constant": False,
    "inputs": [
        {"name": "collateralToken", "type": "address"},
        {"name": "parentCollectionId", "type": "bytes32"},
        {"name": "conditionId", "type": "bytes32"},
        {"name": "indexSets", "type": "uint256[]"}
    ],
    "name": "redeemPositions",
    "outputs": [],
    "payable": False,
    "stateMutability": "nonpayable",
    "type": "function"
}]

def redeem_position(condition_id, pk, w3):
    """Redeem a specific position"""
    account = w3.eth.account.from_key(pk)
    
    ctf = w3.eth.contract(
        address=Web3.to_checksum_address(CTF_ADDRESS),
        abi=REDEEM_ABI
    )
    
    # Build transaction - redeem both outcomes (1 and 2)
    tx = ctf.functions.redeemPositions(
        Web3.to_checksum_address(USDC_ADDRESS),
        bytes.fromhex('00' * 32),  # parentCollectionId
        bytes.fromhex(condition_id[2:]),  # conditionId without 0x
        [1, 2]  # Both outcome indices
    ).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 137
    })
    
    signed = w3.eth.account.sign_transaction(tx, pk)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    
    print(f"  TX: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
    return receipt.status == 1

def main():
    pk = os.getenv('PRIVATE_KEY')
    w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
    
    wallet = w3.eth.account.from_key(pk).address
    print(f"Wallet: {wallet}")
    
    # Get redeemable positions
    r = requests.get(f'https://data-api.polymarket.com/positions?user={wallet.lower()}')
    positions = r.json()
    
    redeemable = [p for p in positions if p.get('redeemable') and p.get('currentValue', 0) > 0]
    
    print(f"\nFound {len(redeemable)} redeemable positions:")
    
    for p in redeemable:
        cid = p['conditionId']
        val = p.get('currentValue', 0)
        title = p['title'][-40:]
        
        print(f"\n📍 {title}")
        print(f"   Value: ${val:.2f}")
        print(f"   Redeeming...")
        
        try:
            success = redeem_position(cid, pk, w3)
            if success:
                print(f"   ✅ REDEEMED!")
            else:
                print(f"   ❌ Failed")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Check new balance
    usdc_abi = [{'constant':True,'inputs':[{'name':'_owner','type':'address'}],'name':'balanceOf','outputs':[{'name':'balance','type':'uint256'}],'type':'function'}]
    usdc = w3.eth.contract(address=Web3.to_checksum_address(USDC_ADDRESS), abi=usdc_abi)
    bal = usdc.functions.balanceOf(Web3.to_checksum_address(wallet)).call()
    print(f"\n💰 New USDC.e balance: ${bal/1e6:.2f}")

if __name__ == '__main__':
    main()
