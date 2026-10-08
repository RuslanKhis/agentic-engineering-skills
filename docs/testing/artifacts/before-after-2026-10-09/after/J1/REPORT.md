# REPORT: ADK system-designer session (customer-support agent)

## 1. Skills invoked and reference files opened, in order

Skills invoked: `adk-system-designer` (via `/adk-system-designer`). No other
skill was invoked. Specialist files were read directly as references.

Files opened, in order (all under `.claude/skills/`):

1. `adk-system-designer/SKILL.md` (loaded by the invocation)
2. `adk-system-designer/references/design-decisions.md` (required by SKILL.md:69)
3. `adk-system-designer/references/failure-review.md` (required by SKILL.md:69)
4. `adk-system-designer/references/gcp-decisions.md` (service selection)
5. `adk-system-designer/references/implementation-handoff.md` (plan contract)
6. `adk-system-designer/assets/implementation-plan-template.md`, `system-design-template.md`, `ticket-template.md`
7. The first 12 lines of every specialist's `references/compatibility.md`, to find the ADK version baseline (SKILL.md:162)
8. `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json` (SKILL.md:165)
9. `adk-agent-interoperability/references/compatibility.md` lines 1–60 (A2A version floors)
10. `adk-agent-interoperability/references/a2a-contracts.md` (all 204 lines)
11. `adk-system-designer/references/runtime-and-delivery.md` (trigger: continuity during weekly releases)

I did not open `adk-release-engineering/references/*` beyond the compatibility
header. The release design (D10) relies on the designer's runtime-and-delivery
summary.

## 2. Tickets: specialist chosen and why

The user did not ask for tickets, so none were written. The plan uses goals
instead, each with a primary skill:

| Goal | Primary specialist | Why |
| --- | --- | --- |
| G01 | `adk-model-and-output-contracts` | The core risk is schema-validated triage output with a refusal shape and pinned models |
| G02 | `safe-api-tool-calls` | Exactly-once refunds: idempotency keys, uncertain outcomes, reconciliation |
| G03 | `adk-memory-architecture` | Governed KB retrieval with release promotion and language filtering |
| G04 | `adk-agent-interoperability` | Consuming the Java team's agent over A2A with `RemoteA2aAgent` |
| G05 | `adk-workflow-design` | Code orchestration around reader agents |
| G06 | `deploy-adk-on-google-cloud` | Ingress path |
| G07 | `adk-operational-guardrails` | Approvals and budgets |
| G08 | `adk-release-engineering` | Weekly release gate, canary and rollback |

G02 is the recommended next goal. It covers the money invariant, needs no model
and no google-adk import, and is runnable offline.

## 3. Files changed, and what was not finished

Created:

- `docs/architecture/support-agent.md`: the draft system design (357 lines).
  It covers:
  - the journey and the scope gate;
  - a Q1–Q14 question log with assumed PO answers;
  - invariants I1–I9 and targets T1–T2;
  - a mermaid component diagram and the success sequence;
  - decisions D1–D12 written as requirement → choice → reason → tradeoff → verification;
  - model-facing contracts, data and authority, security posture, budgets;
  - the failure table and open decisions OD1–OD6.
- `docs/plans/support-agent.md`: the implementation plan (341 lines). It
  contains the implementation map, goals G01–G08 (G01–G05 detailed, G06–G08
  coarse), run prompts and a resume section.
- `REPORT.md`: this file.

Not finished or not done:

- **No implementation.** This was by instruction.
- **No tickets.** They were not requested.
- **Provider facts were not verified.** Network access was off for this
  session. Unverified items: Vertex EU model availability and prices, Gmail
  push residency, Cloud Tasks semantics, the embedding model ID. All are marked
  as open decisions or verification items.
- **Every product-owner answer is assumed.** The design is marked **draft**.
- **Length.** The documents are longer than the "two to four pages" pilot
  guidance (SKILL.md:65). The design runs to about 6–7 printed pages because
  refunds and A2A both brought in failure rows.

## 4. Checks run and not run

Run:

- A relative-link check over both documents: all links resolve.
- Line counts.
- `git status`: only `docs/` and `REPORT.md` were added, plus the pre-existing
  untracked `.claude/` and `skills-lock.json`.

Not run:

- No application tests exist, because there is no code.
- Nothing that imports `google.adk` could run (not installed). Every ADK
  signature in the design (`RemoteA2aAgent` parameters, `DatabaseSessionService`,
  `RunConfig.max_llm_calls`) is source-verified by the specialists, not
  executed.
- No cloud, network or pricing lookups.
- The interoperability skill's `agent_card_check.py` was not run: there is no
  card from the billing team.
- The lifecycle-table audit helper was not run.

## 5. Friction log

