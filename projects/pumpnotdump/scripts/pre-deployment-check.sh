#!/bin/bash

# Pre-Deployment Verification Script
# Checks all prerequisites before deployment
# Exit code 0 = ready to deploy
# Exit code 1 = blockers exist

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔍 Pre-Deployment Verification"
echo "================================"
echo ""

ERRORS=0
WARNINGS=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# 1. Check Solana CLI
echo "1️⃣  Checking Solana CLI..."
if command -v solana &> /dev/null; then
    SOLANA_VERSION=$(solana --version | awk '{print $2}')
    check_pass "Solana CLI installed (v$SOLANA_VERSION)"
    
    # Check configured network
    SOLANA_NETWORK=$(solana config get | grep "RPC URL" | awk '{print $3}')
    if [[ "$SOLANA_NETWORK" == *"devnet"* ]]; then
        check_pass "Configured for devnet"
    else
        check_warn "Not configured for devnet (current: $SOLANA_NETWORK)"
    fi
    
    # Check wallet balance
    BALANCE=$(solana balance 2>/dev/null | awk '{print $1}')
    if (( $(echo "$BALANCE >= 2" | bc -l) )); then
        check_pass "Wallet has sufficient SOL ($BALANCE SOL)"
    else
        check_fail "Insufficient SOL balance ($BALANCE SOL, need >= 2 SOL)"
    fi
    
    # Check keypair
    KEYPAIR_PATH="$HOME/.config/solana/skipper-wallet.json"
    if [ -f "$KEYPAIR_PATH" ]; then
        check_pass "Keypair file exists"
        
        # Verify it's valid JSON
        if jq empty "$KEYPAIR_PATH" 2>/dev/null; then
            check_pass "Keypair is valid JSON"
        else
            check_fail "Keypair is not valid JSON"
        fi
    else
        check_fail "Keypair not found at $KEYPAIR_PATH"
    fi
else
    check_fail "Solana CLI not found in PATH"
fi

echo ""

# 2. Check Anchor
echo "2️⃣  Checking Anchor..."
if command -v anchor &> /dev/null; then
    ANCHOR_VERSION=$(anchor --version | awk '{print $2}')
    check_pass "Anchor CLI installed (v$ANCHOR_VERSION)"
    
    # Check if we can build
    cd "$PROJECT_ROOT/pumpnotdump"
    if anchor build --check; then
        check_pass "Smart contract compiles cleanly"
    else
        check_fail "Smart contract has build errors"
    fi
else
    check_fail "Anchor CLI not found in PATH"
fi

echo ""

# 3. Check Agent Dependencies
echo "3️⃣  Checking Agent..."
cd "$PROJECT_ROOT/agent"

if [ -f "package.json" ]; then
    check_pass "package.json exists"
else
    check_fail "package.json not found"
fi

if [ -d "node_modules" ]; then
    check_pass "Dependencies installed"
else
    check_warn "Dependencies not installed (run: npm install)"
fi

if [ -f ".env" ]; then
    check_pass ".env file exists"
    
    # Check required vars
    source .env
    
    if [ -n "$COLOSSEUM_API_KEY" ]; then
        check_pass "COLOSSEUM_API_KEY is set"
    else
        check_fail "COLOSSEUM_API_KEY not set"
    fi
    
    if [ -n "$PROGRAM_ID" ]; then
        check_pass "PROGRAM_ID is set"
    else
        check_warn "PROGRAM_ID not set (will be set after deploy)"
    fi
    
    if [ -n "$SOLANA_RPC" ]; then
        if [[ "$SOLANA_RPC" == *"devnet"* ]]; then
            check_pass "SOLANA_RPC is devnet"
        else
            check_warn "SOLANA_RPC is not devnet ($SOLANA_RPC)"
        fi
    else
        check_fail "SOLANA_RPC not set"
    fi
else
    check_fail ".env file not found"
fi

# Check TypeScript compilation
if npx tsc --noEmit 2>/dev/null; then
    check_pass "TypeScript compiles without errors"
else
    check_warn "TypeScript has errors (may not block runtime)"
fi

echo ""

# 4. Check Documentation
echo "4️⃣  Checking Documentation..."
cd "$PROJECT_ROOT"

REQUIRED_DOCS=(
    "README.md"
    "ARCHITECTURE.md"
    "DEPLOYMENT_CHECKLIST.md"
    "QUICKSTART.md"
    "X_LAUNCH_THREAD.md"
    "COLOSSEUM_SUBMISSION.md"
)

for doc in "${REQUIRED_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        check_pass "$doc exists"
    else
        check_warn "$doc missing"
    fi
done

echo ""

# 5. Check Git
echo "5️⃣  Checking Git..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    check_pass "Git repository initialized"
    
    # Check if all files are committed
    if [[ -z $(git status --porcelain) ]]; then
        check_pass "All changes committed"
    else
        check_warn "Uncommitted changes exist"
    fi
    
    # Check remote
    if git remote get-url origin &> /dev/null; then
        REMOTE_URL=$(git remote get-url origin)
        check_pass "Remote configured ($REMOTE_URL)"
        
        # Check if pushed
        if git diff --quiet origin/$(git branch --show-current) 2>/dev/null; then
            check_pass "All commits pushed"
        else
            check_warn "Unpushed commits exist"
        fi
    else
        check_warn "No remote configured"
    fi
else
    check_warn "Not a git repository"
fi

echo ""

# 6. Check Network Connectivity
echo "6️⃣  Checking Network..."

# Test devnet RPC
if curl -s -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"getHealth"}' https://api.devnet.solana.com | grep -q "ok"; then
    check_pass "Solana devnet RPC reachable"
else
    check_fail "Cannot reach Solana devnet RPC"
fi

# Test Colosseum API
if curl -s -H "Authorization: Bearer $COLOSSEUM_API_KEY" https://colosseum.org/api/agent/911 &> /dev/null; then
    check_pass "Colosseum API reachable"
else
    check_warn "Cannot verify Colosseum API (may be rate limited)"
fi

echo ""
echo "================================"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ PRE-DEPLOYMENT CHECK PASSED${NC}"
    echo ""
    echo "You are ready to deploy!"
    echo ""
    echo "Next steps:"
    echo "  1. cd $PROJECT_ROOT/pumpnotdump"
    echo "  2. anchor build"
    echo "  3. anchor deploy"
    echo "  4. Copy PROGRAM_ID to agent/.env"
    echo "  5. cd $PROJECT_ROOT/agent && npm start"
    echo ""
    exit 0
else
    echo -e "${RED}❌ PRE-DEPLOYMENT CHECK FAILED${NC}"
    echo ""
    echo "Blockers: $ERRORS"
    echo "Warnings: $WARNINGS"
    echo ""
    echo "Fix the errors above before deploying."
    echo ""
    exit 1
fi
