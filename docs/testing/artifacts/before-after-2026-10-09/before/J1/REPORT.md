# REPORT — ADK customer-support agent design session (2026-10-09)

## 1. Skills invoked and reference files opened, in order

1. Skill `adk-system-designer`, invoked by the user via `/adk-system-designer`.
   Its SKILL.md was loaded with the invocation.
2. `.claude/skills/adk-system-designer/references/design-decisions.md` (all 341 lines)
3. `.claude/skills/adk-system-designer/references/failure-review.md`
4. `.claude/skills/adk-system-designer/references/gcp-decisions.md`
5. `.claude/skills/adk-system-designer/references/implementation-handoff.md`
6. `.claude/skills/adk-system-designer/references/runtime-and-delivery.md`
7. `.claude/skills/adk-system-designer/assets/system-design-template.md`
8. `.claude/skills/adk-system-designer/assets/implementation-plan-template.md`
9. `.claude/skills/adk-agent-interoperability/references/topology.md` (lines 1–60) and
   `compatibility.md` (lines 1–40). I read these to ground the Java billing peer (A2A)
   decision and the ADK version the skills were written against.
10. `.claude/skills/adk-agent-interoperability/references/remote-failures.md`
    (grep only: headings and the timeout/retry rows)
11. `.claude/skills/adk-engineer/SKILL.md` (first 5 lines only, to confirm the
    continuation entry point) and `adk-system-designer/agents/openai.yaml`
    (grep only)

No other skill was invoked through the Skill tool. No specialist skill was loaded
for implementation, because the request was design-only.

## 2. Tickets: specialist chosen and why

No tickets were created; the request was design-only. The plan does assign a
primary specialist to each goal:

- **G03 (next ready): `safe-api-tool-calls`.** The most consequential invariant is
  "one logical refund produces at most one provider refund, and uncertain writes
  are reconciled, never re-dispatched". That is this skill's scope (idempotent
  writes, ambiguous outcomes). `adk-operational-guardrails` supports it for the
  caps and the kill switch.
- **G02: `adk-workflow-design`.** Ordinary code orders the steps: reader, then
  code router, then composer.
- **G05: `adk-agent-interoperability`.** The billing agent sits across a team and
  language boundary (Java, remote A2A).
- **G04: `adk-memory-architecture`.** It covers KB retrieval.
- **G08: `adk-agent-security`.** It covers the trifecta and the adversarial suite.
- **G07: `adk-release-engineering`.** It covers the weekly gate, manifest and canary.
- **G06: `deploy-adk-on-google-cloud`.**
- **G01: `adk-agent-evaluation`.**
- **G00: `adk-engineer`.** It is mixed discovery, routed per question.

## 3. Files changed, and what was not finished

Created:
- `docs/architecture/customer-support-agent.md` (268 lines). It is the design: the
  scope gate, a record of 17 design questions with assumed product-owner answers,
  invariants I1–I7, decisions D1–D11, model-facing contracts, data and authority,
  the security posture, budgets, the failure table, the verification and release
  gate, and open decisions OD1–OD6.
- `docs/plans/customer-support-agent.md` (153 lines). It is the plan: goals G00–G08
  with dependencies, the next ready goal and a continuation prompt.
- `REPORT.md` (this file).

Not finished, or deliberately left out:
- No code. This was a design-only request.
- Every product-owner answer is an **assumption**. The design is marked draft and
  no decision is user-accepted.
- Provider facts are not verified, because no network access was allowed: the
  pinned Gemini model ID, its EU availability, retirement date and prices; Cloud
  Tasks quotas; pgvector availability; ADK-version API behaviour. All of these are
  listed in design §9 and G00.
- Cost appears only as a symbolic formula, with no numbers.
- No sequence diagram for the failure paths. The failure table carries them.

## 4. Checks run and not run

Run:
- Relative-link check on both docs (shell loop). **Result: both links resolve.**
- A check that every ID cited (I1–I7, D1–D11, OD1–OD6) has a defining row in the
  design. **Result: all defined.**

Not run:
- All tests. No code exists, and `google.adk` is not installed, so any
  ADK-importing test **could not run**.
- Live model or evaluation runs, cloud lookups, and contract checks against the
  billing or payments teams. All of these were forbidden by the session rules or
  need external parties.
- Price and region verification (network forbidden).

## 5. Friction log

