# Travel policy Q&A bot: design and plan (compact form)

Status: **draft**. The user was not available, so the answers below are assumed and the decisions that depend on them are provisional.

## 1. Constraints and profile

| Scope-gate question | Answer | Depends on it |
| --- | --- | --- |
| Deadline and afterwards | One afternoon. *Assumed:* the code is kept if the demo lands | D4: kept form, model ID set in one place |
| Who builds it | *Assumed:* one developer, about 4 h, new to ADK; has a Gemini API key or can create one | Capacity, ×1.5 multiplier, D3 |
| Money | *Assumed:* a few dollars of Gemini API usage | D3 model tier, C4 spend cap |
| Users / judge | The team, watching a live `adk web` demo on the builder's laptop | No auth or hosting (deferred) |
| Data and effects | One public travel-policy PDF, no personal data, answers only | Floor only, no write controls |
| **Profile** | **Proof of concept:** one person, one afternoon, a demo audience, public data, read only | |

## 2. Journey and shape

A colleague asks "Can I book business class for a 7-hour flight?" in `adk web`. Today they search the PDF by hand. The bot answers from the policy, quotes the clause and cites the page, or says "the policy does not cover this".

The model only reads and phrases. Code decides which text it sees (the whole PDF, page-tagged), the model ID, the output cap and the fact that no tools exist.

```
adk web ──► LlmAgent "policy_qa" (pinned model, no tools)
              instruction = rules + full policy text with [p.N] markers (loaded once from policy.pdf)
```

## 3. Contracts and decisions

| ID | Invariant (scope) | Enforced where | Check |
| --- | --- | --- | --- |
| C1 | Every answer about the policy cites at least one `[p.N]` page that exists in the loaded PDF, and the quoted clause is present on that page (any user, the loaded version) | Instruction rules plus the page-tagged context (model-side); the gold-question check observes it | G02/A1, G02/A2 |
| C2 | A question the policy does not answer gets "The policy doesn't cover this" and no invented rule (any question) | Instruction rule; the model is the only enforcer, **gap:** no code-side guard in a POC | G02/A3 |
| C3 | The bot has no tools and no write or egress path; text inside the PDF cannot cause an action (whole agent) | Agent constructed with `tools=[]` | G01/A3 |
| C4 | Spend stops at the cap the user sets, and output per answer is bounded (the demo project) | Daily request quota on the key's Google Cloud project; `max_output_tokens` in the agent's generate config | G03/A1 |
| C5 | No API key in source, prompts or the repo; the model ID is pinned (the repository) | `.env` (git-ignored) read by `adk web`; model ID in one constant | G01/A4 |

| ID | Requirement → contract | Choice | Tradeoff | Check |
| --- | --- | --- | --- | --- |
| D1 | Grounded answers → C1, C2 | Put the whole PDF text in the instruction, one `[p.N]` marker per page, extracted once at import with `pypdf` | No RAG or vector store. Fits only while the PDF is a few hundred pages (well inside a 1M-token context); each turn pays for the whole document | G01/A1, G02 |
| D2 | Read only → C3 | One `LlmAgent`, no tools, no sub-agents | Cannot look up anything else (exchange rates, HR system). Not needed | G01/A3 |
| D3 | Pinned, current model → C5 | `gemini-3.8-flash` via the Gemini API key. Status `stable`, no shutdown announced, from the lifecycle table checked on 2026-10-08 (`adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json`) | A Flash model may miss subtle clauses; `gemini-3.5-flash` (Vertex retirement 2027-05-19 or later) is the fallback pin | G01/A4 |
| D4 | Kept slice | Model ID, PDF path and output cap are constants in `policy_qa/agent.py`, not inline literals | A few minutes more than hard-coding | Review |
| D5 | Spend stop under `adk web` → C4 | We cannot pass `RunConfig.max_llm_calls` because `adk web` owns the Runner, so the cap goes on the project quota. With no tools, each turn is one model call | A quota stops calls; a budget alert alone would only warn | G03/A1 |

ADK version: no pin exists yet. The working assumption is google-adk 2.8.0, the version the specialists were read against. Confirming the API against the installed pin is acceptance item G01/A5.

