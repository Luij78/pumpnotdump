# TOOLS.md - Local Notes

## 🖥️ MACHINE MAP (READ THIS FIRST)

| Machine | Address | What's There |
|---------|---------|--------------|
| **Mac Mini** | localhost | Clawdbot, ~/clawd/, TradingPal, FlipHunter, memory files, dashboard |

**Rule:** Everything runs on Mac Mini locally. No remote access needed.

---

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## Skipper's Email
- **Email:** luis.ai.skipper@gmail.com
- **Purpose:** Skipper's dedicated email for sending/receiving
- **Created:** 2026-01-25
- **Config:** ~/.config/himalaya/config.toml
- **Status:** ✅ WORKING (tested 2026-01-26)
- **Luis's personal email:** lucho6913@gmail.com

## Local Machine
- **Mac Mini:** localhost (everything runs here)

## FlipHunter (Deal Finder)
- **Location:** ~/FlipHunter/ (Mac Mini - local)
- **Status:** PAUSED (ready when you need it)
- **Venv:** Python 3.13 with Flask, BeautifulSoup
- **Start:** `cd ~/FlipHunter && source venv/bin/activate && python3 flip_app.py`
- **Web UI:** http://localhost:8080 (when running)

## Trading Bot (Polymarket)
- **Location:** ~/TradingPal/ (Mac Mini - local)
- **Wallet:** 0x3DA89a3dA0a9f4f46329F3cc0732257244E8f7E3
- **Platform:** Polymarket (Polygon network)
- **Venv:** Python 3.13 with py-clob-client, web3
- **Start:** `cd ~/TradingPal && source venv/bin/activate && nohup python3 hold_to_settle.py > hold_to_settle.log 2>&1 &`

## Solana Wallet (Memecoin Trading)
- **Pubkey:** 5x6uz6jsu2GHRsvQmnho2eSZsTCoa2etWobZ7vSxVRir
- **Keypair:** ~/.config/solana/skipper-wallet.json
- **Created:** 2026-01-26
- **Purpose:** Pump.fun hackathon + memecoin trading bot
- **Network:** mainnet-beta

## Voice Transcription
- **Tool:** whisper-cli (whisper.cpp)
- **Model:** ~/.local/share/whisper-cpp/models/ggml-base.en.bin
- **Workflow:** ffmpeg (ogg→wav) → whisper-cli → text
- **Status:** ✅ WORKING (fixed 2026-01-26)

## Scheduled Jobs
- Morning Brief: 6 AM EST
- Overnight Work: 11 PM EST
- Memecoin Scanner: Every 30 minutes
- Session Monitor: Every 30 minutes (auto-checkpoint if context > 70%)

## Token Constraints
**Luis has Anthropic Max plan = OPUS ONLY**
- Cannot switch to Sonnet/Haiku to save tokens
- Weekly limit resets every Tuesday 1:00 PM
- Be efficient: concise responses, minimize browser snapshots, batch work smartly

---

Add whatever helps you do your job. This is your cheat sheet.