| # | Moment | Kind | Pointer |
| --- | --- | --- | --- |
| F1 | The skill says to let the user answer before a material product choice is settled. The user could not answer. I fell back to the one-pass-draft clause and marked every answer as a PO assumption. Neither SKILL.md nor the template has a place to record the questions asked; I added §3 "Design conversation record" myself | Instruction assumed something I could not provide | `.claude/skills/adk-system-designer/SKILL.md:50`, `SKILL.md:83`; `assets/system-design-template.md:3` (status only offers "user-reviewed") |
| F2 | The scope gate was immediately helpful: three questions that sized the document | Helpful | `SKILL.md:52-62` |
| F3 | "Two-week budget": the gate does not separate design time from build time. I had to choose (build time for a pilot) | Unsure | `SKILL.md:52-58`; `references/design-decisions.md:28-35` |
| F4 | I read about 950 lines of references plus templates before writing anything useful. design-decisions.md alone is 341 lines, and most of its analytical-SQL section did not apply. There is no "read this first for email/async back-office agents" path | Heavier than needed | `references/design-decisions.md:325-341`; `SKILL.md:117-145` |
| F5 | The proportionality examples are all about "assignment judged on predictions". The template's verification section asks for "the deliverable the evaluator will judge (predictions, exports, answers)", which fits poorly when the judged artifact is a design document | Instruction didn't fit | `references/design-decisions.md:46-55`; `assets/system-design-template.md:103-107` |
| F6 | The skill requires checking versions, regions and prices and citing dated sources. No network was available, so the provisional fallback applied. That fallback was clear and usable | Assumed unavailable capability; fallback helpful | `SKILL.md:152-158`; `references/gcp-decisions.md:35-50` |
| F7 | The lethal-trifecta rule directly produced the central decision: no model holds the refund write, and code decides | Genuinely helpful | `references/design-decisions.md:180-193` |
| F8 | Identity guidance assumes an authenticated user, a tenant and OIDC. Email is an unauthenticated channel, and the skill gives no guidance on sender verification (SPF/DKIM/DMARC) or on degrading to read-only. I designed D2 unaided | Gap | `references/design-decisions.md:168-172` |
| F9 | runtime-and-delivery.md is mostly browser streaming, which does not apply to async email. Its trigger list in SKILL.md made it unclear whether to read it. Only the release and observability parts were useful | Unsure / heavier | `SKILL.md:140-143`; `references/runtime-and-delivery.md:35-55` vs `:76-117` |
| F10 | The Wayfinder/Matt Pocock workflow section is irrelevant when those workflows are not installed, yet it is in the mandatory handoff reference | Heavier than needed | `references/implementation-handoff.md:95-130` |
| F11 | The handoff table plus the "supporting skills by boundary" paragraph made assigning a specialist per goal quick | Helpful | `references/implementation-handoff.md:19-51` |
| F12 | The designer gives no ADK version. I had to open the interop skill's compatibility file to learn that the skills were read against google-adk 2.8.0, and that `RemoteA2aAgent` defaults to a 600 s timeout (used in D5) | Reference read before useful work | `references/implementation-handoff.md:61-66`; `.claude/skills/adk-agent-interoperability/references/compatibility.md:3-8`; `.../remote-failures.md:31` |
| F13 | The continuation-prompt template gave an exact shape to fill in | Helpful | `assets/implementation-plan-template.md:83-89`; `SKILL.md:217` |
| F14 | The failure-review scenario table worked well as a checklist. Several rows (browser disconnect, forget/revoke) needed a "does not apply because" decision | Mostly helpful | `references/failure-review.md:21-43` |

## 6. Rating and top three changes

**Rating: 3 / 5.** The guidance is substantive and steered the key decisions well (F2, F7, F11, F13). The
friction was volume and fit: about 950 lines to read up front, assignment-flavoured
examples, and no path for an absent user.

Three changes that would help most:
1. **Support for an absent user.** Add a "questions asked / answer source
   (user, assumed, cited)" table to `assets/system-design-template.md`, and a status
   value "assumption-based draft" (F1).
2. **A reading map by application shape.** Split `design-decisions.md` and
   `runtime-and-delivery.md` into short topic files, with a one-line chooser in
   SKILL.md. For example: async back-office agent → external effects, identity,
   release; chat UI → browser contract (F4, F9).
3. **Guidance for unauthenticated channels.** Cover email, SMS and webhooks in
   the identity section: sender-verification signals and a verified-versus-
   unverified capability matrix. Also generalise the "deliverable the evaluator
   judges" wording beyond predictions (F5, F8).

## 7. Exact next prompt the skills told the user to type

The plan template (`assets/implementation-plan-template.md:83-89`) prescribes a
continuation prompt. Filled in as the skill instructs, it reads:

```text
Use adk-engineer to continue G03 "Refund policy and ledger, local" from docs/plans/customer-support-agent.md.
Read docs/architecture/customer-support-agent.md and preserve its accepted decisions (D3, D4, invariants I1, I2).
Use safe-api-tool-calls and adk-operational-guardrails.
Work within local code and a local PostgreSQL container only (no payments API, no cloud), verify the G03 acceptance cases, and update
the plan with actual evidence and remaining blockers.
```

The skill text itself has no literal, ready-to-type prompt, only that template with
placeholders.
