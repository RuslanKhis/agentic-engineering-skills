I wrote the A2A exposure code, but none of it has been run. I had no shell in this session, and google-adk and a2a-sdk aren't installed. The new tests in `tests/test_a2a_surface.py` need neither package, so they should pass with `python -m unittest discover -s tests -t .`.

**What I changed**
- **Approvals (`research_agent/agent.py`, `research_agent/a2a_guard.py`):**
  - **Why the existing gate isn't enough:** ADK issue #6461 was still open in 2.8.0. It lets an approval payload arriving over A2A satisfy a `require_confirmation` gate, so that gate can't be the control here.
  - **New agent:** I added `a2a_root_agent`, which has only the market analyst and no procurement sub-agent. A peer reply can't reach `submit_procurement_request`.
  - **Second layer:** `block_gated_tools` is a before-tool callback that refuses that tool if it is ever added.
  - **Unchanged:** `root_agent` keeps procurement with confirmation for the first-party app.
- **Agent card (`deploy/agent-card.json`):**
  - **Shape:** It uses the a2a-sdk 0.3 shape, since `to_a2a` in 2.8.0 can't declare security schemes and so needs a handwritten card. It includes the fields Gemini Enterprise requires and declares its auth scheme.
  - **Content:** It describes capability only, with no instructions or tool names. `SERVICE_HOST` in its `url` is a placeholder.
- **Authentication (`research_agent/a2a_auth.py`, `research_agent/a2a_app.py`):**
  - **Edge:** The plan is Cloud Run with no unauthenticated access.
  - **In the app:** A middleware requires a bearer token on everything except the card. It returns 401, 403 or 503, and the principal is verified with a Google ID-token check plus an `ALLOWED_CALLERS` email allowlist.
  - **Startup:** The entrypoint is `uvicorn research_agent.a2a_app:app`. It needs `SERVICE_URL` and `ALLOWED_CALLERS`.
- **Docs and tests:** `docs/a2a-exposure.md` has the design, assumptions and open questions. The tests cover each auth status, the approval block and the card fields.

**Questions I couldn't ask, and what I assumed** (also in `docs/a2a-exposure.md`)
- **Service URL and project number:** I used placeholders.
- **Gemini Enterprise token:** Cloud Run documents its token as arriving in `X-Serverless-Authorization`, which Cloud Run consumes, while my middleware reads `Authorization`. If the app never sees a bearer token, every call returns 401. Only a live test will settle this.
- **Per-user identity:** I assumed none, so all calls arrive as one service principal.
- **Buying over A2A:** I assumed Gemini Enterprise users shouldn't be able to buy reports.
- **Pin compatibility:** `to_a2a(agent, agent_card=...)` and `AgentCard.model_validate` are unchecked against the 2.8.0 and a2a-sdk 0.3.x pins.

**Left undone, each needing your approval**
- Deploying to Cloud Run.
- Granting the invoker role to the Discovery Engine service agent.
- Registering the card in Gemini Enterprise.
- A live `message/send`.
- Running `agent_card_check.py` on the generated card.
- A persistent task store and shared session service, so keep max-instances at 1 until then.
- Adding `google-adk[a2a]` and `google-auth` to the image. I left `pyproject.toml` unchanged.