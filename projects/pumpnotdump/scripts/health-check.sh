#!/bin/bash

# Post-Deployment Health Check
# Verifies the deployed agent is operational
# Run this after deployment to confirm everything works

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🏥 Post-Deployment Health Check"
echo "================================"
echo ""

ERRORS=0
WARNINGS=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Load environment
cd "$PROJECT_ROOT/agent"
if [ -f ".env" ]; then
    source .env
else
    echo -e "${RED}Error: .env not found${NC}"
    exit 1
fi

echo "1️⃣  Checking Smart Contract..."

# Verify program is deployed
if [ -z "$PROGRAM_ID" ]; then
    check_fail "PROGRAM_ID not set in .env"
else
    info "Program ID: $PROGRAM_ID"
    
    # Check if program exists on-chain
    PROGRAM_INFO=$(solana program show "$PROGRAM_ID" --url devnet 2>&1)
    
    if echo "$PROGRAM_INFO" | grep -q "Program Id: $PROGRAM_ID"; then
        check_pass "Program deployed on devnet"
        
        # Extract program data
        AUTHORITY=$(echo "$PROGRAM_INFO" | grep "Authority:" | awk '{print $2}')
        info "Upgrade Authority: $AUTHORITY"
        
        DATA_LEN=$(echo "$PROGRAM_INFO" | grep "Data Length:" | awk '{print $3}')
        info "Program Size: $DATA_LEN bytes"
    else
        check_fail "Program not found on devnet"
    fi
fi

echo ""
echo "2️⃣  Checking Agent Process..."

# Check if agent is running
if pgrep -f "autonomous-agent" > /dev/null; then
    check_pass "Agent process is running"
    
    PID=$(pgrep -f "autonomous-agent")
    info "Process ID: $PID"
    
    # Check how long it's been running
    UPTIME=$(ps -p $PID -o etime= | tr -d ' ')
    info "Uptime: $UPTIME"
else
    check_warn "Agent process not running (may need to start it)"
fi

echo ""
echo "3️⃣  Checking Agent Logs..."

LOG_FILE="$PROJECT_ROOT/agent/agent.log"

if [ -f "$LOG_FILE" ]; then
    check_pass "Log file exists"
    
    # Check for recent activity
    LAST_LINE=$(tail -n 1 "$LOG_FILE")
    info "Last log: $LAST_LINE"
    
    # Check for errors
    ERROR_COUNT=$(grep -c "Error" "$LOG_FILE" 2>/dev/null || echo "0")
    if [ "$ERROR_COUNT" -gt 0 ]; then
        check_warn "Found $ERROR_COUNT errors in log"
    else
        check_pass "No errors in log"
    fi
    
    # Check for successful cycles
    CYCLE_COUNT=$(grep -c "Cycle complete" "$LOG_FILE" 2>/dev/null || echo "0")
    if [ "$CYCLE_COUNT" -gt 0 ]; then
        check_pass "Agent completed $CYCLE_COUNT monitoring cycles"
    else
        check_warn "No completed monitoring cycles yet"
    fi
    
    # Check for forum posts
    POST_COUNT=$(grep -c "Posted to Colosseum forum" "$LOG_FILE" 2>/dev/null || echo "0")
    if [ "$POST_COUNT" -gt 0 ]; then
        check_pass "Posted $POST_COUNT times to forum"
    else
        check_warn "No forum posts yet"
    fi
else
    check_warn "Log file not found (agent may not have started yet)"
fi

echo ""
echo "4️⃣  Checking Wallet Balance..."

WALLET=$(solana address)
BALANCE=$(solana balance --url devnet | awk '{print $1}')

info "Wallet: $WALLET"
info "Balance: $BALANCE SOL"

if (( $(echo "$BALANCE >= 0.5" | bc -l) )); then
    check_pass "Wallet has sufficient balance for operations"
elif (( $(echo "$BALANCE > 0" | bc -l) )); then
    check_warn "Wallet balance is low ($BALANCE SOL)"
else
    check_fail "Wallet is empty"
fi

echo ""
echo "5️⃣  Checking Network Connectivity..."

# Test RPC endpoint
if curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"getHealth"}' "$SOLANA_RPC" | grep -q "ok"; then
    check_pass "RPC endpoint is healthy"
else
    check_fail "RPC endpoint not responding"
fi

# Test Colosseum API
if [ -n "$COLOSSEUM_API_KEY" ]; then
    RESPONSE=$(curl -s -H "Authorization: Bearer $COLOSSEUM_API_KEY" "https://colosseum.org/api/agent/$AGENT_ID" 2>&1)
    
    if echo "$RESPONSE" | grep -q "\"agent_id\":$AGENT_ID"; then
        check_pass "Colosseum API authenticated"
    else
        check_warn "Colosseum API response unexpected"
    fi
else
    check_warn "COLOSSEUM_API_KEY not set"
fi

echo ""
echo "6️⃣  Checking GitHub Repository..."

cd "$PROJECT_ROOT"

if git remote get-url origin &> /dev/null; then
    REPO_URL=$(git remote get-url origin)
    info "Repository: $REPO_URL"
    
    # Check if it's public
    if [[ "$REPO_URL" == *"github.com"* ]]; then
        REPO_PATH=$(echo "$REPO_URL" | sed 's/.*github.com[:/]\(.*\)\.git/\1/')
        if curl -s "https://api.github.com/repos/$REPO_PATH" | grep -q "\"private\":false"; then
            check_pass "Repository is public"
        else
            check_warn "Repository may be private"
        fi
    fi
else
    check_warn "No remote repository configured"
fi

echo ""
echo "================================"
echo ""

# Overall status
if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✅ ALL SYSTEMS OPERATIONAL${NC}"
        echo ""
        echo "Your agent is healthy and ready!"
    else
        echo -e "${YELLOW}⚠️  OPERATIONAL WITH WARNINGS${NC}"
        echo ""
        echo "Warnings: $WARNINGS"
        echo "Agent is running but has minor issues."
    fi
    
    echo ""
    echo "Monitoring:"
    echo "  • Logs: tail -f $PROJECT_ROOT/agent/agent.log"
    echo "  • Process: ps aux | grep autonomous-agent"
    echo "  • Wallet: solana balance --url devnet"
    echo ""
    
    exit 0
else
    echo -e "${RED}❌ HEALTH CHECK FAILED${NC}"
    echo ""
    echo "Errors: $ERRORS"
    echo "Warnings: $WARNINGS"
    echo ""
    echo "Agent is not operational. Fix the errors above."
    echo ""
    exit 1
fi
