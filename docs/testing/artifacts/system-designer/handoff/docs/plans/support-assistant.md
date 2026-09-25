# Plan: saved language and streamed support replies

Status: **draft; first local goal ready for a future implementation session**.

Canonical architecture: [Support assistant design](../architecture/support-assistant.md).
This plan is the continuation source of truth until the user adopts another spec/tracker. Nothing has been implemented or tested.

## Destination and scope

A signed-in individual saves, reuses and forgets a language preference, with streamed replies that clearly complete, fail or become interrupted. Preserve the agreed React/OIDC/PostgreSQL/Cloud Run stack and verified user ID. No group preference implementation is part of the pilot. Work authorized for the next coding session is local development and tests only; the current request remains design only.

No application files, dependency pins or entrypoints were inspected. All module/interface names below are proposed responsibilities to map onto existing code at the start of a goal. Do not create a parallel application or replace established routes just to match these names.

## Implementation map

| Linked decision / requirement | Component and concrete integration seam | GCP responsibility | Primary specialist / verification gap |
| --- | --- | --- | --- |
| D02/D03, R01–R03 | `ProfileService`/repository behind current authenticated API; React preferences control; `InvocationContextLoader` loads exact setting before invoking `AgentAdapter` | Existing PostgreSQL persists settings; Cloud Run later hosts application | `adk-memory-architecture`; map actual schema/routes and local DB setup |
| D04, R04/R06 | Streaming gateway projects adapter events into application schema; React chat reducer renders partial and terminal states; status and cancel routes share auth | Later verify Cloud Run forwarding and lifecycle | `adk-frontend-integration`; prove incremental sockets and actual browser behavior |
| D05, R01/R05 | Existing OIDC middleware supplies trusted context; owner-qualified profile/session/status queries; database admission and fenced completion | Workload credentials separate from caller authority | `adk-tool-auth-and-secrets`; inspect existing login and session mapping |
| D06, R02/R04 | Agent factory and `App`/`Runner` adapter; assess `DatabaseSessionService`; current profile projects to invocation-only context; only public text events cross gateway | Model backend remains unselected; hosting stays Cloud Run | `adk-workflow-design`; exact version, signatures, final/error/cancel semantics and session behavior unresolved |
| Bounds and release | Application deadline/output limits; later inspect `RunConfig` call limits, combined retries, pool sizes and shutdown | Cloud Run config/readback, identity/networking and deployment recovery later | `adk-operational-guardrails` for limits; `deploy-adk-on-google-cloud` for hosted follow-up |

The named ADK specialists are available in this session's skill catalogue; their instructions were not applied or verified against an application here. The future session must load the selected specialist. Optional Matt Pocock planning workflows have not been discovered or read and are not prerequisites.

## Dependency order

| ID and goal | Type | Depends on | Primary skill | State / blocker |
| --- | --- | --- | --- | --- |
| G01 — Save a language and apply it in a later local conversation, then forget it | Implementation | None; initial repository/local DB inspection included | `adk-memory-architecture` | Ready for local continuation; no coding authorized in this design turn |
| G02 — Choose and verify ADK integration contracts | Discovery | None; may run independently of G01 | `adk-workflow-design` | Ready as local inspection/documentation; version/provider evidence may remain unavailable |
| G03 — Stream locally with explicit completed, failed and interrupted states | Implementation | G01 public invocation seam | `adk-frontend-integration` | Proposed; uses controlled adapter, independent of cloud and ADK version |
| G04 — Run the pilot through the pinned ADK runtime with controlled model responses | Implementation | G01, G02, G03 | `adk-workflow-design` | Blocked on Q01 and G02 evidence |
| G05 — Validate live behavior and Cloud Run delivery on an approved target | Discovery + later implementation | G04 and Q02/Q03/Q05 decisions | `deploy-adk-on-google-cloud` | Outside current authorization; no credentials/target/provider choice |

### G01 — First useful local behavior

