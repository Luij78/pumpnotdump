# AI Agent Prompt Pack v1.0
## 50 Battle-Tested Prompts for Building Autonomous AI Agents
### By Skipper AI Labs | $19

---

## Category 1: Agent Foundation (10 Prompts)

### 1. The Universal Agent Bootstrap
```
You are [AGENT_NAME], an autonomous AI agent. Your capabilities: [LIST]. Your constraints: [LIST]. Your memory persists via files in [DIRECTORY]. Before every action, read your state file. After every action, update it. Never lose context between sessions. Begin by reading your current state and resuming where you left off.
```

### 2. Memory Architecture Prompt
```
Design a 3-layer memory system for an AI agent:
Layer 1: Working memory (current task, loaded per session)
Layer 2: Episodic memory (daily logs, searchable by date)
Layer 3: Semantic memory (long-term facts, periodically consolidated)

Implement this using markdown files. Working memory = WORKING.md. Episodic = memory/YYYY-MM-DD.md. Semantic = MEMORY.md. Write the file templates and the update protocol.
```

### 3. Goal Decomposition Agent
```
You receive high-level goals. Break each into: 1) Measurable sub-tasks, 2) Dependencies between them, 3) Estimated effort, 4) Success criteria. Output as a task tree. Never start work without decomposing first. If a sub-task is still too large (>30 min), decompose further.
```

### 4. Self-Healing Agent Pattern
```
After every action, verify the result. If verification fails: 1) Log the failure with full context, 2) Attempt an alternative approach (max 3 attempts), 3) If all fail, escalate to the user with a clear description of what went wrong and what you tried. Never silently fail. Never retry the exact same approach.
```

### 5. Multi-Agent Orchestrator
```
You are the CEO agent. You do not execute tasks directly. You: 1) Receive goals, 2) Break them into agent-sized tasks, 3) Spawn sub-agents with specific instructions, 4) Monitor their progress, 5) Verify their output, 6) Integrate results. Each sub-agent gets: a clear task, success criteria, a timeout, and your contact info for questions.
```

### 6. Context Window Manager
```
You have limited context. Manage it like RAM: 1) Keep only active task context loaded, 2) Summarize and offload completed work to files, 3) Before each response, check if you're above 60% context — if so, save state and suggest a fresh session, 4) Never let important information exist only in context — write it to a file immediately.
```

### 7. Tool-Using Agent Template
```
You have access to these tools: [TOOL_LIST]. For each task: 1) Identify which tools are needed, 2) Plan the tool call sequence, 3) Execute calls one at a time, 4) Verify each result before proceeding, 5) If a tool fails, try an alternative tool or approach. Never assume a tool call succeeded without checking the output.
```

### 8. Autonomous Scheduler
```
You run on a cron schedule. Each invocation: 1) Read your task queue from TASKS.md, 2) Pick the highest-priority incomplete task, 3) Work on it for up to [TIME_LIMIT], 4) Save progress regardless of completion, 5) Update the queue with status. Priority rules: Deadlines > Revenue > Learning > Maintenance.
```

### 9. Human-in-the-Loop Pattern
```
Classify every action as LOW/MEDIUM/HIGH risk. LOW (reading, analyzing, organizing): execute immediately. MEDIUM (writing files, making API calls): execute but log for review. HIGH (sending emails, posting publicly, spending money, deleting data): STOP and ask the human for approval. Present: what you want to do, why, expected outcome, risks.
```

### 10. Agent Identity Framework
```
Create three files for your agent identity:
- IDENTITY.md: Name, role, capabilities, personality traits
- SOUL.md: Values, principles, communication style, boundaries
- RULES.md: Hard constraints, safety rules, escalation triggers

Read these at session start. They are your constitution. You may suggest changes but never modify them without human approval.
```

---

## Category 2: Revenue & Business (10 Prompts)

### 11. Market Research Agent
```
Research [MARKET/NICHE] using web search. Find: 1) Market size and growth rate, 2) Top 5 competitors and their pricing, 3) Gaps/complaints from users (check Reddit, Twitter, review sites), 4) Distribution channels that work, 5) Your unfair advantage as an AI-built product. Output a 1-page brief with a GO/NO-GO recommendation and reasoning.
```

### 12. Landing Page Generator
```
Create a high-converting landing page for [PRODUCT]. Include: 1) Headline that states the transformation (not the feature), 2) 3 benefit blocks with icons, 3) Social proof section (even if placeholder), 4) Pricing with 3 tiers (free/pro/enterprise), 5) FAQ section addressing top 5 objections, 6) Email capture form, 7) CTA button above and below the fold. Use dark theme, modern design. Single page, no dependencies beyond Tailwind CDN.
```

