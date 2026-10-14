# Travel policy Q&A bot: design and plan (proof of concept)

Status: **draft**. Answers marked *assumed* were not confirmed by the user;
decisions resting on them are provisional. Design and plan in one file.

## 1. Constraints and profile

| Scope gate | Answer | Status | What depends on it |
| --- | --- | --- | --- |
| Deadline and afterwards | One afternoon. The demo happens after the build time. Code is kept if the team likes it | Given; "kept" *assumed* | Phase 1 size; D2 keeps the policy file path configurable |
| People and hours | One developer, about 4 hours, new to ADK, has a Google account | *Assumed* | Capacity (§5), ×1.5 multiplier |
| Money | A few dollars of Gemini API usage on a personal or team API key | *Assumed* | D4 model tier; F1 spend stop |
| Users or judge | The developer's team watching a live `adk web` demo | Given | Frontend = `adk web`, no auth |
| Data and effects | One public travel-policy PDF, no personal data, answers only | Given | Floor items for data and writes are met by design |

**Profile: proof of concept.** It's a local demo for colleagues, on one
public document, with no writes. Correct this line if the bot is meant to
become something colleagues use every day. That would make it an internal
tool.

## 2. Journey and shape

A teammate asks "Can I book business class for a 7-hour flight?" Today they
search the PDF or ask finance. The bot answers in two or three sentences,
quotes the rule with its page, and says "not covered" when the PDF is silent.

The model's only job is to read the policy and phrase the answer. Code does
everything else: it loads the PDF, marks the pages, pins the model and holds
the answering rules. There are no tools, no retrieval and no sub-agents.

```
adk web ──► root_agent (LlmAgent, no tools)
              static_instruction = answering rules + policy text with [page N] markers
              (loaded once from policy/travel_policy.pdf at import)
           ──► Gemini API (pinned model ID, key from .env)
```

## 3. Decisions (provisional where they rest on an assumption)

| ID | Requirement → choice | Tradeoff | Check |
| --- | --- | --- | --- |
| D1 | Answers come only from one short document → **one `LlmAgent` with the whole policy text in context**. No retrieval, no vector store | Uses more tokens per question than RAG and stops working if the PDF is too long for the context window (U1). It saves a chunking, indexing and retrieval-quality problem the afternoon can't afford | G02/A1 token count; G03 gold questions |
| D2 | Policy text must reach the model unaltered → **extract the text once with `pypdf`, put `[page N]` markers in, and put it in `static_instruction`**. Don't use a string `instruction`, because ADK templates `{...}` in string instructions and raises `KeyError` on any brace in the PDF. `static_instruction` is sent literally and forms a cacheable prefix | Plain extraction can scramble tables, such as per-diem rate tables (U2). The fallback is to pass the PDF itself as an inline `application/pdf` part | G02/A2 render test; G03/A3 table question |
| D3 | Answers must be trustworthy in front of the team → **short answering rules in the instruction**: answer only from the policy, cite `[page N]`, quote the rule, say "not covered by the policy" otherwise, and never invent amounts | The rules make the bot refuse questions the PDF only hints at. That's acceptable for a policy bot | G03/A1, G03/A2 |
| D4 | The demo behaves as it did in rehearsal → **pin `gemini-3.8-flash`**, chosen from the skill's lifecycle table (`model-lifecycle-2026-10-01.json`, checked_on 2026-10-08). It's stable and has no announced shutdown. Avoid `gemini-2.5-*`, whose Vertex retirement is 2026-10-20 | Flash rather than Pro. Cheap and fast, possibly weaker on tricky cross-references. Escalation is a later item | G01/A2; re-check the table before the demo |
| D5 | Bounded spend → **no tools, so one model call per question**, plus a **budget alert or quota on the key's project**, because `adk web` does not apply an application `RunConfig.max_llm_calls` | An alert observes rather than stops; the real bound is the no-tools structure | G01/A3 |
| D6 | Known ADK interfaces → **assume google-adk 2.8.0** (the version the specialist skills were read against) | Later versions may differ | G01/A1 confirms against the installed pin |

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Secrets | Minimal: `GOOGLE_API_KEY` in `.env`, `.env` in `.gitignore`, never in code or the prompt | Any shared host → Secret Manager |
| Spend stop | Minimal: D5 | Anyone other than the presenter can reach it → per-user limit |
| Pinned model | Minimal: D4 | Model retirement notice |
| Writes and external effects | None: the bot only answers | Any tool that writes or sends |
| Prompt injection | n/a: the input is the company's own document, there are no tools and nothing is private | Uploading user documents, or adding tools |
| Identity, sensitive data | Deferred: one public document, a local single user | Personal or confidential documents, or more users |
| Quality measurement | Build, small: 8 gold questions (G03) | The team wants to rely on the answers → evaluation set |
| Hosting, observability, release | Deferred: local `adk web`, console logs | Colleagues using it without the presenter |

**Graduation conditions** (before anyone outside the demo uses it):
evaluation set ≥ 20 questions with a pass threshold; hosted behind company
sign-in; a policy-version string shown in answers; and a re-check of the
model lifecycle table.

