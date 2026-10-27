# Travel desk assistant

A chat assistant for Tidewater Travel's corporate customers. Travellers ask about their company's
travel policy and their itineraries, and ask to change bookings (dates, seats, hotel nights).
Each customer company is a tenant; travellers sign in with the company's OIDC provider.

- Proposal: `docs/architecture/proposal.md`
- Accepted product constraints: `docs/architecture/constraints.md`
- Prototype code: `app/` (Python, google-adk 2.12.0, FastAPI) and `web/chat.js`

Tests: `python -m unittest discover -s tests -t .`
