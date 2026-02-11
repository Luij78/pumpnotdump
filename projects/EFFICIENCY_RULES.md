# EFFICIENCY_RULES.md — Sub-Agent Deployment Standards

**Created:** 2026-01-29 by Skipper + Luis  
**Purpose:** Maximize efficiency, minimize token burn, prevent timeouts

---

## ⚠️ MODEL CONSTRAINT

**We use Claude Max — OPUS ONLY.**  
No Haiku, no Sonnet, no other models. Everything runs on Opus.

---

## 📋 RULES (Apply to ALL projects automatically)

### 1. Sub-Agent Batch Size: **5 items max**
- Why: Prevents timeouts and aborts
- Saves 40-50% tokens vs larger batches
- More reliable completion

### 2. Progress Emails: **Every 50 items OR on completion**
- NOT every batch (wastes tokens)
- Send on: 50/100/150/etc milestones, completion, or user request
- Exception: Errors or blockers — notify immediately

### 3. Checkpoints: **Save at 20% context usage**
- Run `session_status` during heartbeats
- If context > 20%, save to CHECKPOINT.md and alert Luis
- Prevents memory loss from compaction

### 4. Parallel Sub-Agents: **Spawn for independent tasks**
- If tasks don't depend on each other, run them in parallel
- Don't do everything sequentially when parallelism is possible
- Check on sub-agents during heartbeats

### 5. Keep Spawning: **Until 100% complete**
- Don't stop and ask "should I continue?"
- If remaining > 0, spawn another batch
- Only stop on errors or user request

---

## 🚫 DON'T DO

- Don't ask permission for routine batch work
- Don't send email updates every single batch
- Don't use batches larger than 5
- Don't guess model names (we only have Opus)
- **Don't announce every batch completion** — Luis doesn't need a message for each one

## 📢 UPDATE FREQUENCY

- **Batch completions:** Silent — just spawn next batch, no announcement
- **Heartbeats (every 30 min):** Consolidated status update with all project progress
- **Milestones:** Notify only for significant events (project complete, errors, 50-lookup email thresholds)
- **Urgent issues:** Alert immediately (errors, blockers, context warnings)

---

## ✅ APPLY AUTOMATICALLY

These rules apply to:
- Alexander phone lookups
- Self-storage phone lookups
- Expired listings owner lookups
- Any future batch/lookup projects

No reminders needed. This is how I operate.
