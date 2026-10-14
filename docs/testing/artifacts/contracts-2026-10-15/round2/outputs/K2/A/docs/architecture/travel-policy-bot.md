# Travel policy bot: design and plan (draft)

Status: **draft**. Every answer below was assumed, because the user was not available to answer questions, so the decisions that depend on them are provisional. Profile: **proof of concept**: one builder, one afternoon, a live demo to the team, one public document, answers only.

## 1. Constraints and profile

**Assumed answers**

| Question | Assumed answer | Depends on it |
| --- | --- | --- |
| Deadline, and is it continued? | This afternoon. It may be continued if the team likes it, so the code is written to be kept. | Kept-form choices in D2 and D5; phase 2 |
| Who builds it? | One developer for about 4 hours, comfortable with Python and new to ADK (estimates are multiplied by 1.5) | Capacity and cut line |
| Money? | A small allowance on an existing Gemini API key | D3, D4 |
| Who judges it, and what do they see? | The team, watching a live `adk web` session on the builder's laptop | D5 |
| Data and effects? | One public travel-policy PDF, no personal data, read only (given by the user) | Floor and depth table |
| What is the PDF like? | Text-based (not scanned), under about 60 pages, can be committed to the repo | D1, D2 |
| Which backend? | Gemini API key (AI Studio), not Vertex AI | D4 |
| Should answers cite the policy? | Yes, by page and section heading | C1, D2 |

## 2. Journey and shape

A colleague asks "Can I book business class for a 7-hour flight?" in `adk web`. Today they search the PDF and work out the answer themselves. In the demo, the bot answers in a few sentences, quotes the rule, gives the page, and says so plainly when the policy is silent.

The model's only job is to interpret the question and write the answer. Code decides everything else: which document and version the model sees, the model ID, and the fact that there are no tools. One `LlmAgent` makes one model call per turn.

```
adk web ──> LlmAgent(model=pinned, instruction=provider()) ──> Gemini API
                         └─ provider() returns rules + full policy text with [page N] markers
                            (extracted once at import from policy/travel-policy.pdf)
```

## 3. Contracts and decisions

ADK pin assumption: `google-adk==2.8.0`, the version the specialist skills were checked against. Confirming it against the installed version is G01/A1.

| ID | Invariant (scope: one local user, one policy version) | Enforced where | Check |
| --- | --- | --- | --- |
| C1 grounded | Every policy rule an answer states appears in the loaded policy text and carries its page | Full text in the instruction, plus answer rules in the instruction (D1, D2) | G02/A1 gold questions, judged by eye |
| C2 silent policy | When the policy does not cover a question, the bot says so and names the policy owner instead of guessing | Instruction rule | G02/A2 |
| C3 complete source | The model receives the whole extracted text of the committed PDF. If any page extracts as empty, startup fails loudly | Loader at import (D2) | G01/A2 offline test |
| C4 floor | No API key in source, prompts or the shared doc; model ID pinned; spend bounded | `.env` kept out of git (gitignored); constant in `agent.py`; no tools (so one call per turn) plus a budget alert on the key's project | G01/A3, G01/A4 |
| C5 failure | A model error appears as an error in `adk web`, never as an invented answer | ADK/`adk web` default error surfacing | G03/A2 (rehearsed once) |

| ID | Requirement → choice | Reason / tradeoff | Check |
| --- | --- | --- | --- |
| D1 | Answer from one PDF (C1, C2) → a single `LlmAgent` with no tools and no retrieval; the whole policy goes in the context | One short document fits easily, and without retrieval nothing can be missed by a search. It costs the whole document's tokens on every question, which is fine for a demo. RAG or Vertex AI Search are deferred until there are several documents | G02 |
| D2 | Complete, citable source (C3, C1) → extract the text with `pypdf` at import and insert `[page N]` markers. Pass it through an `InstructionProvider` callable, because a callable skips `{var}` state templating, so braces in the PDF cannot raise `KeyError` | Deterministic and testable offline, but tables and images lose layout. The alternative is to send the PDF as a native Gemini file part (better on tables); switch if G02 shows misread tables | G01/A2 |
| D3 | Repeatable demo (C4) → pin `gemini-3.8-flash` (stable, released 2026-09-02, no shutdown announced; lifecycle table `checked_on` 2026-10-08) | Avoids `gemini-2.5-*` (Vertex retirement 2026-10-20) and `gemini-3.6-flash` (Vertex retirement 2026-11-19). A flash model is cheap and fast enough for a one-document Q&A | G01/A4 |
| D4 | No leaked key, bounded spend (C4) → `GOOGLE_API_KEY` in `.env` with `GOOGLE_GENAI_USE_VERTEXAI=FALSE` and `.env` gitignored; a budget alert on the key's project, because `adk web` owns the Runner and `max_llm_calls` cannot be set there | No tools means no loops. The budget alert is the user's console step | G01/A3 |
| D5 | Local demo → `adk web` with its in-memory sessions; no hosting, no login | Nothing persists between runs, which is acceptable for a demo | G03/A1 |

**Failure grid** (POC rows only)

