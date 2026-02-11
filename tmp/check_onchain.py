#!/usr/bin/env python3
"""Check on-chain balances for Polymarket wallet"""
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
wallet = '0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3'

# MATIC balance
matic = w3.eth.get_balance(wallet)
print(f"MATIC: {w3.from_wei(matic, 'ether'):.4f}")

# USDC.e balance (Polygon bridged USDC)
usdc_contract = '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174'
usdc_abi = [{'constant':True,'inputs':[{'name':'_owner','type':'address'}],'name':'balanceOf','outputs':[{'name':'balance','type':'uint256'}],'type':'function'}]
usdc = w3.eth.contract(address=Web3.to_checksum_address(usdc_contract), abi=usdc_abi)
bal = usdc.functions.balanceOf(Web3.to_checksum_address(wallet)).call()
print(f"USDC.e on-chain: ${bal/1e6:.2f}")

# Native USDC balance
native_usdc = '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359'
usdc2 = w3.eth.contract(address=Web3.to_checksum_address(native_usdc), abi=usdc_abi)
bal2 = usdc2.functions.balanceOf(Web3.to_checksum_address(wallet)).call()
print(f"USDC (native) on-chain: ${bal2/1e6:.2f}")
