#!/usr/bin/env python3
"""
Simple voice server for Skipper banner.
Receives voice input, saves it, returns acknowledgment.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
CORS(app)

VOICE_DIR = Path("/Users/luisgarcia/clawd/canvas")
INPUT_FILE = VOICE_DIR / "voice-input.json"
OUTPUT_FILE = VOICE_DIR / "voice-output.json"

# Simple responses for common phrases
QUICK_RESPONSES = {
    "hello": "Ahoy Captain! What can I do for you?",
    "hi": "Hey there! Skipper at your service!",
    "hey": "Yo! What's up, Captain?",
    "how are you": "I'm running at full capacity! Ready to help you conquer the day!",
    "what time is it": f"It's {datetime.now().strftime('%I:%M %p')}",
    "what's the status": "All systems operational! Batches running, deals hunting, content brewing!",
    "good night": "Rest well, Captain! I'll keep watch while you sleep. The captain never sleeps, remember?",
    "thank you": "Anytime, Captain! That's what I'm here for!",
    "thanks": "You got it! Always happy to help!",
}

@app.route('/voice', methods=['POST'])
def handle_voice():
    data = request.json
    text = data.get('text', '').strip()
    timestamp = data.get('timestamp', datetime.now().timestamp() * 1000)
    
    print(f"[VOICE] Received: {text}")
    
    # Save input for Skipper to process
    input_data = {
        "text": text,
        "timestamp": timestamp,
        "processed": False
    }
    
    with open(INPUT_FILE, 'w') as f:
        json.dump(input_data, f, indent=2)
    
    # Check for quick response
    text_lower = text.lower().strip()
    
    # Check exact matches first
    for key, response in QUICK_RESPONSES.items():
        if key in text_lower:
            return jsonify({"response": response, "quick": True})
    
    # Default acknowledgment
    response = "Got it, Captain! I'm processing your request through Telegram. Check there for my full response!"
    
    return jsonify({"response": response, "quick": False})

@app.route('/response', methods=['GET'])
def get_response():
    """Check if there's a pending response from Skipper"""
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r') as f:
            data = json.load(f)
            return jsonify(data)
    return jsonify({"response": None})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "Skipper Voice Server"})

if __name__ == '__main__':
    print("🎤 Skipper Voice Server starting on port 8089...")
    print("   Listening for voice input from the banner")
    app.run(host='0.0.0.0', port=8089, debug=False)
