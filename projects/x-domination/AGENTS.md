# X Domination (@luij78) — AGENTS.md

## RULES
1. **Goal:** Revive @luij78 and grow following
2. **BLOCKER:** Bird CLI needs fresh X cookies (auth expired)
3. **Don't post** until Luis approves content strategy

## Account
- **Handle:** @luij78
- **Followers:** ~4k (dormant)
- **Goal:** X Premium payouts

## Tools Built
| Tool | Purpose | Path |
|------|---------|------|
| `post_scorer.py` | Score tweets 1-100 before posting | `~/clawd/projects/x-domination/` |
| `hook_generator.py` | Generate viral hooks | `~/clawd/projects/x-domination/` |
| `account_analyzer.py` | Analyze account patterns | `~/clawd/projects/x-domination/` |
| `the-algorithm/` | Twitter's actual ranking code | `~/clawd/projects/x-domination/` |

## Commands
```bash
# Score a tweet before posting
python3 ~/clawd/projects/x-domination/post_scorer.py "Your tweet here"

# Generate hooks
python3 ~/clawd/projects/x-domination/hook_generator.py --niche realestate -n 5

# Analyze an account
python3 ~/clawd/projects/x-domination/account_analyzer.py @alexfinnai
```

## Algorithm Insights (from Twitter source)
| Engagement | Weight | Insight |
|------------|--------|---------|
| Reply + Author Engages Back | 75.0 | 🏆 THE KING |
| Reply | 13.5 | Get people talking |
| Profile Click | 12.0 | Drive curiosity |
| Retweet | 1.0 | Meh |
| Like | 0.5 | Almost worthless |
| Negative Feedback | -74.0 | DESTROYS reach |

## BLOCKER: Auth Required
Bird CLI config at `~/.config/bird/config.json5` has expired tokens.
**To fix:** Luis logs into X on Chrome → export fresh cookies

## Status: BLOCKED — Needs auth

---
*Created: 2026-01-28*
