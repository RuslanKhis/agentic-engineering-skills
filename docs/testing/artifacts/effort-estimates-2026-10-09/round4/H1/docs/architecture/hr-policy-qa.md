# HR policy Q&A agent: proof of concept design and plan

Status: **draft**. Every scope answer below is assumed (the user was not
available); decisions marked *provisional* depend on them. Design and plan in one
file (compact form). Written 2026-10-09; nothing implemented.

## 1. Constraints and profile

**Profile: proof of concept.** One builder, about 6 hours, a live demo to HR
leadership. It is read-only, so the risk is low. The floor still holds because
the PDFs are internal documents.

| Scope question | Assumed answer | What depends on it |
| --- | --- | --- |
| Deadline, afterwards | Demo Friday **2026-10-16**. If the demo lands, the code is continued | Phase 1 code is written to be kept (D1–D3) |
| Builder | You alone, 6 h in two 3 h blocks. Comfortable with Python, **new to ADK**. You can already reach a company GCP project with Vertex AI enabled | ×1.5 multiplier, capacity, D4 |
| Money | A small allowance, ≤ USD 20 for the week, with a budget alert on the project | D5 |
| Judge and what they read | HR leadership watches you ask questions in `adk web`. They read the answers and their citations, and may suggest a question | D2, D6, demo backup |
| Data and effects | 30 current HR policy PDFs with a text layer. Internal-confidential, no employee records, English, one policy set. Questions are typed by you. The agent changes nothing | D1, D4, floor |
| Model provider | Company policy allows these PDFs to go to Vertex AI in that project | D4. Confirm before G01 |

## 2. Journey and shape

Today a manager looking for the leave carry-over rule searches PDF after PDF.
In the demo, you ask *"How many days of annual
leave can I carry over?"* The agent searches the indexed pages and answers in
two to four sentences, quoting `[Annual Leave Policy, p.3]`. When the policies
do not cover a question, it says so and points to HR.

```text
data/pdfs/*.pdf --(G01 ingest script)--> data/index/pages.jsonl  (doc, title, page, text)
adk web -> root_agent (LlmAgent, gemini-3.8-flash) -> search_policies(query) -> top pages
```

The **model** decides what to search for, rephrases its query (at most 3
searches) and writes the answer from the returned passages. **Code** controls
which corpus exists, how pages are ranked, how long results may be, which tools
the agent has (one, read-only), and the call limits.

## 3. Decisions (requirement → choice → tradeoff → check)

- **D1 Page-level corpus, built offline.** Answers need to point at a page →
  a script extracts each PDF page into a JSONL record (doc id, title, page,
  text) and reports empty pages and duplicate titles → this cannot read scanned
  PDFs (OCR is deferred) → G01's report shows 30 docs and zero empty pages.
- **D2 One `LlmAgent` with one function tool `search_policies`**, using
  pure-Python BM25 over the pages. It returns at most 5 passages, each capped
  at about 1,500 characters, with a `status` of `ok` or `no_results`. *Considered
  instead:* putting the whole corpus in the prompt (better recall, no retrieval
  code, but every question costs about 100k+ tokens and a page citation is
  harder to check) and Vertex AI Search or RAG Engine (managed, but setup and
  IAM do not fit 6 h). *Tradeoff:* a lexical search misses synonyms, which is
  why the model may rephrase. *Check:* tool unit tests, plus the G03 gold
  questions. If fewer than 4 of 5 find the right page, G05 is brought forward.
- **D3 Grounded answer contract in the instruction.** The agent answers only
  from returned passages, cites `[title, p.N]` for each claim, says "not found
  in the policies, please contact HR" when nothing relevant comes back, and
  ends with "Check the cited policy before acting." The instruction is a
  probabilistic control, not code enforcement. A citation validator waits for
  G06. *Check:* G03 includes one question the policies do not cover.
- **D4 Vertex AI through Application Default Credentials, no API key**
  (*provisional*). Confidential documents need enterprise data terms and no
  secret on disk. *Tradeoff:* this needs the company project. A paid Gemini API
  key in `.env` is the fallback; the free tier is not, because its data-use
  terms are unverified here. *Check:* G01 makes one bounded live call.
