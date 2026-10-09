I've written the design, the plan and three phase 1 tickets; nothing is implemented. Phase 1 only fits your 6 hours if the work runs at the low end of the estimates. You weren't available, so every scope answer is an assumption and the design is marked **draft**.

**Files**
- `docs/architecture/hr-policy-qa.md`: the design and plan in one short file. It is 1,355 words against the skill's ~1,200 target.
- `docs/tickets/hr-policy-qa/G01.md`, `G02.md`, `G03.md`: one ticket per phase 1 goal. Each is 135–165 words, a bit over the ~120 target.
- `REPORT.md`: skills and references opened, the 10 questions I'd have asked with my assumed answers, checks, friction log and next prompt.

**Profile:** proof of concept. It's for you alone, demoed to HR leadership, works only on the published policy PDFs, and only reads them.

**Design in brief:** one ADK agent with one read-only tool.
- **Finding the right policy:** the agent's instructions contain a list of all ~30 documents (titles and headings with page numbers), and it pulls the pages it needs. This avoids building a search index, which wouldn't fit in 6 hours.
- **Answers:** every claim cites document and page. If the policies don't cover a question, it says so and points to HR rather than guessing.
- **Scanned pages:** a check before the demo lists any pages that couldn't be read, so they don't silently turn into a wrong "not covered" answer.
- **Model:** pinned to `gemini-3.8-flash`, taken from the skill's lifecycle table (checked 2026-10-08), not looked up online.
- **Spend:** a quota cap on the project, and each tool call returns a limited number of pages.

**Cut line:** I assumed you're new to ADK, so every estimate is multiplied by 1.5.

| Goal | What it delivers | Hours |
| --- | --- | --- |
| G01 | Text extracted from the PDFs, the unreadable-page report and the document list | 0.5–0.75 |
| G02 | The agent answering with citations in `adk web` (includes first-time key setup) | 1.75–3.25 |
| G03 | 10 checked questions and a demo dry run | 0.75–1.25 |
| **Total** | | **3.0–5.25** |

Your 6 hours at 0.8 focus, minus a 25% reserve, leaves 3.6 hours. If G02 runs long, G03 shrinks to just the five demo questions and the dry run. Phase 2, written into the plan, is a larger evaluation set (G04), a proper search tool if documents get missed (G05), and Cloud Run with sign-in for named HR staff (G06).

**Decisions still open:**
1. A company-billed, paid-tier Gemini API key or Vertex AI, and whether internal HR documents may be sent to that service.
2. Confirming the pinned model and the assumed ADK version (2.8.0) against what you actually install.
3. Accepting the cut line.
4. Whether any PDF contains employee personal data.

**Checks:** I hand-checked that the ticket estimates add up to the plan's totals, and counted words. The skill's schedule script wasn't run: the short-plan format says not to use it, and it needs Python 3.11 while 3.9.13 is installed. No `google.adk` tests ran (nothing is implemented and the package isn't installed). Nothing touched the network, cloud or package installs.

The next prompt, as the skill gives it for G01:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```