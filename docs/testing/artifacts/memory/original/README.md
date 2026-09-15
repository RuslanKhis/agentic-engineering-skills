# Language helper fixture

A small Python Google ADK assistant. A trusted authenticated application constructs
`UserScope(app_name, user_id)` and calls `make_agent(store, scope)`. The scope is
server-owned: there is no client-supplied identity or model tool argument for it.
This fixture begins with a storage seam and agent factory but no preference feature.

## Required interface and behaviour

Keep the public constructors and method signatures in `profile_store.py` and `agent.py`.
A preferred language is one of `English`, `French`, `Spanish`, `Japanese` (exact values).
`save_preferred_language` stores only with explicit `consent=True`; absence of consent
raises `PermissionError` and leaves any existing preference unchanged. Unsupported
language or empty/whitespace scope fields raises `ValueError` without changing data.
`get_preferred_language` returns the stored setting or `None`; save replaces the
previous setting; forget removes it and is idempotent. Settings are isolated by both
app_name and user_id. Use SQLite, including across reconstructed stores and independent
Python processes. Preserve identity strings exactly after validating nonempty content.

`make_agent` returns a real ADK `LlmAgent`. Supply an ADK instruction callable that reads
the trusted user's latest stored language each time instructions are evaluated (including
on an already-constructed agent), and clearly asks the model to answer in that language.
After forgetting, neither old preference nor another user's setting appears; ordinary
instructions may remain. Do not persist conversation content or put identity fields in
model-visible instructions. Tests may evaluate instructions with a ReadonlyContext.
Do not add an HTTP server or cloud service for this fixture.

## Local execution

Use this existing interpreter, which already has the pinned packages and pytest:
`$PYTHON`
Read its installed package source if needed; do not modify that environment or inspect
the surrounding book project. Work only in this fixture. Use synthetic identities.
All tests must run offline: use ADK types, SQLite and local doubles, without Google
model calls, credentials, cloud resources or network-based test dependencies. Do not
install packages or inspect credential files. You may read the installed skills.
