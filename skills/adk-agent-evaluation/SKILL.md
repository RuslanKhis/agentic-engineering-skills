---
name: adk-agent-evaluation
description: "Build, adapt or audit a Python ADK agent's testing strategy: deterministic tool and Runner tests, live evaluation sets, simulated conversations, conformance replay and strict result checks. Use for agent behaviour, regression coverage or evaluation reliability. Do not activate for ordinary non-agent unit tests, standalone model benchmarks, deployment, or cloud cleanup alone."
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "7"
  last-tested: "2026-09-16"
  compatibility: See references/compatibility.md for exact tested versions and limits
---

# ADK agent evaluation

Produce evidence about an agent's decisions, executed effects and final account of those effects. Adapt the target project; keep its business domain, architecture, dependency pins and test conventions. This skill works without the book or its companion repository.

## Inspect and define the job

1. Read repository instructions, manifests/lockfiles, test configuration and existing agent factories, tools, callbacks, session services and evaluation assets. Use the project's existing interpreter to inspect installed package metadata before importing application code. Imports and test collection can have side effects; inspect their entrypoints first. Check the pinned Python, `google-adk`, `google-genai` and any managed-evaluation SDK versions against [compatibility.md](references/compatibility.md). Preserve pins; a version mismatch requires interface verification or a clearly reported blocked live path, not an automatic dependency change.
2. Locate trusted identity, authorised mutations, idempotency keys, business-store lifetime, conversation-state lifetime and the model-injection seam. Read credential variable **names and presence**, never print secrets or dump `.env`. Identify existing offline/live markers and which commands could reach remote services. Finish inspection with a concise map of these boundaries and missing prerequisites.
3. Translate the user's requirement into observable success and forbidden actions: correct tool/arguments, allowed order, resulting effect, truthful response and bounded work. Distinguish deterministic assertions from model-dependent decisions. For an audit or recommendation, report a gap with evidence and a concrete change; do not implement merely because a gap exists. For implementation, present a short plan before broad changes and make the smallest coherent change.

## Select the mode

Combine modes only when the requested outcome needs them. Read the linked reference when entering that mode, rather than loading every file.

| Request or evidence needed | Mode and resource | Completion criterion |
| --- | --- | --- |
| Enforce business rules, reproduce a bad decision, test callbacks/state or HTTP integration without model variance | [Deterministic tests](references/deterministic-tests.md) | Actual effects and state boundaries asserted through the relevant real runtime layer |
| Measure the real model, build fixed cases, add simulated dialogue or calibrate a judge | [Live evaluations](references/live-evaluations.md) | Version-valid assets and offline checks first; approved live work retains complete results and provenance |
| Record or compare provider exchanges after an integration change | [Conformance](references/conformance.md) | Reviewed baseline, nonzero executed case count, isolated tool effects and explicit replay limits |
| Explain a misleading pass, check a CSV, design reliability/holdout gates | [Result auditing](references/result-auditing.md) | Expected coverage checked, failed/incomplete rows retained, conclusions limited to identifiable observations |

Planning a production suite can stop at a reviewable design with cases, budgets and acceptance criteria. Recommendations about holdouts, remote-write reconciliation or production telemetry are not claims those features exist or passed testing.

Load additional implementation detail only for the relevant branch:

- **Setup, project/provider changes or access failures:** [environment and troubleshooting](references/environment-and-troubleshooting.md) gives configuration tracing, API-state reconciliation and scoped cleanup checks.
- **Runtime wiring, fault injection, observers, deadlines or browser timing:** [execution evidence](references/execution-evidence.md) gives concrete recipes and the checks that make their results trustworthy.
- **Dataset curation, judge calibration, work budgets, ambiguous writes or release gates:** [evaluation design](references/evaluation-design.md) gives production implementation procedures and acceptance criteria, explicitly separate from historical companion coverage.

## Apply the pattern

- Put business permission and validation in tools/backends. Use the real runner with a scripted model to force invalid decisions. When a workflow needs fresh verification, bind it to the intended invocation or validity window; an earlier conversational lookup is not automatically permission for a later write.
- For transactional confirmations, consider rendering from trusted tool receipts. Keep facts dynamic, receipt authority separate from conversation text, and successful effects intact after later failures. Compose existing callbacks. Do not impose a fixed response template on a task that needs open-ended synthesis.
- Preserve the distinction between a new session and a fresh backend. Reset or namespace business fixtures at the experimental unit being claimed. Assert attempted calls and stored effects separately.
- Choose trajectory matching for meaningful invariants. ADK 2.8.0's relaxed order modes still compare arguments and allow extra calls; a prohibited extra mutation needs its own assertion. ROUGE checks wording overlap, not truthful completion or authorisation.
- Capture the whole invocation and close its streams/runners. Bound synchronous grading in a worker controlled by an external deadline. Timeouts can leave partial evidence and cannot recall accepted provider requests. Model, simulator, judge, retry, tool and time limits are distinct.

## Authorisation and data boundaries

Inspection is read-only by default. Permission to implement tests is not permission to make paid calls or deploy them. Before enabling APIs, creating billable resources, changing IAM, creating secrets, migrating data, deploying, deleting or running paid/destructive tests, show the exact project, region, resources, commands, isolated test target and work limits, then obtain explicit approval. Reuse approval already given for that exact scope; a different target or expanded scope needs a new decision. Continue independent offline work while approval is pending.

Use synthetic or properly de-identified fixtures. Prefer ADC/workload identity and managed secret storage where relevant; never use Owner, Editor or broad wildcard grants to bypass a failure. Keep provisioning idempotent. Cleanup is a separate, confirmed operation limited to resources owned by this skill's recorded run. Never delete shared project resources to obtain a clean test.

## Validate and report

1. Run the project's meaningful offline checks with external access prevented where hermeticity is claimed. Validate eval/config schemas with its pinned ADK models. Check guards and effects, not just expected strings. Keep failing regressions when diagnosing a real defect.
2. For approved live work, start with a small preflight, then the bounded experiment. Retain case/trial/metric counts and versioned criteria. A skipped paid test, missing score, zero-case conformance run or successful process exit is insufficient evidence. The result-auditing reference documents the bundled read-only [CSV checker](scripts/check_eval_results.py).
3. Check a second invocation for duplicate writes, duplicate test registration and needless configuration churn. Run only newly justified checks after a passing validation; retain failed observations instead of rerunning to green.
4. Report files changed, commands and exit/results, actual versions, what used real providers, what used doubles, what remains unverified, and any precise manual action or approval needed. Distinguish implementing a test from executing it successfully. Use [provenance.md](references/provenance.md) only when explaining the evidence behind this skill; its historical results are not results for the target project.

The skill's own checks and limitations are recorded in [validation.md](references/validation.md). Independent community project; not affiliated with or endorsed by Google.
