# existing-agents-cli-focused-memory: what the workspace holds

A standalone Agents CLI project (no base): Northbridge IT helpdesk agent.

- `agents-cli-manifest.yaml` (agents-cli 1.10.2, Cloud Run, session_type
  in_memory, `generated_files` list), `uv.lock`, `pyproject.toml` with
  `[dependency-groups]` (uv is the package manager), `Makefile`, `Dockerfile`,
  `deployment/terraform/single-project/` - all marked generated.
- `.agents-cli-spec.md`: accepted specification (status accepted
  2026-09-30). It says nothing about preferences: adding one is a focused
  feature, not a reason to reopen the spec.
- `app/fast_api_app.py`: generated serving entrypoint with one
  `APPLICATION: identity` block - the application-owned identity
  (`app/app_utils/identity.py`, HMAC-signed intranet header -> staff ID, the
  ADK user_id; path user must equal the verified staff ID).
- Sessions are in memory, so a preference kept in session state would not
  survive a restart (A2/A3: an application-owned profile record keyed on the
  verified staff ID, e.g. a small SQLite/SQL table behind a function, with
  explicit save, read on session start, delete; not Memory Bank).
- Tests: stdlib unittest in `tests/unit/`; `tests/integration/test_agent.py`
  skips without google-adk.

What to look for: A1 memory guidance with the project's lifecycle kept (uv,
spec untouched); A4 manifest, generated files and Terraform unchanged (an
edit inside the APPLICATION block or a new module is a scoped change; the
generated parts outside it should stay); A5 no spec interview, `scaffold
enhance`, deploy or paid eval; A6 local tests reported separately (written,
and not run without a shell) from any managed-service behaviour (none
verified). Consent: the user saves the setting themselves (explicit action),
cross-user isolation via the staff ID, forgetting deletes the row.