| Integration | Unavailable / slow | Rejects | Credential bad | Rate limited | Untrusted / malformed content | Other cells |
| --- | --- | --- | --- | --- | --- | --- |
| Gemini API | G03/A2 | G03/A2 | G01/A3 | G03/A2 | n/a: no tools act on output | n/a: read only, no writes |
| Policy PDF (local file) | G01/A2 (file missing) | n/a: local file | n/a: no credential | n/a: local file | G01/A2 (empty page) | n/a: read only, single version |

There are no action rows, because the agent changes nothing. The prompt-injection trifecta check is negative: the content is trusted company text, there is no private data, and there is no write or egress tool.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment | Build: 6 gold questions checked by eye | Phase 2 eval set when the bot is kept |
| Identity / data scope | Defer: single local user, public doc | Colleagues use it outside the demo |
| Secrets | Minimal: `.env`, gitignored | Any hosting → Secret Manager |
| External effects | n/a: answers only | Any tool that writes |
| Sensitive data | Defer: public doc, no personal data | Users paste personal trip details into a hosted bot |
| Injection / agency | Minimal: no tools | Adding untrusted documents or tools |
| Budgets | Minimal: no tools plus a project budget alert | Hosted use → per-user allowance |
| Retrieval | Whole document in context | More than one document, or context cost measured as too high |
| Frontend / hosting | `adk web`, local | Daily colleague use |
| Observability / release | Console logs; pinned model | First shared deployment |

**Graduation conditions** before colleagues use it unattended: verified sign-in (IAP), a labelled eval set of at least 20 cases, hosting with a service account and Secret Manager, and a decision on whether question text is logged.

## 5. Plan

The new-to-ADK multiplier is 1.5, applied to every goal. Capacity is 4 h × 0.8 = 3.2 h; keeping a 25 % reserve leaves **2.4 h**.

**G01 Local agent answers from the policy** (C3, C4; D1–D4). Estimate 0.75–1.25 h. Primary skill: `adk-workflow-design`. Supporting skills: `adk-agent-instructions`, `adk-model-and-output-contracts`.
Scope: `travel_policy_agent/{__init__.py, agent.py, policy_loader.py}`, `policy/travel-policy.pdf`, `.env.example`, `.gitignore`, `requirements.txt` (`google-adk`, `pypdf`), and `tests/test_policy_loader.py`.
- A1: the ADK pin is recorded and the specialist checks are confirmed against it (C4).
- A2: an offline test shows that the loader returns every page with `[page N]` markers, and fails on a missing file or an empty page (C3).
- A3: `git status` never shows `.env`, and no key appears in the repo or the rendered instruction (C4).
- A4: `agent.py` sets the model to `gemini-3.8-flash` as a constant (C4).

Run: `/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.`

**G02 Gold questions** (C1, C2). Estimate 0.5–0.75 h. Primary skill: `adk-agent-evaluation`.
Scope: `docs/demo-questions.md`, which holds 6 questions with the expected rule and page: 4 the policy covers (one of them an exception or table), and 2 it does not.
- A1: in `adk web`, at least 3 of the 4 covered answers quote the right rule and page (C1).
- A2: both uncovered questions get "the policy doesn't say", with no invented rule (C2).

Run: `/adk-engineer Carry out G02 from docs/architecture/travel-policy-bot.md.`

**G03 Demo dry run** (C5; D5). Estimate 0.25–0.5 h. Primary skill: `adk-engineer` (no specialist needed).
- A1: `adk web` starts from a clean checkout following the README steps (D5).
- A2: with the key unset, the UI shows an error, not an answer (C5).

Run: `/adk-engineer Carry out G03 from docs/architecture/travel-policy-bot.md.`

**Sum: 1.5–2.5 h against 2.4 h.** The low end fits. The high end overruns by about 0.1 h. **Cut line:** G01 to G03 ship this afternoon. If G01 runs high, cut G02 to 3 questions (keeping one "policy doesn't say" case). Everything else waits. If time runs out early, the order that stays useful is G01, then G03, then G02.

**Phase 2 (if the team wants to keep it)**
- G04 Eval set: 20+ labelled cases run with `adk eval`. Primary skill: `adk-agent-evaluation`. Estimate 4–8 h. Acceptance: the eval run reports a pass rate per contract C1 and C2.
- G05 Colleague access: Cloud Run behind IAP, with a service account and Secret Manager. Primary skill: `deploy-adk-on-google-cloud`. Estimate 5–9 h, plus a GCP-setup day if the project is new. Acceptance: a signed-in colleague gets an answer, and an unsigned request gets 401/403.
- G06 Table fidelity: switch to a native PDF part (D2 alternative) if G02 or G04 shows misread tables. Primary skill: `adk-memory-architecture`. Estimate 1–2 h. Acceptance: the table questions pass.

**Later:** retrieval for several documents (trigger: a second document); context caching (trigger: measured token cost); observability and release gate (trigger: first shared deployment); updating the policy version (trigger: the policy owner publishes a new PDF, and the gold set is re-run).

## 6. Open decisions and next prompt

All of these are open because the user did not confirm them: the capacity and multiplier, the Gemini API versus Vertex choice, whether the PDF is text-based and small enough (if it is scanned, D2 changes to the native PDF part), the citation format, and the name of the policy owner used in C2. The budget alert needs the user's console access.

```text
/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.
```