- **Outcome:** user A saves Spanish, restarts the backend, opens a new conversation and sees a controlled reply generated with Spanish as its active setting; forgetting removes the setting for a later conversation. Links: D02/D03/D05, R01–R03.
- **Bounded scope:** an owner-scoped preference store/API, React save/forget controls, current-setting loading at invocation start and a controlled agent adapter. This is a vertical path through UI → verified-context seam → API → PostgreSQL → invocation → visible response. Full streaming and actual ADK/model behavior follow in G03/G04.
- **First action:** read target project instructions, architecture, dependency manifests, OIDC middleware, chat routes, profile/session models and existing public-boundary tests. Identify existing local PostgreSQL harness and entrypoints without importing application code or exposing secrets. Record actual paths here. If local PostgreSQL is unavailable, record setup as a local prerequisite and complete isolated code/tests where possible; do not claim persistence from an in-memory fake.
- **Implementation route:** extend existing conventions with `ProfileService` and owner-qualified repository; add revision-conditional save/forget; call it from existing preferences UI and invocation handler. Define an `AgentAdapter` input carrying trusted owner/session/invocation and optional language; provide a deterministic local adapter with visible fixtures and input recording. Keep it replaceable by ADK without changing the public preference contract.
- **Prerequisites:** access to the actual target repository and its normal local test setup. No ADK version, cloud resource or group-account decision is required. Use a test-only verified-identity fixture at the trusted boundary for A/B identities; do not add a production auth bypass or accept an arbitrary user ID from the browser.
- **Skills:** primary `adk-memory-architecture`; supporting `adk-tool-auth-and-secrets` for caller/session authority and `adk-frontend-integration` for the UI/API seams. Available by catalogue; future session must read them.
- **Acceptance:** save commits and UI acknowledges; restart the real local backend against the same PostgreSQL data; new conversation's adapter input contains the saved language; B cannot read/update A or invoke A's conversation; missing auth invokes no model; forget clears the value; subsequent invocation has no saved preference; delayed save at an old revision conflicts and cannot resurrect it; DB failure yields an explicit error instead of false success.
- **Verification:** deterministic service tests plus HTTP/database integration and a real React/browser journey. Use public APIs and adapter inputs as the main boundary, not mocks of implementation internals. Commands must be taken from inspected project scripts; none are known yet. Label controlled reply evidence as pipeline correctness, not natural-language quality or verified ADK behavior.
- **Execution scope:** local code, local test database migrations/fixtures and local tests in the next coding session only. No remote calls, provisioning, dependency selection based on guesswork or hosted migrations.
- **Status/evidence:** ready design slice; no files changed, commands run or acceptance tests completed in an application. Proposed test boundaries remain proposals.

### G02 — Resolve the ADK adapter contract

- **Question/outcome:** which package version and supported interfaces supply invocation context, persistent sessions, incremental public text, terminal errors and cancellation while keeping profile data out of durable reusable state?
- **Scope and stopping condition:** inspect the target manifest/lockfile and existing runtime; if no pin exists, select one explicitly in the implementation session and collect version-matched official evidence before coding the ADK adapter. Record exact package pin, supported interface signatures, event-to-public-schema mapping, session ownership/persistence behavior, partial-event selection, cancellation/deadline behavior and retry controls in a short evidence note linked here. Stop when these contracts are proven or name a specific unsupported contract and a bounded replacement decision. No open-ended platform survey.
- **Integration points:** agent factory, Runner invocation, session adapter and gateway event projection; candidate names are `LlmAgent`, `App`/`Runner`, `DatabaseSessionService`, `RunConfig`. None are executable specifications yet.
- **Skills:** primary `adk-workflow-design`; supporting `adk-memory-architecture` for session persistence and `adk-frontend-integration` for event delivery.
- **Acceptance/evidence:** official version-specific references plus a local contract probe, when a dependency version is available, that emits multiple text events and a terminal outcome using a controlled model. Verify error and cancellation paths and what is persisted. No provider credentials needed. If external documentation or installation is not authorized/available, record the exact unanswered interface and leave G04 blocked; G01/G03 continue.
- **Status:** proposed discovery, no evidence collected. This goal chooses the package contract; it does not select a live model by unsupported claim.

### G03 — Honest local streaming

- **Outcome/links:** the user reads progressive text and can distinguish success, failure and interruption. D04/D05, R04–R06.
- **Scope/route:** authenticated streaming endpoint, gateway event projection, owner-qualified invocation status/cancel, durable completion record, session admission/fencing and React reducer. Reuse G01 identity/profile loader and controlled adapter. No replay or automatic generation resume.
- **Prerequisites:** G01's public invocation seam and local DB. Set finite fixture limits; production capacity values remain unknown.
- **Skills:** primary `adk-frontend-integration`; supporting `adk-operational-guardrails` for total deadlines and bounds; auth guidance for newly exposed routes if needed.
- **Acceptance:** controlled adapter sends separate delayed deltas visible before final completion over real sockets; errors after text never become complete; premature EOF and cancellation are visibly interrupted; completed-status lookup recovers a lost terminal event; foreign-user status/cancel access fails; duplicates/gaps follow defined sequence behavior; private runtime fields never reach the browser; overlapping send is rejected; stale worker cannot commit after fencing; process restart exposes interrupted status for abandoned work.
- **Evidence/execution:** deterministic reducer/gateway tests, local PostgreSQL restart checks, real socket timing and actual browser UI. Local only; capture commands and results in this goal. A spinner or buffered test response does not satisfy incremental delivery.
- **Status:** planned; not started. Cloud transport remains unverified even after local acceptance.

### G04 — Real ADK runtime, controlled model

