# HR policy Q&A agent: design and plan (proof of concept)

Status: **draft**. Assumptions are provisional until the user confirms them.
Date: 2026-10-09. This file holds both the design and the plan. The tickets are in
[`docs/tickets/hr-policy-qa/`](../tickets/hr-policy-qa/).

## 1. Constraints and profile

**Profile: proof of concept.** One builder, a demo to HR leadership, read-only,
internal documents. Done means: on the builder's laptop, the agent answers
real questions about the 30 PDFs with document and page citations, and a
short checked question set shows how often it gets them right.

| Scope-gate question | Answer (U = user, A = assumed) | What depends on it |
| --- | --- | --- |
| Deadline, and afterwards? | U: demo on Friday. A: **Friday 2026-10-16** (today, 2026-10-09, is a Friday). A: the code is kept if the demo lands | Phase 1 cut; kept-code form (paths are configured, not hard-coded) |
| Who builds? | U: one person, about 6 h over two days. A: **new to ADK**, has a Google account; no GCP project setup needed | Capacity; the Gemini API key route (D4) |
| Money? | A: a small allowance (under USD 20 for the week) on a **paid-tier** Gemini API key | Model tier (D4); the spend stop |
| Who judges, reading what? | U: HR leadership. A: a live demo on the builder's screen through `adk web`, plus one results table | No hosting or login in phase 1 (D5) |
| Data and effects? | A: the 30 PDFs are current, internal, contain **no employee personal data**, and company policy allows sending them to Gemini on a paid tier. The agent changes nothing | Floor; whether the demo can run at all (O1) |

## 2. Journey and shape

An HR manager asks "How many days of parental leave does a part-time employee
get, and does it carry over?" Today someone searches the PDFs or emails HR and
waits. With the agent, the answer arrives in seconds, quoting the policy and
page. If the policies do not cover the question, the agent says so and points to HR.

The **model** chooses which policies to open and writes the answer. **Code** controls
the document catalogue, how much of each document is returned, how many model
calls are allowed and which model is used.

```text
adk web ──> LlmAgent (pinned Gemini model, instruction + policy catalogue)
                 └─ read_policy(doc_id, start_page)  ──>  data/pages/<doc_id>.json
                                                         (extracted offline by G01)
```

## 3. Decisions