| # | Moment | Kind | Pointer |
| --- | --- | --- | --- |
| F1 | SKILL.md says to let the user answer before settling material product choices and to ask one to three questions per turn. The session rules say the user is unavailable. The only bridge is the one-pass-draft sentence. I had to decide on my own to put a "question log with assumed answers" in the design. The skill has no pattern for recording questions that were asked but never answered. | Instruction assumed something I could not provide | `.claude/skills/adk-system-designer/SKILL.md:48-50`, `:91` |
| F2 | The scope gate was genuinely helpful. It made me ask whether "two-week budget" meant the design or the build, which set the pilot size and the deferred-controls table. | Helpful | `.claude/skills/adk-system-designer/SKILL.md:52-66`; `references/design-decisions.md:26-55` |
| F3 | The pilot is told to be "roughly two to four pages", yet the template asks for about ten sections plus a failure table, and the brief involves money and a cross-team peer. I could not satisfy both, and went over length. | Heavier than needed / conflicting | `SKILL.md:65`; `assets/system-design-template.md:1-131` |
| F4 | "Check service availability, regions, limits and prices … cite sources" cannot be followed offline. The skill says to keep such decisions provisional (useful), but the cost section ends up symbolic. | Assumed network access | `SKILL.md:169-171`; `references/gcp-decisions.md:35-50` |
| F5 | The ADK version to assume conflicts across skills. SKILL.md says to use the specialists' baseline (2.8.0). The interoperability compatibility file says to prefer 2.10/2.11 for A2A. I recorded 2.8.0 as the working pin and made the upgrade decision OD4. | Unsure what to do | `SKILL.md:160-164`; `adk-agent-interoperability/references/compatibility.md:40-49` |
| F6 | The dated model lifecycle table was very helpful. It showed that ADK's default judge `gemini-2.5-flash` retires on Vertex on 2026-10-20, 11 days from the session date. I found the judge default only by grepping `adk-release-engineering/references/compatibility.md:12`. The designer skill never points there. | Helpful, but reached by luck | `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:22`; `adk-release-engineering/references/compatibility.md:12` |
| F7 | The lifecycle table covers Gemini text models only. There is no embedding-model entry, so the retrieval design (D7) has no dated source for its embedding model ID. | Gap | `adk-model-and-output-contracts/assets/model-lifecycle-2026-10-01.json:11-28` |
| F8 | The trifecta rule and "peer messages are data" decided the main architecture: a reader/writer split, no model tools, refunds in code. Very helpful, and quick to apply. | Helpful | `references/design-decisions.md:180-194`; `adk-agent-interoperability/references/a2a-contracts.md:116-127` |
| F9 | The A2A pause semantics (`input-required`) assume a live controlling user. In an email pipeline nobody is live, and neither skill says what to do then. I chose "flag for staff". | Instruction assumed something absent | `adk-agent-interoperability/references/a2a-contracts.md:78-81`; `references/failure-review.md:39` |
| F10 | Five references plus templates (about 1,000 lines) had to be read before writing started, two of them mandatory. That is reasonable for a money-moving design, but `design-decisions.md` (341 lines) has no "which sections apply to my journey" index. I read it end to end. | Reference read before useful work | `SKILL.md:69-71`; `references/design-decisions.md:1-6` |
| F11 | Plan template: every goal needs about 11 fields. Filling them for 8 goals was the heaviest step. The skill allows leaving later goals coarse, and I did that for G06–G08. | Heavier than needed (mitigated) | `assets/implementation-plan-template.md:34-58`; `references/implementation-handoff.md:86-90` |
| F12 | The closing-message instruction and the example prompt made the handoff unambiguous. | Helpful | `SKILL.md:237-246` |
| F13 | It was unclear whether `.claude/skills/*/agents/openai.yaml` mattered. I ignored it. | Minor uncertainty | `.claude/skills/adk-system-designer/agents/openai.yaml` |

## 6. Rating and the three changes that would help most

**Rating: 4/5.** The path from request to an architecture with enforcement
points was clear, and the cross-cutting rules (trifecta, operation identity,
release unit, lifecycle table) produced substantive decisions. Friction came
from the unavailable user, offline provider checks, and length guidance that
conflicts with the template.

The three changes that would help most:

1. **A "user unavailable" mode in SKILL.md.** It would record every question as
   `question → decision it changes → assumed answer → confirm-by`, with a
   template section for it, and keep the document marked draft.
2. **A short index at the top of `design-decisions.md`** mapping journey
   features to sections. For example: money/writes → External effects;
   untrusted input → Identity/trifecta; remote team → Topology. Also a
   pilot-sized variant of the design template that fits two to four pages.
3. **Point the designer at the specialists' known version conflicts and
   dangerous defaults.** Examples: the A2A version floor, and the default judge
   `gemini-2.5-flash` retiring 2026-10-20. Ideally this would be a single
   "pins and defaults to check" table the designer reads, and the lifecycle
   table would also cover embedding models.

## 7. Next prompt the skills told the user to type

The skill's own example (SKILL.md:242), verbatim:
"/adk-engineer Carry out G01 from docs/plans/<topic>.md."

The concrete prompt I wrote into the plan, following the template at
`assets/implementation-plan-template.md:89-95`, for the next ready goal:

```text
/adk-engineer Carry out G02 (Execute an eligible refund exactly once) from docs/plans/support-agent.md.
Read docs/architecture/support-agent.md and preserve its accepted decisions.
Use safe-api-tool-calls with adk-operational-guardrails.
Work locally against a fake Payments server, verify the boundary, lost-response,
concurrency, approval-binding and kill-switch cases, and update
the plan with actual evidence and remaining blockers.
```