- **Outcome/links:** the same local journey passes through a pinned ADK runtime, preserving preference, ownership and stream contracts. D03/D04/D06, R01–R06.
- **Scope/route:** implement the version-proven adapter at agent factory/Runner/session seams; project current preference without storing it as authoritative session memory; translate actual runtime events and terminal conditions; preserve existing support behavior after inspecting its tool boundaries.
- **Prerequisites:** G02 resolved contracts and G01/G03 passing. If support tools have external effects, identify their authorization/replay requirements before enabling them in this test path.
- **Skills:** primary `adk-workflow-design`; supporting `adk-agent-evaluation` for controlled Runner/behavior cases, memory/frontend specialists for their changed seams.
- **Acceptance/evidence:** repeat the saved/new-conversation/forget, wrong-owner, partial failure, cancellation and late terminal-error cases through the real Runner with controlled model responses. Record outgoing preference projection, persisted events and absence of forbidden model/tool attempts. Inspect actual public browser stream. This proves integration, not live model compliance.
- **Execution/status:** local only; blocked on G02. No provider or hosted tests authorized.

### G05 — Future live and hosted evidence

- **Outcome/links:** determine whether the chosen model follows language behavior and the existing Cloud Run deployment preserves the tested stream/lifecycle contract. Architecture Q02/Q03/Q05/Q06.
- **Bounded scope:** first settle product language behavior and retention; identify exact model/provider, region, existing deployment/database target and workload identities. Verify current official limits, buffering/lifecycle, pricing and SDK behavior. Define bounded request/time/token/cost acceptance and rollback before a live run. Do not replace the accepted stack without a demonstrated incompatibility.
- **Skills:** primary `deploy-adk-on-google-cloud`; supporting `adk-agent-evaluation` for language quality and failure coverage, `adk-operational-guardrails` for aggregate work limits.
- **Acceptance/evidence:** future controlled live language cases, hosted progressive timing and failure/restart paths, deployment readback, owner isolation, compatible schema rollout/rollback and forget preservation. Named target, credentials and explicit execution scope are prerequisites.
- **Status:** blocked on future evidence and authorization; no cloud action is part of the current continuation prompt.

## Future decisions and optional Matt Pocock workflow

The only group-account question is: **will a future feature permit shared preferences?** If yes, a later decision must define who owns them, who edits/forgets them and how individual overrides work. It blocks a future shared-preference goal, not G01–G04. Keep that question linked to Q04 instead of making all pilot work wait for a broad architecture interview.

The user mentioned Matt Pocock's skills as a possible later workflow, not an instruction to invoke or install them now. If selected later, discover and read the installed workflow first:

- For settled multi-session work, `to-spec` → `to-tickets` → `implement` may adapt this plan. Keep module/interface choices in its spec and link detailed path/API evidence here if the workflow excludes those details. Small ready work can go directly to `implement` or the relevant ADK specialist.
- For material unresolved planning, `wayfinder` can carry the destination, accepted stack, precise open decisions and dependencies. Q04 is a future decision, not a reason to reopen the agreed pilot. Do not treat this Markdown plan as an already imported native map.
- `tdd` is optional; preserve proposed versus accepted public test boundaries. Do not infer approval of a testing method from this handoff.

No workflows were installed or executed and no tickets were created. Missing optional skills do not block direct continuation with this plan. If a spec/tracker is adopted, use one authoritative status source and make this plan point to it.

## Resume here

**Next ready goal: G01.** It delivers useful behavior using the agreed stack while ADK/provider selection remains isolated to G02.

Copyable continuation prompt:

```text
Use adk-engineer to implement G01, “Save a language and apply it in a later
local conversation, then forget it,” from:
docs/plans/support-assistant.md

Read the linked design:
docs/architecture/support-assistant.md

Preserve React, the existing OIDC login and verified user ID, PostgreSQL,
Cloud Run as the future host, and individual-only preference ownership.
Read the actual target repository instructions and inspect its existing
entrypoints, auth, preference/chat seams and tests before editing. Map the
proposed components onto its conventions; do not scaffold a replacement app.

Use adk-memory-architecture as the primary specialist, with
adk-tool-auth-and-secrets and adk-frontend-integration at the changed seams.
Implement only G01 with a controlled local agent adapter. Do not guess or
require an ADK package version for this slice. Do not wait for the future
group-account decision, install optional planning workflows, create issues,
call live model/provider services, or deploy.

Work within local development and tests. Verify save → backend restart →
new conversation uses the saved setting, wrong-user denial, forget → no
setting on the next invocation, stale-write rejection and database errors.
Use actual local PostgreSQL for persistence evidence and the existing
trusted-identity test seam. Distinguish fixture behavior from live model
quality. Record actual paths, commands, results and remaining blockers in
G01; leave later goals and unverified provider contracts explicit.
```
