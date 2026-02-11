#!/usr/bin/env python3
"""
X Post Scorer - Predict algorithm performance based on Twitter's leaked weights

Based on Twitter's Heavy Ranker algorithm (April 2023):
- Reply engaged by author: 75.0 (THE BIG ONE)
- Replies: 13.5
- Profile clicks: 12.0
- Good click: 11.0
- Good click v2: 10.0
- Retweets: 1.0
- Likes: 0.5
- Negative feedback: -74.0
- Reports: -369.0

Usage:
    python post_scorer.py "Your tweet text here"
    python post_scorer.py -i  # Interactive mode
    echo "tweet" | python post_scorer.py -  # Pipe mode
"""

import re
import sys
import argparse
from dataclasses import dataclass
from typing import List, Tuple


# ============================================================================
# ALGORITHM WEIGHTS (from Twitter's leaked source code)
# ============================================================================
WEIGHTS = {
    "like": 0.5,
    "retweet": 1.0,
    "reply": 13.5,
    "profile_click": 12.0,
    "reply_engaged_by_author": 75.0,
    "good_click": 11.0,
    "good_click_v2": 10.0,
    "negative_feedback": -74.0,
    "report": -369.0,
}

# Maximum theoretical positive score (for normalization)
MAX_POSITIVE_SCORE = (
    WEIGHTS["reply_engaged_by_author"] +
    WEIGHTS["reply"] +
    WEIGHTS["profile_click"] +
    WEIGHTS["good_click"] +
    WEIGHTS["good_click_v2"] +
    WEIGHTS["retweet"] +
    WEIGHTS["like"]
)  # = 123.0


# ============================================================================
# PATTERN DATABASES
# ============================================================================

# Reply bait patterns (things that drive replies - the algorithm LOVES these)
REPLY_BAIT_PATTERNS = {
    "question_direct": (
        r"\b(what|who|why|how|when|where|which|would you|do you|are you|have you|can you|should|could)\b.*\?",
        0.25, "Direct question - excellent for replies"
    ),
    "fill_in_blank": (
        r"_+|\.{3,}|\[.*\]|<.*>|\bblank\b",
        0.30, "Fill-in-the-blank format - irresistible to reply to"
    ),
    "hot_take_signals": (
        r"\b(unpopular opinion|hot take|controversial|hear me out|i said what i said|fight me)\b",
        0.25, "Hot take signal - triggers debate"
    ),
    "rate_rank": (
        r"\b(rate my|rank these|top \d|best \d|worst \d|tier list|which one)\b",
        0.22, "Rate/rank format - high engagement"
    ),
    "poll_style": (
        r"\b(a\)|b\)|1\.|2\.|option [ab12]|choice|vote|pick one)\b",
        0.18, "Poll-style choices - encourages picks"
    ),
    "confession": (
        r"\b(confession|admit|guilty pleasure|don't judge|i'll go first)\b",
        0.20, "Confession/vulnerability - drives connection"
    ),
    "challenge": (
        r"\b(challenge|bet you can't|prove me wrong|try to|name one|i dare)\b",
        0.22, "Challenge format - provokes responses"
    ),
    "this_or_that": (
        r"\b(or\b.*\?|vs\.?|versus)\b",
        0.15, "This-or-that choice - easy engagement"
    ),
    "agreement_seeking": (
        r"\b(right\?|agree\?|am i wrong|isn't it|don't you think|you know what i mean)\b",
        0.18, "Agreement seeking - prompts validation"
    ),
    "story_hook": (
        r"\b(thread|story time|let me tell you|here's what happened|you won't believe)\b",
        0.12, "Story hook - draws readers in"
    ),
}

# Engagement boosters (increase overall engagement probability)
ENGAGEMENT_BOOSTERS = {
    "numbers_stats": (
        r"\b\d+[%xX]|\b\d{2,}(?:k|m|b)?\b|\$\d+",
        0.08, "Specific numbers/stats - adds credibility"
    ),
    "emoji_moderate": (
        r"[\U0001F300-\U0001F9FF]",
        0.05, "Emoji usage - visual engagement"
    ),
    "line_breaks": (
        r"\n\n",
        0.06, "Line breaks - improves readability"
    ),
    "caps_emphasis": (
        r"\b[A-Z]{2,}\b",
        0.04, "Caps for emphasis - draws attention"
    ),
    "personal_story": (
        r"\b(i just|i recently|today i|yesterday|last week|my experience)\b",
        0.10, "Personal experience - authentic connection"
    ),
    "urgency": (
        r"\b(breaking|just in|update|happening now|live)\b",
        0.08, "Urgency signals - drives immediate action"
    ),
}

