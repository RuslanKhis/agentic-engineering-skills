---
name: adk-workflow-design
description: Select, implement or review Google ADK workflow control flow, event consumption, session-state handoffs and callback boundaries. Use when choosing between ordinary code, sequential, parallel, bounded-loop, graph or dynamic orchestration, or repairing those runtime contracts in an existing agent. Do not activate for unrelated UI edits, general LLM explanations, standalone cloud deployment, or implementing RAG, memory or SQL services.
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "00"
  last-tested: "2026-09-16"
---

# ADK workflow design

Produce the smallest justified orchestration change, or an actionable design/review
when implementation is not requested. Establish what constitutes a usable result,
how work stops, and which evidence supports the outcome. The skill is self-contained;
the book and companion repository are optional provenance, not prerequisites.

## Inspect before selecting a pattern

1. Read project instructions, status/diff, manifests and lockfiles, entry points,
   existing tests and startup/cleanup commands. Preserve the package manager,
   conventions and unrelated changes. Inspect configuration names without printing
   credential values or importing application modules just to inspect them.
2. Record the target Python, ADK and GenAI versions, model/backend, current result
   contract, state ownership, side effects and relevant test commands. Use the
   existing project interpreter. The read-only helper can provide an initial map:

   ```bash
   python /path/to/adk-workflow-design/scripts/inspect_project.py --project .
   ```

   Replace the skill path with its installed location. Read
   [compatibility.md](references/compatibility.md) before using an SDK recipe or
   interpreting the helper. A different/missing version blocks claims of tested
   compatibility, not independent planning. Resolve the target API contract or
   report the exact blocker; never silently change dependency pins.
3. Define acceptance in observable terms: ordered handoff, two preserved branch
   outputs, bounded refinement with an explicit result, typed node output, or a
   callback action. An import, HTTP 200 or plausible paragraph is insufficient.
   List missing prerequisites together. Ask only for decisions the project and
   request cannot settle; continue independent offline work.

Inspection is complete when the chosen mode, version baseline, output contract
and validation path are known, or their specific blockers are recorded.

## Choose a mode

| Need | Mode and next reference |
| --- | --- |
| Known rules; no model judgement needed | Prefer ordinary Python. Use [orchestration.md](references/orchestration.md) only if ADK coordination adds value. |
| Fixed order, independent concurrent work, bounded refinement, typed graph, or runtime-sized work | Selection/implementation/review: read [orchestration.md](references/orchestration.md). Preserve an existing supported pattern unless changing it solves the requested problem. |
| Missing final result, lost state, streaming, restart or paused-run semantics | Runtime contract: read [runtime.md](references/runtime.md). |
| Logging hooks, deterministic short-circuits, tool visibility or call-time policy | Callback boundary: read [callbacks.md](references/callbacks.md). |
| Local startup, actual HTTP/UI checks, buffering, timing or retained sessions | Reader/runtime operation: read [local-runbook.md](references/local-runbook.md). |

Modes can combine within one task. Read only relevant references. Cloud hosting,
retrieval, long-term memory and tenant authentication may be architectural
recommendations; implementing them is a separate scope decision.

## Implement or advise

1. Present a short plan before broad edits. For a planning/review request, give
   the selected pattern, alternatives that materially affect the decision, output
   contract, failure boundaries and acceptance plan; stop short of generating an
   unsolicited application.
2. For authorised implementation, reproduce the reported failure through the
   public runner, CLI, HTTP or UI path before a narrow correction. Reuse existing
   orchestration and change only the boundary causing the defect. Keep a regression
   case. Greenfield work starts from the actual user task, not a travel/clock demo.
3. Account for each output, model/tool attempt and state writer. A prompt is not
   authorisation; a loop limit is not a request budget; a checkpoint is not
   exactly-once execution. Label simulated inputs/results explicitly.
4. Keep proposed production controls distinct from implemented controls. Add
   deadlines, idempotency, persistence or observability when the task requires
   them, and validate each claim. Do not copy a historical campaign's limits or
   hard-coded identities into a new project.

## Authority and external work

Repository/cloud inspection is read-only by default. Code-generation permission
does not authorise deployment or paid model calls. Before API activation, IAM or
secret changes, data migration, provisioning, deployment, deletion or live paid
tests, present exact project/account, region, model, resource IDs, commands,
request/retry limits, execution window and cleanup plan; obtain explicit approval.
Reuse an approval only when it already covers those exact operations and scope.
Billing linkage, upgrades and quota increases need separate approval.

Use synthetic data and short-lived ADC/workload identity where applicable. Keep
credentials out of code, model inputs/results, session state and reports; use
placeholder-only environment examples. Use least privilege, never Owner/Editor
or wildcard grants as a shortcut. Read [external-validation.md](references/external-validation.md)
only when real-service acceptance or cloud prerequisites are in scope.

Keep cleanup separate from setup. Obtain confirmation for deletion, target only
resources this task created, retain an ownership inventory, and make setup and
cleanup repeatable. Prepare reviewable commands before seeking approval. Missing
approval leaves consequential work pending; it does not stop safe local checks.

## Validate and finish

Follow [validation.md](references/validation.md) for mode-specific assertions,
offline boundary doubles, browser timings and a concise result format. Run the
project's relevant tests and static/build checks, including a real application
path where applicable. Prove concurrent branches overlap, state survives only as
claimed, and failure cannot be reported as success. Repeat setup/adaptation to
check that it preserves existing work rather than duplicating it.

For strict paid-request limits, SDK retries or campaign restart, read
[model-call-controls.md](references/model-call-controls.md) before choosing the
enforcement point. A callback counter alone does not establish a transport cap.

Report changed files, exact commands and versions, actual outcomes, warnings,
manual prerequisites and outstanding work. Separate PASS/FAIL/BLOCKED/NOT RUN/N/A
for offline execution, live behaviour, browser functionality, latency and cleanup
as applicable; use INCONCLUSIVE when observations cannot resolve a threshold.
Historical companion results are provenance, not a pass for the
target project. Read [provenance.md](references/provenance.md) only to trace a rule
or assess the scope of that prior evidence.

This is an independent community project, not affiliated with or endorsed by Google.
