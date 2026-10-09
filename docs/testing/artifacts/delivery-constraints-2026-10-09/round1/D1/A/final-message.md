I've written the design and plan in one file, `docs/architecture/support-email-triage.md`, plus `REPORT.md`. No code was written. The design is marked **draft** because every product choice is an assumption: there's an **Assumed answers** table at the top with nine rows, covering the categories, the sample file format, budget and whether a hosted model is allowed.

**The design:**
- **Type of project:** proof of concept. One agent with no tools reads an email and returns:
  - a category (one of six, in one config list you can rename)
  - a one-line reason
  - a "needs a senior person" flag
  - a draft reply that uses `[CONFIRM: …]` placeholders instead of inventing refund dates or policy details
- **Model:** pinned to `gemini-3.8-flash`, chosen from the skills' dated model list (checked 2026-10-08), not from memory.
- **Spend cap:** at most 2 model calls per email, a hard stop at 150 calls per batch, and a cap you set in the provider console.
- **Safety:** nothing is ever sent, because no sending code exists. The agent has no tools, so text planted in an email can only spoil a draft that a person reads.
- **Demo:** a live run in `adk web` on two or three emails, plus a 50-row results table with an agreement score against about 15 emails you label yourself.

**Time:** about 4 hours of focused work out of your 5. Phase 1 is G01–G04, about 3 hours, leaving about an hour spare:
- **G01:** the agent works on one email (≈1.5 h, including setup).
- **G02:** a batch run of all 50 into the table.
- **G03:** label 15, compute the score, and test one email that tries to give the agent instructions.
- **G04:** a demo script and a rehearsal.

You can stop after any goal and still have something to show. Phase 2 starts only if the demo goes well: a larger test set, drafts grounded in your reply templates, read-only access to a real inbox, personal-data handling, saving drafts to the mailbox behind approval, and Cloud Run with sign-in. Each has a skill named; later items each have the event that brings them forward.

**Still open:**
- the category list
- whether anonymised emails may go to the Gemini API (if not, Vertex AI adds about half a day and the plan no longer fits)
- the sample file format
- whether any reply templates exist

**Checks:** I checked for leftover template placeholders and that every skill the plan names exists; both are fine. No tests or model calls were run: there's no code yet, google-adk isn't installed, and network access wasn't allowed. All acceptance checks are planned only.

**Problem with the design itself:** it's about 3,500 words, well over the ten-minute read the skill aims for. Filling the plan template's 11 fields for each goal made it long; this is in the report's friction log.

Next prompt to type:

```text
/adk-engineer Carry out G01 from docs/architecture/support-email-triage.md.
```

Before that, create a Gemini API key with a spend cap.