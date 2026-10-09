I've written the design, the plan and three tickets for phase 1. Nothing is implemented and nothing is committed. The schedule check passes, but no code or ADK tests were run, as you asked.

**Approach:** the agent reads a list of the 30 policies, opens one to three whole documents, and answers with *(Policy title, p. N)* citations. When the PDFs don't cover a question, it says "not covered, contact HR". There is no vector store; that waits for phase 2 if the collection grows past about 100 documents. It is one ADK agent with two read-only tools, run locally with `adk web`. The model is pinned to `gemini-3.8-flash`, which the bundled model list marks as stable.

**Capacity:** I treated this as a proof of concept with one builder. 6 h × 0.8 focus leaves 4.8 h. I kept 25% back for demo prep and the dry run, which leaves 3.6 h for the goals. Every estimate includes a ×1.5 allowance for being new to ADK.

**Cut line:** phase 1 is three goals totalling 2.3–3.6 h, so the high end exactly fills the 3.6 h:

| Goal | What it delivers | Hours |
| --- | --- | --- |
| G01 | PDFs extracted to per-page text, plus a list of documents | 0.5–0.8 |
| G02 | Answers with page citations | 1.0–1.5 |
| G03 | About 10 test questions you check by hand, and a recorded dry run as a fallback | 0.8–1.3 |

Phase 2 (G04–G07: hosting with login, a 30+ question test set, managed search) is written into the plan without tickets. If the work runs long, G03 shrinks to 5 questions typed into `adk web`.

**Schedule check:** the first run failed for two reasons. The G02 wait text differed between the plan and the ticket. And the one-day wait for data-use approval (O1) pushed the finish past your two days. It passes now only because I assumed you ask for that approval before you start. **So the first thing to do is ask whoever approves data use whether these PDFs may go to Gemini on your project.**

**Decisions still open:**
- **O1:** whether the policies may be sent to Gemini. This blocks only G02's live check.
- **O2:** whether any PDFs are scanned images. G01's report will tell you.
- **O3:** whether the agent may summarise policies or should only quote them. I assumed summarise with citations.

**Assumptions for you to check:** next Friday (16 Oct), since today is a Friday; you demo by screen share; the PDFs hold no personal data; under US$20 of model spend. All twelve, and the questions behind them, are in `REPORT.md`.

**Over target:** the design is about 1,700 words against the skill's target of about 1,200.

Next prompt to type:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-extract-corpus.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

Files are in `docs/architecture/`, `docs/tickets/hr-policy-qa/` and the project root:
- hr-policy-qa.md (design and plan)
- G01-extract-corpus.md
- G02-answer-with-citations.md
- G03-gold-questions-and-dry-run.md
- REPORT.md