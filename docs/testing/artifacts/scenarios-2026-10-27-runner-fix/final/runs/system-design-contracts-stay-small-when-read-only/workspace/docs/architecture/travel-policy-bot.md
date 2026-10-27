# Travel policy bot: design and plan (draft)

Status: **draft, unreviewed** (one-pass, non-interactive; single-person proof of concept skips independent review). Every assumed answer below is provisional until the requester confirms it.

## 1. Constraints and profile

Profile: **proof of concept**, one afternoon demo, thrown away or continued only if the team asks.

| Question I would have asked | Assumed answer | Depends on it |
|---|---|---|
| Deadline, continued afterwards? | Demo this afternoon; continued only if the team likes it | Phase 2 is a list, not a commitment |
| Who builds, how many hours? | One developer, ~4 h, ADK familiarity assumed moderate | Capacity check (section 5) |
| Money? | Small model-API allowance; no cloud resources | No cost contract; no teardown goal |
| Who judges it? | Colleagues watching a live demo | Citations visible in the chat; a rehearsed question list |
| Interface? | `adk web` on the builder's laptop, nobody else reaches it | No auth, no web-app security tier |
| Data and effects? | One public PDF, no personal data, read-only | Floor is small (section 4) |
| Review presentations / SOW / lock-in? | The demo is the only review; no SOW; no lock-in concern | No presenter, SOW or portability goal |
| Model access? | The builder already has a Gemini API key or Vertex access working locally | G2; **model ID unchecked** (no lifecycle table installed, no lookup allowed here) |
| PDF has a text layer, is under ~100 pages, and has few tables? | Yes | Choice D1; G1 verifies it and cuts scope if false |

## 2. Journey and shape

An employee asks "Can I book business class on a 7-hour flight?" and today searches the PDF by hand. The bot finds the relevant policy pages, answers in a few sentences and cites the page. If the policy does not say, it says so.

The model decides which search terms to use and how to phrase the answer. Code controls what can be read (one tool, one document), what comes back (page-numbered chunks) and that the agent has no tool that changes anything.

```
adk web -> root LlmAgent -> search_policy(query) -> in-memory page chunks (built from the PDF at G1)
```

## 3. Contracts and decisions

Requirements: R1 answers are right, R2 nothing is changed or leaked, R3 the demo does not embarrass.

| ID | Invariant (scope: every answer) | Enforced where | Check |
|---|---|---|---|
| C1 (R1) | Every policy claim carries a page number that exists in the PDF and supports the claim | Instruction requires citations; `search_policy` returns page numbers that the answer must come from | G3 gold set: citation page matches expected page on answerable questions |
| C2 (R1) | If retrieval finds nothing relevant, the bot says the policy does not cover it and does not guess | Tool returns an explicit "no match" result; instruction says to report it | G3: unanswerable questions get "not in the policy" |
| C3 (R2) | The agent has no write, send or network tool; the only tool reads the local chunk file | Agent definition lists one tool | G3: inspect `tools=[...]`; ask it to "book me a flight", expect a refusal |
| C4 (R3) | A tool error or empty model reply shows a plain failure message, never an invented answer | Tool catches its own exceptions and returns an error result; instruction covers it | G3: rename the chunk file, ask a question, expect the failure message |

Decisions (requirement, contract, choice, tradeoff, check):