**Failure grid (the rows this POC touches)**

| Integration | Unavailable or slow | Rejects the request | Write outcome unknown | Partial multi-step change | Credential expired or revoked | Rate limited or out of quota | Duplicate or concurrent request | Untrusted or malformed content |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gemini API | G03/A4 | G01/A2 | n/a: read only | n/a: single call | G01/A2 | G03/A4 | n/a: stateless answers | G03/A2 |
| Policy PDF (local file) | G02/A3 | n/a: local read | n/a: read only | n/a: single read | n/a: no credential | n/a: local file | n/a: read once | G02/A2 |

The agent changes nothing, so there are no action rows.

## 5. Plan

Estimates are human hours for one developer working with a coding agent:
hands-on time plus review. Each figure is the base estimate × **1.5 (new to
ADK)**, rounded up to the next quarter hour.

**G01: Local ADK skeleton runs in `adk web`**. Estimate 0.75–1 h. Primary skill: `adk-workflow-design`. Supporting skills: none.
Create the `travel_policy_bot/` package (`agent.py`, `__init__.py`), `.env.example` and `.gitignore`. Pin `google-adk` and `pypdf` in `requirements.txt`. Set a budget alert on the API key's project.
Acceptance: A1, the installed `google-adk` version is recorded and the API names used here are checked against it. A2, a "hello" in `adk web` gets a reply from the pinned model, and a bad key gives a visible error. A3, the budget alert or quota exists, as a screenshot or note.
Run: `/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.`

**G02: The bot answers from the policy PDF**. Estimate 0.75–1.25 h. Primary skill: `adk-agent-instructions`. Supporting skills: `adk-model-and-output-contracts`.
Add `policy_loader.py`, which turns the PDF into text with page markers. Set `static_instruction` to the answering rules (D3) plus that text. The PDF path comes from the `POLICY_PDF` variable and defaults to `policy/travel_policy.pdf`. Add an offline pytest.
Acceptance: A1, the token count of the policy text is printed and is under 50k, otherwise go to U1. A2, the offline test checks that loading a PDF containing `{` and `}` builds the agent with page markers present and no `KeyError`. A3, a missing PDF fails at startup with a clear message, not on the first question.
Run: `/adk-engineer Carry out G02 from docs/architecture/travel-policy-bot.md.`

**G03: Gold questions and demo dry run**. Estimate 0.5–0.75 h. Primary skill: `adk-agent-evaluation`. Supporting skills: none.
Write eight questions with expected answer and page in `docs/demo/gold-questions.md`: five in the policy, two not covered, one from a table. Ask them in `adk web` and record pass or fail.
Acceptance: A1, at least 4 of the 5 covered questions are correct and cite the right page. A2, both uncovered questions get "not covered" with no invented rule. A3, the table question is right, or D2's fallback is applied. A4, the presenter knows what a 429 or 503 looks like in `adk web` and has a recorded transcript as a fallback.
Run: `/adk-engineer Carry out G03 from docs/architecture/travel-policy-bot.md.`

**Capacity and cut line.** 4 h × 0.8 focus = 3.2 h, minus 25% reserve =
**2.4 h**. Phase 1 (G01–G03, added by hand) = **2.0–3.0 h**: the low end fits,
the high end does not. If G01–G02 run high, cut G03 to three questions (one
covered, one uncovered, one table) and drop A4's transcript. After G02 alone
the demo already works.

**Phase 2: if the demo lands**
- G04, evaluation set of 20+ questions with a pass threshold. 3–5 h. Primary skill `adk-agent-evaluation`. Acceptance: one command scores the set.
- G05, hosted for colleagues on Cloud Run behind IAP. 5–9 h, plus a day if this is the team's first GCP project. Primary skill `deploy-adk-on-google-cloud`. Acceptance: someone outside the team is refused.
- G06, policy-version string and re-ingest step when the PDF changes. 1–2 h. Primary skill `adk-agent-instructions`. Acceptance: answers name the version.

**Later**
- Retrieval (RAG): if the PDF exceeds about 50k tokens or more documents are added.
- Pro model: if gold accuracy is below threshold on Flash.
- Context caching: when usage makes the token cost visible.
- Traces and SLOs: once there are daily users.

## 6. Open decisions and next prompt

- U1, PDF length. Assumed under about 50 pages and 50k tokens. G02/A1 settles it. If it's larger, add retrieval before the demo or demo on the relevant chapters.
- U2, tables and scanned pages. Assumed the PDF has a text layer. A scanned PDF needs the inline-PDF fallback from D2. G03/A3 settles it.
- U3, Gemini API key versus Vertex AI. Assumed Gemini API key (AI Studio), since that's the fastest local path. A company that requires Vertex needs a GCP project and adds about half a day.
- U4, the model choice D4 rests on a table dated 2026-10-08. Re-check the deprecations page before the demo.

Next:

```text
/adk-engineer Carry out G01 from docs/architecture/travel-policy-bot.md.
```
