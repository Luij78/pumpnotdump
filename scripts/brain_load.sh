#!/bin/bash
# BRAIN LOAD — Run at session start to load all project states
# This prevents Skipper from answering from stale memory

echo "=== BRAIN LOAD — $(date) ==="
echo ""

echo "📋 PROJECTS STATUS:"
echo "-------------------"

# Alexander
ALEXANDER_REMAINING=$(cat "/Users/luisgarcia/Documents/FL Geographic/remaining_owners.json" 2>/dev/null | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "ERROR")
echo "• Alexander: $ALEXANDER_REMAINING remaining"

# Self-Storage
STORAGE_STATUS=$(cat /Users/luisgarcia/Documents/Self-Storage-Project/phone_lookup_progress.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{d[\"processed\"]}/632')" 2>/dev/null || echo "ERROR")
echo "• Self-Storage: $STORAGE_STATUS"

# Expired Listings
EXPIRED_STATUS=$(python3 -c "import csv; rows=list(csv.DictReader(open('/Users/luisgarcia/Documents/Expired-Listings/expired_listings_with_owners.csv'))); done=len([x for x in rows if x.get('Owner_Name','').strip()]); print(f'{done}/1309')" 2>/dev/null || echo "ERROR")
echo "• Expired Listings: $EXPIRED_STATUS"

# TradingPal
echo ""
echo "🤖 TRADINGPAL:"
BOTS_RUNNING=$(ps aux | grep -E 'hold_to_settle|strategy_lab|notifier' | grep -v grep | wc -l | tr -d ' ')
echo "• Bots running: $BOTS_RUNNING"
if [ -f /tmp/strategy_lab/results.json ]; then
    TRADES=$(cat /tmp/strategy_lab/results.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{d.get(\"total_trades\", \"?\")} trades')" 2>/dev/null || echo "?")
    echo "• Strategy Lab: $TRADES"
fi

# Brivity
echo ""
echo "🏠 BRIVITY:"
if [ -f ~/clawd/projects/brivity/drafts_log.json ]; then
    TODAY=$(date +%Y-%m-%d)
    DRAFTS=$(cat ~/clawd/projects/brivity/drafts_log.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('drafts_completed',{}).get('$TODAY',[])))" 2>/dev/null || echo "0")
    echo "• Drafts today: $DRAFTS"
fi

echo ""
echo "📁 PROJECT FILES TO READ:"
echo "• ~/clawd/MEMORY.md"
echo "• ~/clawd/memory/$(date +%Y-%m-%d).md"
echo "• ~/clawd/projects/alexander-lookups/ORDERS.md"
echo "• ~/clawd/projects/self-storage/ORDERS.md"
echo "• ~/clawd/projects/expired-listings/ORDERS.md"
echo "• ~/clawd/projects/tradingpal/ORDERS.md"
echo "• ~/clawd/projects/brivity/ORDERS.md"
echo ""
echo "=== READ THESE FILES BEFORE ANSWERING PROJECT QUESTIONS ==="
