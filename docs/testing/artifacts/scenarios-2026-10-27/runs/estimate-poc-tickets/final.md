I wrote the design and plan and three phase 1 ticket files, but I couldn't run `check_tickets.py`. Bash is disabled in this session. I read the checker's rules and fixed the problems I found by hand (one unfilled placeholder and one confusing sentence). Please run it yourself:

`python3 -I .claude/skills/adk-system-designer/scripts/check_tickets.py --tickets docs/tickets/hr-policy-agent`

**Files**
- `docs/architecture/hr-policy-agent.md` is a single compact file (marked draft) with the design and plan.
- `docs/tickets/hr-policy-agent/G01.md`, `G02.md` and `G03.md` are the phase 1 tickets. Nothing is implemented.

**Design**
- **Shape:** it's a proof of concept, one `LlmAgent` with one `search_policies` tool. The demo runs in `adk web` on loopback, screen-shared. Nothing is deployed.
- **Retrieval:** local BM25 search over page-sized units from the PDFs, with no embeddings or managed RAG. That means no cloud resources, no idle cost and no teardown goal. Answers cite document and page.
- **Contracts:** five, covering citations, read-only access to the corpus, an honest "not found", empty pages never read as "no policy", and a spend cap.

**Phase 1 cut line**

| Goal | What it delivers | Hours |
| --- | --- | --- |
| G01 | Page-level PDF extraction, an ingestion report and the search function | 1.25–1.75 |
| G02 | The agent in `adk web`, with the spend cap | 0.75–1.25 |
| G03 | Ten gold questions, a results table and a rehearsed demo script | 1.0–1.5 |
| Total | | 3.0–4.5 |

- **Fit:** the high end uses all of the 4.5 hours left after holding back 25% of your 6, so there is no slack beyond that reserve. I added the hours by hand, with a 1.5× multiplier for being new to ADK.
- **If it runs high:** cut the gold set from 10 to 6 questions first, then drop the cross-document question. The floor and the "not found" behaviour stay.
- **Schedule:** G01 and G02 on day 1, G03 on day 2.
- **Phase 2 and later:** hosting with sign-in, an HR-reviewed question set, better retrieval and OCR for scans are written in the plan but have no tickets.

**Assumptions (nobody could answer, all recorded in the design)**
1. The PDFs are text-based; scans are reported, not read.
2. Sending the policies to a hosted model is approved.
3. The work days are Wed 28 and Thu 29 Oct.
4. The documents contain no employee personal data.
5. Friday's demo is the only review.

**Left undone**
- The model ID isn't chosen. G01 picks one from Google's current lifecycle page and pins it.
- I didn't write a presentation ticket, because `adk-presenter` isn't installed; demo prep is inside G03.
- There was no independent plan review, which a single-person proof of concept skips.
- No dependencies were installed and no PDFs were inspected.

Next prompt:
```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G01.md.
```