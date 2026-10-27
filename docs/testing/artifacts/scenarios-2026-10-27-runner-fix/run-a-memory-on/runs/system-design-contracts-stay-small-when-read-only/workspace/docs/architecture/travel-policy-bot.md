# Travel policy bot: design and plan (draft)

Status: **draft, one-pass.** Nobody could answer questions, so every answer below is assumed and the decisions that rest on it are provisional. Not independently reviewed (single-person proof of concept).

## 1. Constraints and profile

**Profile: proof of concept**, one developer, about 4 h, shown to the team through `adk web` on the builder's laptop.

| Question asked | Assumed answer | Depends on it |
|---|---|---|
| Deadline and afterwards? | Today's demo; not continued unless the team asks | Phase 2 stays a list |
| Builder, hours, ADK familiarity? | One developer, 4 h, new to ADK | Few moving parts; no custom UI |
| Model and cloud money? | Small allowance, no cap stated | C3 needs a quota set before the demo |
| Audience? | Team of colleagues watching a live demo | Eval set and demo script are the evidence |
| Interface and reach? | `adk web`, localhost, builder only | No sign-in work; C3 |
| Data and effects? | One public PDF, no personal data, read only | No governance goal; C2 |
| Presentations, SOW, lock-in? | The demo is the only review; no SOW; no lock-in concern | No presenter, SOW or portability goal |
| The PDF? | Text-based, under about 60 pages, not in this workspace | G1 checks this first |

## 2. Journey and shape

An employee asks, "Can I book business class for a 7-hour flight?" The bot finds the relevant policy passages, answers in plain words and cites the page. If the policy is silent, it says so and names who to ask. Today people search the PDF by hand.

**The model decides** how to phrase the answer and which query to send. **Code controls** what text can be retrieved and which tools exist.

```
adk web (localhost) -> one LlmAgent -> search_policy(query) -> pages.json (built once from the PDF)
```

One agent and one tool. No vector database, no managed RAG: the PDF is small, so a page-chunked JSON file with keyword scoring in the tool is enough. This tradeoff gives up semantic matching on paraphrased questions. The G3 eval measures whether that matters. The fallback is to place the whole text in the prompt, which fits a small PDF's context window and needs no retrieval code.

## 3. Contracts and decisions

| ID | Contract (invariant, scope) | Enforced where | Check |
|---|---|---|---|
| C1 | Every policy claim in an answer cites a page returned by `search_policy` in that turn. | Tool returns only page-tagged passages. The instruction requires citations. The model's compliance is tested, not enforced. | G3: all cited pages exist in `pages.json`; manual read of the demo questions |
| C2 | The agent can read the policy text and nothing else: no network, no writes, no other tools. | Agent is built with exactly one tool. | G2: tool list has length 1; the tool opens only `pages.json` |
| C3 | Model spend has a hard stop and the server is not reachable from other machines. | Quota on the model project, because `adk web` is not configured by us. `adk web` binds to 127.0.0.1. | G4: quota visible in the console; `lsof` shows loopback only |
| C4 | When no passage matches or the tool fails, the bot says it cannot find the policy answer and does not answer from general knowledge. | Tool returns an explicit `no_match`. The instruction handles it. | G3: 3 out-of-policy questions all get a refusal |
| C5 | Every PDF page is in `pages.json` with extracted text, or listed as uncovered. | Ingest script prints a coverage count and fails on a page with empty text. | G1: pages in PDF equals pages in JSON plus listed gaps |

Decisions:
- D1 (C1, C5): chunk by page and keep page numbers, because citations are what make the demo trustworthy. Tradeoff: a rule that spans pages can be split. Check: G3 includes two such questions.
- D2 (C2): use a plain Python function tool, not MCP, to keep the surface minimal. Check: C2.
- D3 (C4): the tool returns structured `{status, passages}` so "no match" is a value the instruction can branch on. Check: C4.
- D4 (floor): pin the model ID in code. The ID is provisional until checked against the ADK version installed and the lifecycle table in `adk-model-and-output-contracts`, which is not installed here. Check: G2 acceptance.
- D5 (floor): ingest the PDF locally. No upload, no cloud storage, no secrets in the repo; credentials come from the environment.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger to raise it |
|---|---|---|
| Secrets | Environment variables only; nothing in source or logs | Any shared deployment |
| Spend stop | Project quota (C3) | Any use beyond the demo |
| Access | Localhost only | Anyone else needs the URL: add sign-in and a hosted runtime |
| Data | Public PDF, no personal data | Questions carrying employee details |
| Retrieval quality | 15-question eval, run by hand | Wrong answers in the demo, or the policy is replaced by many documents |
| Observability | `adk web` trace tab only | More than a demo audience |
| Resources that charge while idle | None created, so no teardown beyond stopping the server | Any managed index or deployed service |

**Graduation conditions** (before more users, real data or outside people): sign-in and hosted runtime; an owner for policy updates and re-ingestion; a larger eval with real employee questions; a decision on semantic retrieval; a spend cap owned by the team.

## 5. Plan (phase 1, estimates in quarter hours)

**G1. Ingest the PDF.** Outcome: `pages.json` with page-tagged text, with a coverage report. Contracts: C5. 0.75 h. Skill: `adk-memory-architecture`. Acceptance: coverage count matches. If any page has no text (scan or table image), stop and decide: OCR, or exclude and say so in the demo. Status and evidence: _empty_.
Prompt: `/adk-engineer Carry out G1 from docs/architecture/travel-policy-bot.md.`

**G2. Agent and tool.** Outcome: `adk web` answers one real question with a page cite. Contracts: C1, C2, C4, D4. 0.75 h. Skill: `adk-engineer`. Acceptance: one tool only; model ID pinned and confirmed against the installed ADK. Status and evidence: _empty_.

**G3. Eval set.** Outcome: 15 questions, with expected page per question, of which 3 are out of policy and 2 span pages. Contracts: C1, C4. 0.75 h. Skill: `adk-engineer`. Acceptance: record the score and the failures. Fix the instruction at most twice, then stop. Status and evidence: _empty_.

**G4. Demo prep.** Outcome: quota set, loopback check done, a 5-minute script with 4 questions including one refusal. Contracts: C3. 0.5 h. Acceptance: one full dry run. Status and evidence: _empty_.

**G5. Close.** Stop the server and record eval results and graduation notes. 0.25 h.

**Capacity:** 0.75 + 0.75 + 0.75 + 0.5 + 0.25 = 3.0 h of 4 h. The 1 h reserve is for the PDF's surprises, which are most likely in G1. **Cut line:** if G1 overruns, cut G3 to 8 questions, not C4 or C3.

**Phase 2** (only if the team wants it): hosted runtime with sign-in; semantic retrieval; re-ingestion workflow.
**Later:** multiple policies; employee-specific rules (needs identity and a data review).

## 6. Open decisions and next prompt

- Does the PDF contain scanned pages or tables? G1 settles it.
- Which model and quota size? Needs the installed ADK version and the team's cloud project; the user decides.
- Does the team want it continued after the demo? That decides phase 2.

```text
/adk-engineer Carry out G1 from docs/architecture/travel-policy-bot.md.
```