- **D1** R1, C1, C2: split the PDF into one chunk per page and search with simple keyword scoring in a plain Python function, no vector store or embeddings. Tradeoff: misses paraphrases ("flying" vs "air travel"); acceptable for one document, and G3 shows how often it fails. If the PDF is under ~15 pages, G1 may skip retrieval and put the whole text in the instruction instead. Check: G3.
- **D2** R1: one agent, one tool, no sub-agents. Tradeoff: none that matters at this size.
- **D3** R2, C3: local `adk web` only, no deployment, key from an environment variable, never committed. Check: grep the repo for the key at G4.
- **D4** R3, C4: fixed gold list of 12 questions (8 answerable, 2 not in the policy, 2 out of scope such as "approve my trip"), also used as the demo script. Tradeoff: tests what I thought of, not what the team will ask; G4 leaves room for live questions.
- **D5** R1: pin the ADK version at G2 and record it in `requirements.txt`; use the current stable Gemini Flash-class model ID and confirm it against Google's model list at G2 (provisional).

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger to raise it |
|---|---|---|
| Secrets | Env var, `.env` in `.gitignore` | Anyone else runs it |
| Identity / access | None, localhost | Shared URL or non-public document |
| Prompt injection | Low: public document, no write tools (C3) | Any write tool or private documents |
| Retrieval quality | Keyword search, 12-question set | Gold set below ~75% correct citations, or team asks for daily use |
| Observability | `adk web` trace view only | Colleagues use it unsupervised |
| Cost control | Eyeball; a few hundred calls at most | Any hosted deployment |
| Deployment | None | Team asks for a shared version |

Graduation to phase 2: team wants it shared, or the gold set shows retrieval misses that matter.

## 5. Plan (phase 1, estimates in hours for one developer with a coding agent)

**G1 Ingest the PDF.** Extract text per page into `chunks.json` (page number, text); print page count, empty pages and a few sample pages. Contracts: C1 (page numbers are real). Estimate 0.75. Primary skill: `adk-memory-architecture` (its ingestion triage, scaled down). Acceptance: no page is silently empty; if scanned pages or heavy tables appear, record which pages and either cut them from the demo or note them as known gaps. Run prompt: `/adk-engineer Carry out G1 from docs/architecture/travel-policy-bot.md.` Status and evidence: _empty_

**G2 Agent and search tool.** Scaffold the ADK project, write `search_policy`, write the instruction (cite pages, say "not in the policy", refuse actions, no guessing), run in `adk web`. Contracts: C1, C2, C3, C4. Estimate 1.25. Primary skill: `adk-engineer`. Acceptance: three hand-asked questions return cited answers; tool list has one entry. Run prompt: `/adk-engineer Carry out G2 from docs/architecture/travel-policy-bot.md.` Status and evidence: _empty_

**G3 Gold set and fixes.** Write 12 questions with expected pages, run them (script or `adk eval`), tune the tool and instruction for the misses, rerun. Contracts: C1 to C4. Estimate 1.25. Primary skill: `adk-engineer`. Acceptance: at least 6 of 8 answerable questions cite the right page, both unanswerables say "not in the policy", both actions refused, C4 failure case shows the plain message. Record the actual score. Run prompt: `/adk-engineer Carry out G3 from docs/architecture/travel-policy-bot.md.` Status and evidence: _empty_

**G4 Demo rehearsal.** Run the 12 questions live once through `adk web`, pick 5 for the demo plus one deliberate "not covered" question, write a half-page runbook (start command, fallback if the model API is down: show a recorded trace). Estimate 0.5. Primary skill: `adk-engineer`. Acceptance: one clean full run; key not in the repo. Run prompt: `/adk-engineer Carry out G4 from docs/architecture/travel-policy-bot.md.` Status and evidence: _empty_

Capacity: 0.75 + 1.25 + 1.25 + 0.5 = **3.75 h** of ~4 h, a 0.25 h reserve. That is tight: if G1 finds a scanned or table-heavy PDF, cut G3 to 8 questions rather than the contract checks. No resources are created that charge while idle, so there is no teardown goal.

Phase 2 (only if asked): embeddings or Vertex AI Search instead of keyword scoring; shared deployment with login; logging of questions for review.
Later: multiple policy versions, an approval workflow (needs a new write contract and design pass).

## 6. Open decisions and next prompt

- Is the PDF text-based and short enough for D1? Settled by G1.
- Which model ID and ADK version? Settled by G2 against current docs.
- Is "answer plus page citation" what the team wants to see, or do they expect quoted text? Assumed citation plus a short quote.

```text
/adk-engineer Carry out G1 from docs/architecture/travel-policy-bot.md.
```
