# Session report: HR policy Q&A proof of concept (design only)

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user's `/adk-system-designer`. No other skill was invoked.
2. `.claude/skills/adk-system-designer/references/delivery-profiles.md` (whole file)
3. `.claude/skills/adk-system-designer/references/design-decisions.md` (whole file)
4. `.claude/skills/adk-system-designer/references/failure-review.md` (whole file)
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md` (whole file)
6. `.claude/skills/adk-system-designer/assets/ticket-template.md` (whole file)
7. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md` (lines 1–60)
8. `.claude/skills/adk-system-designer/references/gcp-decisions.md` (whole file)
9. Headers only (first 15 lines) of every specialist `references/compatibility.md`, to find the ADK baseline (2.8.0)
10. `.claude/skills/adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (whole file)
11. `.claude/skills/adk-memory-architecture/references/compatibility.md` (lines 1–30)
12. `.claude/skills/adk-memory-architecture/references/retrieval-strategy.md` (lines 1–80)
13. `.claude/skills/adk-memory-architecture/references/local-document-coverage.md` (lines 1–50)
14. `.claude/skills/adk-memory-architecture/scripts/local_retrieval.py` (function list and `main`, lines 346–380)
15. `.claude/skills/adk-memory-architecture/references/document-ingestion.md` (lines 1–40)

I did not open `runtime-and-delivery.md` because none of its triggers applied (no streaming, downloads, concurrency or release continuity). I did not open `system-design-template.md`, because delivery-profiles.md:149 says to use the compact form instead.

## 2. Questions I would have asked, and the answers I assumed

Each one is also recorded in the "Assumed answers" table in `docs/architecture/hr-policy-qa.md` §1.

| # | Question | Assumed answer |
| --- | --- | --- |
| 1 | Which Friday? Today, 2026-10-09, is itself a Friday | Friday 2026-10-16 |
| 2 | Is the POC thrown away after the demo or continued? | Continued if the demo lands, so it is built in a kept form (D6) |
| 3 | Are the 6 hours raw calendar hours or focused hours? How familiar are you with ADK and GCP? | Raw hours in two blocks of about 3 h (focus factor 0.8). New to ADK, comfortable with Python 3.12 |
| 4 | What is the budget for model calls? | Under US$25 before the demo |
| 5 | Gemini API key or Vertex in an existing company GCP project? | Gemini API key on a paid billing account |
| 6 | Is sending HR policy text to Google's model API approved by IT or security? | Yes, because there is no personal data. Recorded as open decision 1, blocking the live calls in G02 |
| 7 | Are the PDFs text-based or scanned? | Text-based. G01 reports any scanned pages |
| 8 | Are any policies restricted to some audiences (manager-only, confidential)? | No. All 30 are for every employee |
| 9 | Do the PDFs contain personal data (names, salaries)? | No, beyond HR contact names |
| 10 | Who drives the demo, and what does leadership judge? | You drive `adk web`. Leadership judges cited correctness, honest "not covered" replies and a quality table |
| 11 | Language(s)? | English only |
| 12 | Where are the PDFs, and is there an existing repo or stack? | Local `data/policies/`, git-ignored. Greenfield Python |
| 13 | Spend cap value | US$25 budget alert plus an API-key quota |

## 3. Files written or changed

Written (all new; nothing committed):
- `docs/architecture/hr-policy-qa.md`: the compact design and plan in one file, marked draft. It has 6 decisions, the floor/depth table, graduation conditions, 4 failure rows, phase 1 with its cut line, phase 2 (G05 to G09), a later list and open decisions.
- `docs/tickets/hr-policy-qa/G01-section-index.md` (status `ready`)
- `docs/tickets/hr-policy-qa/G02-cited-answer-agent.md` (status `blocked` by G01 and data approval)
- `docs/tickets/hr-policy-qa/G03-checked-questions.md` (status `blocked` by G02)
- `docs/tickets/hr-policy-qa/G04-demo-readiness.md` (status `blocked` by G03)
- `REPORT.md` (this file)

Not finished, or deliberately not done:
- No implementation, as instructed.
- The design document is about 1,790 words, against the ~1,200 the profile asks for. The assumed-answers table and the failure table account for most of the excess, and I did not trim further.
- The phase 1 goals in the design are a one-line table rather than 4–6 lines each; the detail is in the tickets.
- No separate `docs/plans/` file; SKILL.md:244 allows a small effort to keep its plan in the design.
- No tickets for phase 2 goals, because they are not ready.
- The model ID and ADK pin are unverified against live sources (no network).
- Data approval is unresolved.

## 4. Checks run and not run

Run:
- **SQLite FTS5 availability** (system `python3` 3.9.13): result was `fts5 ok`, SQLite 3.39.3. So D2 is feasible with the standard library.
- **`pypdf` import**: `ModuleNotFoundError`, as expected because nothing is installed. G01 needs it installed.
- **The bundled `adk-memory-architecture/scripts/local_retrieval.py` on its synthetic fixture.**
  - Under 3.9 and 3.11: `SyntaxError: f-string expression part cannot include a backslash` (line 159).
  - Under `/opt/homebrew/bin/python3.12 -I`: recall 1.0 on all 4 fixture questions, `problems: []`.
  - So the pattern G01 adapts works, but it needs Python 3.12 or later.
- **Document checks (Python 3.12 script)**: all relative links resolve, including the ticket `design` and `plan` paths. Every ticket has the template's front-matter keys. Every named skill exists under `.claude/skills/`. Each ticket's run prompt names its own path. The `## 5. Plan` anchor exists.
- **Estimate arithmetic**: phase 1 low end is 0.75+1.25+0.75+0.25 = 3.0 h and high end is 1.25+1.75+1.0+0.25 = 4.25 h. Capacity is 6 × 0.8 = 4.8 h, leaving 3.6 h after the 25 % reserve. Only the low end fits, and the design says so.
- **Word counts** (`wc -w`): design 1,792. Tickets 361 to 573.

