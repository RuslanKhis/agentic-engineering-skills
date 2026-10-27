# Travel policy bot: design and plan (draft)

Status: **draft, unreviewed** (single-person proof of concept skips independent review). Every row under "Assumed answers" is provisional.

## 1. Constraints and profile

**Profile: proof of concept**, demo to the team, run locally with `adk web`. Phase 1 code is kept-form (config in one place) because it costs little more.

| Question (not answered; nobody to ask) | Assumed answer | Depends on it |
| --- | --- | --- |
| Deadline, and continued afterwards? | Demo this afternoon; continued only if the team likes it | Kept-form code; phase 2 list |
| Builder, hours, ADK familiarity? | 1 developer, 4 h, knows ADK basics (no 1.5× multiplier) | Estimates in section 5 |
| Spend? | Small allowance; the user sets a quota on the model project | C4 |
| Judge and what they read? | Team watching a live demo | G04 rehearsal |
| Web UI, reach, handover? | `adk web` on loopback, screen shared, not handed over | No auth work; D6 |
| Data and effects? | One public PDF, no personal data, read only | Floor, C2 |
| Presentations, SoW, lock-in? | The demo is the review; no SoW; no lock-in concern | No presenter or portability goals |
| PDF size and layout? | Text-extractable, under about 60 pages, few tables | D1; **G01 checks this first** |
| Model access? | Gemini through whatever key or Vertex project the developer already has | D5 |

**Journey (running example).** A traveller asks, "What's the hotel limit in Lisbon, and can I fly business on a 7-hour flight?" Today they search the PDF by hand. The bot answers from the policy with the section and page, or says it cannot find it.

## 2. Shape

One `LlmAgent`, no sub-agents, no tools. The model decides how to phrase and cite an answer. Code decides what the model may read: the whole policy text, loaded once from a local file, with `[page N]` markers.

```
adk web (127.0.0.1) -> LlmAgent (pinned model, policy text in instruction) -> answer + page cites
```

## 3. Contracts and decisions

| ID | Contract (invariant, scope) | Enforced where | Check |
| --- | --- | --- | --- |
| C1 | Every policy claim cites a page present in the policy text; if the text does not answer, the bot says so and names the policy owner. Scope: all answers. | Instruction plus page-tagged text. **Gap:** nothing in code refuses an uncited answer. | G03/A1 to A3 |
| C2 | The agent reads one fixed file and cannot write, browse or call anything else. | No tools attached; path set in code, never by the user. | G02/A2 |
| C3 | The bot never approves, books or promises an exception; it points to the travel desk. | Instruction. | G03/A4 |
| C4 | Spend stops: model ID pinned and a quota on the model project. `adk web` does not let us set `max_llm_calls`, so the quota is the stop. | Project quota set by the user. | G02/A3 |
| C5 | Text inside the PDF is data, not instructions. | Structural: no tool, so injected text cannot act. | G03/A5 |

| ID | Decision | Contract | Tradeoff | Check |
| --- | --- | --- | --- | --- |
| D1 | Put the whole policy in context (not RAG) when G01 shows it fits | C1, C2 | Cost per turn grows with page count; keyword search misses paraphrase ("lodging cap" vs "hotel limit"), whole text does not. Fallback if too long: one `search_policy(query)` tool over page chunks | G01/A2 |
| D2 | One agent, no sub-agents | C2 | No specialist split; nothing here needs one | G02/A1 |
| D3 | In-memory sessions (adk web default) | none | Lost on restart; no state worth keeping | n/a |
| D4 | Evaluate with 8 hand-written gold questions, answers checked by eye against the PDF | C1, C3, C5 | No automated regression; fine for a demo | G03 |
| D5 | Pin the model ID; choose it from the ADK model-lifecycle table in G01 (not checked here: no lookup was possible) | C4 | Retirement date must fall after the demo and phase 2 | G01/A3 |
| D6 | Local only: no Cloud Run, no vector index, no managed RAG | C4 | Teammates cannot try it themselves | G04/A2 |

## 4. Floor, depth, deferred

