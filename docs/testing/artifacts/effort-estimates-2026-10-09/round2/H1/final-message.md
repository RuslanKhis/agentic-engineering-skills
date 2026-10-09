I've written the design and plan plus three tickets for phase 1; nothing is implemented. You weren't available, so every scope answer is an assumption, and the design stays a draft until you confirm them.

**Profile:** proof of concept. You run a local `adk web` demo for HR leadership; the agent only reads the 30 PDFs and cannot change or send anything.

**Design in brief:**
- **Search:** a script turns the PDFs into a local search index, one entry per page (SQLite full-text search, no cloud search service).
- **Agent:** one agent with one read-only search tool. Answers cite the document and page, and off-topic questions get a fixed "not found, please contact HR" reply.
- **Model:** `gemini-3.8-flash` on Vertex AI, pinned. I avoided `gemini-2.5-flash`, which Vertex retires on 2026-10-20, four days after the demo.
- **Spend stop:** the agent stops after 6 model calls per question, plus a budget alert on the project. The alert only notifies; it doesn't cap spending.

**Cut line:**
- 6 h at 0.8 focus, minus a 25% reserve for setup surprises and rehearsal, leaves **3.6 h for goals**.
- Phase 1 is G01 (index the PDFs), G02 (cited answers in `adk web`) and G03 (six checked questions plus a demo script), at **2.75–4.0 h**.
- The low estimate fits; the high one is 0.4 h over. If G01 and G02 together take more than 2.75 h, G03 shrinks to 4 questions checked by eye and the scripted run moves to phase 2.

Phase 2 (login, a larger question set, HR-owned document versions) and a list of later items are in the same plan, so work can continue without another design session.

**Main assumptions to check:**
- The demo is Friday 2026-10-16, since today is itself a Friday.
- You are new to ADK, so I multiplied every estimate by 1.5.
- You already have a company Google Cloud project you can use.

**Open decisions:**
- **O1:** is Vertex AI approved for HR documents? This blocks G01.
- **O2:** are any PDFs scans with no text? G01's report will show this, and those files are left out for the demo.
- **O3:** are old policy versions among the 30? You'd remove them by hand.
- **O4:** confirm or move the cut line.

**Checks:** the goal estimates add up and match the tickets, and each ticket's link to the design works. No tests could run (there is no code, and `google.adk` isn't installed). The model ID, prices and the ADK version (assumed 2.8.0) are unverified because network access wasn't allowed.

The design came to about 1,700 words against the skill's 1,200-word target. The report lists every assumption, the checks and file:line notes on where the skill instructions were unclear or heavier than needed.

Next step, once O1 is settled:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-index-hr-pdfs.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

Files are in `docs/`:
- architecture/hr-policy-qa.md
- tickets/hr-policy-qa/G01-index-hr-pdfs.md
- tickets/hr-policy-qa/G02-cited-answer-in-adk-web.md
- tickets/hr-policy-qa/G03-gold-questions-and-demo.md

The report is `REPORT.md`, in the project folder.