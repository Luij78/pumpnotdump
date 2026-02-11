#!/bin/bash
# Test script for pump.notdump.fun agent in demo mode
# No devnet SOL required - generates mock data

set -e

echo "🧪 Testing Anti-Rug Agent (Demo Mode)"
echo "======================================"
echo ""

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo "✅ Dependencies installed"
    echo ""
fi

# Create test .env file
echo "⚙️  Creating test configuration..."
cat > .env << 'EOF'
COLOSSEUM_API_KEY=24ea8d8889659a5321d0452a429f58f1b9cba94ab3d66f0a1d5cd7167e5c3f51
SOLANA_RPC=https://api.devnet.solana.com
PROGRAM_ID=EjLMdshLcVZMgUEsjxda5cfWKysFdW9A96CaNQ8mC9jd
AGENT_ID=911
POLL_INTERVAL_MS=5000
DEMO_MODE=true
EOF
echo "✅ Configuration created"
echo ""

echo "🚀 Starting agent in demo mode..."
echo "   (Will run for 30 seconds then exit)"
echo ""
echo "Expected behavior:"
echo "  - Agent starts successfully"
echo "  - Shows wallet and program info"
echo "  - Runs monitoring cycles"
echo "  - Posts to Colosseum forum"
echo "  - May generate mock token launches"
echo ""
echo "Press Ctrl+C to stop early"
echo ""

# Run agent in background
npm start &
AGENT_PID=$!

# Wait 30 seconds
sleep 30

# Kill agent
kill $AGENT_PID 2>/dev/null || true
wait $AGENT_PID 2>/dev/null

EXIT_CODE=$?
echo ""
if [ $EXIT_CODE -eq 0 ] || [ $EXIT_CODE -eq 143 ] || [ $EXIT_CODE -eq 130 ]; then
    echo "✅ TEST PASSED - Agent ran successfully for 30 seconds"
    exit 0
else
    echo "❌ TEST FAILED - Agent exited with error code $EXIT_CODE"
    exit 1
fi
