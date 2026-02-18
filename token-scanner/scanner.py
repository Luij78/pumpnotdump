#!/usr/bin/env python3
"""
scanner.py — pump.notdump Token Scanner
Scans DexScreener for new Solana token launches and scores them for rug risk.
Part of the OpenClaw autonomous security agent.

Usage:
    python3 scanner.py                    # Scan recent Solana tokens
    python3 scanner.py --limit 20        # Scan and show top 20
    python3 scanner.py --high-risk-only  # Only show high risk tokens
    python3 scanner.py --token <ADDRESS>  # Analyze a specific token
"""

import sys
import json
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Optional

# Add parent dir to path for risk_scorer import
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from risk_scorer import score_token, format_report, RiskReport
from telegram_alerts import send_high_risk_alert, send_medium_risk_alert


# ─── CONSTANTS ────────────────────────────────────────────────────────────────

DEXSCREENER_SEARCH_URL = "https://api.dexscreener.com/latest/dex/search?q=solana"
DEXSCREENER_PAIRS_URL = "https://api.dexscreener.com/latest/dex/pairs/solana/"
DEXSCREENER_TOKEN_URL = "https://api.dexscreener.com/latest/dex/tokens/"

# Tokens newer than this many hours are considered "new launches"
NEW_LAUNCH_WINDOW_HOURS = 2
REQUEST_TIMEOUT = 15
USER_AGENT = "pump.notdump/1.0 (OpenClaw security agent; educational)"


# ─── API HELPERS ──────────────────────────────────────────────────────────────