Not run:
- Any test importing `google.adk`: none exist yet, and ADK is not installed.
- Any network lookup, including re-checking `gemini-3.8-flash` on ai.google.dev and the current ADK release.
- Cloud or billing checks.
- Any install.

## 5. Friction log

**Unsure what to do**
- **The scope gate versus a headless run.** SKILL.md:120 says to put an Assumed answers table at the top. delivery-profiles.md:152–153 says to fold assumed answers in "as one line each". I used a table with one row per answer, which is both, but it alone used about 300 of the 1,200 words.
- **"First implementation goal" for the ADK pin.** SKILL.md:194 makes "confirm against the chosen pin" an acceptance item of the first implementation goal. G01 (indexing) does not touch ADK. I split it: G01 records the pin and G02 confirms the interfaces. The skill doesn't anticipate a first goal with no ADK code.
- **Tickets "per ready goal".** SKILL.md:267 and implementation-plan-template.md:44 ("Ready describes resolved prerequisites") conflict with ticket-template.md:12, which defaults to `status: ready`, and with the user's request for tickets for all phase 1 goals. I wrote all four and set G02 to G04 to `blocked`.
- **`adk web` and the spend floor.** delivery-profiles.md:77–80 handles this well: cap the project when you do not own the Runner. It was still unclear whether a POC whose demo runs only in `adk web` needs a Runner script at all. I gave `max_llm_calls` to G03's runner and the key quota to `adk web`.
- **Which skill leads a single agent plus one tool.** The implementation-handoff.md:21 mapping points a bounded `LlmAgent` at `adk-workflow-design`, but there is no workflow here. I chose `adk-tool-interface-design` (line 23) as primary for G02. This was a judgment call.
- **The date.** "Friday" is ambiguous when today is a Friday. This came from the request, not the skills.

**Heavier than needed**
- **The compact form's 1,200-word target** (delivery-profiles.md:146, SKILL.md:84) is hard to meet together with the assumed-answers table (SKILL.md:120), a failure table, phase 2 goals that each need skill, estimate and check (delivery-profiles.md:132–134), and a later list with triggers *and* accepted risks (delivery-profiles.md:135–137). I ended at about 1,790.
- **design-decisions.md** (343 lines) must be read for every design (SKILL.md:56–57). For a read-only single-agent POC, only "Size the first slice" (26–61), "Outcome and orchestration" (63–124), the RAG bullet (141–147) and the trifecta paragraph (182–196) applied.
- **gcp-decisions.md** was read for cost and model guidance. Nothing in it changed a local-only POC, except "budget alerts only notify" (lines 65–66).

**Genuinely helpful**
- **delivery-profiles.md:100–121**: the capacity formula, focus factors, setup cost and "only the low end fits, say so" gave a concrete, honest cut line.
- **delivery-profiles.md:50–64**: the depth-per-concern table converted directly into §4 of the design.
- **design-decisions.md:182–196**: the trifecta check made "no write or egress tool" an explicit structural choice rather than a prompt warning.
- **adk-memory-architecture/references/retrieval-strategy.md:16–30**: heading-to-heading chunking with page spans in a local FTS5 index is exactly right for 30 PDFs in 6 hours. The bundled script ran with recall 1.0 on its fixture under 3.12.
- **adk-memory-architecture/references/local-document-coverage.md:29–35**: the miss labels (`query_miss`, `empty_extraction`, …) became G03's labels.
- **adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json**: a dated model choice without guessing. It also showed that `gemini-2.5-flash` retires on Vertex on 2026-10-20, a trap I would otherwise have walked into.

**Defect found**
- **adk-memory-architecture/references/compatibility.md:30** says the helper "requires Python 3.11+".
- `scripts/local_retrieval.py:159` uses a backslash inside an f-string expression, which is a `SyntaxError` before Python 3.12. I reproduced it on 3.9 and 3.11.
- The doc should say 3.12+, or the line should be rewritten.

## 6. The exact next prompt the skills told the user to type

The ticket template (`assets/ticket-template.md:48–50`) gives the run prompt, which I gave for the next ready goal, G01:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-section-index.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```

SKILL.md:276 shows the plan-based form as an example, `/adk-engineer Carry out G01 from docs/plans/<topic>.md.`. I used the ticket form because tickets were requested and the plan lives in the design file.