**Failure grid** (integrations: the Gemini API and the local PDF):

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini API | G03/A3 | G03/A2 | n/a: read only | n/a: single call | G03/A2 | G03/A1 | n/a: stateless answers | G02/A3 |
| Policy PDF | G01/A2 | n/a: local file | n/a: never written | n/a: loaded once | n/a: no credential | n/a: no quota | n/a: read once | G01/A3 |

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Grounded answers, measured | Build: 4 hand-checked gold questions | Colleagues rely on it → 20+ case eval set |
| Identity / per-user scope | Defer: public document, demo only | Any non-public document or a shared URL |
| Secrets | Minimal: `.env`, git-ignored | Hosting → Secret Manager |
| Effects / injection | Minimal: no tools (C3) | Any tool that writes or sends |
| Budgets | Minimal: quota and output cap (C4) | More users → per-user allowance |
| Hosting, observability, CI | Defer: laptop, console logs | Team asks to use it daily |

Floor kept: no secrets in code (C5), a spend stop (C4), no effects (C3), no personal data, a pinned model (D3). No risks are accepted.

Graduation conditions (before anyone except the builder uses it): authenticated hosting (Cloud Run behind IAP), a key from Secret Manager, an evaluation set run on every prompt or model change, and a named owner who updates the PDF.

## 5. Plan

Capacity: 4 h × 0.8 focus = 3.2 h. With a 25% reserve, 2.4 h is available for goals. The estimates below already include the ×1.5 new-to-ADK factor.

### G01: Local agent answers from the PDF in `adk web`

(0.75–1.25 h, D1–D4)
Builds `policy_qa/agent.py`, which loads `policy.pdf` into page-tagged text, plus a loader unit test.
Primary skill: `adk-workflow-design`. Supporting skills: `adk-agent-instructions`, `adk-model-and-output-contracts`.
Acceptance:
- A1 (C1): a sample question returns a cited answer.
- A2: a missing or unreadable PDF fails at startup with a clear message, not with an empty context.
- A3 (C3): the agent has zero tools, and a question asking the bot to "email this to HR" gets a refusal.
- A4 (C5): `git grep` finds no key, and the model ID appears once.
- A5: the installed ADK version is recorded and the constructor arguments are checked against it.

Run prompt: `/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.`

### G02: Gold questions

(0.25–0.5 h, C1, C2; after G01)
Four questions with the expected page, written by the builder from the PDF: three in scope and one out of scope. Run them in `adk web` or with a small script, and record pass or fail in this file.
Primary skill: `adk-agent-evaluation`. Supporting skills: none.
Acceptance:
- A1 (C1): the cited page is correct for all three in-scope questions.
- A2 (C1): each quoted clause appears verbatim on the cited page.
- A3 (C2): the out-of-scope question gets "doesn't cover".

Run prompt: `/adk-engineer Carry out G02 from docs/architecture/travel-policy-bot.md.`

### G03: Demo readiness

(0.25–0.5 h, C4; after G01)
Set the quota, run one dry run and prepare a backup screenshot.
Primary skill: `adk-operational-guardrails`. Supporting skills: none.
Acceptance:
- A1 (C4): the quota is visible in the console, and `max_output_tokens` is set.
- A2: with the key unset or invalid, the error is understandable.
- A3: with the network off during the dry run, `adk web` shows an error and the presenter switches to the backup screenshots.

Run prompt: `/adk-engineer Carry out G03 from docs/architecture/travel-policy-bot.md.`

### Cut line

G01 to G03 total 1.25–2.25 h, against 2.4 h available, so the high end fits. G02 was cut from six questions to four so that it fits; the other two move to G04. If time runs out early, work in the order G01 → G03 → G02. Phase 2 and the later list wait.

**Phase 2 (if the demo lands):**
- G04: a 20–30 case evaluation set with `adk eval`. 4–6 h. Skill: `adk-agent-evaluation`. Check: a pass rate is recorded per model pin.
- G05: Cloud Run behind IAP, with the key in Secret Manager. 4–9 h. Skill: `deploy-adk-on-google-cloud`. Check: an unauthenticated request is refused.
- G06: a policy-version owner, with the PDF version shown in answers. 1–2 h. Skill: `adk-memory-architecture`. Check: a replaced PDF changes the cited version.

**Later:**
- Retrieval (RAG): when there are several documents or the PDF outgrows the context.
- CI evaluation gate: when more than one person changes the prompt.
- Traces and cost metrics: when daily use starts.

## 6. Open decisions and next prompt

- Is a Gemini API key available, or must it be Vertex AI? Vertex adds about half a day of project and IAM setup, which would push G03 out of the afternoon.
- Is the PDF text-based? If it is scanned, extraction needs OCR or Gemini's native PDF input, and D1 changes.
- Should the cut line stay as it is?

```text
/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.
```