def fetch_url(url: str, timeout: int = REQUEST_TIMEOUT) -> Optional[dict]:
    """Fetch JSON from a URL with error handling."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        print(f"  [HTTP {e.code}] Failed to fetch: {url}")
        return None
    except urllib.error.URLError as e:
        print(f"  [Network Error] {e.reason} — {url}")
        return None
    except json.JSONDecodeError as e:
        print(f"  [JSON Error] Could not parse response from {url}: {e}")
        return None
    except Exception as e:
        print(f"  [Error] {type(e).__name__}: {e}")
        return None


def fetch_new_solana_tokens(max_age_hours: float = NEW_LAUNCH_WINDOW_HOURS) -> list:
    """
    Fetch recently launched Solana tokens from DexScreener.
    Returns list of pair dicts, filtered by age.
    """
    print(f"🔍 Fetching new Solana token launches (last {max_age_hours:.0f}h)...")

    # Try the search endpoint for Solana tokens
    data = fetch_url(DEXSCREENER_SEARCH_URL)
    if not data:
        # Fallback: try a trending tokens approach
        print("  Search endpoint failed, trying trending fallback...")
        return []

    pairs = data.get("pairs", [])
    if not pairs:
        print("  No pairs found in response.")
        return []

    # Filter to Solana only and recently created
    now_ms = time.time() * 1000
    cutoff_ms = now_ms - (max_age_hours * 60 * 60 * 1000)

    solana_pairs = []
    for pair in pairs:
        # Must be Solana
        if pair.get("chainId", "").lower() != "solana":
            continue
        # Must be recently created
        created_ms = pair.get("pairCreatedAt")
        if created_ms and float(created_ms) >= cutoff_ms:
            solana_pairs.append(pair)
        elif not created_ms:
            # Include if no creation date (we'll age-penalize in scorer)
            solana_pairs.append(pair)

    print(f"  Found {len(solana_pairs)} Solana pairs from last {max_age_hours:.0f}h")
    return solana_pairs


def fetch_token_by_address(token_address: str) -> Optional[dict]:
    """Fetch a specific token by its mint address."""
    url = DEXSCREENER_TOKEN_URL + token_address
    print(f"🔍 Fetching token data for {token_address[:8]}...")
    data = fetch_url(url)
    if not data:
        return None
    pairs = data.get("pairs", [])
    if not pairs:
        print(f"  No pairs found for token {token_address}")
        return None
    # Return the pair with most liquidity
    return sorted(pairs, key=lambda p: float(p.get("liquidity", {}).get("usd", 0) or 0), reverse=True)[0]


def fetch_trending_solana_tokens(limit: int = 30) -> list:
    """
    Fallback: fetch trending Solana tokens when new-launch data isn't available.
    Uses DexScreener's boosted tokens endpoint.
    """
    print("📈 Fetching trending Solana tokens as fallback...")
    url = "https://api.dexscreener.com/token-boosts/top/v1"
    data = fetch_url(url)

    if not data:
        # Last resort: try specific known Solana pairs for demo
        print("  Using demo data (API rate limited)")
        return get_demo_tokens()

    if isinstance(data, list):
        solana_boosts = [item for item in data if item.get("chainId", "").lower() == "solana"][:limit]
    else:
        solana_boosts = []

    if not solana_boosts:
        return get_demo_tokens()

    # Fetch full pair data for each boosted token
    results = []
    for boost in solana_boosts[:10]:  # Limit API calls
        addr = boost.get("tokenAddress", "")
        if addr:
            pair_data = fetch_token_by_address(addr)
            if pair_data:
                results.append(pair_data)
            time.sleep(0.2)  # Rate limit courtesy

    return results if results else get_demo_tokens()


def get_demo_tokens() -> list:
    """
    Return realistic demo token data for when API is unavailable.
    Based on real DexScreener response format.
    """
    now_ms = time.time() * 1000
    return [
        {
            "chainId": "solana",
            "pairAddress": "DemoAddr1111111111111111111111111111111111",
            "baseToken": {
                "address": "MintAuth9999999999999999999999999999999999",
                "name": "AI Mega Moon Token",
                "symbol": "AIMOON",
            },
            "quoteToken": {"symbol": "SOL"},
            "priceUsd": "0.0000023",
            "priceChange": {"h24": 847},
            "liquidity": {"usd": 1800},
            "volume": {"h24": 42000},
            "pairCreatedAt": now_ms - (0.5 * 60 * 60 * 1000),  # 30 min ago
            "topHolderPct": 71,
            "top10HolderPct": 89,
            "mintAuthority": "9xFakeMintAuthority111111111111111111111111",
            "freezeAuthority": "9xFakeFreezeAuth11111111111111111111111111",
        },
        {
            "chainId": "solana",
            "pairAddress": "DemoAddr2222222222222222222222222222222222",
            "baseToken": {
                "address": "SafeToken111111111111111111111111111111111",
                "name": "VestedAI Protocol",
                "symbol": "VESTAI",
            },
            "quoteToken": {"symbol": "SOL"},
            "priceUsd": "0.045",
            "priceChange": {"h24": 34},
            "liquidity": {"usd": 85000},
            "volume": {"h24": 127000},
            "pairCreatedAt": now_ms - (72 * 60 * 60 * 1000),  # 3 days ago
            "topHolderPct": 4.2,
            "top10HolderPct": 22,
            "mintAuthority": None,
            "freezeAuthority": None,
        },
        {
            "chainId": "solana",
            "pairAddress": "DemoAddr3333333333333333333333333333333333",
            "baseToken": {
                "address": "SuspToken11111111111111111111111111111111",
                "name": "Totally Legit Coin",
                "symbol": "LEGIT",
            },
            "quoteToken": {"symbol": "SOL"},
            "priceUsd": "0.00000071",
            "priceChange": {"h24": 2300},
            "liquidity": {"usd": 4200},
            "volume": {"h24": 190000},
            "pairCreatedAt": now_ms - (1.2 * 60 * 60 * 1000),  # 72 min ago
            "topHolderPct": 38,
            "top10HolderPct": 67,
            "mintAuthority": "8xSuspiciousMint11111111111111111111111111",
            "freezeAuthority": None,
        },
        {
            "chainId": "solana",
            "pairAddress": "DemoAddr4444444444444444444444444444444444",
            "baseToken": {
                "address": "NeutToken11111111111111111111111111111111",
                "name": "DeFi Yield Optimizer",
                "symbol": "DYO",
            },
            "quoteToken": {"symbol": "SOL"},
            "priceUsd": "0.12",
            "priceChange": {"h24": 18},
            "liquidity": {"usd": 22000},
            "volume": {"h24": 55000},
            "pairCreatedAt": now_ms - (24 * 60 * 60 * 1000),  # 24 hours ago
            "topHolderPct": 12,
            "top10HolderPct": 41,
            "mintAuthority": None,
            "freezeAuthority": None,
        },
        {
            "chainId": "solana",
            "pairAddress": "DemoAddr5555555555555555555555555555555555",
            "baseToken": {
                "address": "NewScam111111111111111111111111111111111111",
                "name": "Elon Mars Rocket AI",
                "symbol": "ELMRAI",
            },
            "quoteToken": {"symbol": "SOL"},
            "priceUsd": "0.00000001",
            "priceChange": {"h24": 5600},
            "liquidity": {"usd": 300},
            "volume": {"h24": 9800},
            "pairCreatedAt": now_ms - (0.1 * 60 * 60 * 1000),  # 6 min ago
            "topHolderPct": 88,
            "top10HolderPct": 97,
            "mintAuthority": "7xNewScamMint1111111111111111111111111111",
            "freezeAuthority": "7xNewScamFreeze111111111111111111111111",
        },
    ]


# ─── MAIN SCAN LOGIC ──────────────────────────────────────────────────────────

def scan_tokens(tokens: list, send_alerts: bool = False, high_risk_only: bool = False) -> dict:
    """
    Score all tokens and optionally send Telegram alerts.
    Returns summary stats dict.
    """
    if not tokens:
        return {"scanned": 0, "safe": 0, "monitoring": 0, "high_risk": 0, "reports": []}

    reports = []
    counts = {"safe": 0, "monitoring": 0, "high_risk": 0}
    safest = None
    riskiest = None

    print(f"\n{'═' * 60}")
    print(f"🤖 pump.notdump Security Agent — Token Scan")
    print(f"⏰ {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"{'═' * 60}\n")

    for i, token_data in enumerate(tokens, 1):
        token_name = token_data.get("baseToken", {}).get("name", "Unknown")
        print(f"[{i}/{len(tokens)}] Analyzing: {token_name}...")

        try:
            report = score_token(token_data)
        except Exception as e:
            print(f"  ⚠️ Scoring failed: {e} — skipping")
            continue

        reports.append(report)

        # Track extremes
        if safest is None or report.total_score < safest.total_score:
            safest = report
        if riskiest is None or report.total_score > riskiest.total_score:
            riskiest = report

        # Categorize
        if report.total_score >= 76:
            counts["high_risk"] += 1
            if not high_risk_only:
                print(format_report(report))
            else:
                print(f"  🚨 HIGH RISK ({report.total_score}/100): {report.token_name}")
                print(format_report(report))

            if send_alerts:
                send_high_risk_alert(token_data, report)

        elif report.total_score >= 51:
            counts["monitoring"] += 1
            if not high_risk_only:
                print(format_report(report))
            else:
                print(f"  ⚠️ MEDIUM RISK ({report.total_score}/100): {report.token_name}")

            if send_alerts and report.total_score >= 65:
                send_medium_risk_alert(token_data, report)

        else:
            counts["safe"] += 1
            if not high_risk_only:
                print(format_report(report))
            else:
                print(f"  ✅ LOW RISK ({report.total_score}/100): {report.token_name}")

    # Print summary
    total = len(reports)
    print(f"\n{'═' * 60}")
    print(f"📊 SCAN COMPLETE — {datetime.now(timezone.utc).strftime('%H:%M UTC')}")
    print(f"{'═' * 60}")
    print(f"  Tokens analyzed: {total}")
    print(f"  ✅ Low Risk:     {counts['safe']}")
    print(f"  ⚠️  Monitoring:   {counts['monitoring']}")
    print(f"  🚨 High Risk:    {counts['high_risk']}")

    if safest:
        print(f"\n  🏆 Safest:   {safest.token_name} ({safest.total_score}/100)")
    if riskiest:
        print(f"  ☠️  Riskiest: {riskiest.token_name} ({riskiest.total_score}/100)")

    print(f"{'═' * 60}\n")
    print("🛡️  pump.notdump — Powered by OpenClaw Autonomous Agent")

    return {
        "scanned": total,
        "safe": counts["safe"],
        "monitoring": counts["monitoring"],
        "high_risk": counts["high_risk"],
        "reports": reports,
        "safest_token": {"name": safest.token_name, "score": safest.total_score} if safest else None,
        "riskiest_token": {"name": riskiest.token_name, "score": riskiest.total_score} if riskiest else None,
    }


# ─── ENTRYPOINT ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="pump.notdump Token Scanner — Detects Solana rug pulls via DexScreener"
    )
    parser.add_argument("--limit", type=int, default=20, help="Max tokens to scan (default: 20)")
    parser.add_argument("--high-risk-only", action="store_true", help="Only show high/medium risk tokens")
    parser.add_argument("--send-alerts", action="store_true", help="Send Telegram alerts (requires env vars)")
    parser.add_argument("--token", type=str, help="Analyze a specific token by address")
    parser.add_argument("--new", action="store_true", help="Only scan tokens from last 2 hours")
    parser.add_argument("--demo", action="store_true", help="Use built-in demo data (no API calls)")
    args = parser.parse_args()

    if args.token:
        # Analyze a specific token
        token_data = fetch_token_by_address(args.token)
        if token_data:
            scan_tokens([token_data], send_alerts=args.send_alerts)
        else:
            print(f"❌ Could not fetch data for token: {args.token}")
            sys.exit(1)

    elif args.demo:
        # Use demo data
        print("ℹ️  Running with demo data (--demo flag)\n")
        tokens = get_demo_tokens()
        scan_tokens(tokens, send_alerts=args.send_alerts, high_risk_only=args.high_risk_only)

    else:
        # Live scan
        tokens = fetch_new_solana_tokens(max_age_hours=2 if args.new else 24)

        if not tokens:
            print("  No new tokens found via search, trying trending...")
            tokens = fetch_trending_solana_tokens(limit=args.limit)

        if not tokens:
            print("❌ Could not fetch any token data. Try --demo flag for offline testing.")
            sys.exit(1)

        # Cap at limit
        tokens = tokens[:args.limit]
        scan_tokens(tokens, send_alerts=args.send_alerts, high_risk_only=args.high_risk_only)


if __name__ == "__main__":
    main()