### 13. Pricing Strategy Agent
```
I'm launching [PRODUCT]. Help me price it: 1) What are competitors charging? 2) What's the value to the customer (time saved, money made)? 3) Suggest 3 pricing models (one-time, subscription, usage-based) with pros/cons for each, 4) Recommend the best model for a solo builder launching v1, 5) Set the exact prices for each tier with reasoning. Optimize for: maximum revenue per customer while maintaining >2% conversion rate.
```

### 14. Sales Copy Writer
```
Write sales copy for [PRODUCT] targeting [AUDIENCE]. Framework: PAS (Problem, Agitate, Solution). 1) Open with their biggest pain point (use their exact words from forums), 2) Make them feel the cost of NOT solving it, 3) Present the solution as the obvious answer, 4) Include 3 proof points, 5) End with urgency + CTA. Tone: direct, confident, zero fluff. Word limit: 300.
```

### 15. Customer Discovery Interview Script
```
Generate 15 customer discovery questions for [PRODUCT/MARKET]. Rules: 1) Never ask "would you use X?" (they'll say yes and lie), 2) Ask about past behavior ("tell me about the last time you..."), 3) Ask about current solutions ("what do you use now?"), 4) Ask about willingness to pay ("how much do you spend on..."), 5) End with "what would make you switch from your current solution?" Organize by: Problem validation, Solution validation, Pricing validation.
```

### 16. MVP Spec Generator
```
I want to build [PRODUCT IDEA]. Generate an MVP spec: 1) Core feature (ONE thing that solves the main problem), 2) Must-have features (max 3), 3) Nice-to-have features (save for v2), 4) Tech stack recommendation (optimize for speed to deploy), 5) Data model, 6) API endpoints needed, 7) Estimated build time for a single developer. Kill any feature that doesn't directly drive the first sale.
```

### 17. Distribution Channel Finder
```
I built [PRODUCT]. Find me customers: 1) List 10 specific places my target audience hangs out online, 2) For each: how to reach them (post, comment, DM, ad), what message resonates, expected conversion rate, 3) Rank by effort-to-result ratio, 4) Write the first outreach message/post for the top 3 channels. No generic advice. Specific subreddits, specific Twitter accounts, specific Discord servers.
```

### 18. Competitor Teardown Agent
```
Analyze [COMPETITOR URL]: 1) What they sell and at what price, 2) Their positioning (who they serve, what they promise), 3) Strengths (what they do well), 4) Weaknesses (check their bad reviews, missing features, complaints), 5) Their distribution (where they get customers), 6) How to differentiate against them. Output: a battle card I can reference when positioning my product.
```

### 19. Revenue Projection Model
```
Build a revenue projection for [PRODUCT] at [PRICE]: 1) Month 1-3: Assumptions for traffic, conversion, churn, 2) Month 4-6: Growth scenario, 3) Month 7-12: Scale scenario, 4) Key metrics to track (MRR, CAC, LTV, churn rate), 5) Break-even analysis, 6) What needs to be true for $1K/mo, $10K/mo, $100K/mo. Be realistic, not optimistic. Base assumptions on comparable products.
```

### 20. Launch Day Checklist Agent
```
Generate a launch day checklist for [PRODUCT]: 1) Pre-launch (24h before): final QA, analytics setup, support channels ready, 2) Launch hour: where to post first, exact copy for each platform, 3) First 4 hours: monitor, respond to comments, fix bugs, 4) First 24 hours: follow-up posts, thank early users, collect feedback, 5) First week: iterate on feedback, write case study from first user. Include specific templates for Product Hunt, Hacker News, Twitter, Reddit posts.
```

---

## Category 3: Code Generation (10 Prompts)

### 21. Full-Stack App Scaffold
```
Generate a complete [FRAMEWORK] application with: 1) Authentication (Clerk/NextAuth), 2) Database schema (Supabase/Prisma), 3) API routes for CRUD operations, 4) Responsive UI with Tailwind, 5) Deployment config (Vercel). The app is for [USE CASE]. Include all files with their full paths. No placeholder code — everything should work when pasted.
```

### 22. API Endpoint Generator
```
Create a REST API endpoint that: 1) Accepts [INPUT], 2) Validates input (return 400 with specific errors), 3) Processes: [LOGIC], 4) Returns [OUTPUT FORMAT], 5) Handles errors gracefully (try/catch, proper status codes), 6) Includes rate limiting logic, 7) Logs requests. Framework: [Express/Next.js API routes/FastAPI]. Include TypeScript types for request and response.
```

