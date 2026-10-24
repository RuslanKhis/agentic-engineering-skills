# a2a-samples compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [a2aproject/a2a-samples](https://github.com/a2aproject/a2a-samples)
at `main` commit `6603ba3` (2026-08-04; Apache-2.0, no NOTICE), cloned on
24 October 2026 into its own directory and read, never run, with the A2A
specification at main `98279d6` (2026-10-20) and tag v1.0.1 (§7.6 and §8.4).
Files read: `samples/python/agents/sign_and_verify_agent_card/`
(`__main__.py`, `test_client.py`, `requirements.txt`, pins a2a-sdk 1.1.0),
`samples/python/agents/multitenancy/a2a_server.py` and `README.md`,
`samples/python/agents/headless_agent_auth/` (`agent.py`, `pyproject.toml`,
`uv.lock`, its middleware), the Go and JS signing samples' key providers,
and the ADK samples' lock files. Checked against the installed a2a-sdk 1.2.3
(`a2a/utils/signing.py`, `client/card_resolver.py`,
`client/transports/tenant_decorator.py`) and google-adk 2.12.0
(`a2a/agent/_remote_a2a_agent.py`, `a2a/utils/agent_to_a2a.py`,
`a2a/converters/to_adk_event.py`).

**Maintenance.** Quiet: no commit on `main` for 81 days on the day of the
check (October pushes are Dependabot branches); not archived; the latest tag
is an alpha from May. The signing sample was last touched in July, the CIBA
sample in October 2025. Cited at a pinned commit; no helper depends on it.

**Conclusion.** Of the memo's three claims, signed cards hold, and they
expose two framework gaps worth acting on: ADK 2.12.0 never verifies a
signature on a card it fetches by URL, and verifying it yourself switches off
ADK's origin check. CIBA and multitenancy hold only partly: the CIBA sample
runs on pre-1.0 types with Auth0 and LangGraph and does not import on a2a-sdk
1.2.3, and the multitenancy sample routes by path without authentication. The
interoperability skill now carries the signing rules for both sides, the card
checker checks a signed card's structure, and the tool-auth skill says where
CIBA fits.

## Method

Facts were read from the sample source and the SDKs rather than READMEs, and
the signing behaviour was confirmed with two scratch probe scripts against
the installed a2a-sdk 1.2.3, offline; no sample code ran. The research was
done by a read-only agent and its central claims were re-read in the
installed source before any edit. One scenario case covers the journey; the
fresh-agent trial is in the
[testing record](../testing/a2a-samples-alignment-2026-10-24.md).

## Drift corrected

- `a2a-contracts.md` said the repository was "not read here" and listed it by
  name; it is now read and cited at the commit.
- `agent_card_check.py` "does not yet check signing": it now checks the
  structure; the signature's validity, caching headers and extended-card
  authentication remain manual items.
- The existing TCK scenario's assertion about manual items was narrowed to
  match.

## Imported, by specialist

- **adk-agent-interoperability.** A "Signed agent cards" section: the JWS
  fields and header rules (§8.4); the consumer path through
  `get_agent_card(signature_verifier=...)` with the origin re-check it
  requires; the key provider as trust anchor (never the card's `jku`;
  `PyJWTError` for an unknown `kid` so rotation works; asymmetric only); the
  fields a 1.x verifier drops and therefore does not cover; the producer's
  sign-a-copy rule, explicit `alg`, signing once at startup for `to_a2a`
  and the key's source. `tenant` as caller-controlled routing. The card
  checker gained `--require-signature`, `--key-host` and sixteen
  signature codes, with eight tests, and after the trial `--fail-on` for CI.
- **adk-tool-auth-and-secrets.** CIBA as a case of the application-broker
  contract, with the user hint from the verified principal, a pending status
  instead of a blocked request, one-operation scope (§7.6.4) and the caller
  side of `mock_function_call_for_required_user_auth`.

## Routed, not copied

Nothing; the repository holds samples, not skills.

## Vendored assets

None.

## Left out, with reasons

- The samples' key providers (Python, Go, JS) that fetch keys from the
  card's own `jku`, the `{kid: PEM}` key file and the key generated per
  process: they defeat the signature they check.
- `headless_agent_auth`'s code: pre-1.0 a2a-sdk types, a middleware that
  lets every request through when the card declares no auth, a default bind
  on all interfaces, exception text in 403 responses, a blocking CIBA wait,
  a model-chosen user hint and a hard-coded model with no lifecycle date.
- The ADK samples' `_resolve_user_id` (commit 7f05d56), whose anonymous
  fallback puts every unauthenticated caller under one user; ADK 2.12.0's
  `A2A_USER_<context_id>` is stronger and already documented.
- Cryptographic verification inside the helper: it would need a2a-sdk,
  pyjwt and cryptography in a stdlib helper; the reference gives the
  verifier round trip as a project test instead.
- The OID4VP and secure-passport extensions: not reviewed.

## Limits

a2a-sdk 1.2.3 was read; the samples pin 1.1.0. The CIBA flow was read, not
exercised. Whether ADK's route helper passes `cache_control` through to the
card route was not checked.
