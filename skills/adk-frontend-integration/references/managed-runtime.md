# Managed ADK execution behind either interface

Use this reference only when the selected JSON or AG-UI gateway calls managed Agent Runtime. The legacy SDK identifiers `vertexai`, `agent_engines`, `AdkApp` and `reasoningEngines` remain exact code/resource names in the recorded implementation. Do not rename them to match product marketing.

For **connecting an existing Runtime**, **preparing an owned deployment**, or **recovering/cleaning up**, read [deployment-runbook.md](deployment-runbook.md). It provides the scoped preflight, default managed-identity check, pinned deployment/configuration contract and gateway/browser handoff without depending on companion scripts. Continue below for the adapter's session and stream behaviour.

## Inspect before connecting

Read explicit configuration for project, Runtime region, model/backend region, model and exact remote resource name. Runtime location and model location are independent. Confirm that the resource name agrees with the selected project and Runtime region. Review environment precedence without printing values: changing a root `.env` does not update a chapter/app-local key, and an exported shell value can override the edited file.

CLI login, Application Default Credentials and ADC quota project are different settings. Read-only project/API access checks must succeed before claiming connectivity. A selected project in an IDE is not proof that CLI or SDK access works. Missing prerequisites can leave local implementation and tests complete while remote validation remains explicitly unverified. API activation, IAM or secret changes require the approval process in `SKILL.md`.

The helper's installed-version gate does not inspect credentials, billing or enabled APIs. Use the runbook's [read-only preflight](deployment-runbook.md#2-read-only-preflight-bootstrap-only-when-required), adapted to the existing project's tools and selected caller/deployer role. Denied access is unknown, not absent resources. Default managed Runtime identity readiness uses the exact project IAM binding, not a customer-project service-account metadata lookup; functional model access remains a separate check.

## Retain the SDK owner

The tested SDK connection retains both the owning `vertexai.Client` and the remote object returned by `client.agent_engines.get(name=...)`. Keeping only the remote object allowed garbage collection of the owner to close the shared async transport. Own them together for the serving lifecycle.

The demonstrated cache retains lifetime; it does not implement complete async shutdown, bounded synchronous startup or multiprocess pooling. For production, construct clients in the supported lifespan, close them explicitly, clean partial initialisation failures and use bounded worker capacity for unavoidable synchronous calls. Verify lifecycle methods in the installed SDK rather than inventing a universal `close` method.

## Enforce session ownership

1. Validate the requested session ID before interpolating it into a provider resource name.
2. Where the direct Session metadata API is available, read the exact session resource. Treat only that API's typed HTTP 404 as confirmed absence. Validate that the returned resource name matches the request and its nonempty `user_id` matches the authenticated application user. This administrative read is not intrinsically scoped to the end user.
3. Propagate permission, availability and malformed-response failures. The managed `:query` path returned a generic HTTP 400 for a missing session during live testing; treating all 400s or 403s as absence would mask other failures and trigger unsafe creation.
4. For JSON, omitted ID can create; a supplied missing ID should follow the selected resume contract. For a browser-allocated AG-UI thread, create that ID only after confirmed absence and authorised creation. An ambiguous create outcome needs bounded readback in the same user/resource scope, not an unconditional repeat.
5. A warm-turn optimisation may avoid a separate metadata lookup **only** when the exact deployed Runner/session configuration is proven to check user/session scope before model execution. The recorded ADK deployment had auto-creation disabled and met that condition; another remote implementation may not. Test missing/wrong-user IDs with zero model calls before adopting the optimisation. On a query failure, bounded metadata diagnosis may clarify the error without retrying the model action.

Forward only the validated new user message and trusted user/session identifiers. Persistent recall after a gateway restart should come from remote session history, not browser history replay. Test this explicitly when claiming persistence.

## Streaming and parsing

Use the pinned SDK's stream parser for SDK JSON-lines/SSE responses. A hand-written split/parser failed despite a completed real provider run. Request ADK SSE streaming explicitly when adapting to AG-UI. Preserve nonpartial confirmed tool calls while forwarding partial public text. Inspect actual tool result variants before locking the public schema.

Use the selected transport reference for terminal outcomes. Retain a client deadline, a gateway deadline covering preparation and query consumption, and appropriate dependency deadlines. Cancellation of an await is not evidence that remote execution stopped. Do not retry an uncertain mutating invocation to obtain a better latency sample.

Verify the SDK transport's retry policy too. The recorded smoke required both one SDK attempt and an HTTPX transport with retries disabled; application code without a retry loop alone did not establish that bound. The runbook's [verification procedure](deployment-runbook.md#5-verify-without-accidental-repeated-model-work) includes the tested configuration and the required submission-count regressions.

## Authorised live verification and cleanup

Preparation can produce commands and a resource manifest without deploying. Resolve the exact disposable target, region, unique labels, call/attempt limits, deadline and expected spend before paid calls or provisioning. Use the task's existing approval when it covers those exact effects; request approval for missing or expanded scope. A request-count limit and min-zero instances are not spending caps.

Reuse the target's setup scripts only after inspecting their plan and ownership behaviour. Record operation intent before submission, exact resource and operation IDs after acceptance, and provider readback of completion. A CLI exit code or plausible final text alone is insufficient: a tested CLI could print failure and exit zero. Bound polls and reconcile unknown outcomes before resubmitting.

Keep cleanup separate, with confirmation of the exact owned targets and effects unless already authorised in this task. Use the runbook's [recovery table](deployment-runbook.md#6-recover-and-clean-up-the-owned-target) to distinguish unknown acceptance, terminal failure, completed deletion and failed independent inspection. Verify operation completion and exact-resource absence. Preserve unrelated resources and shared prerequisites. A failed inventory is not a clean bill of health, and logical deletion is not proof of physical backup erasure.

Historical evidence covers a prepared API baseline, managed execution and owned cleanup. Fresh-project activation, live interrupted-operation recovery, deployed Cloud Run/GKE variants and production identity were not verified by that campaign. Nothing in this skill authorises repeating it.