| # | Requirement | Choice | Tradeoff | Check |
| --- | --- | --- | --- | --- |
| D1 | Answers need to be trustworthy enough for HR leadership (A) | One `LlmAgent` that answers only from text it has read, cites `[document title, p. N]`, and says "not covered, contact HR" when the policies are silent | Refuses some questions a looser bot would guess at | G03: two out-of-corpus questions get the "not covered" answer; cited pages exist |
| D2 | 30 PDFs, 6 hours | **Read whole documents, not chunks.** Code renders a catalogue (id, title, page count) into the instruction. One tool, `read_policy`, returns up to 40 pages with `--- page N ---` markers. No search index | More tokens per question (roughly 5k–40k), and recall depends on titles. It also removes chunking, ranking and an index. Phase 2 can swap in the local FTS5 index that `adk-memory-architecture` ships (`scripts/local_retrieval.py`) | G01 reports tokens per document; G03 records whether the agent opened the right document for each question |
| D3 | The demo must not depend on scanned pages working | Offline text extraction (`pypdf`) to per-page JSON. Pages with no text are listed in a report, not OCR'd | Scanned policies are unanswerable in phase 1 | G01 report lists empty pages; the user decides whether any are needed for the demo |
| D4 | The demo must behave the same on Friday as on Wednesday; internal data | Pin **`gemini-3.8-flash`**: stable with no shutdown date in the lifecycle table `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (checked 2026-10-08). Use the Gemini API with a paid-tier key from `.env`. Avoid `gemini-2.5-*`, which is limited and retires on Vertex on 2026-10-20 | The paid tier costs a little money. The data-use terms are not verified here (O1) | G02: the captured request shows the pinned ID; `.env` is git-ignored |
| D5 | One person demonstrates it | Run `adk web` locally with in-memory sessions. No login, hosting or frontend | Nobody else can use it. That is accepted for a demo | Run `adk web` and ask the demo questions |
| D6 | Spend must stay bounded | `RunConfig(max_llm_calls=8)` in the evaluation runner. `adk web` does not take this config, so set a budget alert on the key's project and keep the tool's 40-page bound | A budget alert notifies but does not cap spending | G02 test: a scripted loop stops at the limit |

ADK version: assume **google-adk 2.8.0**, the version the specialists'
`references/compatibility.md` were checked against. G02 confirms it against
the version actually installed.

## 4. Floor, depth and deferred

| Concern | Depth now | Trigger that raises it |
| --- | --- | --- |
| Core judgment, measured | Build: 10 checked questions (G03) | More than 1 of 10 wrong leads to phase 2 retrieval work |
| Secrets | Minimal: API key in `.env`, git-ignored, never in prompts or logs | Any shared host leads to Secret Manager |
| External effects | None. The agent is read-only, with one tool | Any write or send tool needs a new design review |
| Prompt injection | Minimal: the PDFs are internal, and the agent has no write or egress tool, so the trifecta is broken | Documents from outside HR, or any write tool |
| Sensitive data | Deferred. Policies only, no employee records | Personal data in the corpus, or user questions about named employees |
| Identity / access | Deferred. Only the builder uses it | Any second user leads to an internal-tool graduation |
| Budgets | Minimal: D6 | Shared use leads to a per-user allowance |
| Hosting, observability, release | Deferred: local run, console logs, model ID pinned | Shared deployment |

**Floor kept:** no secrets in the repo, a spend stop (D6), nothing written or
sent, only data the user chose, and a pinned model ID.

**Graduation conditions** (before colleagues use it): Workspace sign-in behind
IAP, data-use approval for the model provider, an owner and refresh process
for policy versions, a 30-plus-case regression set, and structured logs that do
not contain question text.

## 5. Plan

**Capacity:** 6 h × 0.8 (two dedicated sessions) = 4.8 h, minus a 25 % reserve
for setup surprises and demo rehearsal = **3.6 h for goals**. Estimates are
human hours with a coding agent (hands-on plus review), at new-to-ADK rates.

| Goal | Delivers | Hours | Depends on |
| --- | --- | --- | --- |
| G01 | PDFs extracted to per-page JSON, plus a catalogue and an extraction report | 0.5–1.0 | none |
| G02 | Working `adk web` agent that cites pages | 1.0–1.5 | G01 |
| G03 | 10 checked questions in a results table, plus a demo script | 1.0–1.5 | G02 |
| **Phase 1** | | **2.5–4.0** | chain G01→G02→G03 |

**Cut line:** the low end (2.5 h) fits within 3.6 h. The high end (4.0 h) does
not fit. If the work runs high, G03 drops to 6 questions and skips any prompt
revision; that revision moves to phase 2. After G02 alone, the agent can already be
demonstrated. **User: confirm or move this line.**

- **G01 Extract the policies** (0.5–1.0 h). Primary skill:
  `adk-memory-architecture`. Acceptance: all 30 documents are in the
  catalogue, empty pages are flagged, and a re-run gives identical output.
  Ticket: `G01-extract-policies.md`.
- **G02 Agent answers with citations** (1.0–1.5 h). Primary skill:
  `adk-tool-interface-design`; supporting skills: `adk-agent-instructions` and
  `adk-model-and-output-contracts`. Acceptance: a demo question is answered
  with a correct page; an unknown `doc_id` returns an actionable error; the
  call limit stops a loop. Ticket: `G02-agent-answers.md`.
- **G03 Checked questions and demo script** (1.0–1.5 h). The user writes 10
  questions (8 covered, 2 not covered) and judges the results table. Primary
  skill: `adk-agent-evaluation`. Acceptance: all 10 rows have an answer, the
  documents opened and a verdict. Ticket: `G03-checked-questions.md`.

**Phase 2 (graduate to an internal tool, about 15–25 h):**

- P2-1, retrieval upgrade: if G03 shows wrong-document misses, use the FTS5
  index from `adk-memory-architecture`. Primary skill:
  `adk-memory-architecture`; 3–5 h. Check: recall on the G03 set is not
  worse.
- P2-2, Cloud Run behind IAP with Workspace sign-in. Primary skill:
  `deploy-adk-on-google-cloud`; 5–8 h plus waiting for a GCP project and IAM.
  Check: a non-allowlisted account gets 403.
- P2-3, a regression set of 30 or more cases in CI. Primary skill:
  `adk-agent-evaluation`; 4–6 h. Check: the gate fails on a seeded regression.
- P2-4, OCR for scanned pages if G01 found any that are needed. Primary skill:
  `adk-memory-architecture`; 2–4 h.

**Later:**

- Structured logs and cost per question. Trigger: shared use.
  Skill: `adk-agent-observability`.
- Per-user budget. Trigger: more than 20 users. Skill:
  `adk-operational-guardrails`.
- Policy versioning and refresh. Trigger: the first policy update after
  launch. Skill: `adk-memory-architecture`.
- Personal-data screening. Trigger: employee questions about their own case.
  Skill: `protect-adk-sensitive-data`.

## 6. Failure paths (only those this journey holds)

| Failure | What the user sees | Design response |
| --- | --- | --- |
| The answer is not in the policies | "Not covered, contact HR" | D1 instruction; G03 has 2 such cases |
| The agent opens the wrong document | Wrong or "not covered" answer | G03 records which documents were opened; triggers P2-1 |
| The model is unavailable or rate-limited (429) during the demo | `adk web` shows an error | Rehearse the day before; G03 keeps saved answers as a fallback slide |

## 7. Open decisions

- **O1, blocks the demo:** Does the company allow sending internal HR policies
  to the Gemini API (paid tier) or to Vertex AI? Settled by the user or IT
  before G02's first live call. If only Vertex is allowed, add about 0.5–1 h
  for GCP project setup to G02.
- **O2:** Is the demo date 2026-10-16?
- **O3:** Are any of the 30 PDFs scanned? G01 will answer this.

Next prompt:

```text
/adk-engineer Carry out docs/tickets/hr-policy-qa/G01-extract-policies.md. Read its design and plan,
use its primary and supporting skills, run its verification locally,
fill in the Evidence section and set status. Leave changes uncommitted.
```
