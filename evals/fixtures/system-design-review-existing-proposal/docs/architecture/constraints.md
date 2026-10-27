# Accepted product constraints

Agreed with Tidewater Travel's product owner (Lena Brandt) and security lead (Omar Haddad),
2026-10-09.

- K1 Each customer company sees only its own documents and bookings. The company (tenant) is
  determined from the traveller's verified sign-in, never from anything the browser or the model
  supplies.
- K2 A traveller's access to a document is checked before any of its content is shown to the
  model or the traveller.
- K3 A booking change happens only after the traveller approves that exact change (booking,
  segment, new values and price difference). Approving one change does not authorise another.
- K4 If the booking provider's reply is lost, the traveller is never charged twice for one change,
  and nobody is told a change happened unless we know it did.
- K5 The assistant runs on Google Cloud (Cloud Run, europe-west1). Existing OIDC sign-in stays.
