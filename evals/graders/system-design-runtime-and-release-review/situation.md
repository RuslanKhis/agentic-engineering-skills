# system-design-runtime-and-release-review: what the fixture holds

Docs-only overlay: `docs/architecture/reporting-assistant.md`, a runtime proposal for a reporting
assistant on an accepted stack (React, OIDC, PostgreSQL, google-adk on Cloud Run). The proposal
states, as its design, every item the original context listed:

- three replicas without affinity, all events persisted, only the last 20 sent to the model, and
  that window presented to customers as "history deletion" (A1: context selection is not
  retention or erasure; complete tool exchanges must survive trimming);
- exports written to replica-local `/tmp` and served from local disk (A2: durable owner-scoped
  downloads that survive reconnects and other replicas);
- tool results paired by tool name, any final-response event shown as success, reconnect
  re-sending the message (A2/A3: correlate by call id, partial success and late failure, reattach
  to existing work rather than resubmitting);
- per-process session locks across three replicas and slot release on browser disconnect (A4:
  cross-replica coordination and fencing; disconnect does not release capacity still in use);
- a gradual 2.11 to 2.12 rollout while the session storage format changes, old and new instances
  serving together (A5: compatibility, bounded drain, rollback evidence).

A6: choices tied to requirements, tradeoffs and observable checks; version and provider behaviour
left provisional; no implementation or deployment. Only design documents may be written.

Original context: "React, OIDC and PostgreSQL are accepted. Three replicas persist conversation
events but send only the last 20 events to the model, which the proposal calls history deletion.
Exports use replica-local temporary disk. Tool results are paired by tool name, any final-response
event marks success, and reconnect resubmits the message. Per-process session locks and immediate
reservation release on browser disconnect are proposed. A gradual SDK rollout will change the
session storage format. Only a design review is authorized."
