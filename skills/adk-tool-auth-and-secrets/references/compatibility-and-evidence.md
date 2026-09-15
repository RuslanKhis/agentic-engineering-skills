# Compatibility and provenance

## Preserve the target's version contract

Inspect declared and locked Python/ADK/GenAI/auth/provider versions and the selected environment's installed distribution metadata. Do not import the target application, change its package manager or install a different SDK to make this skill fit. A static manifest observation does not establish the installed environment.

The reusable inspector and public-text adapter require Python 3.11+ and use only the standard library. Before using SDK-shaped adapters, verify the actual pinned event, ToolContext, callback and session contracts. If the target version lacks a required interface, identify it and stop that dependent implementation/live check; propose a compatible local adaptation or an explicitly approved version change. A version different from the historical baseline is unverified, not automatically unsupported. Do not claim compatibility with “latest ADK”.

The source baseline was Python 3.11, google-adk 2.8.0, google-genai 2.23.0, google-cloud-secret-manager 2.30.0, google-auth 2.58.0, httpx 0.28.1, Firebase Admin 7.5.0 and grpcio 1.83.1. The source requirements range for grpcio and its resolved snapshot are different facts. The original offline acceptance used pytest 9.1.1. Newly packaged helper/agent checks have their own versions in [skill-validation.md](skill-validation.md).

## Rule provenance and limits

This skill adapts Chapter 9 of *Agentic Engineering* and its MIT-licensed companion. The following optional source locators are relative to `chapter-09-security-and-secrets/` in the [companion repository](https://github.com/RuslanKhis/agentic-engineering-adk-gcp). They are provenance, not runtime dependencies; all actionable guidance is inside this skill.

| Rule or lesson | Source/test | Evidence boundary |
| --- | --- | --- |
| Verified user → owned session → credential selection | `security_agent/api.py`, `tools.py`; `tests/test_api.py`, `test_services.py` | Offline controlled identities; production Firebase/multi-issuer mapping not certified |
| Exact numeric versions and user-separated cache | `secret_store.py`, `services.py`; `test_secret_store.py`, `test_db.py` | Real Secret Manager used with a shared-container lab; layout not a production default |
| State/PKCE/replay | `services.py`, `db.py`, `oauth_provider.py`; `test_api.py`, `test_db.py` | Mock consent; browser and real account/client binding are production requirements, not supplied guarantees |
| Rotation status/version CAS; losing version retirement | `services.py`, `db.py`; `test_provider_failures.py` | Offline rotating/nonrotating disconnect races; reconnect and replicas need additional coordination |
| Transient token errors preserve consent; local disconnect survives revoke outage | `oauth_provider.py`, `services.py`; `test_provider_failures.py` | Offline injected failures; early local disconnect ordering remains production work |
| Thought filtering and sanitisation before framework logs | `api.py`, `agent.py`; `test_runtime_verification.py` | Actual ADK orchestration with model boundary double; not every exporter |
| IAM propagation/readiness, setup/repeat, exact cleanup absence | `scripts/verify_runtime_identity.py`, `gcp_lifecycle.sh`, `cleanup_gcp.sh`; final audit | Scoped live resource workflow; no blank-project API activation or hosted app |
| Tool execution verified beyond final prose | `audit/verify_gemini_http.py`; `audit/FINAL_VERIFICATION_2026-09-14.md` | Six real Gemini workflows, 12 model sends, six tool calls; real Secret Manager, mock Calendar, development JWT, local gateway |

The historical report records **67 offline tests** and those six live workflows separately. These are not results for a user's project or for newly bundled code. Real Google account linking, Firebase integration, managed consent, distributed lifecycle, hosted deployment and every-exporter auditing remain unverified by that campaign.

Browser binding, trusted provider-account/client continuity, early local disconnect, shared revision checks, cross-replica invalidation and total work budgets are explicit production principles retained from the revised chapter. Do not export the demo OAuth scaffolding as a production starter. The code's broader Calendar scope and one-call policy are local choices, not universal requirements.

Managed-auth documentation was checked on 15 September 2026: current Google guidance documents Agent Identity `/authProviders/` migration for ADK 2.3.0+, while an ADK Preview page still shows legacy `/connectors/`. This is documented support, not a successful test of this skill's managed branch. Recheck the selected API and pinned SDK when implementing; see [continuations](adk-continuations.md).

Independent community project; not affiliated with or endorsed by Google. The bundled adapter is adapted from the companion's response projection; the included MIT notice preserves its licence. No book purchase, local book checkout or proprietary service is required.
