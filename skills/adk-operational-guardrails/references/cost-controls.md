# Application and cloud cost controls

Read for staged degradation, billing notifications, live preflight or emergency shutdown. Outcome: minimise new spend through application controls, with explicit authority for cloud changes.

## Inspect before proposing changes

Identify the selected API backend, model, project, location and runtime identity from non-secret configuration. Root and chapter-local `.env` files can select different backends; changing a root API key does not update nested keys. Inspect variable names/presence and provenance without displaying values. A successful CLI login does not prove ADC identity, quota attribution, service-account permissions or model access.

For Google Cloud, read project access, required enabled APIs and billing status using explicit project/account arguments. Use machine-readable output, timeout each command and suppress credential/provider payloads. Avoid a command that implicitly enables APIs; if a read requires unavailable access/API, report that prerequisite rather than granting roles or enabling services. Model availability requires a separately approved bounded live call. Do not reconfigure login or create credentials during inspection.

Determine needed APIs from the chosen mode: model calls, reading billing and publishing notifications have different requirements. Cloud Billing is not automatically necessary for local tool-guard implementation. Recheck current official setup/CLI help before generating exact commands.

## Control sequence

Use warning → policy-approved degradation → reduced work/output → application kill switch. Configure thresholds for the product; historical percentages are examples. Store one versioned control snapshot so readers do not see contradictory partially updated flags. Specify propagation latency, cache policy, stale-state handling and explicit recovery authority.

Billing notifications are delayed signals, not transactional token admission. Validate envelope/base64/JSON, numeric finiteness, currency, expected account/project/budget and accounting period. Authenticate delivery separately from field validation. Deduplicate and order notifications with a defined version/period policy; apply related controls atomically. A new billing period or lower ratio must not silently clear an operator emergency stop. Design an explicit reset process and test stale/duplicate/reordered/new-period events. The companion's individual flags latch on; it has no such versioned recovery service.

Ordinary alert budgets do not stop usage. Cloud Billing spend cap budgets can pause eligible service usage, but enforcement is delayed and in-flight/fixed costs can remain. Check current eligibility and scope before relying on this optional provider control; it does not replace application admission. [Official spend-cap documentation](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps).

Provider quotas limit capacity/rate, not necessarily total money. Estimate costs with current prices and observed input/output/reasoning, and distinguish estimates from billing invoices. Avoid embedding model names, current prices or account-specific identifiers in reusable code.

## Emergency billing and uncertain operations

Billing unlink is a disruptive infrastructure operation affecting more than the agent. Prefer the application kill switch. Keep billing mutation credentials and code out of model tools and normal runtime imports. If requested, prepare a simulation-first, allowlisted, least-privilege operator plan with exact target and blast radius; obtain explicit approval for the concrete live commands and verify pre/post state.

The original companion `disable_billing_for_project(project_id)` performs a real API mutation; it has no dry-run, allowlist or approval object. Never run it as a simulation or copy it into normal serving code. The skill deliberately supplies no billing-disable executable.

When API activation or any asynchronous mutation was accepted but output parsing failed, reconcile the recorded operation before resubmitting. CLI success payloads can be null/empty and completion can appear on stderr; match the installed CLI contract with fixtures. Unknown state is not failed state. Setup should preserve existing resources and record only newly created resources for a separately confirmed cleanup.

Acceptance tests before live use: application stop prevents model dispatch, malformed/untrusted/stale messages cannot loosen controls, restart retains intended policy, API-operation recovery does not repeat submission, dry-run makes zero mutations, and cleanup refuses unrelated resource ownership. No live deployment, Pub/Sub delivery, billing shutdown or cleanup lifecycle is established by the companion's mocked tests.
