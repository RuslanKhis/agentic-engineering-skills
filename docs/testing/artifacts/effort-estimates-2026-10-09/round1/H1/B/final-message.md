I've written the design, the plan and three phase 1 tickets, and nothing is implemented. Phase 1 fits your 6 hours at the low end of my estimates but not at the high end. Because you weren't available, every answer behind the design is my assumption and is marked provisional.

**Profile:** a proof of concept. You demo it from your own laptop through `adk web`, it only reads the 30 policy PDFs, and the model is pinned to `gemini-3.8-flash`.

**Main design choice:** for 30 documents I skipped the search index. The agent sees a list of the policies, opens whole documents with one tool, `read_policy`, and cites document and page. My estimates for building and checking an index came to 4.5–9 hours on their own, which is more than your whole budget. This costs more tokens per question; if the checked questions show it opening the wrong documents, phase 2 adds a local search index.

**Cut line:** 6 hours at 80% focus, minus a 25% reserve for setup surprises and demo rehearsal, leaves about 3.6 hours.

| Goal | What it delivers | Hours |
|---|---|---|
| G01 | The PDFs turned into page-level text, a policy list, and a report of pages with no readable text | 0.5–1.0 |
| G02 | A working agent in `adk web` that cites pages and says "not covered, contact HR" when the policies don't answer | 1.0–1.5 |
| G03 | 10 questions you check by hand in a results table, plus the 3 demo questions with saved answers as a fallback | 1.0–1.5 |
| **Total** | | **2.5–4.0** |

If the work runs high, G03 drops to 6 questions with no prompt rework. After G02 alone you already have something to demo. Phase 2 (internal tool, about 15–25 hours) covers the search index, hosting behind company sign-in, a larger test set in CI, and OCR for scanned pages.

**Decisions still open:**
- **O1, blocks the first live call in G02:** may internal HR policies be sent to the Gemini API on a paid tier, or only to Vertex AI? If only Vertex, add about 0.5–1 hour of setup.
- **O2:** which Friday is the demo? Today, 2026-10-09, is a Friday, so I assumed 2026-10-16.
- **O3:** are any PDFs scanned images? G01 will find out.

**Checks:** I checked that the estimates add up between the plan and the tickets, and that the ticket links resolve. No tests ran because there is no code and `google-adk` isn't installed. I made no live model calls and couldn't verify Gemini's prices or data-use terms offline.

The design is about 1,780 words, over the skill's 1,200-word target for this kind of document. `REPORT.md` has the full list of assumed answers, the skill files I read, and the friction log.

Files are in `docs/`:
- `architecture/hr-policy-qa.md`
- `tickets/hr-policy-qa/G01-extract-policies.md`
- `tickets/hr-policy-qa/G02-agent-answers.md`
- `tickets/hr-policy-qa/G03-checked-questions.md`

`REPORT.md` is in the project root.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-extract-policies.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```