- **D5 Pinned model `gemini-3.8-flash`.** It is the newest stable Flash in the
  model lifecycle table of `adk-model-and-output-contracts` (checked
  2026-10-08), with no shutdown date. `gemini-3.6-flash` retires on Vertex on
  2026-11-19, so it is avoided. Thinking and sampling stay at their defaults.
  *Check:* G01 confirms the model is available in the project's region. The
  working assumption is ADK `google-adk==2.8.0`, the version the specialists
  were checked against; G01 confirms the pin.
- **D6 Spend stop.** `adk web` owns its Runner, so the cap goes on the project:
  a USD 20 budget alert (alerts only, it does not cap spend). The instruction
  allows at most 3 searches. `scripts/run_gold.py` owns its Runner and sets
  `RunConfig(max_llm_calls=10)` for each question.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Answer quality | Build: 5 gold questions, judged by you (G03) | Any audience beyond the demo → G04 |
| Secrets | Minimal: ADC, `.env` and `data/` gitignored | Shared host → G07 |
| External effects | None: no write or egress tools; a test asserts the tool list | Any action tool |
| Sensitive data | Minimal: policies only, no employee data; nothing logged beyond the console | Employees type their own cases → Later |
| Prompt injection | Minimal: PDFs are company-authored and the agent cannot act | Third-party documents or a write tool |
| Budgets | Minimal: D6 | Shared use → G07 |
| Retrieval and memory | In-memory sessions, local index | G04 shows misses → G05 |
| Frontend and hosting | `adk web` on your laptop | HR team trial → G07 |
| Observability and release | Console logs; pinned model | G07 |

**Graduation conditions** (before anyone but you uses it): an HR owner
approves a labelled evaluation set and its pass rate (G04); a document version
manifest exists (G06); access is restricted to named HR staff on a hosted
service (G07).

**Demo-day failures:** if the model is unavailable or returns 429, `adk web`
shows the error, and you fall back to the saved G03 results table. A
superseded PDF that is still in the folder gives conflicting answers, so G01
lists duplicate titles for you to remove. A question outside the policies gets
the "not found" answer, which is tested in G03.

## 5. Plan

Estimates are human hours (hands-on plus review), agent-assisted, **×1.5 for
new to ADK** (already applied). Capacity: 6 h × 0.8 focus = 4.8 h, less a 25 %
reserve, gives **3.6 h of goals**. The reserve covers the demo rehearsal.
Proposed layout (greenfield, not yet verified): `hr_policy_agent/agent.py`,
`hr_policy_agent/search.py`, `scripts/ingest_pdfs.py`, `scripts/run_gold.py`,
`eval/gold_questions.json`, `tests/`.

```yaml
- goal: G01
  phase: 1
  hands_on: 0.5-0.75
  review: 0.25
  total: 0.75-1
  owner: You
  blocked_by: []
  calendar_waits: confirm PDFs may be sent to Vertex AI (ask today)
  wait_days: 0
- goal: G02
  phase: 1
  hands_on: 0.5-0.75
  review: 0.5-0.75
  total: 1-1.5
  owner: You
  blocked_by: [G01]
  calendar_waits: none
  wait_days: 0
- goal: G03
  phase: 1
  hands_on: 0.5-0.75
  review: 0.25
  total: 0.75-1
  owner: You
  blocked_by: [G02]
  calendar_waits: none
  wait_days: 0
- goal: G04
  phase: 2
  total: 6-12
  owner: You
  blocked_by: [G03]
  calendar_waits: HR subject-matter expert time to label answers
  wait_days: 2-5
- goal: G05
  phase: 2
  total: 4.5-9
  owner: You
  blocked_by: [G04]
- goal: G06
  phase: 2
  total: 3-6
  owner: You
  blocked_by: [G04]
- goal: G07
  phase: 2
  total: 9-15
  owner: You
  blocked_by: [G03]
  calendar_waits: IAP and IAM grants from the platform team
  wait_days: 3-10
```

