#!/usr/bin/env python3
"""
X Account Analyzer - Analyze any X account's winning patterns

Uses the bird CLI to fetch account data and analyze:
- Posting frequency & timing
- Hook styles that work
- Engagement patterns
- Content themes

Usage:
    python account_analyzer.py @alexfinnai
    python account_analyzer.py @naval --deep
"""

import subprocess
import json
import re
import argparse
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Optional
import sys

# Import post scorer for analysis
try:
    from post_scorer import score_post
    HAS_SCORER = True
except ImportError:
    HAS_SCORER = False


def run_bird_command(args: List[str], timeout: int = 30) -> Optional[str]:
    """Run a bird CLI command and return output."""
    try:
        result = subprocess.run(
            ["bird"] + args + ["--json"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"⚠️ Bird command failed: {result.stderr}", file=sys.stderr)
            return None
    except subprocess.TimeoutExpired:
        print("⚠️ Command timed out", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("⚠️ bird CLI not found. Install with: npm install -g @steipete/bird", file=sys.stderr)
        return None


def fetch_user_tweets(handle: str, count: int = 50) -> Optional[List[Dict]]:
    """Fetch recent tweets from a user."""
    handle = handle.lstrip("@")
    output = run_bird_command(["user-tweets", f"@{handle}", "-n", str(count)])
    
    if not output:
        return None
    
    try:
        data = json.loads(output)
        return data if isinstance(data, list) else data.get("tweets", [])
    except json.JSONDecodeError:
        print(f"⚠️ Failed to parse tweets", file=sys.stderr)
        return None


def analyze_posting_times(tweets: List[Dict]) -> Dict:
    """Analyze when the account posts."""
    hours = Counter()
    days = Counter()
    
    for tweet in tweets:
        # Parse created_at timestamp
        created = tweet.get("created_at", "")
        if created:
            try:
                # Handle various date formats
                for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%a %b %d %H:%M:%S +0000 %Y"]:
                    try:
                        dt = datetime.strptime(created, fmt)
                        hours[dt.hour] += 1
                        days[dt.strftime("%A")] += 1
                        break
                    except ValueError:
                        continue
            except Exception:
                pass
    
    # Find peak times
    peak_hours = hours.most_common(3)
    peak_days = days.most_common(3)
    
    return {
        "peak_hours": [h for h, _ in peak_hours],
        "peak_days": [d for d, _ in peak_days],
        "hour_distribution": dict(hours),
        "day_distribution": dict(days)
    }


def analyze_content_style(tweets: List[Dict]) -> Dict:
    """Analyze content patterns and styles."""
    
    # Pattern counters
    has_question = 0
    has_thread = 0
    has_link = 0
    has_media = 0
    has_numbers = 0
    has_emoji = 0
    is_reply = 0
    is_quote = 0
    
    lengths = []
    
    for tweet in tweets:
        text = tweet.get("text", tweet.get("full_text", ""))
        
        if not text:
            continue
            
        lengths.append(len(text))
        
        # Content analysis
        if "?" in text:
            has_question += 1
        if re.search(r"^1/|🧵|\bthread\b", text, re.I):
            has_thread += 1
        if "http" in text:
            has_link += 1
        if tweet.get("media") or tweet.get("entities", {}).get("media"):
            has_media += 1
        if re.search(r"\d+", text):
            has_numbers += 1
        if re.search(r"[\U0001F300-\U0001F9FF]", text):
            has_emoji += 1
        if tweet.get("in_reply_to_status_id"):
            is_reply += 1
        if tweet.get("quoted_status") or tweet.get("is_quote_status"):
            is_quote += 1
    
    total = len(tweets) or 1
    
    return {
        "avg_length": sum(lengths) / len(lengths) if lengths else 0,
        "question_rate": has_question / total,
        "thread_rate": has_thread / total,
        "link_rate": has_link / total,
        "media_rate": has_media / total,
        "numbers_rate": has_numbers / total,
        "emoji_rate": has_emoji / total,
        "reply_rate": is_reply / total,
        "quote_rate": is_quote / total,
    }


def analyze_engagement(tweets: List[Dict]) -> Dict:
    """Analyze engagement metrics."""
    
    likes = []
    retweets = []
    replies = []
    
    top_tweets = []
    
    for tweet in tweets:
        like_count = tweet.get("favorite_count", tweet.get("public_metrics", {}).get("like_count", 0)) or 0
        rt_count = tweet.get("retweet_count", tweet.get("public_metrics", {}).get("retweet_count", 0)) or 0
        reply_count = tweet.get("reply_count", tweet.get("public_metrics", {}).get("reply_count", 0)) or 0
        
        likes.append(like_count)
        retweets.append(rt_count)
        replies.append(reply_count)
        
        # Score for top tweets (weighted by algorithm)
        score = (reply_count * 13.5) + (rt_count * 1.0) + (like_count * 0.5)
        
        top_tweets.append({
            "text": (tweet.get("text", tweet.get("full_text", ""))[:100] + "..."),
            "likes": like_count,
            "retweets": rt_count,
            "replies": reply_count,
            "algo_score": score
        })
    
    # Sort by algorithm score
    top_tweets.sort(key=lambda x: x["algo_score"], reverse=True)
    
    return {
        "avg_likes": sum(likes) / len(likes) if likes else 0,
        "avg_retweets": sum(retweets) / len(retweets) if retweets else 0,
        "avg_replies": sum(replies) / len(replies) if replies else 0,
        "max_likes": max(likes) if likes else 0,
        "max_retweets": max(retweets) if retweets else 0,
        "max_replies": max(replies) if replies else 0,
        "top_5_tweets": top_tweets[:5]
    }


def find_common_hooks(tweets: List[Dict]) -> List[str]:
    """Find common opening patterns in successful tweets."""
    
    openers = []
    
    for tweet in tweets:
        text = tweet.get("text", tweet.get("full_text", ""))
        if not text:
            continue
        
        # Get first line/sentence
        first_line = text.split("\n")[0][:50]
        
        # Categorize opener type
        text_lower = first_line.lower()
        
        if text_lower.startswith(("what", "who", "why", "how", "when", "where", "which")):
            openers.append("Question")
        elif "___" in text or "..." in text:
            openers.append("Fill-in-blank")
        elif any(w in text_lower for w in ["unpopular", "hot take", "controversial"]):
            openers.append("Hot take")
        elif any(w in text_lower for w in ["i just", "i recently", "today i"]):
            openers.append("Personal story")
        elif re.match(r"^\d+", text):
            openers.append("Number hook")
        elif text_lower.startswith(("the ", "this ")):
            openers.append("Declarative")
        elif "🧵" in text or "thread" in text_lower:
            openers.append("Thread")
        else:
            openers.append("Other")
    
    return Counter(openers).most_common(5)


def display_analysis(handle: str, analysis: Dict):
    """Display analysis results."""
    
    print("\n" + "=" * 60)
    print(f"📊 ACCOUNT ANALYSIS: @{handle}")
    print("=" * 60)
    
    # Posting times
    timing = analysis.get("timing", {})
    if timing:
        print("\n⏰ POSTING PATTERNS")
        print(f"   Peak hours: {timing.get('peak_hours', 'N/A')}")
        print(f"   Peak days: {timing.get('peak_days', 'N/A')}")
    
    # Content style
    style = analysis.get("style", {})
    if style:
        print("\n✍️ CONTENT STYLE")
        print(f"   Avg length: {style.get('avg_length', 0):.0f} chars")
        print(f"   Questions: {style.get('question_rate', 0)*100:.0f}% of posts")
        print(f"   Threads: {style.get('thread_rate', 0)*100:.0f}% of posts")
        print(f"   With links: {style.get('link_rate', 0)*100:.0f}% of posts")
        print(f"   With media: {style.get('media_rate', 0)*100:.0f}% of posts")
        print(f"   Using emojis: {style.get('emoji_rate', 0)*100:.0f}% of posts")
    
    # Engagement
    engagement = analysis.get("engagement", {})
    if engagement:
        print("\n📈 ENGAGEMENT AVERAGES")
        print(f"   Likes: {engagement.get('avg_likes', 0):.0f} (max: {engagement.get('max_likes', 0)})")
        print(f"   Retweets: {engagement.get('avg_retweets', 0):.0f} (max: {engagement.get('max_retweets', 0)})")
        print(f"   Replies: {engagement.get('avg_replies', 0):.0f} (max: {engagement.get('max_replies', 0)})")
    
    # Hook patterns
    hooks = analysis.get("hooks", [])
    if hooks:
        print("\n🎣 COMMON HOOK TYPES")
        for hook_type, count in hooks:
            print(f"   • {hook_type}: {count}")
    
    # Top tweets
    top = engagement.get("top_5_tweets", []) if engagement else []
    if top:
        print("\n🏆 TOP TWEETS (by algorithm score)")
        for i, tweet in enumerate(top[:3], 1):
            print(f"\n   {i}. {tweet['text']}")
            print(f"      💬 {tweet['replies']} replies | 🔁 {tweet['retweets']} RTs | ❤️ {tweet['likes']} likes")
    
    print("\n" + "=" * 60)
    print("💡 KEY INSIGHT: Copy their question rate & hook styles.")
    print("   The algorithm rewards replies 27x more than likes!")
    print("=" * 60 + "\n")


def analyze_account(handle: str, count: int = 50) -> Optional[Dict]:
    """Run full account analysis."""
    
    handle = handle.lstrip("@")
    print(f"📡 Fetching tweets from @{handle}...")
    
    tweets = fetch_user_tweets(handle, count)
    
    if not tweets:
        print(f"❌ Could not fetch tweets for @{handle}")
        print("   Make sure bird CLI is configured with X cookies.")
        return None
    
    print(f"✅ Got {len(tweets)} tweets. Analyzing...")
    
    analysis = {
        "handle": handle,
        "tweet_count": len(tweets),
        "timing": analyze_posting_times(tweets),
        "style": analyze_content_style(tweets),
        "engagement": analyze_engagement(tweets),
        "hooks": find_common_hooks(tweets)
    }
    
    return analysis


def main():
    parser = argparse.ArgumentParser(
        description="Analyze X account patterns for growth insights"
    )
    parser.add_argument("handle", help="X handle to analyze (e.g., @alexfinnai)")
    parser.add_argument("-n", "--count", type=int, default=50, help="Number of tweets to analyze")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--deep", action="store_true", help="Deep analysis (more tweets)")
    
    args = parser.parse_args()
    
    count = 100 if args.deep else args.count
    
    analysis = analyze_account(args.handle, count)
    
    if analysis:
        if args.json:
            print(json.dumps(analysis, indent=2))
        else:
            display_analysis(args.handle.lstrip("@"), analysis)


if __name__ == "__main__":
    main()
