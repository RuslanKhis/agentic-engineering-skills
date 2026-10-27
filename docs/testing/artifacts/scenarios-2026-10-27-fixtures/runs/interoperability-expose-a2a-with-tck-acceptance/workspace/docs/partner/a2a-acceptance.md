# A2A exposure: acceptance checks (dealer-portal)

Status: **nothing here has been run against the real packages.** The session had
no google-adk, a2a-sdk, PyJWT, TCK checkout or network. Every check below is
marked with the evidence it has today. Do not register the agent anywhere until
the `not run` rows pass; registration needs its own approval.

## Questions I could not ask, and the assumption used

| Question | Assumption in the files |
| --- | --- |
| Public origin of the agent? | `https://triage.service-desk.example` (placeholder in `a2a/agent-card.json`; replace before serving) |
| Scope the partner's token carries? | `triage:invoke`, one scope for the one skill |
| Issuer / JWKS / token URL? | issuer `https://auth.service-desk.example`, JWKS `<issuer>/.well-known/jwks.json`, token URL `<issuer>/oauth2/token`; confirm all three with the auth-server owner |
| Is `aud` exactly `warranty-triage`? | Yes, per the integration request (not the served origin) |
| One instance or several? | One. `to_a2a` uses in-memory sessions and tasks; several instances or restarts need a shared session service and a persistent `task_store` first |
| May the partner trigger `record_triage` (a write)? | Assumed yes, since that is the agent's job. Confirm with the service-desk owner: a partner with this scope can create triage records |
| PyJWT as a new dependency? | Assumed acceptable. It is not in `pyproject.toml` (I may not install or re-pin); add `PyJWT[crypto]` with an exact pin as a reviewed change |
| Does the card's `version` track `pyproject` version? | Yes (test-enforced), see Versioning |

## Files

- `a2a/agent-card.json`: hand-curated 1.0-shape card. Skill text is written for the partner; it carries no instruction text or tool names. Caveat: a top-level `a2a/` directory sits beside the SDK's `a2a` import name. It has no `__init__.py`, so an installed regular package should win, but I would move it (for example to `deploy/agent-card.json`) and update `CARD_FILE` in `triage/a2a_app.py` and `tests/test_a2a_card.py`. I had no shell to move it.
- `triage/a2a_auth.py`: ASGI bearer gate (401 / 403 / 503, only `GET /.well-known/agent-card.json` public, sets `scope["user"]` so ADK takes the user id from a verified principal) plus the PyJWT verifier.
- `triage/a2a_app.py`: `to_a2a(root_agent, agent_card=card)` plus the gate. Uses unverified calls (`ParseDict` into `AgentCard`; `add_middleware`); see check C0.
- `tests/test_a2a_card.py`, `tests/test_a2a_auth.py`: stdlib-only unit tests (no ADK or SDK imports). Written but **not executed**: this session had no shell.

## Versioning policy (answer to the partner)

Two independent numbers, both visible in the card:

1. **Protocol version**: `supportedInterfaces[].protocolVersion` (`1.0`). The partner pins this. We change it only by adding a second interface entry next to the old one, announced with at least one release cycle's notice (period to be agreed with the partner; proposed 90 days), then dropping the old one.
2. **Agent version**: card `version`, semver, equal to the `pyproject.toml` version.
   - patch: prompt or wording change, no change to what the skill accepts or returns;
   - minor: new skill, or a new optional behaviour;
   - major: skill removed or renamed, categories or urgency scale changed, security scheme or scope changed, new required input.
   A major bump gets the same notice as a protocol change. The card is the contract: the model, instruction and tool docstrings are not.

## Acceptance checks

Evidence labels: `offline` = no SDK needed; `local` = needs installed packages on loopback; `not run` = nothing executed.

### Card

| # | Check | How | Evidence today |
| --- | --- | --- | --- |
| C1 | Card is 1.0 shape, https interface with `protocolVersion`, no 0.3 fields | `tests/test_a2a_card.py` | offline, not run (no shell) |
| C2 | Card `version` equals project version and is semver | same | offline, not run |
| C3 | Only `clientCredentials` flow declared; card and skill requirements reference a declared scheme and scope | same | offline, not run |
| C4 | No instruction text or tool names in the card | same | offline, not run |
| C0 | `triage.a2a_app` imports and serves the card on the pinned stack | start with `uvicorn triage.a2a_app:app --host 127.0.0.1 --port 8001`, then `curl -s http://127.0.0.1:8001/.well-known/agent-card.json` and diff against `a2a/agent-card.json` | not run |
| C5 | Served card passes the helper, zero errors | `python .claude/skills/adk-agent-interoperability/scripts/agent_card_check.py --file a2a/agent-card.json --installed-a2a-sdk <exact pinned version> --fail-on error`. Use `--file`, not `--url`: the card advertises the public origin, not loopback | not run |
| C6 | Card is a fetch of the **served** card, not just the file | compare C0 output to the file; a mismatch means the SDK rewrote something | not run |
| C7 | `Cache-Control` / `ETag` on the card (TCK `CARD-CACHE-001..003`, SHOULD) | TCK run below; manual `curl -I` | not run |

