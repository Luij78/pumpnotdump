"""
risk_scorer.py — pump.notdump Token Risk Scorer
Scores Solana tokens 0-100 based on rug pull indicators.
Used by the OpenClaw security agent.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RiskFactor:
    name: str
    score: int
    description: str
    severity: str  # 'critical', 'major', 'moderate', 'info'


@dataclass
class RiskReport:
    token_address: str
    token_name: str
    token_symbol: str
    total_score: int
    risk_level: str
    factors: list = field(default_factory=list)
    positive_signals: list = field(default_factory=list)
    liquidity_usd: float = 0.0
    volume_24h: float = 0.0
    age_hours: float = 0.0
    top_holder_pct: float = 0.0
    mint_authority: Optional[str] = None
    freeze_authority: Optional[str] = None

    def verdict(self) -> str:
        if self.total_score >= 76:
            return "🚨 AVOID — HIGH RUG RISK"
        elif self.total_score >= 51:
            return "⚠️ CAUTION — Monitor closely"
        elif self.total_score >= 31:
            return "🟡 LOW CAUTION — Trade carefully"
        else:
            return "✅ APPEARS SAFE — Standard DYOR applies"

    def risk_emoji(self) -> str:
        if self.total_score >= 76:
            return "🚨"
        elif self.total_score >= 51:
            return "⚠️"
        elif self.total_score >= 31:
            return "🟡"
        else:
            return "✅"


def score_token(token_data: dict) -> RiskReport:
    """
    Score a token based on rug pull indicators.

    Args:
        token_data: Dict from DexScreener API response (pairs endpoint)

    Returns:
        RiskReport with total score and breakdown
    """

    # Extract fields from DexScreener data
    token_address = token_data.get("baseToken", {}).get("address", "unknown")
    token_name = token_data.get("baseToken", {}).get("name", "Unknown Token")
    token_symbol = token_data.get("baseToken", {}).get("symbol", "???")

    liquidity_usd = float(token_data.get("liquidity", {}).get("usd", 0) or 0)
    volume_24h = float(token_data.get("volume", {}).get("h24", 0) or 0)
    price_change_24h = float(token_data.get("priceChange", {}).get("h24", 0) or 0)

    # Token age: DexScreener provides pairCreatedAt in milliseconds
    pair_created_ms = token_data.get("pairCreatedAt", None)
    age_hours = 0.0
    if pair_created_ms:
        import time
        age_ms = (time.time() * 1000) - float(pair_created_ms)
        age_hours = age_ms / (1000 * 60 * 60)

    # Holder info (from enriched data if available)
    top_holder_pct = float(token_data.get("topHolderPct", 0) or 0)
    top10_holder_pct = float(token_data.get("top10HolderPct", 0) or 0)

    # Authority info (from enriched data)
    mint_authority = token_data.get("mintAuthority", None)
    freeze_authority = token_data.get("freezeAuthority", None)

    # Initialize report
    report = RiskReport(
        token_address=token_address,
        token_name=token_name,
        token_symbol=token_symbol,
        total_score=0,
        risk_level="",
        liquidity_usd=liquidity_usd,
        volume_24h=volume_24h,
        age_hours=age_hours,
        top_holder_pct=top_holder_pct,
        mint_authority=mint_authority,
        freeze_authority=freeze_authority,
    )

    factors = []
    positive_signals = []

    # ─── FACTOR 1: LIQUIDITY DEPTH ─────────────────────────────────────────────
    if liquidity_usd == 0:
        factors.append(RiskFactor(
            name="Zero Liquidity",
            score=30,
            description="No liquidity found — token cannot be traded safely",
            severity="critical"
        ))
    elif liquidity_usd < 1_000:
        factors.append(RiskFactor(
            name="Extremely Low Liquidity",
            score=25,
            description=f"Only ${liquidity_usd:,.0f} in liquidity — highly manipulable",
            severity="critical"
        ))
    elif liquidity_usd < 5_000:
        factors.append(RiskFactor(
            name="Very Low Liquidity",
            score=20,
            description=f"${liquidity_usd:,.0f} liquidity — easily drained",
            severity="major"
        ))
    elif liquidity_usd < 10_000:
        factors.append(RiskFactor(
            name="Low Liquidity",
            score=12,
            description=f"${liquidity_usd:,.0f} liquidity — below $10K safety threshold",
            severity="moderate"
        ))
    elif liquidity_usd >= 50_000:
        positive_signals.append("Healthy liquidity > $50K")
    elif liquidity_usd >= 10_000:
        positive_signals.append(f"Adequate liquidity: ${liquidity_usd:,.0f}")

    # ─── FACTOR 2: TOKEN AGE ───────────────────────────────────────────────────
    if age_hours < 1:
        factors.append(RiskFactor(
            name="Brand New Token",
            score=20,
            description=f"Only {age_hours:.1f} hours old — no track record",
            severity="major"
        ))
    elif age_hours < 6:
        factors.append(RiskFactor(
            name="Very New Token",
            score=15,
            description=f"{age_hours:.1f} hours old — early stage, high risk window",
            severity="major"
        ))
    elif age_hours < 24:
        factors.append(RiskFactor(
            name="Less Than 24h Old",
            score=10,
            description=f"{age_hours:.1f} hours old — in the high-risk rug window",
            severity="moderate"
        ))
    elif age_hours > 168:  # 1 week
        positive_signals.append(f"Token survived {age_hours/24:.0f} days — lower exit risk")

    # ─── FACTOR 3: VOLUME vs LIQUIDITY (PUMP PATTERN) ─────────────────────────
    if liquidity_usd > 0 and volume_24h > 0:
        vol_liq_ratio = volume_24h / liquidity_usd
        if vol_liq_ratio > 50:
            factors.append(RiskFactor(
                name="Extreme Volume Spike",
                score=25,
                description=f"Volume is {vol_liq_ratio:.0f}x the liquidity — classic pump signature",
                severity="critical"
            ))
        elif vol_liq_ratio > 20:
            factors.append(RiskFactor(
                name="Suspicious Volume Pattern",
                score=18,
                description=f"Volume is {vol_liq_ratio:.0f}x the liquidity — wash trading suspected",
                severity="major"
            ))
        elif vol_liq_ratio > 10:
            factors.append(RiskFactor(
                name="High Volume/Liquidity Ratio",
                score=10,
                description=f"Volume is {vol_liq_ratio:.0f}x liquidity — elevated pump risk",
                severity="moderate"
            ))
        elif vol_liq_ratio < 3:
            positive_signals.append(f"Healthy volume/liquidity ratio ({vol_liq_ratio:.1f}x)")

    # ─── FACTOR 4: MINT AUTHORITY ──────────────────────────────────────────────
    if mint_authority and mint_authority not in ("null", "None", "", "0" * 32):
        factors.append(RiskFactor(
            name="Mint Authority Active",
            score=35,
            description="Creator can print unlimited tokens and crash the price",
            severity="critical"
        ))
    elif mint_authority in (None, "null", "None", ""):
        positive_signals.append("Mint authority revoked — supply is fixed ✓")

    # ─── FACTOR 5: FREEZE AUTHORITY ───────────────────────────────────────────
    if freeze_authority and freeze_authority not in ("null", "None", "", "0" * 32):
        factors.append(RiskFactor(
            name="Freeze Authority Active",
            score=30,
            description="Creator can freeze all token accounts — investors could be locked out",
            severity="critical"
        ))
    elif freeze_authority in (None, "null", "None", ""):
        positive_signals.append("Freeze authority revoked — investors cannot be frozen ✓")

    # ─── FACTOR 6: HOLDER CONCENTRATION ───────────────────────────────────────
    if top_holder_pct > 0:
        if top_holder_pct > 50:
            factors.append(RiskFactor(
                name="Extreme Holder Concentration",
                score=30,
                description=f"Top holder owns {top_holder_pct:.1f}% — single entity controls the price",
                severity="critical"
            ))
        elif top_holder_pct > 30:
            factors.append(RiskFactor(
                name="High Holder Concentration",
                score=20,
                description=f"Top holder owns {top_holder_pct:.1f}% — significant manipulation risk",
                severity="major"
            ))
        elif top_holder_pct > 15:
            factors.append(RiskFactor(
                name="Elevated Holder Concentration",
                score=10,
                description=f"Top holder owns {top_holder_pct:.1f}% — worth monitoring",
                severity="moderate"
            ))
        elif top_holder_pct < 5:
            positive_signals.append(f"Well distributed — top holder only {top_holder_pct:.1f}% ✓")

    if top10_holder_pct > 80:
        factors.append(RiskFactor(
            name="Top 10 Holders Control 80%+",
            score=20,
            description=f"Top 10 wallets hold {top10_holder_pct:.1f}% — coordinated dump risk",
            severity="major"
        ))
    elif top10_holder_pct > 50:
        factors.append(RiskFactor(
            name="Top 10 Holders Control 50%+",
            score=10,
            description=f"Top 10 wallets hold {top10_holder_pct:.1f}% — concentrated supply",
            severity="moderate"
        ))

    # ─── FACTOR 7: PRICE CHANGE ANOMALY ───────────────────────────────────────
    if price_change_24h > 500:
        factors.append(RiskFactor(
            name="Extreme Price Pump",
            score=15,
            description=f"+{price_change_24h:.0f}% in 24h — likely coordinated pump before dump",
            severity="major"
        ))
    elif price_change_24h < -80:
        factors.append(RiskFactor(
            name="Severe Price Crash",
            score=10,
            description=f"{price_change_24h:.0f}% in 24h — possible rug already in progress",
            severity="major"
        ))

    # ─── CALCULATE TOTAL SCORE ─────────────────────────────────────────────────
    total_score = sum(f.score for f in factors)
    total_score = min(100, total_score)  # Cap at 100

    # Determine risk level
    if total_score >= 76:
        risk_level = "HIGH RISK"
    elif total_score >= 51:
        risk_level = "MEDIUM RISK"
    elif total_score >= 31:
        risk_level = "LOW CAUTION"
    else:
        risk_level = "LOW RISK"

    report.total_score = total_score
    report.risk_level = risk_level
    report.factors = factors
    report.positive_signals = positive_signals

    return report


def format_report(report: RiskReport) -> str:
    """Format a RiskReport for display."""
    lines = [
        f"{'─' * 60}",
        f"🔍 Token Analysis: {report.token_name} (${report.token_symbol})",
        f"📍 {report.token_address[:8]}...{report.token_address[-8:]}",
        f"",
        f"RISK SCORE: {report.total_score}/100 — {report.risk_level} {report.risk_emoji()}",
        f"",
    ]

    if report.factors:
        lines.append("⚠️  Risk Factors:")
        for f in sorted(report.factors, key=lambda x: x.score, reverse=True):
            severity_icon = {"critical": "🚨", "major": "⛔", "moderate": "⚠️", "info": "ℹ️"}.get(f.severity, "•")
            lines.append(f"   {severity_icon} [{f.score:+d} pts] {f.name}: {f.description}")
        lines.append("")

    if report.positive_signals:
        lines.append("✅ Positive Signals:")
        for signal in report.positive_signals:
            lines.append(f"   • {signal}")
        lines.append("")

    lines.extend([
        "📊 Token Stats:",
        f"   💧 Liquidity: ${report.liquidity_usd:,.2f}",
        f"   📈 24h Volume: ${report.volume_24h:,.2f}",
        f"   📅 Age: {report.age_hours:.1f} hours",
        f"   👥 Top Holder: {report.top_holder_pct:.1f}%",
        f"   🔒 Mint Authority: {'ACTIVE ⛔' if report.mint_authority else 'Revoked ✓'}",
        f"   ❄️  Freeze Authority: {'ACTIVE ⛔' if report.freeze_authority else 'Revoked ✓'}",
        "",
        f"VERDICT: {report.verdict()}",
        f"{'─' * 60}",
    ])

    return "\n".join(lines)


if __name__ == "__main__":
    # Test with sample data
    sample_token = {
        "baseToken": {
            "address": "So11111111111111111111111111111111111111112",
            "name": "Test Scam Token",
            "symbol": "SCAM",
        },
        "liquidity": {"usd": 3500},
        "volume": {"h24": 85000},
        "priceChange": {"h24": 320},
        "pairCreatedAt": None,
        "topHolderPct": 45,
        "top10HolderPct": 78,
        "mintAuthority": "9xSomeFakeMintAuth111111111111111111111111",
        "freezeAuthority": None,
    }

    report = score_token(sample_token)
    print(format_report(report))