| Concern | Depth now | Trigger to raise |
| --- | --- | --- |
| Secrets | Minimal: key in `.env`, never in code, prompt or the shared screen | Any shared repo |
| Spend stop | Minimal: pinned model plus project quota (C4) | A URL others can reach |
| Identity, sessions | Defer: loopback, one user | Anyone but the builder connects |
| Network exposure | Minimal: no `--host 0.0.0.0`; ADK routes never public | Hosting |
| Retrieval | Build: whole text in context (D1) | Policy over about 60 pages, or several documents |
| Evaluation | Minimal: 8 gold questions (D4) | Policy changes, or team adopts it |
| Observability, CI, release | Defer: console logs; model ID pinned | Daily use |
| Writes, personal data | n/a: read only, public PDF | Any booking or expense feature |

Graduation conditions (before more users or other documents): sign-in, hosted deployment behind it, a larger gold set with a rerun script, and an owner for policy updates.

## 5. Plan

Capacity: 4 h × 0.8 focus = 3.2 h; 25% reserve leaves 2.4 h for goals. Estimates are hands-on plus review, in quarter hours, summed by hand.

**G01. Prepare the policy text.** Extract the PDF to `policy.md` with `[page N]` markers; check page count, tables, scanned pages. Contracts: C1, D1, D5. Estimate 0.5 to 0.75 h. Skill: `adk-memory-architecture` (document preparation). Acceptance: A1 page count and text-layer check recorded; A2 spot-check 3 pages against the PDF, tables intact; A3 model ID picked from the lifecycle table. If the PDF is scanned or table-heavy, stop and report: that adds an OCR step and breaks the budget. Run: `/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.` Status and evidence:

**G02. Agent running in `adk web`.** One `LlmAgent`, instruction with grounding and citation rules, policy text loaded from the fixed path. Contracts: C2, C4, D2. Estimate 0.5 to 1.0 h. Skill: `adk-engineer`. Acceptance: A1 the lisbon question gets an answer; A2 the agent has no tools and the path is not user-controlled; A3 project quota is set and the model ID is pinned. Run: `/adk-engineer Carry out G02 from docs/architecture/travel-policy-bot.md.` Status and evidence:

**G03. Gold questions.** Write 8 questions with expected page: 3 answerable (A1 to A3), 1 request for approval or exception (A4), 1 with an injected line in the question or a planted line in a copy of the text asking it to ignore the rules (A5), plus 3 out-of-scope or unanswerable ones counted under A1. Check by eye, record in `gold.md`. Contracts: C1, C3, C5. Estimate 0.5 to 0.75 h. Skill: `adk-agent-evaluation`. Run: `/adk-engineer Carry out G03 from docs/architecture/travel-policy-bot.md.` Status and evidence:

**G04. Demo dry run.** Run the 8 questions live once, with a fallback screenshot of each answer. Estimate 0.25 h. Acceptance: A1 full run with no surprise; A2 `adk web` started on loopback. **Teardown: n/a, nothing that charges while idle is provisioned.** Run: `/adk-engineer Carry out G04 from docs/architecture/travel-policy-bot.md.` Status and evidence:

**Sum:** 1.75 to 2.75 h against 2.4 h available. The low end fits; the high end overruns the reserve by 0.35 h. **Cut line:** G01 to G04 stay. If running high, shrink G03 to 5 questions (keep A1, A4, A5), never the floor. If time runs out early, stop order of usefulness: G01, G02, G04, G03.

**Phase 2 (if the team wants it):**
- P2-1 Hosted on Cloud Run behind sign-in, 3 to 6 h, `adk-security`; acceptance: unauthenticated request refused.
- P2-2 50-case gold set with rerun script, 4 to 8 h, `adk-agent-evaluation`; acceptance: scripted pass rate recorded.
- P2-3 Chunked retrieval for several documents, 3 to 6 h, `adk-memory-architecture`; acceptance: cross-document gold question cites the right file.

**Later:** observability and CI evaluation (trigger: daily use); policy-update process (trigger: next policy revision).

## 6. Open decisions

1. PDF page count and layout (G01 settles it; decides D1).
2. Which Gemini access path and who sets the quota (C4).
3. Whether the demo is continued (decides phase 2).
