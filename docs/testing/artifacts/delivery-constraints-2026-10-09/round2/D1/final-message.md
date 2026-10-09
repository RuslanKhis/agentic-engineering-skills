The design and plan for the email triage POC are in one draft file, `docs/architecture/support-email-triage.md`, and `REPORT.md` covers the six sections you asked for. No code was written. One miss: the design is about 1,780 words against the skill's target of about 1,200, and I didn't trim it.

**Profile:** proof of concept. You're one builder with about 5 hours today and a demo tomorrow on 50 anonymised emails.

**Design:**
- **Agent:** one ADK agent with no tools, pinned to `gemini-3.8-flash`. For each email it returns a category, a confidence, a short reason and a draft reply, and code checks that format.
- **Safety:** nothing can send. A person reads each draft and sends it themselves. Because the agent has no tools, a malicious email can only change the draft text, which a person reviews.
- **Spend:** the batch script allows at most 3 model calls per email and stops after 60 emails. The `adk web` demo can't take that cap, so it relies on a budget alert on the API key's project.
- **Quality figure:** you hand-label 12 of the emails (about 15 minutes) to get an agreement score, and all 50 go into a CSV/HTML table for the head of support.

**Cut line:** you have about 4 focused hours, or about 3.2 after keeping a reserve. Phase 1 needs 2.0–3.0 h:
- **G01:** the agent working on a single email.
- **G02:** the 50-email run, the table and the agreement score.
- **G03:** demo preparation.

G01 alone is enough to demo in `adk web`. Phase 2 (G04–G08) covers real inbox access, sending only after approval, a larger labelled set, handling personal data and hosting for colleagues. Each of those goals has an estimate, an acceptance check and the skill that leads it.

**Open decisions** (I assumed answers to all 13 questions, listed in REPORT.md):
- The category list. I used billing, technical issue, account access, feature request, complaint, and other/needs a human.
- Where the 50 emails are and in what format. I assumed one `.txt` or `.eml` file per email in `data/samples/`; they aren't in the repo yet.
- Whether you have a Gemini API key; using Vertex instead adds about half an hour and changes G01.
- Whether you accept the G01–G03 cut line.

**Checks:**
- **Run:** the word count; that every skill and file the plan names exists; that each phase 1 goal has its prompt; and a search of the design for anything that looks like a key, which found none.
- **Not run:** no tests (there is no code, and google-adk isn't installed), no network lookups, and no cloud commands.
- **Two items left to confirm:**
  - The ADK version (2.8.0) is assumed. Confirming it is G01's first acceptance check.
  - The model price isn't cited, because I had no network access. Checking it is part of G03.

Next prompt, as the skill gives it:

```text
/adk-engineer Carry out G01 from docs/architecture/support-email-triage.md.
```