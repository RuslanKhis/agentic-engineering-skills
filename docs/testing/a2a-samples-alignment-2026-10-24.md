# a2a-samples alignment — 24 October 2026

Source note: [a2a-samples comparison](../research/a2a-samples-comparison-2026-10-24.md).

## Changed journey

`adk-agent-interoperability`, consuming and exposing a signed A2A agent card;
`adk-tool-auth-and-secrets` gained the CIBA paragraph (reference only, no
journey change of its own).

## Offline evidence

`agent_card_check.py` gained structural signature checks
(`--require-signature`, `--key-host`, sixteen signature codes) and, after the
trial, `--fail-on error|review` (exit 3). The helper suite has 43 tests, ten
of them new: eight for signatures (well-formed, jku origin and https, required
signature, weak or incomplete protected headers, missing components and
unprotected header, uncovered fields, a signed 0.3 card, a fetched card's own
origin), one for `--fail-on` and one for the 1.0 `protocolVersion` message.

## Fresh-agent trial

A fresh agent with only the skill package built a synthetic `catalog_agent`
exposed with `to_a2a` and an orchestrator consuming a partner's signed card,
on google-adk 2.12.0 and a2a-sdk 1.2.3, offline and model-free. Task: sign our
card with ES256, verify the partner's card against an out-of-band key set,
keep the RPC origin pinned, and test a good card, a tampered card, an
attacker re-sign with an attacker `jku`, an unknown `kid` with rotation and
our card served three times; then run the card checker on a good and a bad
card.

Result: 18 of 18 tests passed (`python -m unittest discover -s tests -t .`).
Tampered description and RPC URL were rejected; the attacker re-sign was
rejected with a pinned provider and, as a control, accepted by a provider
that follows `jku`; rotation worked with old and new signatures, a provider
raising `KeyError` aborted it, and an updated key set verified the new `kid`;
an off-origin interface, card URL, request host and an http interface were
refused; our card served three times carried 1, 1 and 1 signatures (3 when
signed in place, as a control); an in-process end-to-end call through the
verified card object completed. The checker reported 0 errors on our card and
7 errors on the bad card (`rpc_url_not_https`, `no_security_schemes`, two
`signature_alg_not_asymmetric`, `signature_kid_missing`,
`signature_jku_not_https`, `signature_field_missing`), and 0 errors on a
tampered card, as the skill says a structural check would.

Ease: 4 of 5. Every claim in the new section that the trial tested held.

## Frictions and fixes (same day)

1. The module-level rule for `RemoteA2aAgent` clashed with an async verified
   fetch. Fixed: the signed-card section and `SKILL.md` say to build that
   agent in a startup factory (`lifespan` or `asyncio.run`).
2. Origin pinning had no ADK recipe. Fixed: an httpx request hook passed
   through `a2a_client_factory=ClientFactory(ClientConfig(httpx_client=...))`.
3. The advertised URL was shown with a trailing slash; 2.12.0 strips it.
   Fixed in the `to_a2a` notes.
4. The checker said "ADK's AgentCardBuilder writes one" for a 1.0 card that
   declares `protocolVersion` per interface. Fixed: the message now says the
   card declares it per interface and that Gemini Enterprise reads the
   top-level field; test added.
5. The checker exited 0 with errors and had no CI gate. Fixed: `--fail-on`,
   exit 3, documented in `SKILL.md` and validation; test added.
6. Helper messages named only `RemoteA2aAgent` 2.8.0. Fixed: "2.8.0 to
   2.12.0" (the check is present in the 2.12.0 source).
7. Nothing said that `default_skill_security` leaves the card-level
   requirement empty. Fixed: stated with the builder's docstring as source.
8. No pattern for a PEM key in Secret Manager. Fixed: pinned secret version,
   `load_pem_private_key`, publish the public key with its `kid`.
9. No "before" report for a new service, and `--url` on a local `to_a2a`
   advertising its public URL trips the origin check. Fixed: use `--file` on
   the generated card; `--url` only where the fetched and advertised origins
   match.
10. No test runner named; pytest absent. Not changed: the validation
    reference already says to use the target's interpreter, pins and runner.

## Limits

The trial ran in-process with a model-free agent; no network peer, no
Secret Manager and no Gemini Enterprise registration were exercised.
