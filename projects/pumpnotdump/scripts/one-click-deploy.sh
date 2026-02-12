#!/bin/bash

# One-Click Deployment Script
# Deploys the entire Colosseum hackathon project in one command
# 
# Prerequisites:
#   - Solana wallet funded with >= 2 SOL on devnet
#   - Anchor CLI installed
#   - Node.js installed
#
# Usage: ./scripts/one-click-deploy.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${BOLD}🚀 One-Click Colosseum Deployment${NC}"
echo "=================================="
echo ""

# Step 0: Pre-flight checks
echo -e "${BLUE}[0/7]${NC} Running pre-deployment checks..."
if ! "$SCRIPT_DIR/pre-deployment-check.sh"; then
    echo ""
    echo -e "${RED}Pre-deployment checks failed. Fix errors and try again.${NC}"
    exit 1
fi

echo ""
read -p "Pre-checks passed. Continue with deployment? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""

# Step 1: Build smart contract
echo -e "${BLUE}[1/7]${NC} Building smart contract..."
cd "$PROJECT_ROOT/pumpnotdump"

if anchor build; then
    echo -e "${GREEN}✓${NC} Smart contract built successfully"
else
    echo -e "${RED}✗${NC} Build failed"
    exit 1
fi

echo ""

# Step 2: Deploy smart contract
echo -e "${BLUE}[2/7]${NC} Deploying smart contract to devnet..."

# Capture deploy output
DEPLOY_OUTPUT=$(anchor deploy 2>&1)
echo "$DEPLOY_OUTPUT"

# Extract Program ID
PROGRAM_ID=$(echo "$DEPLOY_OUTPUT" | grep "Program Id:" | awk '{print $3}')

if [ -z "$PROGRAM_ID" ]; then
    echo -e "${RED}✗${NC} Failed to extract Program ID"
    exit 1
fi

echo ""
echo -e "${GREEN}✓${NC} Smart contract deployed"
echo -e "${BOLD}Program ID: $PROGRAM_ID${NC}"
echo ""

# Step 3: Update agent .env
echo -e "${BLUE}[3/7]${NC} Configuring agent..."
cd "$PROJECT_ROOT/agent"

# Update PROGRAM_ID in .env
if [ -f ".env" ]; then
    # Replace existing PROGRAM_ID or add it
    if grep -q "^PROGRAM_ID=" .env; then
        sed -i.bak "s|^PROGRAM_ID=.*|PROGRAM_ID=$PROGRAM_ID|" .env
    else
        echo "PROGRAM_ID=$PROGRAM_ID" >> .env
    fi
    rm -f .env.bak
    echo -e "${GREEN}✓${NC} Updated .env with Program ID"
else
    echo -e "${RED}✗${NC} .env file not found"
    exit 1
fi

# Verify dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo ""

# Step 4: Compile TypeScript
echo -e "${BLUE}[4/7]${NC} Compiling agent..."
if npm run build; then
    echo -e "${GREEN}✓${NC} Agent compiled successfully"
else
    echo -e "${YELLOW}⚠${NC} Compilation warnings (non-blocking)"
fi

echo ""

# Step 5: Start agent
echo -e "${BLUE}[5/7]${NC} Starting agent..."

# Kill any existing agent processes
pkill -f "autonomous-agent" 2>/dev/null || true

# Start agent in background
nohup npm start > agent.log 2>&1 &
AGENT_PID=$!

echo -e "${GREEN}✓${NC} Agent started (PID: $AGENT_PID)"
echo ""

# Wait for agent to initialize
echo "Waiting for agent to initialize..."
sleep 10

# Check if still running
if ps -p $AGENT_PID > /dev/null; then
    echo -e "${GREEN}✓${NC} Agent is running"
else
    echo -e "${RED}✗${NC} Agent crashed on startup"
    echo ""
    echo "Last 20 lines of log:"
    tail -n 20 agent.log
    exit 1
fi

echo ""

# Step 6: Verify deployment
echo -e "${BLUE}[6/7]${NC} Running health checks..."
if "$SCRIPT_DIR/health-check.sh"; then
    echo -e "${GREEN}✓${NC} Health checks passed"
else
    echo -e "${YELLOW}⚠${NC} Some health checks failed (see above)"
fi

echo ""

# Step 7: Display next steps
echo -e "${BLUE}[7/7]${NC} Deployment complete!"
echo ""
echo "=================================="
echo -e "${GREEN}${BOLD}✅ DEPLOYMENT SUCCESSFUL${NC}"
echo "=================================="
echo ""
echo "Your agent is now running on Solana devnet!"
echo ""
echo -e "${BOLD}Program ID:${NC} $PROGRAM_ID"
echo -e "${BOLD}Agent PID:${NC} $AGENT_PID"
echo -e "${BOLD}Log file:${NC} $PROJECT_ROOT/agent/agent.log"
echo ""
echo -e "${BOLD}Next Steps:${NC}"
echo ""
echo "1. Monitor agent activity:"
echo "   tail -f $PROJECT_ROOT/agent/agent.log"
echo ""
echo "2. Verify on Solana Explorer:"
echo "   https://explorer.solana.com/address/$PROGRAM_ID?cluster=devnet"
echo ""
echo "3. Post to Colosseum forum:"
echo "   See: $PROJECT_ROOT/COLOSSEUM_SUBMISSION.md"
echo ""
echo "4. Post X thread:"
echo "   See: $PROJECT_ROOT/X_LAUNCH_THREAD.md"
echo ""
echo "5. Take screenshots for submission:"
echo "   - Terminal output (this screen)"
echo "   - Solana Explorer"
echo "   - Agent logs"
echo "   - Forum post"
echo ""
echo "6. Submit to Colosseum:"
echo "   https://colosseum.com/agent-hackathon/claim/c8d9faf7-029b-430e-b58d-fcbaae7caec8"
echo ""
echo -e "${BOLD}Useful Commands:${NC}"
echo "  • Check agent: ps aux | grep autonomous-agent"
echo "  • View logs: tail -f $PROJECT_ROOT/agent/agent.log"
echo "  • Health check: $SCRIPT_DIR/health-check.sh"
echo "  • Stop agent: pkill -f autonomous-agent"
echo "  • Wallet balance: solana balance --url devnet"
echo ""
echo -e "${YELLOW}Deadline: February 12, 2026${NC}"
echo "Time remaining: $(( ($(date -d '2026-02-12' +%s) - $(date +%s)) / 86400 )) days"
echo ""
echo "Good luck! 🚀"
echo ""
