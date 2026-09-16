# Carry guardrails into a deployed service

Read when moving guarded work from a local runner to an API/worker, increasing replicas, or verifying resource cleanup. Outcome: a concrete integration and acceptance plan for the chosen host. This is a production design, not a supplied deployment or a claim that Chapter 2 ran in a managed service. The chapter's proposed cloud implementation was removed before deployment; its verified model work used a local application.

## Build the serving contract before infrastructure

Map these responsibilities onto existing components. Keep the chosen framework, hosting platform and storage rather than replacing them with the chapter demo.

| Boundary | Implementation decision | Evidence needed |
| --- | --- | --- |
| HTTP/CLI/worker entry | Derive principal, tenant, request and owned session from trusted context; reject malformed input before expensive work | The actual served route rejects forged identity without model/tool dispatch |
| Admission | Read a valid control snapshot; acquire bounded execution capacity and atomically reserve required allowances | Two competing requests cannot both consume the last shared allowance |
| Runner construction | Apply the selected model/output settings and explicit model-call limit to the runner that actually executes | Inspect the outgoing SDK request, including a policy change between turns |
| Tool execution | Share one invocation guard; resolve existing business operations; authorise any new effect | Parallel/repeated calls respect the chosen batch contract and cannot bypass approval |
| Event consumption | Account completed usage, preserve partial/unknown states, render trusted business receipts and consume to completion | Final-answer-like events do not suppress later accounting; an empty/error stream is not labelled successful |
| Exit/recovery | Close iterators/clients, settle or retain uncertain reservations, release locally owned permits and preserve durable operation state | Exceptions, disconnects, restarts and retry all leave honest state |

One useful ordering is: authenticate/validate → read policy → acquire capacity within a bounded wait → reserve allowances → create configured runner → execute guarded work → account and settle → release capacity. If the architecture reserves before queueing, bound the reservation's queue lifetime too. Recheck policy when a long wait could make it stale. Track whether each acquisition succeeded so cleanup never releases an unowned permit or refunds an uncreated reservation.

For a web service, use lifespan/startup hooks for reusable clients and supported SDK preparation. Readiness should test the required configuration and dependencies without generating model responses, publishing reviews or executing a business tool. Give the application enough time to return its static stop before the hosting/proxy timeout: choose an inner work deadline plus a bounded accounting/cleanup margin, then an outer request deadline. A platform timeout or client disconnect cannot prove remote work was cancelled.

## Bound traffic as well as individual invocations

Token allowance, request/token rate, active model-work concurrency and queue depth solve different problems. Define all that the service needs, including per-tenant fairness. A queue wait consumes the request's time allowance; a full queue should return a static busy response before provider dispatch rather than grow without bound. Avoid acquiring an execution slot and then sleeping through automatic retries indefinitely.

A semaphore limits one process only. If there are several workers or replicas, use a shared admission service or explicitly document the aggregate bound. Hosting instance limits can constrain part of the system but do not supply shared tenant quotas or a monetary cap. For Cloud Run, evaluate configured concurrency and autoscaling together using the [official autoscaling guide](https://docs.cloud.google.com/run/docs/about-instance-autoscaling); validate the actual settings after deployment.

Separate local request slots from distributed leases/reservations. After cancellation, release a local slot when local work has stopped, but do not mark a possibly running remote operation completed or free its reserved spend merely because its caller disconnected. Define reconciliation and lease recovery so another worker cannot replay an uncertain write.

Acceptance: saturate a synthetic queue/permit pool and verify zero provider calls for rejected work; cancel a queued request; inject an exception after each acquisition; run two processes against the intended shared store; restart one process with an outstanding operation. Use fakes/emulators first, then an approved isolated service test if required. A local lock or in-memory test is not evidence of distributed correctness.

## Prepare and verify the selected deployment

Before requesting deployment approval, prepare the actual application/configuration, offline tests, target-specific command plan, resource ownership record and readback/rollback/cleanup plan. Review the deployment tool's current contract; this reference does not supply generic commands that happen to fit every host.

- Package only the required application, dependency declarations and runtime assets. Exclude credentials, `.env` files, test ledgers, local sessions and fake-provider launchers from the deployed entry point. Preserve dependency pins and capture the resulting image/source identity.
- Configure model backend, project, location, store, review transport, time limits and concurrency explicitly. Verify the effective configuration in the container/process. A configured production review transport must fail clearly when incomplete rather than silently select an in-memory mock.
- Use a dedicated runtime identity and least-privilege access to the selected store/topic. Local CLI or ADC success does not establish deployed permissions. Cloud Run uses its configured service identity for authorised Google API access; verify that identity separately. Attach the intended service account rather than shipping a key or setting `GOOGLE_APPLICATION_CREDENTIALS` in the service. [Official service identity guidance](https://docs.cloud.google.com/run/docs/securing/service-identity).
- Persist only the state whose contract needs restart survival; keep caller ownership checks even when sessions are durable. Avoid assuming instance affinity makes local counters or pending reviews reliable.
- Smoke-test the actual deployed route: identity rejection, disabled admission with zero model dispatch, permitted operation, dependency failure/recovery and truthful user-visible state. Health checks, successful image builds and a development UI loading are separate evidence.

In an SSE/browser adapter, keep status, business receipts and completion distinct. A pending review can be shown before the final prose; an empty final response, missing usage, provider failure or disconnect needs an explicit incomplete/unknown state. Recover the input/loading state after an error without automatically resubmitting a consequential action. Treat these as production acceptance requirements; not every one was implemented in the local chapter.

## Cleanup evidence and remaining costs

Use a private ownership record with resource kind, exact project/location/ID, creation operation, creator/run label and whether the resource pre-existed. A new project needs fresh state; do not reuse old deployment IDs. Record accepted-but-unresolved operations and reconcile them before deciding what exists or resubmitting creation. Obtain separate confirmation for exact owned deletions; never infer ownership from a convenient name prefix alone.

Report cleanup in distinct categories:

| Category | Check and honest interpretation |
| --- | --- |
| Running compute/services/jobs | Direct service inventories across recorded locations, including all pages; deletion acceptance is not absence |
| Persistent and ancillary resources | Owned storage, images, disks, reservations, secrets/versions and service-managed backends as applicable; removing the frontend may leave them |
| Retained/soft-deleted data | Inspect retention/version metadata and expiry; an empty live-object list does not prove no retained storage |
| Unknown or denied inventory | Record permission/API/pagination gaps; `403`, disabled API and a partial listing are not zero resources |
| Shared/pre-existing resources | Preserve them; record remaining dependencies and settings without treating their existence as failed owned cleanup |
| Billing evidence | Distinguish removed active resources, retained chargeable state, historical charges and delayed reporting; avoid a universal zero-cost promise |

Cloud Storage soft-deleted objects remain billable until their retention expires. Existing retention is not shortened by changing the policy later; deleted buckets can hide contents that cannot be inventoried without restoration. Do not restore or alter shared retention merely to make an audit look complete. Record known expiry and uncertainty, and seek a separate decision if restoration is actually needed. [Official soft-delete behaviour and pricing](https://docs.cloud.google.com/storage/docs/soft-delete).

The project's historical cleanup recheck exposed these distinctions: empty runtime inventories coexisted with retained storage and denied/disabled inventory paths. That was a broader project inspection, not proof of a Chapter 2 cloud deployment. Use asset search to discover candidates, then direct service APIs and ownership evidence to resolve them. Do not enable APIs or delete unfamiliar resources simply to turn unknowns into a clean report.