### Versioning

| # | Check | How | Evidence today |
| --- | --- | --- | --- |
| V1 | `A2A-Version` handling, empty header means 0.3 (TCK `VER-SERVER-001..003`, MUST) | TCK, scoped (below). The TCK sends no token, so expect these to fail behind the gate; accept only with V2 | not run |
| V2 | Own test: with a valid token, `A2A-Version: 1.0` is accepted; an unsupported major (e.g. `9.0`) is rejected with a version error, not a 500 | add to a loopback test using a locally signed test token (see A5) | not written; needs the SDK |
| V3 | Version bump discipline | CI: fail if `pyproject` version changes without the card `version` changing (C2 does this) and a changelog line in `docs/partner/` | C2 only |

### Authentication

| # | Check | How | Evidence today |
| --- | --- | --- | --- |
| A1 | No token, bad token, wrong scheme, no subject: 401 with `WWW-Authenticate` | `tests/test_a2a_auth.py` | offline, not run |
| A2 | Valid token without `triage:invoke`: 403 `insufficient_scope` | same | offline, not run |
| A3 | Verifier outage: 503, no challenge (so the partner retries instead of re-authenticating) | same | offline, not run |
| A4 | Only `GET` on the exact card path is public | same | offline, not run |
| A5 | **Real token path**: locally generated key pair, JWKS served on loopback, tokens with wrong `iss`, wrong `aud`, expired, `alg=none`, HS256 signed with the public key, unknown `kid` all give 401; correct token gives 200 | write against `make_jwt_verifier` once PyJWT is installed | not written, not run |
| A6 | Principal reaches ADK: the session `user_id` equals the token `sub`, and a body-supplied `user_id` is ignored | local run with a scripted model; read the created session's user id | not run |
| A7 | A message claiming approval or identity does not run a gated action | N/A today (no `require_confirmation` tools); revisit if one is added | n/a |
| A8 | TCK `AUTH-SERVER-002` (every request authenticated) | **Fails by design**: the TCK sends no credential. A1 is the evidence | accepted deviation |
| A9 | TLS 1.2+ in production (`AUTH-TLS-001`) | deployment check at the real ingress | not run |

### Conformance (A2A TCK), scoped

Run from a separate directory, with the TCK pinned to a2aproject/a2a-tck v0.2.5 (commit 5daf014). It is a downloaded repository, so **review it and keep it in its own empty directory**, passing paths as arguments:

```
./run_tck.py --sut-host http://127.0.0.1:8001 --level must -- -k 'agent_card or versioning'
```

Against a local instance only; never Agent Runtime or a registered endpoint. Because the gate rejects the TCK's unauthenticated RPCs, run it twice and record both:

1. gate on: expect `CARD-DISC-001`, `CARD-EXT-001`, `CARD-SIGN-*` (card unsigned, so skipped) to pass; `VER-SERVER-*` and `AUTH-SERVER-002` fail by design.
2. a test-only instance without the middleware (start it from a scratch module, never from `a2a_app`): `VER-SERVER-*` must pass.

Record `reports/compatibility.json`, the exit code, and the deferred ids. Deferred and why: core-operation scenarios (scripted `messageId` prefixes a real agent does not honour); `AUTH-SERVER-002` (no credential option). Whether the TCK works with an a2a-sdk 1.x server is unconfirmed; an unexpected failure there is a finding, not a pass.

## Known risks left open

- Task history returned to the caller includes tool calls and their arguments and tool results (observed in the skill's trial on 2.12.0). Decide what the partner may see before go-live; `lookup_product` and `record_triage` currently return no personal data.
- `triage/tools.py` `record_triage` accepts any `claim_id`: a partner can record triage for a claim that is not theirs. Per-caller claim ownership is out of scope here (owner: `adk-tool-auth-and-secrets`).
- No rate limiting or token-lifetime policy; no signed card (optional; see the skill's signed-card section).
- Registration (Agent Registry, Gemini Enterprise) not started; needs approval and the platform's own test call.
