# Travel policy bot: design and plan (draft)

Status: **draft**, one-pass, unreviewed (single-person POC skips independent review). Every row under "Assumed answers" is an assumption, not a user decision.

## 1. Constraints and profile

**Profile: proof of concept, kept (not thrown away) if the demo lands.** One developer, about 4 hours, demo to the team via `adk web` on loopback.

| Question (not answered; nobody to ask) | Assumed answer | Depends on it |
| --- | --- | --- |
| Deadline / afterwards? | Demo this afternoon; continued if liked | Code kept in a configurable shape (D1) |
| Who builds, how familiar? | One dev, 4h, ADK experience unknown, so x1.5 on ADK work | Estimates in section 5 |
| Spend? | Small allowance; user sets a cap on the model project | C4 |
| Who judges? | Team, watching a live demo | G03, gold questions |
| Web UI / URL / handover? | `adk web`, localhost only, builder's machine; not handed over | No auth work; security tiers 1-2 only |
| Data / effects? | One public PDF, no personal data, read only | Floor, C2 |
| Presentations / SOW / lock-in? | The demo is the review; no SOW; no lock-in concern | No presenter, SOW or portability goals |

Unknown, to confirm in G01: PDF page count, whether it is text or scanned, ADK version and model ID (to be taken from the dated model lifecycle table and pinned; not checked here).

## 2. Journey and shape

An employee asks "Can I book business class on a 7-hour flight?" The bot finds the relevant policy passages, answers in plain words and cites the page. If the policy is silent or the question is about a personal exception, it says so and points to the travel team.

One `LlmAgent` with one function tool, `search_policy(query)`. The PDF is extracted once, offline, into page-tagged chunks (`policy_chunks.json`). The tool does keyword/BM25 ranking over those chunks and returns the top few with page numbers. The model decides what to search and how to word the answer. Code decides what text is reachable. No sub-agents, no vector database, no cloud resources.

## 3. Contracts and decisions

| ID | Contract (invariant, scope) | Enforced where | Check |
| --- | --- | --- | --- |
| C1 | Any policy claim is backed by a passage returned by `search_policy` in the same turn and cites its page. When nothing relevant is returned, the bot says it found nothing and does not answer from general knowledge. | Instruction plus the tool's empty-result message. Prompt-level, so not hard-enforced: measured, not guaranteed. | 8 gold questions (6 answerable, 2 not in the PDF) checked by hand, citation page matched |
| C2 | Read only: the agent's sole tool reads the local chunk file. No network, writes or other tools. | Tool list in `agent.py`; nothing else registered | Code read in G02; the tool list is one entry |
| C3 | Out-of-scope requests (booking, approvals, "can I make an exception") get a refusal pointing to the travel team. | Instruction | 2 of the gold questions are of this type |
| C4 | Spend is bounded and the model behaves as yesterday. | Pinned model ID in config; spend cap on the model project (adk web does not let us set `max_llm_calls`) | Cap visible in the console; model ID in one place |
| C5 | If the chunk file is missing or unreadable, the tool returns an error and the bot says the policy is unavailable. | Tool catches the error and returns a message | Rename the file, ask a question |

Decisions:
- **D1** (C1): local page-chunked retrieval instead of Vertex AI RAG or pasting the whole PDF. Reason: cites pages, costs nothing idle, runs offline. Tradeoff: weak on paraphrase. If the PDF is under about 30 pages, G01 may instead inline it, which is simpler; decide after seeing the size.
- **D2** (C1, C3): the instruction carries the rules (cite pages, refuse exceptions). The PDF text is data, so the instruction says to ignore any instructions found inside it.
- **D3** (C4): one config module holds the model ID. Tradeoff: none worth noting.
- **D4** (C2): no memory, no artifacts, in-memory sessions. Tradeoff: no cross-session history, which the demo does not need.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger to raise |
| --- | --- | --- |
| Secrets | Minimal: API key in env, not in repo | Any shared deployment |
| Identity / access | Deferred: loopback only | Anyone else reaches a URL (then managed sign-in plus Cloud Run) |
| Spend | Minimal: project cap, pinned model | Any other user |
| Evaluation | Build: 8 gold questions by hand | Policy updates or a second document (then a runnable eval set) |
| Observability, release, hosting | Deferred: console logs, local | Colleagues using it daily |
| Retrieval quality | Minimal: BM25 | Gold questions miss on paraphrase (then embeddings) |

Graduation conditions (to be used by others): sign-in and hosting, a re-ingest path for policy updates, a larger eval set, a named policy owner who confirms answers. Resources that charge while idle: none, so no teardown goal.

## 5. Plan (phase 1)

Capacity: 4h x 0.8 focus = 3.2h, less a 25% reserve (0.8h) leaves 2.4h. Estimates are human hours, quarter-hour precision, ADK x1.5 already applied. They are assumptions.

- **G01 Ingest and search tool.** 0.75-1h. Primary skill: `adk-memory-architecture` (document ingestion). Extract the PDF to page-tagged chunks, check a couple of pages against the original (tables are the usual casualty), and write `search_policy` with the C5 handling. Proves C2, C5. Acceptance: asking the tool for "business class" in a Python shell returns the right page; renamed file gives the error message. Status and evidence: _empty_.
  Prompt: `/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.`
- **G02 Agent, instruction and gold questions.** 0.5-0.75h. Primary skill: `adk-engineer` (agent instructions as supporting). Create the agent with the pinned model and the one tool. Write the 8 gold questions and run them in `adk web`. Proves C1, C3, C4. Acceptance: all 6 answerable questions cite the right page; the 2 others get a refusal or "not found". Status and evidence: _empty_.
- **G03 Demo readiness.** 0.25-0.5h. Pick 3 demo questions and one failure (an unanswerable one), do a full dry run, confirm the cap is set. Acceptance: the dry run passes twice. Status and evidence: _empty_.

Total 1.5-2.25h against 2.4h available: **fits**, with the high end leaving about 0.15h more than the reserve. Cut order if time runs out: G03's extra demo questions, then gold questions down to 5. Never the cap (C4) or C1's not-found case. Phase 1 was added by hand; no schedule helper was run for one person.

Phase 2 (if the demo lands, not estimated finely): hosting plus sign-in (`deploy-adk-on-google-cloud`, 3-6h); re-ingest script and a runnable eval set (`adk-agent-evaluation`, 4-8h); embeddings if gold questions miss (`adk-memory-architecture`, 3-6h).

## 6. Open decisions

- PDF size and whether it is scanned (a scan needs OCR, which would break the estimates). Settled in the first 15 minutes of G01.
- Model ID and ADK pin: not looked up here. G01 confirms against the installed version.
- Who owns the policy content, if the team asks "is this answer official"? The bot is a finder, not an authority, and the demo should say so.

Next: `/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.`