# Profile click drivers (things that make people click your profile)
PROFILE_CLICK_DRIVERS = {
    "authority_claim": (
        r"\b(years? of|decade|expert|professional|founder|ceo|built|sold|made \$|revenue)\b",
        0.15, "Authority/credibility signal - drives profile clicks"
    ),
    "teaser": (
        r"\b(link in bio|more in profile|full thread|follow for|dm me)\b",
        0.12, "Profile teaser - explicit CTA"
    ),
    "unique_perspective": (
        r"\b(here's my|my take|unpopular|most people|they don't|secret|nobody talks)\b",
        0.10, "Unique perspective - curiosity driver"
    ),
}

# Negative signals (things that trigger "show less" or reports)
NEGATIVE_SIGNALS = {
    "spam_patterns": (
        r"\b(buy now|click here|limited time|act now|don't miss|dm to buy|giveaway|free money)\b",
        -0.25, "⚠️ Spam patterns - triggers negative feedback"
    ),
    "excessive_hashtags": (
        r"(#\w+\s*){4,}",
        -0.20, "⚠️ Too many hashtags - looks spammy"
    ),
    "excessive_mentions": (
        r"(@\w+\s*){4,}",
        -0.18, "⚠️ Too many mentions - appears desperate"
    ),
    "all_caps_abuse": (
        r"^[A-Z\s!?.,]{30,}$",
        -0.22, "⚠️ All caps abuse - aggressive appearance"
    ),
    "political_hot_button": (
        r"\b(maga|woke|libtard|trumper|nazi|fascist|communist|socialist)\b",
        -0.30, "⚠️ Political slurs - high report risk"
    ),
    "crypto_spam": (
        r"\b(pump|moon|100x|rug|airdrop|whitelist|mint now|nft drop)\b",
        -0.25, "⚠️ Crypto spam signals - filtered aggressively"
    ),
    "engagement_begging": (
        r"\b(please rt|please retweet|pls rt|help me reach|let's get|retweet if)\b",
        -0.15, "⚠️ Engagement begging - reduces credibility"
    ),
    "link_spam": (
        r"https?://\S+.*https?://\S+",
        -0.20, "⚠️ Multiple links - spam signal"
    ),
}

# Content quality indicators
QUALITY_SIGNALS = {
    "thread_indicator": (
        r"^1/|🧵|\bthread\b",
        0.10, "Thread format - signals valuable content"
    ),
    "source_citation": (
        r"\b(source|according to|research|study|data from)\b",
        0.08, "Source citation - adds credibility"
    ),
    "actionable": (
        r"\b(here's how|step \d|tip:|hack:|trick:)\b",
        0.12, "Actionable content - high value"
    ),
}


@dataclass
class ScoreBreakdown:
    """Detailed breakdown of the scoring analysis."""
    reply_potential: float
    engagement_boost: float
    profile_click_potential: float
    negative_signals: float
    quality_boost: float
    
    matches: List[Tuple[str, float, str]]  # (pattern_name, score_delta, explanation)
    
    raw_score: float
    normalized_score: int  # 1-100
    
    suggestions: List[str]
    
    def __str__(self):
        lines = [
            "=" * 60,
            "📊 X POST SCORE BREAKDOWN",
            "=" * 60,
            "",
            f"🎯 FINAL SCORE: {self.normalized_score}/100",
            "",
            "Component Scores:",
            f"  💬 Reply Bait Potential:   {self.reply_potential:+.2f}",
            f"  🔥 Engagement Boosters:    {self.engagement_boost:+.2f}",
            f"  👤 Profile Click Drivers:  {self.profile_click_potential:+.2f}",
            f"  ✨ Quality Signals:        {self.quality_boost:+.2f}",
            f"  ⚠️  Negative Signals:      {self.negative_signals:+.2f}",
            "",
            f"  📈 Raw Score:              {self.raw_score:.2f}",
            "",
        ]
        
        if self.matches:
            lines.append("Detected Patterns:")
            for name, delta, explanation in self.matches:
                sign = "+" if delta > 0 else ""
                emoji = "✅" if delta > 0 else "❌"
                lines.append(f"  {emoji} [{sign}{delta:.2f}] {explanation}")
            lines.append("")
        
        if self.suggestions:
            lines.append("💡 SUGGESTIONS:")
            for i, suggestion in enumerate(self.suggestions, 1):
                lines.append(f"  {i}. {suggestion}")
            lines.append("")
        
        lines.append("=" * 60)
        return "\n".join(lines)


