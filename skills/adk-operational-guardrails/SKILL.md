---
name: adk-operational-guardrails
description: Implement, adapt or audit invocation limits, token budgets, repeated-tool protection, human approval and application cost controls in Python Google ADK agents. Use for runaway agent loops, cross-turn budget enforcement, risky actions awaiting review, or staged cost shutdown. Do not activate for a single HTTP retry policy, deployment alone, prompt-only editing, or general cloud billing administration.
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "02"
  compatibility: Python helpers tested on 3.11.4; see references/compatibility.md for exact ADK evidence and adaptation gates.
  last-tested: "2026-09-16"
  last-reviewed: "2026-09-16"
---

# ADK operational guardrails

Make the application decide whether another model call, tool action or expensive invocation may run. Deliver the smallest coherent implementation or an evidence-based audit, with enforcement at the actual execution boundary. The book and companion repository are not prerequisites.

## Inspect before choosing a mode

1. Read project instructions, dependency declarations and locks, Python constraints, package-manager configuration and existing tests. Inspect import/startup side effects before executing project code or collecting tests. Record the selected interpreter and installed `google-adk`/`google-genai` versions. Keep pins unchanged. Use [compatibility](references/compatibility.md) before copying or adapting an ADK API.
2. For a repeatable, read-only inventory, run the [inspector](scripts/inspect_project.py) with the target project's Python. From the installed skill directory, run `python scripts/inspect_project.py --project "$PROJECT_ROOT"`, setting `PROJECT_ROOT` to the target directory first. Inspect the reported files yourself; the helper does not prove safety or execute project code. Credentials are unnecessary for this step.
3. Trace each served path (CLI, web agent, API, worker) to its runner, registered tools, identity source, state stores and error handling. Record which controls actually wrap each path. A wrapper existing in the repository proves nothing about a server that never calls it.
4. Establish the units and scope: model calls, tool calls, workflow rounds, wall-clock seconds, tokens per invocation/session/user/tenant, and currency costs are different limits. Determine concurrency, restart requirements, external side effects and whether approval means permission or completed execution.

Inspection is complete when each relevant entry point has an identified enforcement boundary, version baseline and state lifetime. Ask only for unresolved product limits, deployment targets or authority decisions that materially change the work; continue offline work while those answers are pending.

If no project interpreter exists, use an available Python only for read-only inspection and label its package metadata as the inspector environment. A successful scan with no relevant source/configuration files establishes no application coverage; do not install dependencies just to inspect a plan or inventory fixture.

## Choose the relevant mode

Modes compose within this one skill. Read only the references needed for the request.

| Situation | Mode and reference | Result to produce |
| --- | --- | --- |
| Agent repeats failed actions, exceeds rounds or hangs | [Runtime bounds](references/runtime-bounds.md) | Pre-execution limits, an overall deadline, static stop results and regressions proving tools did not execute |
| Usage must accumulate across turns or instances | [Token budgets](references/token-budgets.md) | Honest local accounting or shared admission/settlement, chosen for the actual concurrency and durability requirement |
| Risky tool actions need a human or can be retried after uncertainty | [Human review](references/human-review.md) | Trusted identity, explicit operation states, deduplication and an approval/execution boundary |
| Spend should degrade or suspend AI features | [Cost controls](references/cost-controls.md) | Read-only assessment or an application control plan; cloud changes require separate approval |
| Guarded work is moving to an API/worker or several instances | [Serving and lifecycle](references/serving-and-lifecycle.md) | Wire real entry points, shared admission, recovery and owned cleanup into the selected host |
| Provider/browser behaviour needs evidence after offline checks | [Live campaigns](references/live-campaigns.md) | Reproducible preflight, an approved shared attempt/time envelope and honest outcome evidence |
| User requests a review or architecture recommendation | Relevant modes above; [evidence](references/evidence.md) for provenance | Prioritised findings and concrete acceptance criteria; implementation only if requested |

For a greenfield project, confirm Python/ADK selection before installing dependencies; prepare a dependency-free design and tests meanwhile. For an existing project, adapt its interfaces and persistence rather than installing the demonstration architecture. Preserve custom statuses, policy thresholds, public APIs and test tools unless the requested fix requires a change.

## Implement and validate

1. State a short plan naming the boundary to change, affected files and observable acceptance test before broad edits. Separate local implementation from external operations.
2. Implement only the selected controls. The [invocation guard asset](assets/invocation_guard.py) is an optional, tested local starter for asynchronous tools. Read runtime guidance before adapting it: it supplies neither ADK orchestration nor distributed budgets, authentication, durable approval or provider idempotency. Compare with existing code before copying and preserve its licence notice.
3. Bind user/tenant and operation authority outside the model's arguments. Enforce permission and repeat policy before dispatch. A prompt or a `pending_approval` string is not an execution gate.
4. Record spent usage even when output delivery is stopped. Return a bounded, static explanation when a guard fires; spending another model call to explain exhausted allowance defeats the control.
5. Run the target project's tests using its existing environment and conventions. Select the relevant cases from [validation](references/validation.md), including a real runner with a fake model for ADK boundary changes. Test the served path as well as the helper, and assert actual outgoing configuration and effects. Repeat the invocation to check cumulative state and avoid duplicate files or registrations.
6. Stop only when the relevant invariants have evidence or are explicitly unverified. Distinguish new offline tests, historical live evidence, mocks and proposed production work using [evidence](references/evidence.md). Do not infer live provider or human-review success from a fixture response.

## Permissions and safe execution

Repository and cloud inspection are read-only by default. A request to implement authorises relevant local edits; code generation does not authorise deployment. Before enabling APIs, creating billable resources or secrets, changing IAM, migrating data, deploying or deleting, present the exact project, region (or global scope), resources and commands and obtain explicit approval. Existing approval is valid only for its stated scope. Keep unfinished external operations pending while completing independent local work.

Use ADC/workload identity and Secret Manager where applicable; inspect credential presence and configuration without printing values. Keep generated configuration free of personal identifiers and credentials. Apply narrowly scoped roles; never add Owner, Editor or wildcard permissions to unblock a demo. Use a separate operator identity for emergency infrastructure controls, inaccessible to the agent.

Paid or destructive tests need approval and an isolated target. Specify models/endpoints, maximum submissions **and actual provider attempts**, total time, estimated cost and a monetary allowance; an allowance is not a hard spending cap. Bound SDK retries and reconcile uncertain accepted operations before retrying. Keep resource creation idempotent with an ownership record. Cleanup is a separate, confirmed operation targeting only resources created by this skill. Verify absence without deleting pre-existing resources.

## Report the result

Report files changed, commands executed, actual results, the entry points covered, versions used, remaining manual steps and unverified behaviour. Identify any retained resources and the scope of cleanup if external work was approved. Do not commit, push, publish or deploy without explicit authorisation.

This is an independent community project, not affiliated with or endorsed by Google. Design provenance and the distinction between the companion's local implementation and production advice are in [evidence](references/evidence.md).