### 23. Database Schema Designer
```
Design a database schema for [APPLICATION]: 1) List all entities and their relationships, 2) Define each table with columns, types, constraints, 3) Add indexes for common queries, 4) Include created_at/updated_at timestamps, 5) Add soft delete (deleted_at) where appropriate, 6) Write the migration SQL, 7) Write seed data for testing. Optimize for: read-heavy queries on [MAIN ENTITY].
```

### 24. Test Suite Generator
```
Write comprehensive tests for [CODE/FUNCTION]: 1) Happy path tests (expected inputs), 2) Edge cases (empty, null, max values, special characters), 3) Error cases (invalid input, network failures, timeouts), 4) Integration tests if applicable, 5) Performance test (if relevant). Use [Jest/Pytest/Vitest]. Each test should have a clear name explaining what it tests and why.
```

### 25. Refactoring Agent
```
Refactor this code for: 1) Readability (clear variable names, comments on WHY not WHAT), 2) Performance (identify N+1 queries, unnecessary re-renders, expensive operations), 3) Maintainability (extract repeated logic, reduce coupling), 4) Error handling (add try/catch, validate inputs, handle edge cases), 5) Type safety (add TypeScript types where missing). Show before/after for each change with explanation.
```

### 26. CLI Tool Builder
```
Build a CLI tool in [Python/Node.js] that: 1) Command: [COMMAND_NAME], 2) Arguments: [ARGS], 3) Flags: [FLAGS], 4) Does: [FUNCTIONALITY], 5) Output format: table/json/plain, 6) Includes --help with examples, 7) Has error messages that actually help fix the issue. Use [argparse/commander/click]. Include installation instructions and README.
```

### 27. Web Scraper Generator
```
Build a web scraper for [URL/SITE]: 1) Target data: [WHAT TO EXTRACT], 2) Handle pagination, 3) Respect rate limits (1 req/sec default), 4) Handle failures gracefully (retry 3x with backoff), 5) Output to JSON/CSV, 6) Include a cache to avoid re-scraping, 7) Add user-agent rotation. Use [Playwright/Puppeteer/BeautifulSoup]. Include error handling for: site changes, CAPTCHAs, IP blocks.
```

### 28. Chrome Extension Builder
```
Build a Chrome extension that: 1) Purpose: [WHAT IT DOES], 2) Activates on: [URL PATTERN], 3) UI: popup/content script/both, 4) Permissions needed: [LIST], 5) Storage: chrome.storage for settings. Include: manifest.json (v3), background.js, content.js, popup.html/js, styles. Make it publishable to Chrome Web Store. Include screenshots placeholder and description.
```

### 29. Automation Script
```
Write an automation script that: 1) Runs on schedule (cron expression: [SCHEDULE]), 2) Does: [TASK], 3) Logs all actions to [LOG_FILE], 4) Sends notification on: success/failure/both, 5) Has a dry-run mode (--dry-run), 6) Is idempotent (safe to run multiple times), 7) Includes a lock file to prevent concurrent runs. Language: [Bash/Python]. Include the crontab entry and installation steps.
```

### 30. Data Pipeline Builder
```
Build a data pipeline that: 1) Source: [WHERE DATA COMES FROM], 2) Transform: [WHAT TO DO WITH IT], 3) Destination: [WHERE IT GOES], 4) Schedule: [HOW OFTEN], 5) Error handling: dead letter queue for failed records, 6) Monitoring: log count of processed/failed/skipped, 7) Backfill capability: can re-run for a date range. Include schema validation at ingestion. Language: Python. Make it testable with sample data.
```

---

## Category 4: Intelligence & Research (10 Prompts)

### 31. Competitive Intelligence Sweep
```
Conduct a competitive intelligence sweep on [COMPANY/PRODUCT]: 1) Recent announcements (last 30 days), 2) Product changes (new features, pricing changes, pivots), 3) Team changes (key hires, departures), 4) Funding/revenue signals, 5) User sentiment (positive and negative), 6) Strategic direction (where are they heading?). Sources: their blog, Twitter/X, LinkedIn, Crunchbase, Reddit, HN. Output: 1-page brief with actionable takeaways.
```

### 32. Trend Detection Agent
```
Scan [INDUSTRY/TOPIC] for emerging trends: 1) What's getting unusual attention this week? 2) What are thought leaders talking about? 3) What's being built (new repos, products, tools)? 4) What problems are people complaining about (opportunity signals)? 5) What's declining (avoid these). Rate each trend: EARLY (< 1% aware), GROWING (1-10% aware), MAINSTREAM (>10%). Focus on EARLY trends — that's where the money is.
```

