# Language helper fixture

A small Python Google ADK assistant. A trusted authenticated application constructs
`UserScope(app_name, user_id)` and calls `make_agent(store, scope)`. The scope is
server-owned: there is no client-supplied identity or model tool argument for it.
The SQLite profile store retains each user's consented preferred language, and the
agent factory reads the latest setting whenever ADK evaluates its instructions.

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

## Using the setting

```python
from agent import make_agent
from profile_store import ProfileStore, UserScope

store = ProfileStore("profiles.sqlite3")
alice = UserScope("example-app", "synthetic-alice")  # From trusted application code.
bob = UserScope("example-app", "synthetic-bob")
store.save_preferred_language(alice, "French", consent=True)
store.save_preferred_language(bob, "Japanese", consent=True)
alice_agent = make_agent(store, alice)

store.forget_preferred_language(alice)
assert store.get_preferred_language(alice) is None
assert store.get_preferred_language(bob) == "Japanese"
# alice_agent's next instruction evaluation also reflects the forgotten setting.
```

Reuse the same SQLite file across conversations and process restarts. Each operation
uses a short-lived connection; successful writes commit before returning, and failures
propagate to the caller. The store retains only the exact application ID, user ID and
language. Instruction evaluation reads the trusted scope captured by `make_agent`,
without caching the setting or copying session state or conversation content.

## Offline tests

Run from this fixture using the documented interpreter, without loading unrelated
pytest plugins or writing bytecode into the preinstalled environment:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  "$PYTHON" \
  -B -m pytest -q -p no:cacheprovider --basetemp=.pytest-tmp
```

The suite checks validation and consent without mutation, replacement, exact identity
preservation, isolation across users and applications, repeated forgetting, and storage
across reconstructed stores and four independent Python processes. Agent tests use real
ADK `LlmAgent`, `ReadonlyContext` and instruction evaluation, covering new conversations,
updates and forgetting on existing agents, untrusted session state, and storage failures.
Network connection attempts, Google credential discovery/loading and Google Gen AI client
construction are blocked in the tests. No model is invoked.
