#!/bin/bash
# Start Skipper Face server and open in browser

cd "$(dirname "$0")"

# Kill any existing server on port 8088
lsof -ti:8088 | xargs kill -9 2>/dev/null

# Start Python HTTP server in background
echo "⚓ Starting Skipper Face server on http://localhost:8088"
python3 -m http.server 8088 &
SERVER_PID=$!

# Wait for server to start
sleep 1

# Open in default browser
open "http://localhost:8088/skipper-face-live.html"

echo "✅ Skipper Face is live!"
echo "   Server PID: $SERVER_PID"
echo "   URL: http://localhost:8088/skipper-face-live.html"
echo ""
echo "To stop: kill $SERVER_PID"
