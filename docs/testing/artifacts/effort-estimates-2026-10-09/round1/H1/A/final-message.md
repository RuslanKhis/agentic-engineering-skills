The design, plan and four phase 1 tickets are written. Nothing is implemented, and no tests importing `google.adk` were run because it isn't installed. Since you weren't available, every scoping answer is an assumption; they're listed at the top of the design and in `REPORT.md`.

**Saved files:**
- `docs/architecture/hr-policy-qa.md` holds the design and plan in one file, marked draft.
- `docs/tickets/hr-policy-qa/` has one ticket each for G01 to G04.
- `REPORT.md` has the six sections you asked for.

**Profile:** proof of concept. One person, a live demo, read-only access, internal policy documents. The agent has no tool that writes or sends anything, so text inside a PDF can't make it take an action.

**Design:** one ADK agent with one search tool. The 30 PDFs are split into sections (heading to heading, with page numbers) and stored in a local SQLite full-text index, built offline. The agent answers with a citation (document, section, page) or says the policies don't cover the question and to contact HR. The model is pinned to `gemini-3.8-flash`. It runs in `adk web` on your laptop, with a quota on the API key as the spend stop.

**Cut line:**

| Goal | What it delivers | Estimate |
| --- | --- | --- |
| G01 | PDFs become a searchable section index, with a report of unreadable pages | 0.75–1.25 h |
| G02 | Ask a question in `adk web`, get a cited answer or "not covered" | 1.25–1.75 h |
| G03 | 12 checked questions produce a results table for the demo | 0.75–1.0 h |
| G04 | Spend cap, version record and a rehearsal | 0.25 h |

That totals 3.0 to 4.25 hours. Your 6 hours give about 4.8 focused hours, or 3.6 after a 25% reserve, so only the low estimate fits. If G02 runs long (first-time ADK setup), G03 drops to 6 questions; the spend cap and the pinned model stay.

**After the demo:** phase 2 turns it into a pilot for HR staff (G05 to G09: hosting with company sign-in, a document approval process, 40+ reviewed questions in CI, keeping question text out of logs, cost logging). A later list covers the rest, each with what would bring it forward.

**Decisions still open:**
1. **Data approval:** is it allowed to send policy text to the Gemini API, or must it go through a company GCP project? This blocks the live part of G02 only.
2. **Model check:** confirm `gemini-3.8-flash` is still stable on Google's models page before G02. My source was a list dated 2026-10-08.
3. **Profile:** if HR wants staff using it within weeks, phase 2 becomes the main plan.
4. **Spend cap:** US$25 is assumed.

**Checks:**
- SQLite's full-text search works here.
- The bundled retrieval script that G01 adapts found every expected section on its sample data under Python 3.12. It fails with a syntax error on 3.11, even though its compatibility doc says 3.11+; that's logged as a skill defect in the report.
- All links, ticket headers and skill names in the new documents check out.
- The design is about 1,790 words against the ~1,200 target, which I left untrimmed.

Next step, for G01:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-section-index.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```