# Journey report: J1 greenfield — `/adk-system-designer` for a customer-support agent

Skill root referenced below: `/Users/ruslankhissamiyev/Documents/Coding Projects/skills/agentic-engineering-skills/skills/` (abbreviated `skills/`).
Project root: `/private/tmp/claude-501/-Users-ruslankhissamiyev-Documents-Coding-Projects-skills-agentic-engineering-skills/25bf1de8-6b74-48d2-bd2d-fbf8580f5e5e/scratchpad/journeys/j1-greenfield/`

## 1. Files created

| File | Lines | Content |
| --- | --- | --- |
| `docs/architecture/customer-support-agent.md` | 252 | System design: purpose/journey, scope gate + deferred controls, 9 invariants, component + sequence diagrams (mermaid), 10 decisions (D1–D10) with status, model-facing contracts, data/authority table, security-posture (trifecta) table, budgets, failure/recovery table, verification + observability + release, open decisions |
| `docs/plans/customer-support-agent.md` | 177 | Implementation plan: destination, proposed module layout, implementation map (decision → component → GCP → skill), goals G00–G08 with dependencies and a 10-day schedule for two engineers, detailed G00–G06, reviewer reading list, open decisions, "Resume here" with continuation prompt |
| `REPORT.md` | — | this file |

No code, dependencies or cloud resources were created (the request said "do not implement").

## 2. Questions asked, in order (and the product-owner answers I supplied)

| # | Turn | Question (abridged) | Answer supplied |
| --- | --- | --- | --- |
| Q1 | 1 scope gate | Artifact type: internal-staff pilot or customer-facing production from day one? | Pilot (4 weeks drafts for staff) → production |
| Q2 | 1 | Money: monthly model-spend allowance; existing GCP footprint and Cloud Run experience? | ≤ EUR 1,500/month; existing GCP org; team runs Cloud Run |
| Q3 | 1 | Does the two weeks cover design plus a first build slice, or design only? | Design (2 days) + first build slice, 2 engineers |
| Q4 | 2 | Who acts on output: direct replies to customers, or drafts for a human in the helpdesk? | Drafts into Freshdesk, human sends; auto-send later for low-risk |
| Q5 | 2 | Volume, languages, regions? | ~2,000 emails/day, EU, EN/DE/FR |
| Q6 | 2 | Refund rules: thresholds, approvers, per-order limits? | < EUR 200 auto-approvable if order < 30 days and not refunded; above needs a support lead; one refund per order |
| Q7 | 3 | What exists: login, databases, orders/refunds API, KB location and format, email ingress? | Workspace OIDC; Cloud SQL PostgreSQL; Orders REST API with idempotency key; 1,200 Markdown KB articles in Git → CMS; Freshdesk webhook JSON |
| Q8 | 3 | Billing team's Java agent: protocol exposed, service auth, answers only or actions? | A2A agent card; SA ID-token auth; answers invoice/VAT/payment, can open a billing ticket, cannot refund |
| Q9 | 4 | Baseline, success measure, unacceptable outcomes? | 9 h median first response, 40 emails/agent/day; ≥ 60 % drafts accepted, < 1 h; unacceptable: wrong/double refund, cross-customer data, refund by instruction in email |
| Q10 | 4 | Data residency, retention, erasure? | EU only, Vertex AI in EU; 90-day retention; erasure within 30 days |
| Q11 | 5 | What "no regressions" means: gate contents, sign-off, gate cost/time, existing labelled data? | No eval set; 500 consent-cleared labelled tickets available; PR tests + judge eval + lead reviews 50 canary drafts; ≤ EUR 50, ≤ 30 min |
| Q12 | 5 | Hosting: Cloud Run or Agent Runtime; constraints? | Cloud Run preferred; Vertex AI fine |
| Q13 | 6 | Accept reader/actions split with policy module in code and A2A peer as data? | Accepted |
| Q14 | 6 | Phase 1: human approves every refund, auto-execution < 200 deferred? | Accepted |

## 3. Skills and reference files read, in order

1. `Skill: adk-system-designer` → `skills/adk-system-designer/SKILL.md` (233 lines)
2. `skills/adk-system-designer/references/design-decisions.md` (341 lines)
3. `skills/adk-system-designer/references/runtime-and-delivery.md` (117)
4. `skills/adk-system-designer/references/gcp-decisions.md` (72)
5. `skills/adk-system-designer/references/implementation-handoff.md` (130)
6. `skills/adk-system-designer/references/failure-review.md` (71)
7. `skills/adk-system-designer/assets/system-design-template.md` (131)
8. `skills/adk-system-designer/assets/implementation-plan-template.md` (92)
9. `skills/adk-agent-interoperability/references/compatibility.md` (first 40 lines, to anchor an ADK version — not required by the skill, prompted by implementation-handoff.md:63)

