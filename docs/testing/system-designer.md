# System designer checks — 25 September 2026

The new [adk-system-designer](../../skills/adk-system-designer/SKILL.md) turns
the author's supplied system-engineering document into a requirements and
architecture conversation. Its central design rule is to connect each important
product promise to an invariant, an enforcing component, a failure outcome and
planned evidence. Its references cover the decisions relevant to that journey;
they do not require every application to use every ADK or GCP feature.

## Initial package and offline checks

Ran `python scripts/check_repo.py` in a fresh temporary environment on macOS
with Python **3.12.9**, PyYAML **6.0.3**, markdown-it-py **4.0.0** and
pytest **9.1.1**, using the repository's pinned maintainer requirements.
ADK and the optional cloud SDKs were not installed in that environment.

| Check | Result |
| --- | --- |
| Skill packages | **13 validated**, zero errors or warnings |
| Evaluation input structure | **29 activation cases and 8 contextual scenarios valid** |
| Repository checker regressions and offline helper suites | **395 passed, 59 optional SDK checks skipped**; process exit 0 |
| Skill-creator package validator | New designer passed |

The [full check output](artifacts/system-designer/check-repo.txt) records the
suite results. These totals cover the repository, not new executable code in
the designer: this skill contains instructions, references and a document
template. The 59 skips comprise 3 auth, 43 optimisation and 13 data-protection
checks. Other optional runtime suites remain outside the offline runner's tier;
see the [coverage guide](skill-quality.md).

Five activation cases and two contextual scenarios were added, including
near-misses for focused memory work, an already-approved deployment, and a
non-ADK application. Checking their structure does **not** evaluate model selection.

## Initial independent behavioral trials

Two fresh Codex subagents received the skill path and synthetic requests, with
access to its bundled resources and public documentation. They did not receive
the evaluator's expected outcomes or source analysis. Outputs were restricted
to documentation in temporary directories: no application implementation,
cloud changes, paid provider calls or real-user question prompts.

The executing model was the host's inherited model; no model override was set.
These were explicit-invocation trials during skill development, not a benchmark
against another skill or a version-pinned model evaluation. Reference guidance
was refined during development, and a final read-only review checked the package
and its README/router integration.

Read the [exact task inputs](artifacts/system-designer/prompts.md).

### Requirements conversation

The first request described a customer-support application without specifying
users, data sources or escalation policy. The agent's
[first response](artifacts/system-designer/conversation/turn-1.md) asked three
questions about those decisions before selecting services. The evaluator then
supplied the existing React/OIDC/PostgreSQL stack, an escalation API with an
unverified deduplication contract, and provisional workload and budget targets.

The [resulting design](artifacts/system-designer/conversation/design.md) and
[reply](artifacts/system-designer/conversation/turn-2.md) were reviewed against
that request:

| Observation | Assessment |
| --- | --- |
| Adaptive discovery | Three relevant questions with reasons; no upfront exhaustive questionnaire or premature service list |
| Minimal architecture | One ADK application, existing stack reused, deterministic authority and confirmation boundaries |
| Ambiguous external writes | Reference search was not treated as safe replay; one local dispatch and explicit uncertain/manual recovery were retained pending provider evidence |
| Cost and latency | Numbers labelled as proposals or illustrations; dated sources, excluded costs and unmeasured targets disclosed |
| Deliverable and scope | Draft architecture, open decisions, failure paths and planned acceptance cases; no claim of implementation or executed application tests |

### One-pass architecture review

The supplied proposal included browser-controlled customer IDs, a fresh refund
key for every retry, session persistence mistaken for operation recovery,
background receipt persistence, misleading UI completion, process-local locks,
a billing alert described as a cap, and deletion racing with queued retries.

The [revised design](artifacts/system-designer/review/design.md) was reviewed:

