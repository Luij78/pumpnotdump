#!/bin/bash

# pump.notdump.fun - Autonomous Agent Demo Script
# Colosseum Agent Hackathon 2026

set -e

echo "🤖 pump.notdump.fun - Autonomous Anti-Rug Agent Demo"
echo "==================================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v solana &> /dev/null; then
    echo -e "${RED}✗ Solana CLI not found${NC}"
    echo "Install: sh -c \"\$(curl -sSfL https://release.anza.xyz/agave-v3.1.8/install)\""
    exit 1
fi
echo -e "${GREEN}✓ Solana CLI found${NC}"

if ! command -v anchor &> /dev/null; then
    echo -e "${RED}✗ Anchor CLI not found${NC}"
    echo "Install: cargo install --git https://github.com/coral-xyz/anchor avm --locked --force"
    exit 1
fi
echo -e "${GREEN}✓ Anchor CLI found${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Node.js not found${NC}"
    echo "Install: brew install node"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found${NC}"

echo ""

# Set Solana config
echo "⚙️  Configuring Solana..."
solana config set --url devnet > /dev/null
echo -e "${GREEN}✓ Connected to devnet${NC}"

# Check wallet balance
BALANCE=$(solana balance 2>/dev/null | cut -d' ' -f1)
echo "💰 Wallet balance: $BALANCE SOL"

if (( $(echo "$BALANCE < 1" | bc -l) )); then
    echo -e "${YELLOW}⚠️  Low balance. Requesting airdrop...${NC}"
    solana airdrop 2 > /dev/null 2>&1 || echo -e "${YELLOW}   (Faucet may be rate-limited - continuing anyway)${NC}"
fi

echo ""

# Navigate to project root
cd "$(dirname "$0")/.."

# Build smart contract
echo "🔨 Building smart contract..."
cd pumpnotdump
anchor build > /dev/null 2>&1
echo -e "${GREEN}✓ Program compiled${NC}"

PROGRAM_ID=$(solana address -k target/deploy/pumpnotdump-keypair.json)
echo "📝 Program ID: $PROGRAM_ID"

echo ""

# Check if deployed
echo "🌐 Checking deployment..."
if solana account "$PROGRAM_ID" &> /dev/null; then
    echo -e "${GREEN}✓ Program deployed to devnet${NC}"
else
    echo -e "${YELLOW}⚠️  Program not yet deployed${NC}"
    echo "   Run: anchor deploy"
    echo "   (Requires 2-3 SOL in wallet)"
fi

echo ""

# Install agent dependencies
echo "📦 Installing agent dependencies..."
cd ../agent
if [ ! -d "node_modules" ]; then
    npm install --silent > /dev/null 2>&1
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

echo ""

# Set API key
export COLOSSEUM_API_KEY="24ea8d8889659a5321d0452a429f58f1b9cba94ab3d66f0a1d5cd7167e5c3f51"
echo "🔑 Colosseum API key configured"

echo ""
echo "================================="
echo -e "${GREEN}✅ Demo setup complete!${NC}"
echo "================================="
echo ""
echo "To run the autonomous agent:"
echo -e "${BLUE}  cd agent && npm start${NC}"
echo ""
echo "The agent will:"
echo "  • Monitor blockchain for new token launches"
echo "  • Calculate rug scores in real-time"
echo "  • Post warnings for high-risk tokens"
echo "  • Update Colosseum forum autonomously"
echo ""
echo "Press Ctrl+C to stop the agent."
echo ""

read -p "Start the agent now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting autonomous agent..."
    echo ""
    npm start
fi
