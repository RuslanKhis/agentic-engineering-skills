# From a working deployment to a production service

Read this when the task includes real users, durable state, multiple replicas, bounded execution or release operations. Select only the sections the target needs. These are implementation contracts derived from the chapter's production advice and inspected SDK behaviour; the chapter's live lab did **not** implement or validate this whole design. A production recommendation becomes a completion claim only after the target's corresponding tests pass.

## Follow configuration to its consumer

For each setting, record `configuration key → reader → generated/deployed value → runtime observation`. A variable in a root `.env`, a Cloud Build substitution or the operator's shell is ineffective if the relevant wrapper/SDK never reads it. Do not report secret values; record presence, source and version/reference instead.

Keep four separate locations where applicable: hosting, build, inference and session/artefact storage. Check the model client's explicit arguments as well as environment variables. Inspect generated files and SDK configuration before provider submission. Cloud Run's native generator and Runtime's generator have different environment channels; use their mode reference rather than assuming a shared convention.

Acceptance: a local test varies each non-secret setting and observes the actual constructed app/model client or generated deployment configuration. A live check then verifies the running revision's non-secret configuration and one authorised model/tool result. Deliberately conflicting shell and deployment values should resolve according to the intended precedence. Test secret absence in source, logs and error responses separately.

## Separate service entry, network reachability and user ownership

Choose the access path before configuring CORS or issuing browser tokens:

| Requirement | Implementation decision | Acceptance that matters |
| --- | --- | --- |
| Operator walkthrough | Private Run IAM plus an owned loopback transport, or GKE RBAC plus a loopback port-forward | Anonymous remote access denied; local Host/Origin and forwarding boundaries tested; teardown stops the owned transport. This does not establish application tenant isolation. |
| Service-to-service caller | Provider-verified identity token for the correct audience, narrow invocation permission and application authorisation | Correct caller succeeds; wrong audience, expired token and unauthorised principal fail. Keep runtime model permissions separate from caller invocation. |
| Browser users | Supported IAP topology or an authenticated application/frontend with server-side credential handling | Signed-out and unauthorised users fail; sign-in, streaming and error recovery work through the actual browser path. A script with a token is insufficient. |
| Network restriction | Explicit ingress, load-balancer, firewall and egress choices for the selected service | Test intended and unintended entry paths independently of IAM. Authenticated does not mean network-private; ClusterIP does not authorise one application user. |