| Observation | Assessment |
| --- | --- |
| One-pass request | Produced a draft with assumptions without requiring an interview; preserved React, OIDC and PostgreSQL |
| Authorization and duplicate effects | Derived trusted user scope; separated operation identity from attempts; bound confirmation and replay to the exact payload and verified provider contract |
| Recovery and completion | Durable ledger/dispatch/receipt boundaries; session history and final-response events did not establish business success |
| Concurrent workers and erasure | Shared reservations/coordination; deletion generations and late-writer checks; unresolved immediate-erasure scope remained explicit |
| Capacity and spending | Conditional arrival-rate arithmetic and downstream limits; billing observation separated from application enforcement |
| Evidence and handoff | Planned verification and implementation slices; provider/release gaps were not presented as proven guarantees |

Both designs are illustrative drafts that need application-specific review.
Their service references and price examples are dated observations, not enduring
defaults for the skill. The final independent package review found one factual
wording issue: Cloud Billing now distinguishes alerts-only budgets from
spend-cap features. The reference was narrowed and requires verification of any
spend-cap coverage before relying on it.

## Conversation pattern refinement

The interaction was then refined to explain consequential decisions through
**requirement → design choice → reason → tradeoff → verification**, in natural
prose or a compact row. The design template records the same links, with decision
status and revisions explicit. The references also distinguish technical
correctness, model quality and evidence of improved user outcomes.

