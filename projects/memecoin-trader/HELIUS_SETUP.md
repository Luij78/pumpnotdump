# Helius RPC Setup Guide 🔧

## Why Helius?
Our current trading bot has transaction landing issues due to public RPC congestion.
Helius provides:
- Better transaction landing rates
- "Sender" feature (sends to Helius + Jito in parallel)
- FREE tier is enough for our trading volume

## Setup Steps

### 1. Create Account
1. Go to: https://dashboard.helius.dev/signup?plan=free
2. Sign up with email
3. Verify email

### 2. Get API Key
1. Log into dashboard
2. Go to "API Keys" section
3. Create new key for "Skipper Trading Bot"
4. Copy the API key

### 3. Get RPC URL
Your RPC URLs will look like:
```
Mainnet: https://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY
Devnet:  https://devnet.helius-rpc.com/?api-key=YOUR_API_KEY
```

### 4. Update Trading Bot

In `swap.py` and other scripts, replace:
```python
# OLD (public RPC - slow)
RPC_URL = "https://api.mainnet-beta.solana.com"

# NEW (Helius - fast)
RPC_URL = "https://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY"
```

Or better, use environment variable:
```python
import os
RPC_URL = os.getenv("HELIUS_RPC_URL", "https://api.mainnet-beta.solana.com")
```

Then set in shell:
```bash
export HELIUS_RPC_URL="https://mainnet.helius-rpc.com/?api-key=YOUR_KEY"
```

### 5. Using Sender for Better Landing

For priority transactions, add a tip:
```python
# When sending transaction, include priority fee
# Minimum tip: 0.0002 SOL (200,000 lamports)
```

Helius Sender endpoints:
- `https://mainnet.helius-rpc.com/?api-key=KEY` (standard)
- Add `priority-fee` compute unit for faster landing

## Free Tier Limits
- 1 million credits/month
- 10 RPC requests per second
- 1 sendTransaction per second
- Enough for manual/semi-automated trading

## Upgrade Path
If we need more:
- Developer ($49/mo): 10M credits, 50 RPS, 5 tx/sec
- Business ($499/mo): 100M credits, 200 RPS, 50 tx/sec

## Testing
After setup, test with:
```bash
cd ~/clawd/projects/memecoin-trader
python3 -c "
from solana.rpc.api import Client
import os
client = Client(os.getenv('HELIUS_RPC_URL'))
print('Connected:', client.is_connected())
print('Block height:', client.get_block_height()['result'])
"
```

---
*Helius will solve our tx landing issues! - Skipper ⚓*
