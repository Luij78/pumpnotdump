#!/bin/bash
# DEPLOY_NOW.sh - One-click deployment script for Colosseum Hackathon
# Run this script once the Helius wallet has at least 0.5 SOL on devnet

set -e  # Exit on any error

echo "🚀 Starting Colosseum Hackathon Deployment..."
echo "================================================"
echo ""

# Set paths
SOLANA_CLI="/Users/luisgarcia/.local/share/solana/install/active_release/bin/solana"
ANCHOR_CLI="anchor"
PROJECT_DIR="/Users/luisgarcia/clawd/projects/pumpnotdump"
HELIUS_WALLET="9LxrENgXEaidARTVyifUU7uuB3TfbwYXGZ99ySsPax9X"

# Check if we're in the right directory
cd "$PROJECT_DIR/pumpnotdump" || { echo "❌ Failed to navigate to project directory"; exit 1; }

echo "Step 1/7: Checking wallet balance..."
BALANCE=$($SOLANA_CLI balance $HELIUS_WALLET --url devnet | awk '{print $1}')
echo "Wallet balance: $BALANCE SOL"

if (( $(echo "$BALANCE < 0.3" | bc -l) )); then
    echo "❌ Insufficient SOL balance. Need at least 0.3 SOL for deployment."
    echo "   Current balance: $BALANCE SOL"
    echo ""
    echo "Get devnet SOL from one of these faucets:"
    echo "  • https://faucet.solana.com"
    echo "  • https://solfaucet.com"
    echo "  • https://faucet.quicknode.com/solana/devnet"
    exit 1
fi

echo "✅ Sufficient balance detected"
echo ""

echo "Step 2/7: Configuring Solana CLI for devnet..."
$SOLANA_CLI config set --url devnet
echo "✅ Configured for devnet"
echo ""

echo "Step 3/7: Setting wallet keypair..."
# Check if keypair exists
if [ ! -f ~/.config/solana/skipper-wallet.json ]; then
    echo "❌ Keypair not found at ~/.config/solana/skipper-wallet.json"
    exit 1
fi
$SOLANA_CLI config set --keypair ~/.config/solana/skipper-wallet.json
echo "✅ Keypair configured"
echo ""

echo "Step 4/7: Building smart contract..."
$ANCHOR_CLI build
echo "✅ Contract built successfully"
echo ""

echo "Step 5/7: Deploying to Solana devnet..."
DEPLOY_OUTPUT=$($ANCHOR_CLI deploy 2>&1)
echo "$DEPLOY_OUTPUT"

# Extract program ID from deployment output
PROGRAM_ID=$(echo "$DEPLOY_OUTPUT" | grep "Program Id:" | awk '{print $3}')

if [ -z "$PROGRAM_ID" ]; then
    echo "❌ Failed to extract program ID from deployment"
    exit 1
fi

echo "✅ Contract deployed successfully"
echo "   Program ID: $PROGRAM_ID"
echo ""

echo "Step 6/7: Running tests..."
$ANCHOR_CLI test --skip-local-validator
echo "✅ Tests passed"
echo ""

echo "Step 7/7: Starting autonomous agent..."
cd ../agent

# Update agent configuration with new program ID
cat > .env << EOF
COLOSSEUM_API_KEY=24ea8d8889659a5321d0452a429f58f1b9cba94ab3d66f0a1d5cd7167e5c3f51
PROGRAM_ID=$PROGRAM_ID
SOLANA_WALLET_PATH=/Users/luisgarcia/.config/solana/skipper-wallet.json
SOLANA_RPC_URL=https://api.devnet.solana.com
EOF

echo "✅ Agent configured with program ID: $PROGRAM_ID"
echo ""

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing agent dependencies..."
    npm install
fi

echo ""
echo "================================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "================================================"
echo ""
echo "Program ID: $PROGRAM_ID"
echo "Wallet: $HELIUS_WALLET"
echo "Network: Solana Devnet"
echo ""
echo "Next steps:"
echo "  1. Start the agent: npm start"
echo "  2. Post submission to Colosseum forum"
echo "  3. Submit claim link to Luis (@luij78)"
echo ""
echo "Claim URL: https://colosseum.com/agent-hackathon/claim/c8d9faf7-029b-430e-b58d-fcbaae7caec8"
echo ""