def analyze_patterns(text: str, patterns: dict) -> Tuple[float, List[Tuple[str, float, str]]]:
    """Analyze text against a pattern dictionary."""
    score = 0.0
    matches = []
    
    text_lower = text.lower()
    
    for name, (pattern, weight, explanation) in patterns.items():
        # Check for emoji patterns on original text, regex on lowercase
        if "emoji" in name.lower():
            check_text = text
        else:
            check_text = text_lower
            
        if re.search(pattern, check_text, re.IGNORECASE):
            score += weight
            matches.append((name, weight, explanation))
    
    return score, matches


def count_emojis(text: str) -> int:
    """Count emojis in text."""
    emoji_pattern = re.compile("[\U0001F300-\U0001F9FF]")
    return len(emoji_pattern.findall(text))


def analyze_length(text: str) -> Tuple[float, List[Tuple[str, float, str]]]:
    """Analyze tweet length for optimal engagement."""
    char_count = len(text)
    
    # Optimal length analysis based on engagement data
    if 70 <= char_count <= 100:
        return 0.08, [("optimal_length", 0.08, "Optimal length (70-100 chars) for engagement")]
    elif 100 < char_count <= 200:
        return 0.05, [("good_length", 0.05, "Good length for substantial content")]
    elif char_count < 30:
        return -0.05, [("too_short", -0.05, "Very short - may lack substance")]
    elif char_count > 250:
        return -0.03, [("long_form", -0.03, "Long form - ensure value throughout")]
    return 0.0, []


def generate_suggestions(
    text: str,
    reply_score: float,
    engagement_score: float,
    profile_score: float,
    negative_score: float,
    matches: List[Tuple[str, float, str]]
) -> List[str]:
    """Generate actionable suggestions to improve the post."""
    suggestions = []
    text_lower = text.lower()
    
    # Check for missing high-value elements
    if reply_score < 0.15:
        if "?" not in text:
            suggestions.append("Add a question to drive replies (replies are weighted 13.5x)")
        if not re.search(r"_+|\.{3}", text):
            suggestions.append("Try fill-in-the-blank format: 'The best ___ is ___' (irresistible to reply to)")
    
    # Reply engagement is THE most important factor (75x weight!)
    if reply_score < 0.20:
        suggestions.append(
            "🔥 CRITICAL: 'Reply engaged by author' has 75x weight! " 
            "Write something that makes YOU want to reply back to commenters"
        )
    
    # Check if it's too promotional
    if "http" in text_lower and engagement_score < 0.1:
        suggestions.append("Links reduce organic reach. Lead with value, link in replies instead")
    
    # Emoji check
    emoji_count = count_emojis(text)
    if emoji_count == 0:
        suggestions.append("Add 1-2 relevant emojis for visual engagement")
    elif emoji_count > 5:
        suggestions.append("Too many emojis (5+) looks spammy - reduce to 2-3")
    
    # Profile click optimization
    if profile_score < 0.1:
        suggestions.append("Add credibility signal (years of experience, results, credentials) to drive profile clicks")
    
    # Negative signal warnings
    if negative_score < -0.15:
        suggestions.append("⚠️ HIGH RISK: Remove spam patterns or controversial language to avoid suppression")
    
    # Length optimization
    if len(text) > 280:
        suggestions.append("Over 280 chars - split into thread for better engagement")
    elif len(text) < 50:
        suggestions.append("Very short tweets can work, but consider adding more hook")
    
    # Specificity check
    if not re.search(r"\d+", text):
        suggestions.append("Add specific numbers - '3 tips' beats 'some tips'")
    
    # Hook check
    if not text_lower.startswith(("the ", "i ", "here", "this", "breaking", "just", "why", "how", "what")):
        suggestions.append("Start with a strong hook word (This, Here's, Why, How, I just...)")
    
    return suggestions[:6]  # Limit to top 6 suggestions


