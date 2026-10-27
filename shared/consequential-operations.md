<!--
The approval and resource-safety rules every building specialist shares. It
reconciles the per-skill permission sections that existed before 2026-10-27
(deploy's end-the-turn and typed-deletion rules are now universal). Skill-specific
operations and limits stay in each SKILL.md. Edit here, then run
scripts/sync_shared.py.
carriers: adk-agent-evaluation, adk-agent-instructions, adk-agent-interoperability, adk-agent-observability, adk-agent-security, adk-fastapi-backend, adk-frontend-integration, adk-memory-architecture, adk-model-and-output-contracts, adk-operational-guardrails, adk-release-engineering, adk-sql-agent-engineering, adk-tool-auth-and-secrets, adk-tool-interface-design, adk-workflow-design, deploy-adk-on-google-cloud, optimise-adk-on-google-cloud, protect-adk-sensitive-data, safe-api-tool-calls
-->

## Consequential operations

Repository and cloud inspection are read-only by default. A request to
implement authorises local edits only: code generation does not authorise
deployment, paid model calls or live tests. An earlier campaign, an approval for
another project, a budget balance or elapsed time authorises nothing, and a
generic "build it" or "go ahead" is not approval of a concrete operation.

**Ask first.** Before enabling an API, linking billing, upgrading a plan,
raising a quota, creating a billable resource or a secret, changing IAM,
migrating data, deploying, deleting, or running a paid or destructive test,
finish the local work and offline checks so the request is concrete. Present
the exact account and project, region or global scope, model and endpoint,
resource names, identities, commands, request, retry, time and cost limits, the
isolated test target and the cleanup scope, then obtain explicit approval. End
the turn after asking: a command run in the same turn as its approval request
was not approved. An approval covers only the scope it named; another target or
a widened scope needs a new decision. Irreversible deletion needs a typed
confirmation naming the resource. Continue independent local work while a
decision is pending; missing approval or credentials leave the live work
`not run`, not failed.

**Credentials and data.** Prefer ADC or workload identity and the project's
secret manager. Check that a credential is present without printing its value,
and never silently change global CLI or ADC configuration. Keep credentials,
service-account keys, customer content and personal resource identifiers out of
source, model inputs and results, session state, logs, generated examples and
reports; environment examples hold placeholders only. Test with synthetic or
properly de-identified data.

**Least privilege.** Derive the narrow roles the work needs. Owner, Editor,
wildcard grants and public unauthenticated access are never a way past a
failure.

**Bounded live work.** Run paid or destructive tests only on an approved
isolated target, never against production data or identities. Bound calls,
actual provider attempts (SDK retries included), polling and wall-clock time;
state the estimated cost and a monetary allowance, which is not a spending cap.
Keep a reserve for cleanup and inspection and stop optional tests before they
consume it; a refusal can consume requests too. Stop on an unapproved target or
an exhausted allowance.

**Idempotent setup.** Record intent and ownership before creating anything, read
the result back, and make setup safe to repeat. Reconcile an uncertain outcome
before retrying: an empty state file, a permission-denied read or a failed
inventory is not proof of absence, and never a reason to delete or recreate. An
already-enabled API or a no-op repeat is not evidence that this task created it.

**Cleanup.** Cleanup is a separate, confirmed operation: list what this task
created, show the exact deletion commands, delete only resources the ownership
record shows this workflow created (dependants before owners), then verify
absence independently. Preserve pre-existing resources, grants, shared APIs and
credentials, and never adopt a pre-existing resource by relabelling it.
