"""
telegram_alerts.py — pump.notdump Telegram Alert System
Sends formatted alerts for high-risk tokens detected by the OpenClaw agent.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Optional

# Load env vars
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
DEXSCREENER_BASE = "https://dexscreener.com/solana/"


def send_telegram_message(text: str, bot_token: str = None, chat_id: str = None,
                           parse_mode: str = "HTML", disable_preview: bool = True) -> bool:
    """
    Send a message via Telegram Bot API.

    Args:
        text: Message text (HTML formatted)
        bot_token: Telegram bot token (defaults to env var)
        chat_id: Target chat ID (defaults to env var)
        parse_mode: "HTML" or "MarkdownV2"
        disable_preview: Suppress link previews

    Returns:
        True if sent successfully, False otherwise
    """
    token = bot_token or BOT_TOKEN
    chat = chat_id or CHAT_ID

    if not token or not chat:
        print("[telegram_alerts] ⚠️  No TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID set.")
        print("[telegram_alerts] Message would have been:")
        print(text[:500] + "..." if len(text) > 500 else text)
        return False

    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": disable_preview,
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(api_url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("ok"):
                print(f"[telegram_alerts] ✅ Alert sent successfully (message_id: {result['result']['message_id']})")
                return True
            else:
                print(f"[telegram_alerts] ❌ Telegram API error: {result}")
                return False
    except Exception as e:
        print(f"[telegram_alerts] ❌ Failed to send alert: {e}")
        return False


def build_high_risk_alert(token_data: dict, risk_report) -> str:
    """Build HTML-formatted HIGH RISK alert message."""
    name = risk_report.token_name
    symbol = risk_report.token_symbol
    address = risk_report.token_address
    score = risk_report.total_score
    dex_url = DEXSCREENER_BASE + address

    # Build risk factors list
    critical_factors = [f for f in risk_report.factors if f.severity == "critical"]
    major_factors = [f for f in risk_report.factors if f.severity == "major"]

    factors_html = ""
    for f in (critical_factors + major_factors)[:4]:  # Top 4 flags
        factors_html += f"  • {f.name}: {f.description}\n"

    age_str = f"{risk_report.age_hours:.1f}h" if risk_report.age_hours else "Unknown"
    liq_str = f"${risk_report.liquidity_usd:,.0f}" if risk_report.liquidity_usd else "$0"
    mint_str = "⛔ ACTIVE" if risk_report.mint_authority else "✓ Revoked"
    holder_str = f"{risk_report.top_holder_pct:.1f}%" if risk_report.top_holder_pct else "Unknown"

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    message = (
        f"🚨 <b>HIGH RISK TOKEN DETECTED</b>\n"
        f"\n"
        f"Token: <b>{name}</b> (${symbol})\n"
        f"Risk Score: <b>{score}/100</b> 🔴\n"
        f"\n"
        f"<b>⚠️ Why this is dangerous:</b>\n"
        f"{factors_html}"
        f"\n"
        f"<b>📊 Stats:</b>\n"
        f"  💧 Liquidity: {liq_str}\n"
        f"  📅 Age: {age_str}\n"
        f"  🔒 Mint Authority: {mint_str}\n"
        f"  👥 Top Holder: {holder_str}\n"
        f"\n"
        f"🔗 <a href='{dex_url}'>View on DexScreener</a>\n"
        f"\n"
        f"🛡️ <i>pump.notdump Agent — protecting investors 24/7</i>\n"
        f"<i>{timestamp}</i>"
    )
    return message


def build_medium_risk_alert(token_data: dict, risk_report) -> str:
    """Build HTML-formatted MEDIUM RISK monitoring alert."""
    name = risk_report.token_name
    symbol = risk_report.token_symbol
    address = risk_report.token_address
    score = risk_report.total_score
    dex_url = DEXSCREENER_BASE + address

    top_flag = risk_report.factors[0].name if risk_report.factors else "Multiple risk factors"
    timestamp = datetime.utcnow().strftime("%H:%M UTC")

    message = (
        f"⚠️ <b>Token Under Monitoring</b>\n"
        f"\n"
        f"Token: <b>{name}</b> (${symbol})\n"
        f"Risk Score: <b>{score}/100</b> 🟡\n"
        f"\n"
        f"Flagged for: {top_flag}\n"
        f"Will re-scan in 30 minutes.\n"
        f"\n"
        f"🔗 <a href='{dex_url}'>DexScreener</a>\n"
        f"<i>{timestamp}</i>"
    )
    return message


def build_hourly_summary(stats: dict) -> str:
    """Build hourly summary report message."""
    scanned = stats.get("scanned", 0)
    safe = stats.get("safe", 0)
    monitoring = stats.get("monitoring", 0)
    high_risk = stats.get("high_risk", 0)
    uptime = stats.get("uptime_pct", 99.9)
    safest = stats.get("safest_token", {})
    riskiest = stats.get("riskiest_token", {})
    funds_protected = stats.get("funds_protected_usd", 0)

    period_start = stats.get("period_start", "last hour")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    safest_str = ""
    if safest:
        safest_str = f"\n🏆 Safest: {safest.get('name', '?')} ({safest.get('score', 0)}/100)"

    riskiest_str = ""
    if riskiest:
        riskiest_str = f"\n☠️ Riskiest: {riskiest.get('name', '?')} ({riskiest.get('score', 0)}/100)"

    message = (
        f"📊 <b>pump.notdump Hourly Report</b>\n"
        f"⏰ {period_start} → {timestamp}\n"
        f"\n"
        f"<b>Tokens Scanned:</b> {scanned}\n"
        f"  ✅ Safe: {safe}\n"
        f"  ⚠️ Monitoring: {monitoring}\n"
        f"  🚨 High Risk: {high_risk}"
        f"{safest_str}"
        f"{riskiest_str}\n"
        f"\n"
        f"💰 Estimated funds protected: ${funds_protected:,.0f}\n"
        f"🤖 Agent uptime: {uptime:.1f}%\n"
        f"\n"
        f"<i>🛡️ pump.notdump — Autonomous token security</i>"
    )
    return message


def build_pattern_alert(tokens: list, pattern: str, common_wallets: int) -> str:
    """Build coordinated attack pattern alert."""
    token_list = "\n".join([f"  • {t}" for t in tokens[:5]])
    if len(tokens) > 5:
        token_list += f"\n  ... and {len(tokens) - 5} more"

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    message = (
        f"🔔 <b>COORDINATED RUG PATTERN DETECTED</b>\n"
        f"\n"
        f"The agent has identified <b>{len(tokens)} related tokens</b>\n"
        f"with similar rug pull signatures:\n"
        f"\n"
        f"<b>Tokens:</b>\n{token_list}\n"
        f"\n"
        f"<b>Pattern:</b> {pattern}\n"
        f"<b>Wallets in common:</b> {common_wallets}\n"
        f"\n"
        f"⛔ This appears to be a coordinated operation.\n"
        f"Avoid all related tokens.\n"
        f"\n"
        f"🛡️ <i>pump.notdump Agent | {timestamp}</i>"
    )
    return message


def send_high_risk_alert(token_data: dict, risk_report, bot_token: str = None, chat_id: str = None) -> bool:
    """Send an immediate high-risk token alert."""
    message = build_high_risk_alert(token_data, risk_report)
    return send_telegram_message(message, bot_token=bot_token, chat_id=chat_id)


def send_medium_risk_alert(token_data: dict, risk_report, bot_token: str = None, chat_id: str = None) -> bool:
    """Send a medium-risk monitoring alert."""
    message = build_medium_risk_alert(token_data, risk_report)
    return send_telegram_message(message, bot_token=bot_token, chat_id=chat_id)


def send_hourly_summary(stats: dict, bot_token: str = None, chat_id: str = None) -> bool:
    """Send the hourly summary report."""
    message = build_hourly_summary(stats)
    return send_telegram_message(message, bot_token=bot_token, chat_id=chat_id)


def send_pattern_alert(tokens: list, pattern: str, common_wallets: int,
                        bot_token: str = None, chat_id: str = None) -> bool:
    """Send a coordinated attack pattern alert."""
    message = build_pattern_alert(tokens, pattern, common_wallets)
    return send_telegram_message(message, bot_token=bot_token, chat_id=chat_id)


if __name__ == "__main__":
    # Test: print a sample alert (no actual send without env vars)
    from risk_scorer import RiskReport, RiskFactor

    sample_report = RiskReport(
        token_address="AbcDef123456789012345678901234567890123456",
        token_name="Fake Moon Token",
        token_symbol="MOON",
        total_score=87,
        risk_level="HIGH RISK",
        liquidity_usd=2500,
        volume_24h=45000,
        age_hours=0.8,
        top_holder_pct=62,
        mint_authority="9xSomeFakeMintAuth",
        freeze_authority=None,
    )
    sample_report.factors = [
        RiskFactor("Mint Authority Active", 35, "Creator can print unlimited tokens", "critical"),
        RiskFactor("Extreme Holder Concentration", 30, "Top holder owns 62%", "critical"),
        RiskFactor("Brand New Token", 20, "Only 0.8 hours old", "major"),
        RiskFactor("Very Low Liquidity", 20, "Only $2,500 in liquidity", "major"),
    ]
    sample_report.positive_signals = ["Freeze authority revoked"]

    print("=== SAMPLE HIGH RISK ALERT (no credentials needed to preview) ===\n")
    print(build_high_risk_alert({}, sample_report))
    print("\n=== SAMPLE HOURLY SUMMARY ===\n")
    print(build_hourly_summary({
        "scanned": 47,
        "safe": 39,
        "monitoring": 5,
        "high_risk": 3,
        "uptime_pct": 99.8,
        "funds_protected_usd": 47500,
        "period_start": "14:00 UTC",
        "safest_token": {"name": "VESTED_AI", "score": 8},
        "riskiest_token": {"name": "FAKE_MOON", "score": 87},
    }))
