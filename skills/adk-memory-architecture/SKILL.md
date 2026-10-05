---
name: adk-memory-architecture
description: >-
  Design, implement, adapt or audit memory and retrieval in Python Google ADK
  agents. Select and combine conversation sessions/state, governed RAG,
  Agent Platform Memory Bank and scoped BigQuery history; enforce identity,
  consent, retention, replay and erasure boundaries. Use for agent memory,
  knowledge retrieval or cross-session continuity work. Do not activate for
  general database administration, arbitrary SQL generation, deployment alone,
  prompt-only editing (adk-agent-evaluation owns decision quality) or
  non-agent caching.
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  source-chapter: "6"
  last-tested: "2026-09-16"
---

# ADK memory architecture

Deliver a focused implementation, adaptation, audit or decision for the target
agent's memory architecture. Keep the target's domain, interfaces, package
manager and dependency pins. The book and companion repository are not required.

## Inspect the actual boundary

1. Read project instructions, manifests and lockfiles, configuration templates,
   application startup, agent/Runner assembly, tools, storage adapters and tests.
   Identify the requested outcome; an audit or recommendation ends in a list
   of gaps with remedies, and implementation waits for its own request. Inspect imports and test setup before
   executing them: either can initialise remote clients or load credentials.
2. Use the target's existing interpreter. Optionally run the bounded, read-only
   [inspector](scripts/inspect_project.py):
   `"$PYTHON" "$SKILL_DIR/scripts/inspect_project.py" --project "$PROJECT_DIR"`.
   Set these variables to the selected interpreter, installed skill directory
   and target project. Read [compatibility.md](references/compatibility.md) for
   its exit codes, coverage and version checks. It reports signals, not proof of
   correct authorisation. Inspect unresolved pins and unscanned files manually.
3. Map authenticated user/tenant/customer identity, session ownership, state
   scopes, exact profiles, memory submission and retrieval, document releases,
   structured data freshness, replay, telemetry and erasure. Record which
   controls are constructed by the real serving entrypoint, by reading that
   entrypoint; the bare agent module shows only the agent.
4. Record configuration key names and provenance without exposing values.
   Root and nested configuration, CLI account, ADC quota project, model API
   key and deployed workload identity can differ. Missing credentials block
   live verification; continue safe local implementation and offline checks.

## Select the mode from the fact's meaning

Load only the relevant reference; combine modes when the requirement needs it.

| Required fact or operation | Mode | Authority and completion boundary |
| --- | --- | --- |
| Current conversation, working state, continuation or completed-response retry | [Sessions and state](references/sessions-state.md) | Owner-qualified history and explicit persistence/replay contract |
| Approved policies, manuals or other versioned reference evidence | [Governed RAG](references/rag.md) | Approved release, entitled sources and evidence-supported answer |
| Useful low-risk facts across sessions; consent, correction or forgetting | [Memory Bank](references/memory-bank.md) | Scoped, eligible, expiring claims; accepted, completed and retrievable are separate |
| Dated structured records and analytical history | [BigQuery](references/bigquery.md) | Narrow parameterised reads with trusted scope and an honest freshness contract |

Use the owning transactional service for current entitlements or business
mutations. Exact user-controlled settings belong in a deterministic profile.
For example, a saved response language is a profile row read at invocation;
"the customer prefers morning calls" is a semantic memory claim with consent
and expiry; the current balance comes from the ledger service every time.
Neither semantic memory nor retrieved prose authorises an action. Add a
store when a required fact needs its authority and lifetime; one store is
the usual answer.

For local PDFs, supplementary authorities or image-only evidence, read
[local-document-coverage.md](references/local-document-coverage.md) for the
coverage fixture and the visual-review or unresolved-evidence boundary.
Before the first model call over a document pack, read
[document-ingestion.md](references/document-ingestion.md): produce a per-page
ingestion report, route scanned and low-density pages to OCR or vision, and
choose text, image or both per page. For how retrieval finds the operative
section (chunking by heading, one query per issue, deterministic lookup of
named references, one bounded second round, a local hybrid index and a recall
measurement on a gold set), read
[retrieval-strategy.md](references/retrieval-strategy.md).

When implementing the HTTP/ADK boundary, read
[integration-recipes.md](references/integration-recipes.md) for concrete
assembly, trusted-context, event and replay contracts. When connecting or
hosting managed backends, read
[managed-deployment.md](references/managed-deployment.md). For failed setup,
retrieval, protection, probes or cleanup, use
[failure-recovery.md](references/failure-recovery.md) before proposing a retry.

## Implement or adapt

1. Present a short plan before broad changes: affected seams/files, identity
   and lifetime contracts, failure behaviour and observable acceptance tests.
   Preserve custom implementations that already meet those contracts. Make
   the smallest coherent change on the app's own modules and conventions.
2. Derive scope in trusted code, outside model arguments and client state.
   Reauthorise each data access. Protect material before model exposure and
   before persistence, then project public output separately, because a tool's
   side effect stands whatever the output screen later decides.
3. Follow the chosen reference's implementation sequence and error cases.
   Treat recommendations labelled **production additions** as work needing
   implementation and tests, and report their verification status with them.
   Preserve pending and indeterminate writes and their operation identities,
   and recover a timed-out write by status lookup under the same identity.
4. Keep models, resource names, locations, timeouts, retention and budgets
   configurable. Use ADC/workload identity and managed secrets where relevant.
   Keep credentials in the secret store and refer to them by name in memory,
   events, fixtures and logs. Configuration examples use synthetic placeholders.

## Permission and lifecycle

Inspection is read-only by default. Before enabling APIs, creating resources or
secrets, changing IAM, migrating data, deploying, deleting, increasing quotas or
running paid/destructive tests, show the exact project, regions, resources,
identities, commands and bounded work allowance, then obtain explicit approval.
Code-generation permission is not deployment permission. Reuse an existing
approval only for its exact scope; continue independent offline work while a
required decision is pending. Never use Owner, Editor or wildcard grants as a
troubleshooting shortcut.

Read [operations-validation.md](references/operations-validation.md) before
cloud work, recovery or cleanup. Use isolated test targets and synthetic data,
idempotent setup and an ownership journal. Cleanup is separate, requires
confirmation, and may target only resources created by this workflow. Shared
regional RAG infrastructure is outside routine corpus cleanup. Bound retries,
polling and total elapsed work, with screening in place throughout recovery.

## Validate and report

1. Run the target's applicable offline tests and checks using its existing
   environment. Exercise the actual boundary through deterministic doubles:
   cross-user access, consent denial, duplicate submission/replay, expiry,
   unknown retrieval sources, stale structured data and protection failure as
   relevant. Assert stored effects as well as returned text. Include failure
   and retry paths; the model and persistence tests read stored state after
   a real invocation.
2. Inspect the second invocation: no duplicate files, configuration churn,
   repeated side effects or untracked operations. For production additions,
   test worker loss, lease expiry and late writes at the relevant seam.
3. Run live acceptance only within approved scope. Report each phase as
   **passed**, **failed**, **blocked** or **not run**. Separate local doubles,
   real managed services from a local API, and deployed hosted behaviour.
   A target deployment is certified by its own acceptance run.
4. Finish with files changed, commands actually executed and exit/results,
   exact versions, evidence type, unverified behaviour and precise manual or
   approval steps. For an audit, pair each gap with a concrete remedy and test.
   Use [provenance.md](references/provenance.md) when the origin of a rule
   matters; [skill-validation.md](references/skill-validation.md) records this
   package's own checks and limits.

Independent community project; not affiliated with or endorsed by Google.