For Cloud Run, direct IAP and load-balancer IAP are different supported designs. Current direct-IAP guidance requires its service agent to invoke Run and users to have IAP access; do not enable both IAP layers on the same path. IAP changes the identity seen by the downstream IAM check, so recheck service callers when adopting it. If using a load balancer, restrict alternate origins so they cannot bypass the intended boundary. Follow the chosen design's current setup requirements rather than assuming the lab's local bridge is a production sign-in service. [Official Cloud Run IAP guidance](https://docs.cloud.google.com/run/docs/securing/identity-aware-proxy-cloud-run).

On GKE, select a supported Ingress/load-balancer or Gateway configuration; attaching an annotation to an arbitrary ClusterIP Service is not a complete IAP design. The Ingress route uses BackendConfig; the documented Gateway route uses a different configuration, so preserve the platform's chosen mechanism. [Official GKE IAP guidance](https://docs.cloud.google.com/iap/docs/enabling-kubernetes-howto). Keep readiness paths cheap, and expose only routes the production frontend needs. A development UI or debugging route need not be internet-facing.

At the application boundary, validate the trusted principal and map it to permitted application/user/session/artefact namespaces. Never accept a caller's `userId`, session ID, forwarded email or decoded-but-unverified JWT as proof of ownership. Perform authorisation **before** reads, writes and tool execution, including session listing/history/deletion and artefact downloads. Signed proxy headers require a verified trusted proxy path; otherwise reject or strip them.

Acceptance: two authenticated users create separate synthetic conversations. Each must fail to list, read, continue, delete or obtain artefacts from the other's session, even after substituting URL/body IDs or spoofing identity headers. Verify rejected requests produce no model/tool calls. If a route intentionally shares data, test that explicit permission instead. Provider sessions partitioned by user ID alone do not prove this boundary.

## Choose and prove session and artefact durability independently

The lab proved same-session recall and local process recreation against SQLite, plus managed Runtime sessions. It did not prove multi-replica state, retention, tenant authorisation or replacement durability for every platform.

For a production store, record:

1. The installed ADK adapter/class, its constructor or supported URI scheme, required driver/extras and schema/version requirements. A product name is not a valid `SESSION_SERVICE_URI`. Preserve a working adapter; do not infer Firestore, Memorystore, Spanner or any other backend support from its name.
2. Workload identity/database authentication, TLS/network connectivity and resource-level permissions. Secret-bearing connection strings must not appear in build arguments or reports.
3. Connection-pool bounds per worker, workers per replica, replica ceiling and database quota. Include rolling-release overlap. A shared database can exhaust its connections before compute reaches its scaling limit.
4. Which state is stored: events and session state, artefact bytes/versions, durable tool-operation receipts, and optional cross-session memory are distinct services with distinct retention.
5. Schema migration, backup/restore, expiry/deletion, region and data-access requirements. Define who can perform each operation and what a failed deletion reports.

ADK 2.8.0's inspected service factory can choose in-memory services when Cloud Run/Kubernetes is detected; forcing local storage still does not make local files durable. Its session factory tries a registered adapter, then a SQLAlchemy-backed database adapter for other URIs. Its artefact factory can fall back to memory for an unsupported URI unless strict handling is selected. Inspect the target factory and validate the **constructed service**, not only a nonempty environment variable. A misspelt artefact URI must fail startup or a mandatory readiness check, not pass chat tests while losing files.

Acceptance: write a synthetic fact and artefact through replica A, read/recall them through B, replace A and verify again. Exercise concurrent updates and document the supported ordering/conflict semantics. Verify expiry, deletion and restoration using a disposable store and authorised scope. Local recreation against the same SQLite file is a useful earlier test, but cannot substitute for these cases. Make startup fail clearly when the configured production adapter or credentials are missing; do not silently downgrade to memory.

## Make execution limits real application controls

Infrastructure instance/CPU/concurrency limits and billing alerts do not cap model calls or tool effects. Define finite controls at their actual enforcement points:

| Limit | Where it belongs | Test |
| --- | --- | --- |
| Model calls per invocation | Server-owned ADK `RunConfig` passed to the actual runner | A fake model repeatedly asks to continue; the run terminates at the configured bound. |
| Output tokens | The selected model's supported generation configuration | Inspect the constructed request and test provider rejection/limit behaviour separately; this is not a total monetary cap. |
| Tool calls and external writes | Tool wrapper/operation service, before the effect | Exhaust the budget, including parallel/retried calls; no extra side effect occurs. A durable receipt distinguishes accepted work from a failed response. |
| Wall time | Request and downstream deadlines, with explicit cancellation/reconciliation | Timeout after provider acceptance does not automatically replay the effect. Prove cancellation where supported; otherwise retain pending work. |
| Concurrent work | Application admission, worker/replica limits and downstream quotas | Load a disposable target within approval; observe rejection/backpressure and database/model capacity instead of assuming autoscaling fixes it. |

At the inspected ADK 2.8.0 baseline, `RunConfig.max_llm_calls <= 0` means **unbounded**, not “disable the model”. Its default reads `ADK_MAX_LLM_CALLS`, falling back to 500 on an invalid integer. Do not depend on that fallback for a fail-closed application policy. Validate a server-owned positive finite integer and pass the resulting config to the runner; callers may lower an approved limit only if the application explicitly supports it, never raise or disable it.

```python
import re
import sys
from google.adk.agents.run_config import RunConfig

def bounded_run_config(raw: str) -> RunConfig:
    # Load raw from trusted application configuration, not a request body.
    if not isinstance(raw, str) or not re.fullmatch(r"[0-9]{1,18}", raw):
        raise ValueError("Model-call limit must be a positive finite integer")
    limit = int(raw)
    if not 0 < limit < sys.maxsize:
        raise ValueError("Model-call limit must be a positive finite integer")
    return RunConfig(max_llm_calls=limit)
```

This is a policy-construction fragment, not a complete serving layer. Wire it into the actual invocation and test that path. The generated ADK server may expose a different configuration seam than a custom runner; inspect its installed schema before assuming a request field exists. Reject zero, negative, malformed and excessive values without echoing them. Test any caller override boundary. A model-call limit alone does not limit parallel tool writes, background work or all billable tokens.

Handle exhaustion as a specific application outcome. At the tested baseline the runner raises `LlmCallsLimitExceededError` from `google.adk.agents.invocation_context`; earlier tool effects and session events may already exist. Return a controlled error without raw inputs, retain the accepted operation evidence, and prohibit automatic replay. A local forward test exercised the real runner's counter and exception with a looping fake model; production status codes and recovery UX still belong to the target application's contract.

Size capacity from the slowest constrained dependency. Start with measured request duration, active model/tool work and database connections under a representative concurrency. Record per-instance admission and the deployment's maximum aggregate work, including workers, replicas and release overlap. Set upstream/client timeouts consistently and distinguish queueing, first response, full response and tool latency. Only claim a latency or availability objective against a defined test; the chapter's successful walkthrough was not a load/SLA test.

## Release a traceable artefact and preserve rollback

Record the chain `reviewed source → resolved dependencies/base image → build identity/result → image digest or managed package version → serving revision → accepted test`. A unique tag or successful local test does not prove what receives traffic. Test required files and private-file exclusions on the actual staged context, then protect that snapshot from source drift.

For production, choose a reproducible lock/resolution strategy, reviewed build identity and immutable deployment reference supported by the platform. Account for managed generators that augment requirements. Separate build from promotion when the repository supports it; avoid rebuilding silently during rollback. Verify traffic points to the candidate actually tested.

Prepare rollback before promotion: retained prior artefact/configuration, identity and secret-version references, database schema compatibility and the treatment of in-flight sessions/tool operations. A previous image cannot undo an incompatible data migration or an already accepted external effect. Test the chosen rollback and migration strategy in an isolated environment. These are production extensions; the lab's build-ID tags and cleanup receipts did not implement a release system.

## Observe enough to diagnose without logging the conversation

Prefer allowlisted metadata: revision/digest, request/invocation ID, opaque operation ID, stage, duration, status/error class and bounded usage counters. Avoid raw prompts, credentials, session state, customer IDs and private tool arguments/results in ordinary logs. Hashing a guessable customer identifier is not automatically anonymisation. Give any protected diagnostic capture a specific purpose, access scope, retention and deletion policy.

Secret Manager addresses secret retrieval/storage, not subsequent leakage into a prompt, tool result, trace or error. Test synthetic secret markers across those output paths. Confirm model-call/tool budgets emit useful final status without dumping the rejected input. Distinguish application failures, authentication/permission failures and verifier/harness defects; use [troubleshooting.md](troubleshooting.md) for the observed lab cases.

Completion evidence lists which contracts above were implemented and how each was tested, plus the deliberately deferred items. No single health check, test count or provider deployment status establishes all of them.