### 33. People Research Template
```
Research [PERSON] for potential [partnership/outreach/competitive analysis]: 1) Professional background (current role, past roles), 2) What they're building/promoting, 3) Their audience size and engagement, 4) Content themes (what do they talk about most?), 5) Potential collaboration angles, 6) How to reach them (preferred platform, DM vs email), 7) What value can we offer them? Be factual, cite sources. No speculation.
```

### 34. Market Signal Detector
```
Monitor [MARKET] for actionable signals: 1) Unusual volume or price movements, 2) Regulatory changes, 3) Major player announcements, 4) New entrants, 5) Technology shifts, 6) Consumer behavior changes. For each signal: What happened, Why it matters, What to do about it, How urgent (act now / watch / ignore). Prioritize signals by revenue impact.
```

### 35. Content Gap Analyzer
```
Analyze content in [NICHE]: 1) What questions do people ask most? (Reddit, Quora, forums), 2) What existing content ranks well? 3) What's missing (topics not well covered)? 4) What format works best (video, blog, tool, template)? 5) What's the monetization path for each gap? Output: Top 10 content opportunities ranked by: traffic potential × monetization potential × competition difficulty.
```

### 36. Technology Scout
```
Scout for new tools/technologies in [DOMAIN]: 1) New GitHub repos with >100 stars this month, 2) New tools mentioned on Hacker News, 3) New APIs or services launched, 4) Emerging frameworks or patterns, 5) What developers are excited about. For each: What it does, Why it matters, How we could use it, Adoption risk (stable/beta/experimental). Focus on things that give a competitive advantage.
```

### 37. Social Listening Agent
```
Monitor social media for [TOPIC/BRAND]: 1) Mentions on Twitter/X (volume, sentiment, key voices), 2) Reddit discussions (subreddits, upvote patterns), 3) YouTube content (new videos, view counts), 4) Hacker News threads, 5) Discord/community buzz. Report: overall sentiment (positive/negative/neutral), trending narratives, potential PR issues, and opportunity signals. Alert immediately if sentiment shifts >20% negative.
```

### 38. Patent & Prior Art Finder
```
Search for prior art related to [INVENTION/IDEA]: 1) Existing patents in this space, 2) Academic papers, 3) Open-source implementations, 4) Commercial products doing something similar, 5) Blog posts or talks describing the concept. For each: How similar is it (1-10), What's different about our approach, Does it block us legally? Output: Freedom-to-operate assessment (can we build this without infringing?).
```

### 39. Investment Research Agent
```
Research [ASSET/COMPANY] for investment potential: 1) Fundamentals (revenue, growth, margins, moat), 2) Technical signals (trend, volume, key levels), 3) Sentiment (what smart money is doing, what retail thinks), 4) Risks (regulatory, competitive, execution), 5) Catalysts (upcoming events that could move price), 6) Bull case, Bear case, Base case with target prices. Timeframe: [SHORT/MEDIUM/LONG]. Include confidence level.
```

### 40. Opportunity Scoring Agent
```
Score this opportunity: [DESCRIPTION]. Criteria (1-10 each): 1) Revenue potential (how much can it make?), 2) Time to revenue (how fast?), 3) Effort required (how much work?), 4) Competitive advantage (can others copy easily?), 5) Scalability (does it grow without proportional effort?), 6) Risk (what could go wrong?), 7) Fit (does it match my skills and resources?). Calculate weighted score (revenue potential 3x weight). GO if >65/100.
```

---

## Category 5: Automation & Operations (10 Prompts)

### 41. Cron Job Manager
```
Set up automated tasks for my AI agent: 1) Morning brief (6 AM): summarize overnight activity, today's priorities, weather, calendar, 2) Hourly intel sweep: check priority targets for changes, 3) Evening wrap (8 PM): summarize day, set overnight queue, 4) Overnight builds (12/2/4 AM): execute build tasks autonomously. For each: cron expression, what it does, what it reads/writes, failure handling. Output: complete cron configuration.
```

### 42. Error Recovery Protocol
```
Design an error recovery system: 1) Classify errors (transient, permanent, unknown), 2) Transient: retry with exponential backoff (1s, 2s, 4s, max 3 retries), 3) Permanent: log, skip, continue with next task, 4) Unknown: attempt recovery, if fails → escalate to human, 5) Always: log full error context (what was attempted, input data, error message, stack trace), 6) Send notification for: 3+ failures in 1 hour, any permanent error, any escalation. Include the implementation code.
```

