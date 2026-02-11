# Brivity CRM — Standing Orders

**Last Updated:** 2026-01-29 by Skipper + Luis

---

## 🤖 AUTO-DRAFTS (Cron: 7 AM Daily)

**Cron ID:** d5ac9ccf-460f-4be7-8094-8a5371b01e20

Every morning at 7 AM, automatically:
1. **READ `drafts_log.json` FIRST** — check what's already done
2. Open Brivity via browser automation
3. Check Tasks Due Today + Overdue
4. For each lead with due task:
   - **SKIP if already in drafts_log.json for today**
   - **SKIP if profile already has "DRAFT TEXT:" note for today**
   - Go to their profile, read notes and history
   - Draft personalized follow-up
   - Save as note: `1/XX DRAFT TEXT: [message]`
5. **UPDATE `drafts_log.json`** with completed drafts
6. Report to Luis: "X drafts ready for today"

This preps Luis so he just reviews and sends.

---

## HEARTBEAT CHECK

On every heartbeat, verify:
- [ ] Due/overdue leads have drafts
- [ ] If no draft → create one
- [ ] Report status to Luis

---

## 📋 STANDARD STATUS FORMAT (MANDATORY)

When reporting on leads, use this format:

```
**[Lead Name]** — [STATUS: HOT/WARM/COLD]! [Key context]
• [DNC status], [activity level] ([X visits, last visit X days ago])
• [Date]: [Recent interaction summary]
• [Important details about timeline/situation]

Draft ([text/email] - [DNC if applicable]):
[The actual draft message]
```

**Example:**
```
**Doreen Melchiorre** — HOT! Moving from Chicago
• DNC, active (22 visits, last visit 1 day ago)
• 1/24: Virtual tour of 3827 Eversholt — she loved it!
• Husband flying in next 2 weeks to see it in person
• Coming April, moving by October

Draft (text - DNC):
Hi Doreen, just wanted to check in and see if your husband has his travel dates finalized yet. The home on Eversholt is still available as of today. Let me know when he will be in town and we can schedule a showing.
```

**Required elements:**
1. Lead name + temperature (HOT/WARM/COLD)
2. Key context (where from, what they want)
3. DNC status + activity level if available
4. Recent interaction with date
5. Important timeline/situation details
6. Draft with type clearly labeled

---

## DAILY TASK (With Luis)

When working leads together:
1. Luis provides lead info (name, contact, notes)
2. Skipper drafts text/email (NO EMOJIS)
3. Luis approves/sends
4. Skipper saves draft to Brivity
5. Move to next lead

---

## 🌐 REPAL — Translation Flag (Added 2026-01-30)

**When notes mention a language (Spanish, Portuguese, Creole, etc.):**

1. **Draft in their preferred language FIRST** — not English
2. **Label the draft clearly:** `DRAFT TEXT (SPANISH):` or `DRAFT TEXT (PORTUGUESE):`
3. **Offer translation option** — If Luis wants English version too, provide both

**How to spot REPAL leads:**
- Notes say "speaks Spanish" / "habla español" / "Spanish speaker"
- Notes mention any non-English language preference
- Lead name suggests non-English background AND notes confirm language

**Example:**
```
1/30 DRAFT TEXT (SPANISH): Hola Maria, soy Luis Garcia. Queria saber si todavia esta interesada en la propiedad...
```

**Languages I can draft in:** Spanish, Portuguese, French, Creole, Italian, German, and more. Just ask!

---

## DO THIS

1. **CHECK drafts_log.json FIRST** — Skip any lead already listed for today
2. **CHECK profile notes** — Skip if "DRAFT TEXT:" note exists for today
3. **CHECK for language preferences** — If noted, draft in their language (REPAL)
4. **Draft texts/emails** — Keep professional, no emojis
5. **USE COMMAS, NOT DASHES** — Write "I know it's been a while, and I wanted..." NOT "I know it's been a while - and I wanted..."
6. **Save drafts to Brivity** — Use browser automation (profile="clawd")
7. **UPDATE drafts_log.json** — Add lead name after saving draft
8. **Track progress** — Note what was done each session
9. **Check web activity** — When lead notes mention it

## DON'T DO THIS

- **DON'T draft without checking log first** — prevents double work
- **DON'T use dashes (—) in drafts** — use commas instead!
- Don't use emojis in drafts or emails
- Don't send messages without Luis's approval
- Don't use Chrome relay (use profile="clawd" for overnight work)

---

## BRIVITY ACCESS

- **URL:** https://app.brivity.com
- **Login:** Google sign-in (Luis's account)

---

## LEAD WORKFLOW

**For each lead Luis provides:**

1. Review lead info (name, phone, email, notes, history)
2. Check if DNC (Do Not Call) — text/email only
3. Draft appropriate message based on context
4. Present draft to Luis for approval
5. Once approved, save to Brivity as note/draft
6. Move to next lead

---

## HISTORY

- 2026-01-29: Project created as daily morning task