Total: ~1,190 lines of guidance read before the first design question was asked; no other skills were invoked (the designer explicitly says it needs none).

## 4. Friction log

Format: **[type]** observation — pointer. Types: UNSURE (did not know what to do next), READ-FIRST (had to read before anything useful happened), ASSUMES (assumes something a greenfield user cannot supply), MAINTAINER (talks to the skill author/maintainer, not the user), HEAVY (heavier than needed), HELPFUL.

1. **[READ-FIRST]** The skill body is 233 lines and names six further files to read (design-decisions at SKILL.md:74, :98, :117; runtime-and-delivery :140; gcp-decisions :147; implementation-handoff :165; failure-review :183; both templates :199–200). For a "production service that changes money" design-decisions.md:35 says "needs most of this file", so in practice all ~950 reference lines must be read before the document can be written. None of it is wasted, but nothing user-visible happens for the first several minutes of a session. — `skills/adk-system-designer/SKILL.md:74-200`
2. **[HELPFUL]** The scope gate (SKILL.md:52-61) is the single best idea in the skill: two of three answers were already in the request, so only one real question (artifact type) was needed, and the "deferred controls" table it mandates kept the document honest about Phase 1 vs Phase 2. — `SKILL.md:52-61`, `references/design-decisions.md:26-59`
3. **[UNSURE]** The scope gate's first question ("How much time and money") conflates two things; the user had given time but not money. I had to decide whether to re-ask time. A user who typed "two-week budget" may feel the skill did not read the prompt. Suggest: "ask only the gate answers the request does not already contain". — `SKILL.md:55`
4. **[UNSURE]** "Use the host's question interface if available" (SKILL.md:48) — in a Claude Code session there is no `AskUserQuestion` tool in this toolset; the skill does not say what the fallback cadence should be (one message per question? a batch?). I batched 2–3 per turn as SKILL.md:47 suggests, which worked, but a first-time user sees a wall of questions. — `SKILL.md:47-50`
5. **[ASSUMES]** "Check version-dependent ADK interfaces against the target's installed/deployed versions and current official documentation... cite sources and dates" (SKILL.md:152-154) and gcp-decisions.md:35-41. A greenfield project has no installed version and this session had no network. The skill's own escape hatch (SKILL.md:155-157, "keep those decisions provisional and name the exact verification needed") is good, but it is buried after the demand; I only found an ADK version anchor by chasing implementation-handoff.md:63 into another skill's `compatibility.md`. Suggest the designer surface "the collection was read against google-adk X.Y" itself. — `SKILL.md:152-157`, `references/gcp-decisions.md:35-41`, `references/implementation-handoff.md:62-66`
6. **[MAINTAINER]** "This skill does not require other skills, the book, a starter repository or cloud access" (SKILL.md:23). "The book" means nothing to a new user; it is a note from the author to themselves/other maintainers. Similarly "Interface names were checked on 25 September 2026; skill names in the table were checked against the installed collection on 8 October 2026" (implementation-handoff.md:62-64) and "Reviewed upstream workflow references on 25 September 2026" (:127) are provenance notes a user never acts on. — `SKILL.md:23`, `references/implementation-handoff.md:62-66,127-130`
7. **[MAINTAINER/HEAVY]** The whole "Continue through the user's chosen workflow" section (implementation-handoff.md:95-125) about Wayfinder, `to-spec`, `to-tickets`, `implement` and Agents CLI (SKILL.md:220-228) is irrelevant to a user who has none of those installed; it is ~35 lines of optional-tooling discussion in the critical path of a mandatory read. — `references/implementation-handoff.md:95-130`, `SKILL.md:220-228`
8. **[HEAVY]** design-decisions.md is a 341-line checklist written as dense imperative prose ("Specify...", "Trace...", "Separate..."). Each sentence is correct, but there is no hierarchy of "must for a money-moving system" vs "if applicable", so the reader must triage the whole file. The §"When the application answers analytical questions" (:325-341) was irrelevant here and had to be read to know that. — `references/design-decisions.md:124-341`
9. **[HELPFUL]** The lethal-trifecta rule (design-decisions.md:180-194) and the failure-review table (failure-review.md:23-43) directly produced the two most important design decisions (D1 split, D2 separate actions service) and the §7 failure table. The "Requirement → choice → reason → tradeoff → verification" chain (SKILL.md:103-116) made the decision table easy to write and easy to review. — `references/design-decisions.md:180-194`, `references/failure-review.md:23-43`
10. **[HELPFUL]** The templates are well-shaped; the plan template's "Resume here" block with a copyable continuation prompt (implementation-plan-template.md:76-89) gives the user a concrete next step, which many design skills lack. — `assets/implementation-plan-template.md:76-89`
11. **[UNSURE]** SKILL.md:197 says to use `docs/architecture/<topic>.md` and `docs/plans/<topic>.md` "when none exists", but does not say whether to also record the conversation (the Q&A) anywhere. I folded it into the design's "User-accepted decisions" paragraph; a reviewer may want the transcript. — `SKILL.md:195-201`
12. **[HEAVY]** The design template's "Model-facing contracts" table (system-design-template.md:53-59) and the plan template's implementation map both require naming the implementing specialist skill per row. For a reviewer who is not a skills user, skill names (`adk-tool-interface-design` etc.) are noise in an architecture document. They belong in the plan only. — `assets/system-design-template.md:53-59`
13. **[ASSUMES]** "Record what actually ran when a goal is later completed" and "evidence tier" fields assume a long-lived session/tracker; harmless but they add fields a two-week team must maintain by hand. — `SKILL.md:214-215`, `assets/implementation-plan-template.md:48-49`
14. **[UNSURE]** The skill never says how long the document should be for a given scope beyond "a four-hour assignment gets ... ten minutes" (SKILL.md:62-64). For a two-week, money-moving pilot I produced 252 + 177 lines; I do not know whether the author considers that right-sized. A rough table (assignment / pilot / production → page counts) would remove the guess. — `SKILL.md:61-66`
15. **[HELPFUL]** "A service already present is a constraint to evaluate, not an automatic choice" (SKILL.md:32-33) and "Compare only credible alternatives, including ordinary code or one agent when sufficient" (SKILL.md:120-121) stopped me from adding Memory Bank, Vertex AI Search and Agent Runtime by default; each landed in the deferred-controls table with a reason instead. — `SKILL.md:30-33,120-123`
16. **[MAINTAINER]** Trailer "Independent community project; not affiliated with or endorsed by Google." (SKILL.md:233) is a license/legal line, not an instruction; fine, but it is loaded into every session's context. — `SKILL.md:233`
17. **[UNSURE]** The base directory reported on launch was `.claude/skills/adk-system-designer` (a symlink) while the task said skills live under `skills/`; harmless, but file:line pointers depend on knowing they are the same. — `.claude/skills/adk-system-designer -> ../../skills/adk-system-designer`

