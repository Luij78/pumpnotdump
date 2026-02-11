#!/usr/bin/env python3
"""
X Hook Generator - Generate viral hooks based on algorithm weights

Based on what X's algorithm rewards:
- Replies (13.5x) > Retweets (1.0x) > Likes (0.5x)
- Author engaging with replies = 75x multiplier
- Questions, fill-in-blanks, hot takes drive replies

Usage:
    python hook_generator.py                    # Random hooks
    python hook_generator.py --topic "AI"       # Topic-specific
    python hook_generator.py --style hot_take   # Specific style
    python hook_generator.py --niche realestate # Industry hooks
"""

import argparse
import random
from typing import List, Dict

# ============================================================================
# HOOK TEMPLATES BY STYLE (All designed to maximize REPLIES)
# ============================================================================

HOOK_TEMPLATES = {
    "question": [
        "What's the biggest {topic} mistake you made in {year}?",
        "If you could only give ONE piece of {topic} advice, what would it be?",
        "What's something about {topic} that most people get completely wrong?",
        "{topic} question: What would you do differently if starting over?",
        "Honest question: Is {topic} overrated or underrated right now?",
        "What's your most controversial {topic} opinion? 👇",
        "What {topic} lesson took you the longest to learn?",
        "Drop your best {topic} tip in one sentence:",
        "What {topic} advice do you wish you'd gotten earlier?",
        "Hot take time: What's dying in {topic}? What's rising?",
    ],
    
    "fill_in_blank": [
        "The best {topic} advice I ever got was: ___",
        "Most people think {topic} is about ___. It's actually about ___.",
        "If I had to restart in {topic}, I'd focus 100% on ___.",
        "The secret to {topic} that nobody talks about: ___",
        "{topic} in 2024: More ___, less ___.",
        "My biggest {topic} mistake: thinking ___ when I should have ___.",
        "The difference between good and great in {topic}: ___",
        "One {topic} habit that changed everything for me: ___",
        "{topic} tip that sounds wrong but works: ___",
        "The {topic} hill I'll die on: ___",
    ],
    
    "hot_take": [
        "Unpopular opinion: Most {topic} advice is completely backwards.",
        "Hot take: {topic} is about to change dramatically. Here's why:",
        "Controversial but true: The best {topic} people do the opposite of what's taught.",
        "I said what I said: {topic} 'best practices' are holding people back.",
        "This will upset some people, but {topic} needs to hear it:",
        "Hear me out: Everything you know about {topic} might be wrong.",
        "Unpopular {topic} opinion that I stand by 100%:",
        "The {topic} industry doesn't want you to know this:",
        "I'm gonna get hate for this {topic} take, but...",
        "Hot take: The {topic} game has completely changed. Most haven't noticed.",
    ],
    
    "story_hook": [
        "I spent 5 years getting {topic} completely wrong. Here's what changed:",
        "Story time: How I went from {topic} failure to success in 12 months.",
        "The {topic} moment that changed everything for me:",
        "I almost quit {topic}. Then this happened:",
        "3 years ago I knew nothing about {topic}. Now I:",
        "The {topic} lesson that cost me $___. Learn from my mistake:",
        "When I started in {topic}, everyone said I was crazy. They were right, but not how they thought.",
        "Plot twist: The {topic} advice I ignored became my biggest win.",
        "True story: I failed at {topic} 7 times before this clicked:",
        "The {topic} journey nobody talks about (thread):",
    ],
    
    "listicle": [
        "5 {topic} truths that took me years to accept:",
        "The 3 {topic} mistakes killing your results (I made all of them):",
        "7 {topic} lessons I learned the hard way:",
        "{topic} in 2024: 5 things that work, 5 that don't.",
        "3 {topic} skills that will never go out of style:",
        "The 4 {topic} books that actually changed how I think:",
        "5 {topic} myths that need to die:",
        "3 {topic} habits of the top 1%:",
        "7 {topic} red flags nobody warns you about:",
        "The 5 {topic} rules I break constantly (and why):",
    ],
    
    "challenge": [
        "Challenge: Describe your {topic} approach in 3 words. Go 👇",
        "I bet you can't name 3 {topic} mistakes you've made. Prove me wrong.",
        "Try to change my mind: {topic} is ___",
        "Name ONE {topic} thing you'd change if you could. Just one.",
        "Challenge accepted: Drop your worst {topic} take ever 👇",
        "Roast my {topic} strategy. I can take it.",
        "Unpopular {topic} opinion time. Drop yours, I'll drop mine.",
        "In 10 words or less: What does {topic} success look like to you?",
        "Quick: What's ONE {topic} thing you're doing this week?",
        "Rate your {topic} knowledge 1-10. Be honest.",
    ],
    
    "rate_rank": [
        "Rate this {topic} strategy 1-10:",
        "Rank these {topic} priorities: A) ___ B) ___ C) ___",
        "What's your {topic} tier list? S-tier to F-tier:",
        "Hot or not: This {topic} trend.",
        "{topic} debate: Which matters more? Reply with A or B.",
        "Rate my {topic} take 🔥 or 🗑️:",
        "Agree or disagree: {topic} statement. Vote below 👇",
        "Which {topic} approach wins? Pick one:",
        "Score this {topic} move: Genius or disaster?",
        "A/B test: Which {topic} angle resonates more?",
    ],
    
    "confession": [
        "Confession: I used to think {topic} was all about ___. I was so wrong.",
        "Guilty pleasure: My {topic} habit that everyone judges:",
        "I'll go first: My biggest {topic} insecurity is ___",
        "Truth time: The {topic} thing I'm secretly terrible at:",
        "Honest confession: {topic} still confuses me sometimes. Anyone else?",
        "Vulnerable moment: Here's where I'm struggling with {topic}:",
        "Don't judge: My {topic} guilty habit is ___",
        "Real talk: {topic} is harder than people make it look. Here's proof:",
        "Confession time: The {topic} thing I pretend to understand but don't:",
        "I'm going to admit something about {topic} that might shock you:",
    ],
}

