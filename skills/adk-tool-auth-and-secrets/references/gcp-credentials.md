# Keyless credentials, Secret Manager and approved live work

Read only when workload identity, application credentials, Secret Manager or an approved GCP verification is involved. Discovery and plan preparation are read-only. Use the entrypoint's exact-plan approval boundary before external changes or paid calls.

## Choose the authority

| Destination | Credential choice |
| --- | --- |
| Google Cloud API acting on project-owned data | ADC using attached workload identity, impersonation or federation appropriate to the environment |
| Private Cloud Run service | Caller ID token with the receiving service's exact audience and scoped invoker permission |
| Application-wide external API | Provider credential from a protected store; workload IAM governs retrieval |
| User-owned external data | Delegated credential; also read [OAuth lifecycle](oauth-lifecycle.md) |

Keep deployer, gateway and tool-runtime permissions separate when they are separate principals. Avoid service-account private keys as a Secret Manager bootstrap mechanism. Preserve the target's backend and model choice; a Gemini API key does not establish permissions for Secret Manager or a delegated provider.

## Inspect without revealing credentials

Record project, location/global resources, expected runtime identity, operator identity, quota project, enabled-service requirements, secret container/version references and resource ownership. Check presence/configuration without printing payloads. Reading a secret or minting a short-lived token is a separate credential operation, even if it creates no infrastructure. Never run an inherited deployment script merely to discover its targets.

Inspect the target's dependency/configuration mechanism. A root environment file does not update a service-specific environment automatically; a long-running process may need a restart after configuration changes. Keep generated `.env.example` values illustrative/configurable; never copy the operator's live values. Secret references remain sensitive metadata and need careful reporting.

## Implement custody and activation

Use the smallest justified IAM role at the lowest suitable resource boundary. A combined broker may need payload read plus version-management permissions; a separated agent reader usually does not need to rotate credentials. Inspect conditional grants where needed rather than claiming version restrictions are impossible. Do not use project-wide roles to overcome propagation.

Select exact numeric secret versions from trusted configuration/index data. With several users in one container, `latest` can select another user's token. This demonstrates the mapping risk; it is not a recommendation to use that layout universally. Large/high-risk credential populations can justify a dedicated broker or managed vault.

A version write and metadata activation are different operations. Use conditional publication and reconcile losing writes; keep provider invalidation semantics in mind before rollback. Bounded caches must include the credential identity/version/revision, expire conservatively and honour invalidation. API access is network I/O: thread offloading does not create an end-to-end deadline or cancel underlying SDK work. Bound transport attempts and total work using the pinned clients.

## Plan, validate, clean up

Before an approved campaign, prepare a concrete ledger: exact project/location, identity and IAM changes, resource names/ownership markers, existing resources to preserve, commands, maximum attempts/wall time/model sends or spend, expected outcomes and exact cleanup commands. Check required APIs without automatically enabling them. Use fresh explicitly owned names; do not assume a deployment-state-file feature exists in the target.

After account creation, distinguish resource visibility from IAM effectiveness. Under the approved credential probe, check the intended impersonated ADC identity and quota project first. Retry only recognised propagation conditions, with a configured finite deadline/attempt count. The historical successful grant took about 90 seconds; it is evidence for bounded readiness, not a universal delay or reason to broaden access. Scope/API errors and persistent denial require diagnosis.

Test actual secret access after identity readiness, then the deterministic application/provider boundary, then any approved model acceptance. Reuse neither old deployment IDs nor the historical campaign's permission to spend. A paid model response must prove correlated tool use, not only fluent text.

Cleanup is a separate confirmed operation targeting only resources recorded as created in this invocation. Preview all targets and verify ownership before the first deletion. Preserve pre-existing secrets, grants and identities, including when setup was partial. Retry safely for already-absent owned resources and confirm absence through successful exact listings. Permission denial is not absence. Report any unconfirmed deletion/revocation rather than claiming cost closure. Disconnect, remote provider revocation, disabled secret versions, resource deletion and local credential cleanup are different outcomes.

Official references, consulted only for the selected platform/version: [Secret Manager practices](https://docs.cloud.google.com/secret-manager/docs/best-practices), [access control](https://docs.cloud.google.com/secret-manager/docs/access-control), [Cloud Run caller authentication](https://docs.cloud.google.com/run/docs/authenticating/service-to-service).
