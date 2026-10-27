# Situation: interoperability-verify-signed-agent-card

Overlay on support-assistant: a2a-sdk 1.2.3 pinned; `app/agent.py` adds
`RemoteA2aAgent(agent_card='https://partner.example/.well-known/agent-card.json')` (A1: no
signature verification for a card fetched by URL; resolve with get_agent_card(signature_verifier=...)
and pass the AgentCard; re-apply https/same-origin check). Partner email gives the JWKS URL and
key ids out of band, with rotation (A2: key provider on the out-of-band set, not jku; asymmetric
only; PyJWTError subclass for unknown kid; fail closed). The sample card's protected header decodes
to {"alg":"ES256","kid":"card-2026-10","typ":"JOSE","jku":"https://cdn.partner-assets.example/jwks.json"}
— jku on a different host than the out-of-band key set — and it also carries an unprotected
`header` with kid (A3: agent_card_check.py --require-signature --key-host findings; helper does
not verify signatures). A4 graded from answer. Context unchanged.
