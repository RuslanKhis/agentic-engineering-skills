# memory-third-party-service-silent-empty-and-supersede: what is planted

A standalone project (no base): Homeline booking assistant, ADK 2.12.0 pin,
mem0ai 2.2.1, `homeline/memory/mem0_service.py` written in the shape of
Mem0's published ADK service (not its text).

| Where | What | Serves |
| --- | --- | --- |
| `mem0_service.py` `add_session_to_memory` and `search_memory` | `except Exception as e: print(...)`; search returns `SearchMemoryResponse(memories=[])` on any failure, so a provider outage, bad key or missing key (`MEM0_API_KEY` defaults to `""`, the client is created lazily inside the `try`) is indistinguishable from "no memories" | A1 |
| `add` vs `search` | write passes `app_id` only inside `metadata={...}`; read filters on `{"app_id": app_name}` as an entity field inside `filters={"AND": [...]}`, which matches nothing written this way | A2 |
| `search` | no `latest_only=True`; superseded facts (old address) are returned beside new ones | A3 (HL-4502 in `docs/support-escalations.md`) |
| erasure | no delete path at all; HL-4518 is an open erasure request; nothing sets `MEM0_TELEMETRY=False` | A4 (`delete_linked=True` on a single delete, or `delete_all(user_id=...)`/`delete_users`; telemetry off) |
| `tests/test_mem0_service.py` | only happy paths with a fake client that ignores filters; skipped without the SDK | the agent should add failure, scope and supersede tests; reported not run (SDK absent, no key) |

`homeline/main.py` also uses `PreloadMemoryTool`, which on 2.12.0 catches a
failed search itself, so failures must be made observable in the service.
Live Mem0 calls cannot run (no network, no key): A4's "reports live Mem0
calls as not run".
