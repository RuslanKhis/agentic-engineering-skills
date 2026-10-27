I wrote the G02 code and tests, but none of it has been run: Bash is disabled in this session, so I couldn't run the tests or import the code. The ADK 2.12.0 import paths and signatures are unchecked against the installed package. I didn't look outside the workspace for it.

**What changed**
- `claims/memory.py` (new): an `after_agent_callback` that writes the session to Memory Bank with the verified user ID as scope. It writes nothing if the policyholder declined, if the setting can't be read, or if no settings source is configured. A failed write is logged and doesn't break the reply.
- `claims/agent.py`: added `PreloadMemoryTool()` for recall and wired in the callback.
- `claims/server.py`: passes `VertexAiMemoryBankService` on the existing `AGENT_ENGINE_ID` to the Runner and sets up the Firestore-backed settings.
- `claims/firestore_repo.py`: added `FirestoreMemorySettings`.
- `tests/test_memory.py` (new): offline tests with `InMemoryMemoryService` for A1 (earlier facts recalled), A2 (another policyholder gets nothing), A3 (declined means no write), plus the unconfigured and failing-setting cases.
- `docs/plans/claims.md`: updated the G02 status and evidence line.

**Assumptions** (nobody was available to ask)
- **Where the setting lives:** the plan doesn't say where "declined memory" is stored. I assumed a `memory_declined` boolean on Firestore `policyholders/{id}`, with a missing document or field meaning not declined. Is that where it actually lives?
- **Callback tests:** they use a fake callback context rather than a full Runner with a scripted model, so the real Runner path isn't covered yet.

**Left undone**
- Run `python -m unittest` locally.
- The live recall check on the dev Agent Engine, which needs approval.
- Memory Bank topic limiting from D1, because `add_session_to_memory` takes no topic config. Wiring it would mean switching to `add_events_to_memory` with `custom_metadata`, which I couldn't check without the installed package.
- G07 (the portability write-up) is untouched.