I wrote the A2A entry point, an OAuth bearer gate, a curated agent card, tests and an acceptance document. I ran none of it. This session had no shell, no google-adk, no a2a-sdk and no PyJWT, so every check is `not run`.

**What I added**
- `a2a/agent-card.json` is the card, written by hand in the 1.0 shape. It declares only the `clientCredentials` flow with scope `triage:invoke`, and has one skill. Card and skill both carry the security requirement. It has no instruction text and no tool names.
- `triage/a2a_auth.py` is the bearer gate:
  - A missing or invalid token gets 401 with a challenge.
  - A valid token without the scope gets 403.
  - A JWKS outage gets 503, so the partner retries instead of re-authenticating.
  - Only `GET /.well-known/agent-card.json` is public.
  - It sets `scope["user"]` so ADK takes the user id from the verified token subject.
  - The PyJWT verifier checks issuer, audience `warranty-triage`, expiry and subject.
- `triage/a2a_app.py` wires `to_a2a(root_agent, agent_card=card)` behind the gate. It uses `ParseDict` into `AgentCard` and `add_middleware`, which I couldn't verify against the pinned packages.
- `tests/test_a2a_card.py` and `tests/test_a2a_auth.py` are stdlib-only unit tests. They cover the card shape, version, scheme and scope consistency, no leaked internals, and every gate outcome.
- `docs/partner/a2a-acceptance.md` has the card, versioning and authentication checks, each with its evidence status. It also has the scoped TCK command and the versioning policy to give the partner.

**Versioning policy**
- The partner pins the interface `protocolVersion`.
- The card `version` is semver and must equal the `pyproject.toml` version; a test enforces it.
- Breaking changes (a major bump) get advance notice. I proposed 90 days, which you need to agree with the partner.

**Questions and assumptions** (all listed in the doc)
- **Public origin:** I used the placeholder `https://triage.service-desk.example`.
- **Scope:** `triage:invoke`.
- **Issuer and token URL:** `https://auth.service-desk.example`, with the JWKS at `/.well-known/jwks.json` and the token URL at `/oauth2/token`.
- **Instances:** a single instance, since sessions and tasks are in memory.
- **Writes:** I assumed a partner may trigger `record_triage`, which writes a triage record. Please confirm.
- **PyJWT:** I assumed adding it as a new dependency is acceptable.

**Left undone**
- **Tests:** I haven't run the unit tests, so run `python -m unittest discover -s tests -t .` first.
- **TCK:** the A2A TCK is not run. Behind the gate, `AUTH-SERVER-002` and `VER-SERVER-*` fail by design. The doc says to run a second instance without the gate to cover versioning.
- **Card and token checks:** I did not run the card helper against the card. I also did not write the real-token tests (A5) or the `A2A-Version` rejection test (V2).
- **Dependencies:** `PyJWT[crypto]` is not in `pyproject.toml`. I couldn't install or pin it, so add an exact pin.
- **Stray directory:** the top-level `a2a/` directory sits next to the SDK's `a2a` import name. I had no shell to move it, so move it, for example to `deploy/`, and update the path in two files.
- **Known risks:** `record_triage` accepts any `claim_id`, so a partner can write triage for claims that aren't theirs. Task history returned to the caller includes tool calls and results. There is no rate limiting.
- **Registration:** not started.