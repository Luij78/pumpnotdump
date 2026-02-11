# X Domination Suite 🚀

**Goal:** Build an AI-powered X (Twitter) growth engine that exceeds Creator Buddy

## Project Status
- **Started:** 2026-01-27
- **Updated:** 2026-01-28 06:00 AM
- **Owner:** Skipper for Luis (@luij78)

## Components

### 1. Algorithm Analyzer ✅ DONE
- Cloned `twitter/the-algorithm` — X's actual recommendation code
- Cloned `twitter/the-algorithm-ml` — ML models for ranking
- **FOUND THE WEIGHTS:** Replies 13.5x, Author reply-back 75x, Likes only 0.5x

### 2. Post Scorer ✅ DONE
- `post_scorer.py` — Scores posts 1-100 before posting
- Uses ACTUAL algorithm weights from source code
- Gives actionable suggestions to improve hooks
- **Usage:** `python3 post_scorer.py "Your tweet here"`

### 3. Hook Generator ✅ DONE  
- `hook_generator.py` — Generates viral hooks optimized for replies
- 8 hook styles: questions, fill-in-blank, hot takes, stories, challenges, etc.
- Industry-specific niches (realestate, crypto, ai, business, etc.)
- **Usage:** `python3 hook_generator.py --niche realestate -n 5`

### 4. Account Analyzer ✅ DONE
- `account_analyzer.py` — Analyze any X account's patterns
- Posting times, hook styles, engagement metrics
- Find what works for successful accounts
- **Usage:** `python3 account_analyzer.py @alexfinnai`
- **NEEDS:** bird CLI auth working to fetch tweets

### 5. Bird CLI Auth ⏳ NEEDS FRESH COOKIES
- Config exists at `~/.config/bird/config.json5`
- Current tokens appear expired (commands hang)
- **Need Luis to:** Log into X on Chrome, then refresh cookies

### 6. Reply Guy Assistant (Planned)
- Monitor key accounts
- Draft high-value replies
- Timing optimization

### 7. Engagement Predictor (Planned)
- Predict which followers will engage
- Optimal posting times
- Best hashtag/topic combinations

## Key Algorithm Insights

### Signals That Matter (from source code):
| Signal | Impact |
|--------|--------|
| Tweet Favorite (Like) | High - used as training label |
| Retweet | High - used as training label |
| Quote Tweet | High - used as training label |
| Tweet Reply | Medium - feature only |
| Tweet Click | Medium - used as label |
| Video Watch | Medium - used as label |
| Bookmark | Low |
| Share | Low |

### For You Timeline Composition:
- ~50% from accounts you follow (In-Network)
- ~50% from algorithm recommendations (Out-of-Network)

### Key Components:
- **TweepCred** — PageRank reputation score
- **SimClusters** — Community/interest groupings
- **Heavy Ranker** — Neural net that picks winners
- **Real-Graph** — User-to-user interaction predictions

## Resources
- X Algorithm: `./the-algorithm/`
- X ML Models: `./the-algorithm-ml/`
- Official blog: https://blog.x.com/engineering/en_us/topics/open-source/2023/twitter-recommendation-algorithm

## Next Steps
1. [ ] Analyze heavy ranker model weights
2. [ ] Build post scoring function
3. [ ] Connect to Luis's X account data
4. [ ] Create hook generator
5. [ ] Build Chrome extension for real-time scoring
