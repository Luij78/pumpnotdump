#!/bin/bash

# Real-Time Agent Dashboard
# Displays live stats and activity
# Usage: ./scripts/dashboard.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# Load env
cd "$PROJECT_ROOT/agent"
[ -f .env ] && source .env

# Get wallet address
WALLET=$(solana address 2>/dev/null || echo "Unknown")

# Function to display dashboard
show_dashboard() {
    clear
    
    echo -e "${BOLD}${CYAN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BOLD}${CYAN}║          🤖 ANTI-RUG AGENT DASHBOARD                          ║${NC}"
    echo -e "${BOLD}${CYAN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Agent Status
    if pgrep -f "autonomous-agent" > /dev/null; then
        PID=$(pgrep -f "autonomous-agent")
        UPTIME=$(ps -p $PID -o etime= | tr -d ' ')
        echo -e "${GREEN}●${NC} ${BOLD}Status:${NC} RUNNING (PID: $PID, Uptime: $UPTIME)"
    else
        echo -e "${RED}●${NC} ${BOLD}Status:${NC} STOPPED"
    fi
    
    # Wallet Info
    BALANCE=$(solana balance --url devnet 2>/dev/null | awk '{print $1}' || echo "?.??")
    echo -e "${BOLD}Wallet:${NC} $WALLET"
    echo -e "${BOLD}Balance:${NC} $BALANCE SOL"
    
    # Program Info
    if [ -n "$PROGRAM_ID" ]; then
        echo -e "${BOLD}Program:${NC} $PROGRAM_ID"
    else
        echo -e "${BOLD}Program:${NC} ${DIM}Not deployed${NC}"
    fi
    
    echo ""
    echo -e "${BOLD}${BLUE}─────────────────────────────────────────────────────────────────${NC}"
    echo ""
    
    # Activity Stats (from log file)
    LOG_FILE="$PROJECT_ROOT/agent/agent.log"
    
    if [ -f "$LOG_FILE" ]; then
        CYCLES=$(grep -c "Cycle complete" "$LOG_FILE" 2>/dev/null || echo "0")
        TOKENS=$(grep -c "Detected token" "$LOG_FILE" 2>/dev/null || echo "0")
        WARNINGS=$(grep -c "⚠️ WARNING" "$LOG_FILE" 2>/dev/null || echo "0")
        CAUTIONS=$(grep -c "⚠️ CAUTION" "$LOG_FILE" 2>/dev/null || echo "0")
        SAFE=$(grep -c "✅ SAFE" "$LOG_FILE" 2>/dev/null || echo "0")
        POSTS=$(grep -c "Posted to Colosseum" "$LOG_FILE" 2>/dev/null || echo "0")
        ERRORS=$(grep -c "Error:" "$LOG_FILE" 2>/dev/null || echo "0")
        
        echo -e "${BOLD}Activity Stats:${NC}"
        echo ""
        echo -e "  Monitoring Cycles: ${CYAN}$CYCLES${NC}"
        echo -e "  Tokens Analyzed:   ${CYAN}$TOKENS${NC}"
        echo -e "  Forum Posts:       ${CYAN}$POSTS${NC}"
        echo ""
        echo -e "${BOLD}Risk Distribution:${NC}"
        echo ""
        echo -e "  ${RED}●${NC} High Risk (Warnings): $WARNINGS"
        echo -e "  ${YELLOW}●${NC} Caution:              $CAUTIONS"
        echo -e "  ${GREEN}●${NC} Safe:                 $SAFE"
        echo ""
        
        if [ "$ERRORS" -gt 0 ]; then
            echo -e "${RED}⚠ Errors detected: $ERRORS${NC}"
            echo ""
        fi
        
        # Recent Activity
        echo -e "${BOLD}${BLUE}─────────────────────────────────────────────────────────────────${NC}"
        echo ""
        echo -e "${BOLD}Recent Activity:${NC}"
        echo ""
        
        tail -n 10 "$LOG_FILE" | while IFS= read -r line; do
            # Color-code log lines
            if [[ "$line" == *"ERROR"* ]] || [[ "$line" == *"Error"* ]]; then
                echo -e "${RED}${line}${NC}"
            elif [[ "$line" == *"WARNING"* ]] || [[ "$line" == *"CAUTION"* ]]; then
                echo -e "${YELLOW}${line}${NC}"
            elif [[ "$line" == *"✓"* ]] || [[ "$line" == *"SUCCESS"* ]]; then
                echo -e "${GREEN}${line}${NC}"
            else
                echo -e "${DIM}${line}${NC}"
            fi
        done
    else
        echo -e "${YELLOW}No log file found${NC}"
        echo ""
        echo "Agent hasn't started yet or log file is missing."
    fi
    
    echo ""
    echo -e "${BOLD}${BLUE}─────────────────────────────────────────────────────────────────${NC}"
    echo ""
    echo -e "${DIM}Press Ctrl+C to exit${NC}"
    echo -e "${DIM}Updated: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
}

# Main loop
while true; do
    show_dashboard
    sleep 5
done
