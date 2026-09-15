---
name: safe-api-tool-calls
license: MIT
description: Implement, adapt or review safe external API tools in Python and ADK projects, including selective retries, cooperative deadlines, idempotent writes and confirmation. Use for unreliable API calls, ambiguous write outcomes or unsafe tool replay. Do not activate for model-only tuning, general cloud deployment, UI-only changes or database query optimisation without an external-call safety problem.
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "01"
  last-tested: "2026-09-15"
---

# Safe API tool calls

Deliver a small integration change or an actionable review that bounds API work, preserves operation identity and reports uncertain outcomes honestly. Work with the target's existing clients, tool interfaces, package manager and tests. The book and companion repository are not dependencies.

## Inspect before choosing a mode

1. Read project instructions, dependency manifests and lockfiles, API adapters, tool registration, error contracts and relevant tests. Trace one request from the public tool to the provider, including SDK retries and confirmation.
2. Identify the actual Python, ADK and client versions using the project's existing interpreter and declared pins. Do not install, upgrade or downgrade packages to reproduce the historical example. Read [compatibility and evidence](references/compatibility.md) before using version-dependent ADK or timeout behaviour.
3. Establish whether the operation reads state or changes it. For writes, find the provider's replay contract, the trusted business identity, payload binding, authorisation and existing durable storage. An HTTP method, a UUID or a prompt is not enough evidence of safe replay.
4. Record the permitted attempts, complete operation budget, cancellation behaviour, result schema and validation command. Ask only for missing decisions that cannot be inferred from source or authoritative provider documentation. Continue independent offline work while external prerequisites remain unresolved.

For a bounded, read-only inventory, resolve `SKILL_DIR` to this skill's installed directory and run the helper with an available Python 3.11+ interpreter. If none is available, inspect manually without changing the target's Python version:

```bash
python "$SKILL_DIR/scripts/inspect_project.py" --project . --dry-run
```

The helper reads source and declarations without importing project code, loading `.env`, running commands or contacting services. Its signals direct inspection; they do not certify safety or report the installed dependency versions. Read [inspection limits](references/inspection.md) when using its output. A partial scan is a reason to inspect the omitted area, not a clean result.

## Choose the relevant path

| Mode | Decision and reference |
| --- | --- |
| Read or replay-safe request | Read [reads and deadlines](references/reads-and-deadlines.md); implement selective retries and separate transport, attempt and complete-operation budgets. |
| State-changing request or approval flow | Read [writes and confirmation](references/writes-and-confirmation.md) before enabling retries. If replay safety is unknown, retain a single attempt and an honest uncertain result; prepare reconciliation or a provider-contract question. |
| Review or recommendation | Use the applicable reference above. Compare guarantees against actual control flow and tests; report concrete findings without changing code unless requested. |

A request may need both read and write paths. Keep them in the same skill; do not replace the application with a demonstration project or introduce a database solely because the chapter discusses one.

## Implement the smallest coherent change

State a short plan naming the affected boundary and tests before broad edits. Reuse an existing retry layer, operation store and result contract where they can express the required guarantee. Change public interfaces only when necessary, identifying affected callers.

Put retry policy in trusted code and make it provider-specific. Distinguish internal attempts from a new tool invocation. A bounded tool call is not a bounded model conversation. Preserve caller cancellation and inspect the actual deadline object's state before attributing a timeout.

For a write, preserve the same authorised logical operation, canonical payload and provider replay identity across permitted retries. Reconcile an ambiguous outcome; a later rejected attempt does not establish that earlier attempts had no effect. Durable recovery, exact money and business authorisation are production design requirements, not features supplied by this skill or by a mock test.

For ADK, test the real tool wrapper and chosen client/session path. Missing or rejected confirmation must not run the side effect. Rejection should be explained as cancellation with no attempt, separately from provider uncertainty. Confirmation does not authenticate the caller; prompt instructions do not deterministically block another approved tool call.

## Permissions and consequential operations

Inspection is read-only. Local implementation authority does not authorise deployment or live testing. Prepare a concrete plan before enabling APIs, creating billable resources, changing IAM, creating secrets, migrating data, deploying or deleting resources/data. Show the exact project, region, resource names and commands, expected effects and relevant cost/time limits; obtain explicit approval before execution. Preserve approval already granted for that exact scope; approval for another project or an earlier campaign does not transfer.

Paid or destructive tests require an explicitly approved isolated target and bounded calls, retries and duration. Use least privilege and existing ADC/workload identity where relevant; never expose credentials or use broad roles to bypass a blocked prerequisite. Keep configuration examples synthetic and configurable. Missing credentials should leave live work unverified while offline validation proceeds.

Keep cleanup separate. Inventory what this task created, show the exact deletion commands and obtain confirmation. Delete only task-owned resources, then verify absence independently. Preserve pre-existing resources, shared APIs and credentials. A no-op setup repeat or an already-enabled API is not evidence of creating it successfully.

## Validate and finish

Read [validation and reporting](references/validation.md) for the selected behaviour. Run the project's existing checks without network calls by default. Cover the public tool/client boundary, real cancellation or retry sleeps where relevant, transient recovery, terminal failure and the write/confirmation invariants. Do not substitute a print-only random demo for assertions.

On a second invocation, inspect existing changes and recorded state, rerun the relevant checks, and avoid duplicating wrappers, configuration, keys or resources. If the pinned version cannot support the chosen implementation, identify the incompatible API and stop that path; adapt within the existing version or request a version decision rather than silently changing dependencies.

Report files changed, commands and actual results, remaining actions, and unverified behaviour. Separate **offline simulated**, **live verified** and **not run** evidence. Measure successful retrieval separately from response time, including error responses. Never promote a mock payment, a source syntax check or a historical test into production integration proof.

Independent community project; not affiliated with or endorsed by Google.