## 5. Rating and the three most valuable changes

**Rating: 3 / 5 for frictionlessness.** The output quality the skill drives is high (clear invariants, structural security split, failure table, resumable plan), and the scope gate is excellent. The cost is a long silent reading phase, reference prose with no "must / if applicable" triage, and maintainer-facing notes and optional-workflow material sitting in the mandatory path.

Three changes that would most improve it:

1. **Split each reference into a short "always" core and an "if applicable" tail, and tell the designer which tail to read by artifact type.** E.g. design-decisions.md → 60 lines mandatory (outcome, trifecta, topology, write/recovery, release pinning) + topic appendices (analytics, OAuth, memory). Expected effect: halve the read-before-first-question time without losing the production-grade checks.
2. **Make the scope gate request-aware and give it a fallback cadence.** "Ask only the gate answers missing from the request; in plain chat ask at most two questions per turn and show the reasoned default you will take if unanswered." Also ship the ADK/collection version anchor ("read against google-adk 2.8.0") in the designer itself so a greenfield user is not asked to verify against an installation that does not exist.
3. **Move maintainer and optional-tooling text out of the user path.** Drop "the book"/starter-repo sentence, move the Wayfinder/to-spec/Agents-CLI section to a separate `references/workflows.md` that is read only if such a skill is installed, and move the dated "checked on ..." provenance lines to a CHANGELOG. Keep skill names in the plan's implementation map but out of the reviewer-facing design template.

## 6. The exact "next prompt" the design told the user to type

From `docs/plans/customer-support-agent.md`, section "Resume here":

```text
Use adk-engineer to continue G01 "Reader + policy gate produce a validated assessment offline" from docs/plans/customer-support-agent.md.
Read docs/architecture/customer-support-agent.md and preserve its accepted decisions (D1, D2, security posture in 5.1).
Use adk-workflow-design as primary and adk-tool-interface-design, adk-model-and-output-contracts and adk-agent-security as supporting skills.
Work locally only (no cloud, no paid model calls), verify the G01 acceptance cases with an offline pytest suite, and update the plan with actual evidence and remaining blockers.
```