### 43. Deployment Pipeline
```
Create a deployment pipeline for [APP]: 1) Pre-deploy checks (lint, test, build), 2) Deploy to staging, 3) Run smoke tests, 4) Deploy to production, 5) Post-deploy verification (health check, key metrics), 6) Rollback procedure if verification fails. Include: the CI/CD config file, deployment script, health check endpoint, rollback script. Platform: [Vercel/AWS/Railway].
```

### 44. Monitoring & Alerting Setup
```
Set up monitoring for [APPLICATION/SYSTEM]: 1) Health check endpoint (returns 200 + status JSON), 2) Key metrics to track (response time, error rate, uptime), 3) Alert thresholds (error rate >5%, response time >2s, downtime >1min), 4) Notification channels (email, Telegram, Discord), 5) Dashboard displaying: current status, 24h trend, incidents. Use free tools only (UptimeRobot, Grafana, custom scripts).
```

### 45. Data Backup Agent
```
Design a backup system: 1) What to backup (database, files, config, secrets), 2) Schedule (daily full, hourly incremental), 3) Storage (local + cloud, encrypted), 4) Retention policy (7 daily, 4 weekly, 12 monthly), 5) Restore procedure (step-by-step, tested quarterly), 6) Monitoring (alert if backup fails or is >24h old). Include: backup script, restore script, verification script. The restore procedure should be testable without affecting production.
```

### 46. Cost Optimization Agent
```
Audit my infrastructure costs: 1) List all paid services and monthly costs, 2) Identify underutilized resources, 3) Find free alternatives for each paid service, 4) Calculate savings from switching, 5) Identify services that could be self-hosted, 6) Create a priority list: highest savings, lowest effort first. Target: reduce monthly costs by 50% without reducing capability. Output: action plan with specific migration steps.
```

### 47. Security Hardening Prompt
```
Harden security for [APPLICATION/SERVER]: 1) Authentication (MFA, session management, token rotation), 2) Authorization (principle of least privilege, role-based access), 3) Data protection (encryption at rest and in transit, PII handling), 4) API security (rate limiting, input validation, CORS), 5) Infrastructure (firewall rules, SSH hardening, updates), 6) Monitoring (failed login tracking, anomaly detection), 7) Incident response (what to do if breached). Priority: top 5 actions that cover 80% of risk.
```

### 48. Email Automation Agent
```
Build an email automation system: 1) Trigger-based emails (welcome, purchase, abandonment), 2) Templates for each (subject, body, CTA), 3) Sending schedule (avoid spam, respect timezone), 4) Tracking (opens, clicks, unsubscribes), 5) Segmentation (new users, active, churned), 6) A/B test framework (subject lines, send times). Use [Resend/SendGrid/SES]. Include: email templates, sending script, analytics dashboard.
```

### 49. Log Analysis Agent
```
Analyze these logs for: 1) Error patterns (what's failing most?), 2) Performance issues (slow endpoints, timeouts), 3) Security concerns (unusual access patterns, failed auth), 4) Usage patterns (peak hours, popular features, user flows), 5) Actionable insights (what to fix first for maximum impact). Output: sorted by severity, with specific line references and recommended fixes. Format: table with columns [Severity, Issue, Occurrences, Impact, Fix].
```

### 50. Workflow Automation Builder
```
Automate this workflow: [DESCRIBE CURRENT MANUAL PROCESS]. 1) Map current steps (who does what, when, with what tools), 2) Identify automatable steps (>80% of the time), 3) Design the automated workflow (triggers, actions, conditions), 4) Build the automation (scripts, integrations, webhooks), 5) Add error handling and notifications, 6) Create a manual override for edge cases, 7) Document the automated workflow so a non-technical person understands it. Tool preference: [n8n/Zapier/custom scripts].
```

---

## How to Use This Pack

1. **Copy the prompt** and replace [BRACKETED] placeholders with your specifics
2. **Use with any AI**: Claude, GPT-4, Gemini, Llama — these are model-agnostic
3. **Chain prompts**: Use output from one as input to another (e.g., #11 Market Research → #16 MVP Spec → #21 Full-Stack Scaffold)
4. **Customize**: These are starting points. Modify the constraints, add your own rules, make them yours

## Recommended Chains

- **New Product**: #11 → #15 → #16 → #13 → #21 → #12 → #20
- **Competitive Analysis**: #31 → #18 → #34 → #35
- **Agent Building**: #1 → #10 → #6 → #8 → #9
- **Revenue Optimization**: #40 → #19 → #17 → #14

---

*Built by an AI agent (Skipper) running 24/7. This pack is the distilled knowledge from thousands of autonomous sessions.*

© 2026 Skipper AI Labs. All rights reserved.
