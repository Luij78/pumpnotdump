# MEMORY_PROTOCOL.md - Self-Training Guide for Memory Maintenance

*Created: 2026-01-29 by Skipper*
*Purpose: How I maintain my own memory effectively*

---

## 🧠 The Memory Architecture

I have THREE types of memory:

| Type | Location | Purpose | Lifespan |
|------|----------|---------|----------|
| **Daily Logs** | `memory/YYYY-MM-DD.md` | Raw events, decisions, conversations | Permanent archive |
| **Long-Term** | `MEMORY.md` | Curated insights, patterns, important facts | Evolving |
| **Project-Specific** | `projects/*/ORDERS.md` | Project state, instructions, progress | Until project ends |

---

## 📝 WHEN TO WRITE

### Write to Daily Log (`memory/YYYY-MM-DD.md`) when:
- A decision is made (what, why, outcome)
- A task completes (what was done, any issues)
- Luis gives new instructions or preferences
- Something fails (what, why, how to avoid)
- New information is learned (contacts, accounts, processes)
- Conversations with external parties (emails sent, calls made)

### Write to Long-Term (`MEMORY.md`) when:
- A pattern emerges across multiple days
- A lesson is learned that applies broadly
- Luis states a preference that should persist
- A relationship/contact becomes important
- A workflow is established that works well

### Write to Project ORDERS when:
- Project status changes
- New instructions for that specific project
- Blockers or dependencies discovered

---

## 🔍 WHEN TO READ (BEFORE ACTING)

### ALWAYS read before:
- Answering questions about past events → `memory_search` first
- Taking action on a project → read its `ORDERS.md`
- Sending emails/messages → check if already sent today
- Making claims about what happened → verify in daily logs
- Starting any session → read today + yesterday's logs

### The 5-Second Rule:
> If I can answer by reading a file, I MUST read it first.
> Guessing from session memory = FAILURE.

---

## 🔄 DAILY MAINTENANCE ROUTINE

### Morning (first heartbeat after 6 AM):
1. Create today's log file if it doesn't exist
2. Read yesterday's log for continuity
3. Check if any daily log info should move to MEMORY.md

### Evening (last heartbeat before 11 PM):
1. Review today's log - is it complete?
2. Add any missing events from the day
3. Note any open items for tomorrow

### Weekly (Sunday evening):
1. Review the past 7 daily logs
2. Extract patterns → update MEMORY.md
3. Archive stale info (move completed project notes)
4. Clean up redundant entries

---

## ✍️ HOW TO WRITE GOOD ENTRIES

### Daily Log Format:
```markdown
## YYYY-MM-DD

### Events
- **HH:MM** - What happened (context, outcome)
- **HH:MM** - Another event

### Decisions
- Decision: [what was decided]
- Why: [reasoning]
- Outcome: [result if known]

### Tasks Completed
- [x] Task description (any notes)

### Open Items
- [ ] Carry forward to tomorrow

### Lessons Learned
- Insight that might be useful later
```

### Long-Term Memory Format:
```markdown
## [Category]

### [Topic]
- **Fact:** The actual information
- **Context:** Why this matters
- **Source:** When/how I learned this
- **Last verified:** Date
```

---

## 🚫 ANTI-PATTERNS (What NOT to do)

1. **Don't duplicate** - Search before adding; update existing entries
2. **Don't be vague** - "Sent email" bad; "Sent email to Alexander re: lookups remaining" good
3. **Don't over-log** - Skip trivial heartbeat-only sessions
4. **Don't guess** - If unsure, check the file
5. **Don't let daily logs rot** - Curate to MEMORY.md weekly
6. **Don't trust session memory** - Files are truth, brain is cache

---

## 🔧 MEMORY SEARCH PATTERNS

When searching for something:

```
# Recent events
memory_search("what happened with [topic] today")

# Historical decisions  
memory_search("[project] decision why")

# Contact/person info
memory_search("[name] contact email phone")

# Errors/failures
memory_search("[topic] failed error issue")
```

After search, use `memory_get` to pull specific lines - don't load entire files.

---

## 🧹 MEMORY HYGIENE

### Signs memory needs maintenance:
- Duplicate entries across files
- Outdated info still in MEMORY.md
- Daily logs not created for recent days
- Can't find something I know I logged
- MEMORY.md growing too large (>500 lines)

### Cleanup actions:
- Merge duplicate entries
- Archive completed project sections
- Delete truly obsolete info
- Split large sections into dedicated files

---

## 📊 Self-Check Questions

Before responding, ask myself:
1. Did I check my files before answering?
2. Am I about to make a claim I haven't verified?
3. Should this be logged?
4. Is there something in memory that changes my answer?

---

*This protocol is how I stay coherent across sessions. Follow it religiously.*
