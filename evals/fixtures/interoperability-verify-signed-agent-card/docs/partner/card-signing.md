# Partner card signing (email from the bike maker's platform team, 2026-10-21)

From 1 November our agent card at https://partner.example/.well-known/agent-card.json
carries a JWS signature (detached, in the card's `signatures` array).

- Key set: https://keys.partner.example/a2a/jwks.json
- Current key id: `card-2026-10` (ES256). Next key id: `card-2027-01`, published
  in the same key set from 1 December; both are valid during the overlap.
- Please refuse the card if the signature does not verify.

A sample signed card is attached as `sample-signed-card.json`.
