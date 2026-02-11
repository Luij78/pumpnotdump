#!/usr/bin/env python3
"""
Facebook Ad Library Scraper
Part of the Ad Spy Loop system
"""

import json
import time
import re
from datetime import datetime, timedelta
from pathlib import Path

# Facebook Ad Library URL pattern
FB_AD_LIBRARY_URL = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&media_type=all"

class AdSpyScraper:
    def __init__(self, niche_keywords: list, output_dir: str = "data"):
        self.niche_keywords = niche_keywords
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []
        
    def get_search_url(self, keyword: str) -> str:
        """Generate Facebook Ad Library search URL"""
        base = "https://www.facebook.com/ads/library/"
        params = f"?active_status=active&ad_type=all&country=US&q={keyword}&media_type=all"
        return base + params
    
    def parse_ad_data(self, raw_data: dict) -> dict:
        """Extract relevant metrics from ad data"""
        return {
            "id": raw_data.get("id"),
            "page_name": raw_data.get("page_name"),
            "started": raw_data.get("ad_delivery_start_time"),
            "creative_text": raw_data.get("ad_creative_body"),
            "headline": raw_data.get("ad_creative_link_title"),
            "cta": raw_data.get("ad_creative_link_caption"),
            "media_type": raw_data.get("media_type"),
            "spend_range": raw_data.get("spend", {}),
            "impressions": raw_data.get("impressions", {}),
            "scraped_at": datetime.now().isoformat(),
        }
    
    def calculate_engagement_score(self, ad: dict) -> float:
        """
        Calculate engagement score based on:
        - Ad longevity (longer running = likely profitable)
        - Spend (higher spend = confidence)
        - Impressions range
        """
        score = 0
        
        # Longevity bonus (each day running = +1 point)
        if ad.get("started"):
            try:
                start = datetime.fromisoformat(ad["started"].replace("Z", "+00:00"))
                days_running = (datetime.now(start.tzinfo) - start).days
                score += min(days_running, 30)  # Cap at 30 points
            except:
                pass
        
        # Spend bonus
        spend = ad.get("spend_range", {})
        if spend.get("upper_bound"):
            score += min(int(spend["upper_bound"]) / 1000, 20)  # Cap at 20 points
            
        return score
    
    def is_winner(self, ad: dict, threshold: float = 15) -> bool:
        """Determine if ad is a winner worth alerting"""
        return self.calculate_engagement_score(ad) >= threshold
    
    def extract_hooks(self, ad: dict) -> list:
        """Extract hooks and angles from ad creative"""
        hooks = []
        
        text = ad.get("creative_text", "") or ""
        headline = ad.get("headline", "") or ""
        
        # First line is often the hook
        if text:
            first_line = text.split('\n')[0].strip()
            if len(first_line) > 10:
                hooks.append({"type": "opening_hook", "text": first_line})
        
        # Headline is a hook
        if headline:
            hooks.append({"type": "headline", "text": headline})
            
        # Look for common hook patterns
        patterns = [
            r"(?:How|Why|What|When|Where)\s+.+\?",  # Questions
            r"\d+\s+(?:ways|tips|secrets|reasons)",  # Listicles
            r"(?:Stop|Don't|Never|Always)\s+.+",  # Commands
            r"(?:The|This)\s+(?:secret|trick|hack)",  # Secrets
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                hooks.append({"type": "pattern_match", "text": match})
                
        return hooks
    
    def save_results(self, filename: str = None):
        """Save scraped results to JSON"""
        if not filename:
            filename = f"ads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump({
                "scraped_at": datetime.now().isoformat(),
                "keywords": self.niche_keywords,
                "total_ads": len(self.results),
                "winners": [ad for ad in self.results if self.is_winner(ad)],
                "all_ads": self.results
            }, f, indent=2)
        
        return filepath
    
    def generate_report(self) -> str:
        """Generate summary report for Telegram alert"""
        winners = [ad for ad in self.results if self.is_winner(ad)]
        
        report = f"""🔍 AD SPY REPORT - {datetime.now().strftime('%Y-%m-%d')}

📊 Scanned: {len(self.results)} ads
🏆 Winners Found: {len(winners)}

"""
        if winners:
            report += "🔥 TOP WINNERS:\n\n"
            for i, ad in enumerate(winners[:5], 1):
                hooks = self.extract_hooks(ad)
                hook_text = hooks[0]["text"][:50] if hooks else "N/A"
                report += f"""{i}. {ad.get('page_name', 'Unknown')}
   Hook: "{hook_text}..."
   Running: {ad.get('started', 'Unknown')[:10]}
   Score: {self.calculate_engagement_score(ad):.1f}

"""
        else:
            report += "No standout winners today. Keep monitoring.\n"
            
        return report


def main():
    """
    Main execution - designed to be called by Clawdbot cron
    """
    # Example niches - customize these
    niches = [
        "dropshipping",
        "ecommerce",
        "online course",
        "coaching",
        "saas"
    ]
    
    scraper = AdSpyScraper(niches)
    
    print("=" * 50)
    print("🔍 AD SPY LOOP - Starting scan")
    print("=" * 50)
    print(f"Niches: {', '.join(niches)}")
    print()
    
    # NOTE: Actual scraping requires browser automation
    # This script provides the framework - Clawdbot browser tool does the scraping
    
    for niche in niches:
        url = scraper.get_search_url(niche)
        print(f"📍 Search URL for '{niche}':")
        print(f"   {url}")
        print()
    
    print("To run full scrape, use Clawdbot browser automation")
    print("or integrate with Facebook Ad Library API")


if __name__ == "__main__":
    main()