# ============================================================================
# NICHE-SPECIFIC TOPICS
# ============================================================================

NICHE_TOPICS = {
    "realestate": [
        "real estate", "home buying", "property investing", "house flipping",
        "rental properties", "real estate deals", "the market", "listings",
        "open houses", "closing deals", "buyer's agents", "seller's markets"
    ],
    "crypto": [
        "crypto", "Bitcoin", "trading", "DeFi", "meme coins", "the market",
        "portfolio management", "token launches", "blockchain", "web3"
    ],
    "ai": [
        "AI", "automation", "ChatGPT", "AI agents", "machine learning",
        "prompting", "AI tools", "the AI revolution", "building with AI"
    ],
    "business": [
        "business", "startups", "entrepreneurship", "side hustles", "scaling",
        "marketing", "sales", "customer acquisition", "revenue", "growth"
    ],
    "creator": [
        "content creation", "building an audience", "monetization", "engagement",
        "the algorithm", "growing on X", "personal branding", "going viral"
    ],
    "finance": [
        "investing", "money", "wealth building", "passive income", "budgeting",
        "financial freedom", "portfolio allocation", "market timing"
    ],
    "tech": [
        "tech", "coding", "software", "building products", "shipping fast",
        "developer experience", "no-code", "automation", "SaaS"
    ],
}

# ============================================================================
# POWER WORDS (boost engagement)
# ============================================================================

POWER_WORDS = [
    "secret", "truth", "actually", "really", "biggest", "worst", "best",
    "most people", "nobody", "everyone", "controversial", "unpopular",
    "honest", "real", "brutal", "hard", "simple", "easy", "fast",
    "proven", "tested", "guaranteed", "finally", "discovered"
]

EMOJIS = ["👇", "🔥", "💡", "🚀", "💰", "📈", "⚡", "🎯", "✨", "👀", "🧵", "💪", "🏆"]


