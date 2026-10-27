I wrote the design and plan and four phase 1 ticket files, and implemented nothing. I could not run `check_tickets.py` because this session has no shell tool. The tickets may have placeholder, skill-name or `docs` errors the checker would catch. The skills I named are `adk-memory-architecture`, `adk-engineer`, `adk-agent-evaluation` and `adk-presenter`. Only `adk-system-designer` is installed under this workspace's `.claude/skills`, and I left `docs:` empty in every ticket. From the project root, run:
`python3 .claude/skills/adk-system-designer/scripts/check_tickets.py --tickets docs/tickets/hr-policy-agent`

**Files**
- `docs/architecture/hr-policy-agent.md` is the design and plan in one file.
- `docs/tickets/hr-policy-agent/G01.md` to `G04.md` are the phase 1 tickets.

**Design**
- **Profile:** proof of concept, with config kept separate so phase 2 can build on it.
- **Retrieval:** local SQLite full-text search with one chunk per PDF page, so citations carry exact page numbers. It uses no cloud resources and no embeddings, so there is no idle cost and no teardown goal.
- **Agent:** one ADK agent with one read-only search tool. It cites document and page, and says so when the policies don't cover a question.

**Phase 1 goals**

| Goal | What it delivers | Hours |
| --- | --- | --- |
| G01 | Ingest and page-level search over the PDFs, with a coverage report that flags scanned files | 0.75–1.25 |
| G02 | The agent running in `adk web`, with a pinned model and a spend cap | 1.25–1.75 |
| G03 | About 10 labelled questions plus 3 out-of-scope ones run into a review table | 0.5–0.75 |
| G04 | Demo script, fallback screenshots and one rehearsal | 0.5–0.75 |

**Fit:** the total is 3.0–4.5 h against 6 h less a 25% reserve, so it fits at the high end with no slack beyond the reserve. I assumed work on Wed 28 and Thu 29 Oct, with the demo on Fri 30 Oct. If time runs short, cut in this order: G01, G02, G04, and shrink G03 to five questions read by eye before touching G04. Hours are added by hand, as the compact one-person form allows.

**Questions I couldn't ask, with the assumption I used** (all in the design)
- **Q1:** I assumed the PDFs are text, not scans. G01's coverage report will show which are not.
- **Q2:** I assumed policy text may be sent to the model provider. Please confirm this before G02's first live call.
- **Q3:** I assumed you already have a working model key and no new cloud resources are needed.
- **Q4:** I assumed a USD 10 spend cap, set on the model project. You need to set it in G02.
- **Q5:** I assumed one policy set, not different policies per country.

**Left undone**
- Citation checking only happens after the fact in G03. Nothing blocks a bad citation while the agent answers, so in the demo the model alone enforces it. I wrote that down as an accepted risk and made it phase 2 item P2-2.
- Phase 2 and the later list are outlined without tickets.
- The plan has not been independently reviewed, which is normal for a one-person proof of concept.
- I did not look up model IDs or ADK versions. G02 picks them from the lifecycle table in `adk-model-and-output-contracts`.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/hr-policy-agent/G01.md
```