**Phase 1.** The schedule check (`check_schedule.py --capacity 3.6 --days 2
--reserve 0.25 --person "You=2.4"`, run 2026-10-09 with Python 3.13) reports
2.5–3.5 h of 3.6 h, so phase 1 fits. The longest chain is G01 → G02 → G03,
taking 1.39–1.94 of 2 working days. Day 1: G01 and G02. Day 2: G03 and a
rehearsal. If time runs out, each finished goal is still useful. If G02 runs
high, G03 drops to 3 questions.

- **G01 Index the 30 PDFs and prove model access.** The ingest script writes
  `pages.jsonl` and a report (docs, pages, empty pages, duplicate titles,
  approximate tokens). Also: confirm the ADK pin, and make one live
  `gemini-3.8-flash` call through ADC. Primary skill: `adk-memory-architecture`.
  Ticket: `docs/tickets/hr-policy-qa/G01-index-policies.md`.
- **G02 Cited answers in `adk web`.** This builds `search_policies`, the
  instruction from D3, and `root_agent`. Offline tests cover ranking, result
  bounds, `no_results`, and the tool list. Acceptance: 3 questions you ask by
  hand come back with correct citations. Primary skill:
  `adk-tool-interface-design`. Ticket: `G02-cited-answers.md`.
- **G03 Five gold questions and a demo backup.** Four questions the policies
  answer, with the expected doc and page, and one they do not cover.
  `run_gold.py` writes a results table that you judge. One tuning pass at most.
  Primary skill: `adk-agent-evaluation`. Ticket: `G03-gold-check.md`.

**Cut line:** phase 1 is G01–G03. Phase 2 waits.

**Phase 2: graduate to an HR team trial** (each goal has its primary skill
and one acceptance check). The schedule check gives 22.5–42 h. At this week's
pace of 2.4 h a day, that is 14.5–28 working days, with the waits included.

- **G04** Evaluation set of 25–40 questions labelled by an HR expert, with a
  source-support check (`adk-agent-evaluation`). Acceptance: the pass rate is
  measured and HR agrees the threshold.
- **G05** Better retrieval: hybrid or semantic search, or Vertex AI Search,
  chosen from G04's misses (`adk-memory-architecture`). Acceptance: the G04
  retrieval misses are halved.
- **G06** Document version manifest and refresh, plus a citation validator in
  code (`adk-memory-architecture`, with `adk-model-and-output-contracts`).
  Acceptance: a removed PDF is never cited.
- **G07** Cloud Run behind IAP for named HR staff, with a service account,
  structured logs and a release manifest (`deploy-adk-on-google-cloud`).
  Acceptance: a non-allowlisted user is denied.

**Later:**

| Item | Trigger | Risk while it waits | Skill |
| --- | --- | --- | --- |
| Employee-wide access with SSO, and policy variants by region or role | Rollout beyond HR | Wrong policy variant for a user | `adk-tool-auth-and-secrets` |
| Screening employees' questions for personal data | Employees describe their own cases | Personal data in prompts and logs | `protect-adk-sensitive-data` |
| OCR for scanned PDFs | G01 reports empty pages | Those docs are unanswerable | `adk-memory-architecture` |
| Evaluation gate in CI, model migration calendar | Second contributor or a model retirement notice | Silent regressions | `adk-release-engineering` |
| Traces, token cost, context caching | Shared use or measured cost | Unattributed spend | `adk-agent-observability` |

## 6. Open decisions and next prompt

1. Is the demo on 2026-10-16? (Phase 1 needs 2 working days.)
2. May the PDFs go to Vertex AI in your company project, and in which region?
   This blocks G01's live call; the ingest work can start without it.
3. Are any of the PDFs scanned, superseded or country-specific? G01 will show
   this.
4. Are you new to ADK? If not, drop the ×1.5 multiplier and phase 1 has room
   to spare.

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-index-policies.md.
```
