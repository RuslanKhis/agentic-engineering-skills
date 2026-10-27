# A2A exposure for Gemini Enterprise

Status: code written, **not executed** (no shell, google-adk and a2a-sdk not installed, no cloud access).

## Design

| Item | Decision |
| --- | --- |
| Served agent | `a2a_root_agent` (`research_agent/agent.py`): market research only. No procurement sub-agent. |
| Poisoned-peer / approval rule | Procurement is unreachable over A2A (structural), plus `block_gated_tools` before-tool callback (second layer). Reason: ADK issue #6461, open at 2.8.0, lets an approval payload arriving over A2A satisfy a `require_confirmation` gate, so the existing confirmation is not a safe control on this surface. Approvals stay in the first-party app (`root_agent`) only. |
| Card | `deploy/agent-card.json`, a2a-sdk 0.3 shape (`protocolVersion 0.3.0`, top-level `url`), handwritten: capability only, no instructions or tool docstrings, `securitySchemes` + `security` declared. `to_a2a` on 2.8.0 has no `security_schemes` parameter, so the card is passed in. |
| Authentication | Layer 1: Cloud Run `--no-allow-unauthenticated`; Discovery Engine service agent gets the invoker role (approval, not done). Layer 2: `BearerAuthMiddleware` (401/403/503, only the card is public) with a Google ID-token verifier (audience = `SERVICE_URL`) and an email allowlist (`ALLOWED_CALLERS`). |
| State | In-memory task store and sessions: deploy with max-instances=1 until a `DatabaseTaskStore` and shared session service exist. |

## Questions I could not ask, and the assumption I made

1. Which service URL and project number? Assumed placeholders: `SERVICE_URL` env, `SERVICE_HOST` in the card.
2. Does Gemini Enterprise's token reach the app? Cloud Run documents the Google-signed OIDC token for Gemini Enterprise in `X-Serverless-Authorization`, which Cloud Run's front end consumes. The middleware reads `Authorization`. **Unverified:** if the app never sees a bearer token, every call gets 401. Resolve in a live test; the fallback is to rely on Cloud Run IAM alone and drop layer 2 (not recommended to do silently).
3. Per-user identity? Assumed none: all calls arrive as one service principal unless end-user OAuth is configured at registration. Sessions are then scoped per that principal/conversation.
4. Should Gemini Enterprise users be able to buy reports? Assumed no (read-only over A2A).
5. Is a2a-sdk 0.3.x compatible with `to_a2a` on 2.8.0 as written? Not checked (not installed): confirm `to_a2a(agent, agent_card=...)` and `AgentCard.model_validate` on the pins.

## Run (after approval)

```
SERVICE_URL=https://<host> ALLOWED_CALLERS=service-<N>@gcp-sa-discoveryengine.iam.gserviceaccount.com \
  uvicorn research_agent.a2a_app:app --host 0.0.0.0 --port $PORT
```
`google-adk[a2a]` and `google-auth` must be in the image; `pyproject.toml` pins were left unchanged.

## Not done (each needs approval)

Deploy to Cloud Run, grant `roles/run.invoker`, register the card in Gemini Enterprise (`a2aAgentDefinition.jsonAgentCard`), live `message/send`, `agent_card_check.py` run on the generated card, a2a-tck, persistent task store.
