Our side now refuses the partner card unless its signature verifies against a key set we pin. The 21 unit tests pass (`python3 -m unittest discover -s tests -t .`). That run is local (mocked), on Python 3.9 with PyJWT and cryptography. `google-adk` and `a2a-sdk` are not installed here, so the real fetch and verify path has not run.

**What changed**
- **`app/card_trust.py` (new):**
  - `PinnedKeyProvider` takes keys from a pinned JWKS file and ignores the `jku` in the card. It allows only `card-2026-10` and `card-2027-01`, so the 1 December rotation needs no code change. Unknown key ids raise a `PyJWTError` subclass, which lets the verifier move on to the next signature.
  - `fetch_verified_card` verifies with ES256 only through a2a-sdk's `create_signature_verifier`.
  - `check_interface_origins` requires every RPC URL to be https on the origin the card came from. ADK skips that check for a card passed as an object.
- **`app/agent.py`:**
  - `build_verified_agent` is async.
  - On any fetch or signature failure, or a missing JWKS file, it logs the reason and builds the agent without `warranty_partner`. The prompt then tells the model that warranty lookups are unavailable.
  - `RemoteA2aAgent` now receives the verified card object, never the URL.
  - I removed the module-level `root_agent`, because the fetch is async. Nothing else in the repo referenced it.
- **`app/server.py`:** a `lifespan` hook builds the verified agent and the `Runner` at startup.
- **`app/settings.py`:** adds the card URL, key ids and `PARTNER_JWKS_PATH` (default `config/partner-jwks.json`).
- **`tests/test_card_trust.py` (new):**
  - Both rotation keys verify.
  - A rogue key reusing the pinned `kid` is rejected.
  - A `jku` pointing at an attacker host is ignored.
  - An unknown key id fails.
  - Origin and https checks are covered.
- **Pins:** untouched. The `[signing]` extra on `a2a-sdk` is needed for `a2a.utils.signing`, but I didn't edit `pyproject.toml` because AGENTS.md says not to change pins in a feature change. Deciding on the extra is yours.

**What the card checker should flag**

I ran `agent_card_check.py` on `docs/partner/sample-signed-card.json` with `--require-signature` and `--key-host keys.partner.example`. It reported the first three below. The last four came from my own reading of the sample.
1. **`signature_jku_off_origin` (error):** the protected header's `jku` is `cdn.partner-assets.example`. That is neither the card's origin nor the agreed `keys.partner.example`. Ask the partner why. Our provider ignores it either way.
2. **`no_security_schemes` (error):** the card declares no `securitySchemes`.
3. **`signature_unprotected_header` (review):** `header.kid` is not integrity-protected. Only the `kid` in the protected header should be trusted.
4. **Card shape:** it mixes `protocolVersion: "1.0"` with 0.3 fields (`url`, no `supportedInterfaces`). With a2a-sdk 1.2.3 that may fail parsing or transport selection, so ask the partner for a real 1.0-shaped card.
5. **Signature encoding:** the sample signature looks DER-encoded (`MEUC…`). JWS ES256 needs raw 64-byte r‖s, so the sample is probably illustrative. Verify against their real signed card before 1 November.
6. **Uncovered fields:** a2a-sdk drops unknown fields before verifying, so nothing outside its schema is covered by the signature. Ours takes nothing security-relevant from those fields.
7. **Expected fixes:** the checker should also flag signatures on cards that lack `kid`, use symmetric `alg`, or have `typ` other than `JOSE`. It currently reports these only structurally; it does not verify signatures.

**Left undone**
- **Pinned JWKS:** `config/partner-jwks.json` does not exist, because I had no network. Someone must fetch it from `https://keys.partner.example/a2a/jwks.json`, confirm the key ids, and commit or mount it. Until then the service starts but runs without the warranty agent.
- **a2a-sdk interfaces unconfirmed:** I did not run against a2a-sdk 1.2.3, so I have not confirmed:
  - the `key_provider(kid, jku)` signature;
  - the `A2ACardResolver` constructor arguments;
  - the `supported_interfaces` attribute name.
  The code follows the skill reference. Install the pinned SDK and run one real fetch against a signed fixture first.
- **No host-restricted httpx client:** the defence-in-depth client from the reference (refusing any non-card host) is not wired in.
- **Rotation overlap:** from 1 December, both ids need to be in the JWKS file.

**Assumptions I made, since no one could answer**
- Failing closed means degrading to no warranty agent, not refusing to start. Say if you'd rather the service not start.
- The JWKS is a human-reviewed pinned file, not fetched at runtime. That keeps the trust anchor out of the network path.