def generate_hook(
    style: str = None,
    topic: str = None,
    niche: str = None,
    add_emoji: bool = True
) -> Dict:
    """Generate a single hook."""
    
    # Pick style
    if style and style in HOOK_TEMPLATES:
        selected_style = style
    else:
        # Weight towards high-reply styles
        styles_weighted = (
            ["question"] * 3 +
            ["fill_in_blank"] * 3 +
            ["hot_take"] * 2 +
            ["challenge"] * 2 +
            ["confession"] * 2 +
            ["story_hook"] * 1 +
            ["listicle"] * 1 +
            ["rate_rank"] * 1
        )
        selected_style = random.choice(styles_weighted)
    
    # Pick topic
    if topic:
        selected_topic = topic
    elif niche and niche in NICHE_TOPICS:
        selected_topic = random.choice(NICHE_TOPICS[niche])
    else:
        # Generic topics
        selected_topic = random.choice([
            "this", "your field", "your industry", "what you do",
            "your work", "your craft", "building", "growth"
        ])
    
    # Pick template
    template = random.choice(HOOK_TEMPLATES[selected_style])
    
    # Fill in template
    year = random.choice(["2024", "2025", "this year", "last year"])
    hook = template.format(topic=selected_topic, year=year)
    
    # Add emoji
    if add_emoji and not any(e in hook for e in EMOJIS):
        if random.random() > 0.3:  # 70% chance
            emoji = random.choice(EMOJIS)
            if "?" in hook:
                hook = hook.replace("?", f"? {emoji}", 1)
            else:
                hook = f"{hook} {emoji}"
    
    return {
        "hook": hook,
        "style": selected_style,
        "topic": selected_topic,
        "reply_potential": "HIGH" if selected_style in ["question", "fill_in_blank", "challenge", "confession"] else "MEDIUM"
    }


def generate_hooks(
    count: int = 5,
    style: str = None,
    topic: str = None,
    niche: str = None
) -> List[Dict]:
    """Generate multiple hooks."""
    hooks = []
    seen = set()
    
    attempts = 0
    while len(hooks) < count and attempts < count * 3:
        hook_data = generate_hook(style=style, topic=topic, niche=niche)
        if hook_data["hook"] not in seen:
            seen.add(hook_data["hook"])
            hooks.append(hook_data)
        attempts += 1
    
    return hooks


def display_hooks(hooks: List[Dict], verbose: bool = False):
    """Display hooks nicely."""
    print("\n" + "=" * 60)
    print("🎣 GENERATED HOOKS (Optimized for X Algorithm)")
    print("=" * 60)
    
    for i, h in enumerate(hooks, 1):
        print(f"\n{i}. {h['hook']}")
        if verbose:
            print(f"   Style: {h['style']} | Reply Potential: {h['reply_potential']}")
    
    print("\n" + "-" * 60)
    print("💡 TIP: Reply potential is based on X's algorithm weights.")
    print("   Questions & fill-in-blanks drive the most replies (13.5x boost)")
    print("   When people reply, ALWAYS reply back (75x boost!)")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate viral X hooks based on algorithm insights"
    )
    parser.add_argument("-n", "--count", type=int, default=5, help="Number of hooks")
    parser.add_argument("-s", "--style", choices=list(HOOK_TEMPLATES.keys()), help="Hook style")
    parser.add_argument("-t", "--topic", help="Specific topic")
    parser.add_argument("--niche", choices=list(NICHE_TOPICS.keys()), help="Industry niche")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show style/potential info")
    parser.add_argument("--list-styles", action="store_true", help="List available styles")
    parser.add_argument("--list-niches", action="store_true", help="List available niches")
    
    args = parser.parse_args()
    
    if args.list_styles:
        print("\nAvailable styles:")
        for style in HOOK_TEMPLATES:
            print(f"  • {style}")
        return
    
    if args.list_niches:
        print("\nAvailable niches:")
        for niche in NICHE_TOPICS:
            print(f"  • {niche}")
        return
    
    hooks = generate_hooks(
        count=args.count,
        style=args.style,
        topic=args.topic,
        niche=args.niche
    )
    
    display_hooks(hooks, verbose=args.verbose)


if __name__ == "__main__":
    main()
