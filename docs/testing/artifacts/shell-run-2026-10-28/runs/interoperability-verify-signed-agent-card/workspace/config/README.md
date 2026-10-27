Place `partner-jwks.json` here: the partner's key set, copied by a person from
https://keys.partner.example/a2a/jwks.json and checked against the key ids the
partner announced (`card-2026-10`, `card-2027-01`) over a second channel. The
service refuses the warranty card if this file is missing or has no allowed kid.
