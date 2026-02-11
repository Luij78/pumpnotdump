#!/usr/bin/env python3
"""
Update Skipper's face state.
Usage:
    python3 update-skipper-state.py working "Processing phone lookups..."
    python3 update-skipper-state.py thinking "Analyzing data..."
    python3 update-skipper-state.py idle "Ready to help!"
    python3 update-skipper-state.py sleeping "Resting..."
    python3 update-skipper-state.py add-agent "Lookup Bot" "🔍" "Phone searches"
    python3 update-skipper-state.py remove-agent "Lookup Bot"
"""

import json
import sys
import os
from datetime import datetime

STATE_FILE = os.path.expanduser("~/clawd/canvas/skipper-state.json")

def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {
            "state": "idle",
            "activity": "Ready to help, Captain! 🫡",
            "subAgents": [],
            "lastUpdate": int(datetime.now().timestamp() * 1000)
        }

def save_state(state):
    state["lastUpdate"] = int(datetime.now().timestamp() * 1000)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    print(f"✅ State updated: {state['state']} - {state['activity']}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    action = sys.argv[1]
    state = load_state()
    
    if action in ['idle', 'working', 'thinking', 'sleeping']:
        state['state'] = action
        if len(sys.argv) > 2:
            state['activity'] = ' '.join(sys.argv[2:])
        elif action == 'idle':
            state['activity'] = "Ready to help, Captain! 🫡"
        elif action == 'sleeping':
            state['activity'] = "Resting... 💤"
        save_state(state)
    
    elif action == 'add-agent':
        if len(sys.argv) < 4:
            print("Usage: add-agent <name> <icon> [task]")
            sys.exit(1)
        name = sys.argv[2]
        icon = sys.argv[3]
        task = sys.argv[4] if len(sys.argv) > 4 else "Working..."
        
        # Remove existing agent with same name
        state['subAgents'] = [a for a in state['subAgents'] if a.get('name') != name]
        state['subAgents'].append({"name": name, "icon": icon, "task": task})
        save_state(state)
        print(f"✅ Added sub-agent: {name}")
    
    elif action == 'remove-agent':
        if len(sys.argv) < 3:
            print("Usage: remove-agent <name>")
            sys.exit(1)
        name = sys.argv[2]
        state['subAgents'] = [a for a in state['subAgents'] if a.get('name') != name]
        save_state(state)
        print(f"✅ Removed sub-agent: {name}")
    
    elif action == 'clear-agents':
        state['subAgents'] = []
        save_state(state)
        print("✅ Cleared all sub-agents")
    
    elif action == 'status':
        print(json.dumps(state, indent=2))
    
    else:
        print(f"Unknown action: {action}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