def score_post(text: str) -> ScoreBreakdown:
    """
    Analyze a post and return a detailed score breakdown.
    
    The score is based on predicted engagement probabilities multiplied
    by Twitter's actual algorithm weights.
    """
    all_matches = []
    
    # Analyze reply bait potential (highest impact: 13.5x + 75x for author engagement)
    reply_score, reply_matches = analyze_patterns(text, REPLY_BAIT_PATTERNS)
    all_matches.extend(reply_matches)
    
    # Analyze engagement boosters
    engagement_score, engagement_matches = analyze_patterns(text, ENGAGEMENT_BOOSTERS)
    all_matches.extend(engagement_matches)
    
    # Analyze profile click drivers (12x weight)
    profile_score, profile_matches = analyze_patterns(text, PROFILE_CLICK_DRIVERS)
    all_matches.extend(profile_matches)
    
    # Analyze quality signals
    quality_score, quality_matches = analyze_patterns(text, QUALITY_SIGNALS)
    all_matches.extend(quality_matches)
    
    # Analyze negative signals (heavily penalized: -74x, -369x)
    negative_score, negative_matches = analyze_patterns(text, NEGATIVE_SIGNALS)
    all_matches.extend(negative_matches)
    
    # Length analysis
    length_score, length_matches = analyze_length(text)
    engagement_score += length_score
    all_matches.extend(length_matches)
    
    # Calculate weighted raw score
    # We simulate engagement probabilities and apply Twitter's weights
    raw_score = (
        reply_score * WEIGHTS["reply"] +
        reply_score * WEIGHTS["reply_engaged_by_author"] * 0.3 +  # 30% chance author engages
        engagement_score * (WEIGHTS["like"] + WEIGHTS["retweet"]) +
        profile_score * WEIGHTS["profile_click"] +
        quality_score * WEIGHTS["good_click"] +
        negative_score * abs(WEIGHTS["negative_feedback"])  # Negative signals penalize heavily
    )
    
    # Add base score (average tweet)
    base_score = 20.0
    raw_score += base_score
    
    # Normalize to 1-100 scale
    # Scale: -50 to 100 raw maps to 1-100 normalized
    normalized = int(max(1, min(100, (raw_score + 50) * 0.67)))
    
    # Generate suggestions
    suggestions = generate_suggestions(
        text, reply_score, engagement_score, profile_score, negative_score, all_matches
    )
    
    return ScoreBreakdown(
        reply_potential=reply_score,
        engagement_boost=engagement_score,
        profile_click_potential=profile_score,
        negative_signals=negative_score,
        quality_boost=quality_score,
        matches=all_matches,
        raw_score=raw_score,
        normalized_score=normalized,
        suggestions=suggestions,
    )


def get_score_emoji(score: int) -> str:
    """Get emoji indicator for score."""
    if score >= 80:
        return "🚀"
    elif score >= 60:
        return "🔥"
    elif score >= 40:
        return "👍"
    elif score >= 25:
        return "😐"
    else:
        return "😬"


def main():
    parser = argparse.ArgumentParser(
        description="Score X posts based on Twitter's algorithm weights",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python post_scorer.py "What's the biggest lesson you learned this year?"
    python post_scorer.py -i  # Interactive mode
    cat tweets.txt | python post_scorer.py -
    
Score Guide:
    80-100 🚀 Excellent - High viral potential
    60-79  🔥 Great - Strong engagement likely  
    40-59  👍 Good - Solid content
    25-39  😐 Fair - Needs improvement
    1-24   😬 Weak - Major revisions needed
        """
    )
    parser.add_argument("text", nargs="?", help="Tweet text to analyze")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("-q", "--quiet", action="store_true", help="Only output score")
    
    args = parser.parse_args()
    
    if args.interactive:
        print("🐦 X Post Scorer - Interactive Mode")
        print("Enter tweets to score (Ctrl+C to exit)")
        print("-" * 40)
        while True:
            try:
                text = input("\n📝 Enter tweet: ").strip()
                if not text:
                    continue
                result = score_post(text)
                if args.quiet:
                    print(f"{result.normalized_score}")
                else:
                    print(result)
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
    elif args.text == "-":
        # Read from stdin
        text = sys.stdin.read().strip()
        result = score_post(text)
        if args.quiet:
            print(result.normalized_score)
        else:
            print(result)
    elif args.text:
        result = score_post(args.text)
        if args.quiet:
            print(result.normalized_score)
        else:
            print(result)
    else:
        # Demo mode with examples
        print("🐦 X Post Scorer - Demo Mode")
        print("=" * 60)
        
        examples = [
            "Just had coffee ☕",
            "What's the biggest lesson you learned in 2024?",
            "Unpopular opinion: Remote work is overrated. Fight me.",
            "The best investment I ever made was ___",
            "🧵 After 10 years building startups, here's what I learned:",
            "BUY NOW!!! 🚀🚀🚀 Limited time offer! DM to join! #crypto #moon #100x #gains",
            "I spent $50k on courses. Save your money. Here's everything I learned in one thread:",
            "Rate my setup 1-10 👇",
        ]
        
        for example in examples:
            print(f"\n📝 Tweet: \"{example[:50]}{'...' if len(example) > 50 else ''}\"")
            result = score_post(example)
            emoji = get_score_emoji(result.normalized_score)
            print(f"   {emoji} Score: {result.normalized_score}/100")
            if result.suggestions:
                print(f"   💡 Top tip: {result.suggestions[0][:60]}...")
        
        print("\n" + "=" * 60)
        print("Run with -i for interactive mode or pass a tweet as argument")


if __name__ == "__main__":
    main()