A third fresh Codex subagent received the revised skill and a synthetic
lesson-planning request, then a reply that added shared editing. The same
documentation-only constraints applied, with no expected answer supplied.
The [inputs](artifacts/system-designer/prompts.md#interaction-refinement)
and both responses are saved:

- [Turn 1](artifacts/system-designer/interaction/turn-1.md) connected reopening
  an edited plan to an application-owned record, explained its revision/access
  overhead, proposed a restart/isolation check, and asked about explicit saving.
- [Turn 2](artifacts/system-designer/interaction/turn-2.md) accepted the save
  choice, revised owner-only access for named collaborators, explained atomic
  revision checks and the manual-conflict tradeoff, and updated the planned
  checks for competing saves and revoked access. It asked one relevant next
  question without expanding into a full architecture or implementation.

The responses passed this qualitative review. This trial demonstrates the
explanation and revision behavior in one short conversation; it does not test
the proposed application or establish product benefit.

After the refinement, all **13 packages** and the skill-creator validation
passed again. Evaluation structure passed with **29 activation cases and 9
contextual scenarios**, and the **5 repository-runner regression tests** passed.
The new scenario covers a changed collaboration requirement; the two existing
design scenarios now check decision explanations and appropriate evidence.
The full helper-suite results above remain those of the initial run.

## Complete source coverage review

A subsequent [source coverage audit](../research/system-designer-source-coverage.md)
reviewed all 1,058 lines of the supplied system-design document. Its map records
retained principles, strengthened contracts and the implementation detail left
with existing specialists. The designer gained a conditional runtime/delivery
reference plus explicit approval, credential, policy, control-store and analytical
contracts. Coverage is a review of instructions, not proof of implemented guarantees.

A fourth fresh Codex subagent reviewed a synthetic reporting architecture using
the skill directly. It received the [raw proposal](artifacts/system-designer/prompts.md#runtime-and-release-review)
without grading expectations. Its [response](artifacts/system-designer/runtime/review.md)
was checked for these behaviors:

| Observation | Assessment |
| --- | --- |
| Context, retention and result storage | Distinguished context trimming from deletion; retained protocol pairs; bounded payloads and proposed durable, owner-scoped downloads |
| Public delivery | Used exact call identities, truthful terminal/partial outcomes, bounded buffers and real browser-path checks |
| Recovery and concurrency | Separated reconnect from resubmission, recommended shared coordination and stale-owner fencing, and retained reservations for unresolved remote work |
| Release continuity | Required mixed-version storage compatibility, drain and rollback evidence |
| Explanation and scope | Connected decisions to requirements, costs and planned checks; provider/version facts stayed provisional, with no code, external calls or executed application-test claims |

This qualitative trial passed for the reviewed concerns. It does not exercise
every addition from the source audit, including delegated OAuth revocation and
historical privacy-policy migration. All **13 packages** and the new skill's
package validation passed after the audit; evaluation structure is now **29
activation cases and 10 contextual scenarios**. No helper code changed.

## Practical implementation handoff

The designer now maps recommendations to ADK/application components, integration
points, GCP responsibilities and primary skills. Its plan template records goals,
dependencies, acceptance, blockers, actual evidence and a continuation prompt.
The router can resume a named goal while preserving accepted decisions.

A fifth fresh subagent received the [handoff request](artifacts/system-designer/prompts.md#practical-implementation-handoff)
with an agreed React/OIDC/PostgreSQL/Cloud Run stack, no selected ADK version or
cloud credentials, and an out-of-scope future group-preference question. It had
only the brief, skill and bundled resources; application code and planning-tool
execution were outside the trial. It produced:

- [Architecture](artifacts/system-designer/handoff/docs/architecture/support-assistant.md)
- [Goal plan and continuation prompt](artifacts/system-designer/handoff/docs/plans/support-assistant.md)
- [User-facing reply](artifacts/system-designer/handoff/response.md)

| Observation | Assessment |
| --- | --- |
| Implementation mapping | Named profile API/repository, trusted invocation-context loader, agent adapter and stream projection; mapped them to accepted infrastructure and relevant specialists |
| Grounding | Proposed modules were distinguished from inspected code; exact SDK interfaces and the unchosen version remained verification work |
| Useful first goal | G01 specified save, real local restart, new-conversation use, forget, stale-write rejection and cross-user denial with a controlled adapter |
| Dependencies and scope | ADK compatibility was a separate discovery goal; hosted work required a later target/authorization; future group preferences did not block individual pilot work |
| Resumption | Stable goal IDs, linked decisions, primary/supporting skills, acceptance cases, proposed public test boundaries and a copyable continuation prompt were present |
| Optional workflows | Suggested direct or spec/ticket continuation; Wayfinder remained decision planning rather than an automatically executed build map |

The plan passed this qualitative review for practical handoff. Its local goal
still requires access to the real application's repository and test environment.
A controlled adapter proves the proposed local pipeline only when implemented
and tested; it does not establish real ADK integration or model quality.

Matt Pocock workflow boundaries were checked against installed and current
upstream instructions on 25 September 2026; the
[integration guide](../integrations/design-to-implementation.md) cites the sources.
No native Wayfinder map, spec/ticket conversion or downstream implementation was
executed in this trial. Two new authored scenarios cover practical handoff and
router continuation, bringing fixtures to **29 activation cases and 12 contextual
scenarios**. Their structure passed, all **13 packages** passed validation, and
the **5 repository-runner regression tests** passed. No helper code changed.

## Limits and reproduction

- These five qualitative trials do not establish reliable natural activation,
  all-task performance or superiority to another architecture workflow.
- No new-package installation or trial in Claude Code, Gemini CLI or Antigravity
  was run here. Earlier installation results cover the previous 12-skill set.
- No application code, ADK runtime integration, live business provider,
  deployed service, latency target or budget was validated by these designs.
- Saved outputs preserve the generated text; the temporary design link in the
  conversation's second reply was normalized to its adjacent saved file. The
  handoff plan's temporary absolute paths were normalized to paths relative to
  that example's root; its existing document links are preserved.

To reproduce, install the maintainer dependencies and run the repository check
command. For behavior, start a fresh coding-agent session with the designer
available, supply the recorded first request, then its recorded follow-up after
the questions. Run the review prompt in a separate fresh session. Assess the
result against the stated requirements and boundary cases, recording the client,
model, skill revision, outputs and any repairs. Keep expectations out of the
executing agent's prompt.
