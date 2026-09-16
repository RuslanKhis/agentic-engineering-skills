# Saved response-language preference

## Decision and inspected boundary

Extend the accepted deterministic SQLite profile design. An exact, user-controlled language setting belongs in the existing profile database; semantic memory and transcript extraction are unnecessary.

The accepted spec describes a Cloud Run support assistant with SQLite for the local prototype and identity supplied by authenticated middleware. The manifest declares `agent_directory: app` and `deployment_target: cloud_run`. `app/agent.py` constructs `support` with `configured-model` and the instruction “Answer support questions.” `app/profiles.py` contains only a parameterised `get_profile(db, trusted_user_id)` query returning a language tuple or no row. `app/serving.py` contains comments describing the trusted boundary, not executable authentication or Runner assembly. No schema, database-path configuration, session backend, or tests are supplied. Requirements pin `google-adk==2.8.0` and `google-genai==2.19.0`; installed versions are unverified.

Preserve the accepted spec, generated transport, model, dependency pins and infrastructure ownership. Use the memory specialist for data lifetime and isolation, and the existing Agents CLI conventions for integration.

## Proposed behavior

- **Consent:** “Reply in French” applies to the current request without saving. “Remember French as my response language” explicitly opts into future use. If intent is ambiguous, offer a clear save confirmation explaining persistence and how to forget; denial causes no profile write. Bind any pending confirmation to the authenticated subject and proposed language. A model-supplied consent flag or quoted instruction does not authorise storage.
- **Save/change:** Validate and normalise against supported language codes in trusted code. Extend `app/profiles.py` with owner-qualified, parameterised transactional operations for setting and clearing language. Persist the language and minimal consent metadata, such as consent time/version, after verified explicit consent. Confirm success only after commit. Changing the saved language requires the same explicit intent.
- **Use:** At the existing authenticated serving seam, derive the subject from middleware, authorise session ownership where applicable, and read the profile for each invocation. Supply only the validated language through per-invocation instruction/context integration in `app/agent.py`; keep identity and consent authority in server code. Never mutate the shared root agent's instruction per user. A current explicit language request takes precedence, followed by the saved preference, then existing default behavior. Invalid or absent values use the default.
- **Forget:** Clear only this preference and its consent metadata, preserving unrelated profile fields. Repeating forget is safe. Invalidate derived context/cache values, and prevent old session history from restoring the preference automatically. New saving requires fresh explicit consent. Report success after the transaction commits; a storage failure must report that forgetting was not completed.
- **Concurrency/retry:** Use a per-user preference revision and compare-and-set for pending saves, changes and forget. Forget advances the revision; stale confirmations and replayed saves cannot resurrect the language. A minimal revision marker may remain without the forgotten language. Serialise conflicting operations or reject stale writes and require fresh intent. Refresh derived context before subsequent model invocations.
- **Failure:** A profile-read failure may fall back to the current request/default while reporting that the saved preference is temporarily unavailable. A failed write must never produce “saved.” Keep preference payloads and consent text out of routine telemetry. Retain the setting until changed, forgotten or the account is erased; preference forgetting does not claim to delete historical chat messages or existing backups, whose retention is not specified here.

## Restart persistence and integration

Use a configured, stable file path for the existing SQLite database. A process restart and a new conversation must reopen the same committed file. Do not use an in-memory SQLite database, process dictionary, or ADK state prefix as evidence of persistence. Inspect the existing schema before proposing any additive migration, preserving other profile columns and establishing how legacy language rows demonstrate consent.

Integrate profile access through the existing serving entrypoint rather than replacing its transport or creating a second Runner. Verify its actual authentication/session wiring and the pinned SDK's supported per-invocation instruction or callback seam before implementation. Local SQLite restart persistence does not establish durability across Cloud Run instance replacement or multiple replicas. Shared hosted persistence remains a separate infrastructure decision; this design leaves that ownership unchanged.

## Acceptance checks for later implementation

1. Through the serving boundary with deterministic model/storage doubles, verify trusted identity, cross-user isolation, and rejection of client/model-supplied identity or consent.
2. Verify temporary language selection and declined consent leave the database unchanged; explicit save and change commit only validated values.
3. Close and restart the local process against the same SQLite file; a new session retrieves the saved language and injects the intended per-request instruction.
4. Forget, restart, and verify absence; repeat forget, replay an old save, and complete a stale confirmation without restoring the setting. Preserve another user's preference and unrelated profile fields.
5. Exercise read/write failures and concurrent requests, asserting stored effects and truthful status. Verify shared agent configuration never leaks a user's language.

These checks validate application contracts, not model fluency. Real-model language adherence would need a separately scoped evaluation using the project's adopted Agents CLI process.

## Sources and verification record

Project sources read: `project/.agents-cli-spec.md`, `project/agents-cli-manifest.yaml`, `project/requirements.txt`, `project/app/agent.py`, `project/app/profiles.py`, `project/app/serving.py`.

Skill/reference files used:

- `skills/adk-engineer/SKILL.md`
- `skills/adk-engineer/references/composition.md`
- `skills/adk-memory-architecture/SKILL.md`
- `skills/adk-memory-architecture/references/compatibility.md`
- `skills/adk-memory-architecture/references/sessions-state.md`
- `skills/google-agents-cli-workflow/SKILL.md`
- `skills/google-agents-cli-adk-code/SKILL.md`
- `skills/google-agents-cli-adk-code/references/samples.md`
- `skills/google-agents-cli-adk-code/references/adk-python.md` (instruction, state, memory and callback sections)

Installed domain skills inspected: the four sibling packages listed above. The recipe index identifies `cross-session-memory`, a Memory Bank recipe; its code was not available locally or fetched. Reuse the local references' per-invocation context guidance, while preserving SQLite as the authoritative exact-setting store. The user's read-only design scope supersedes workflow instructions to clone, install, scaffold or run live evaluations; no new design interview or platform prerequisites are needed to deliver this proposal.

Static inspection completed with `rg`, `cat` and `sed` (exit 0); the first login-shell inventory emitted an incidental `rvm`/`ps` warning, and subsequent reads used a non-login shell. No project imports, tests, CLI platform commands, external/model/provider calls or deployments ran. Only this design document was written. Implementation, local behavior and hosted persistence are **not run/unverified**.
