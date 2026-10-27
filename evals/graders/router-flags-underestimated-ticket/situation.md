# router-flags-underestimated-ticket: what the fixture holds

Original context: "The journeys fixture support agent with T-202: per-customer Gmail
connection estimated at 1-2 hours of agent-assisted human effort, for a 30-customer
pilot in three weeks. ADK is not installed."

Workspace = support-assistant base + `tickets/T-202.md`.

- T-202 asks for per-customer Gmail connection (delegated OAuth: consent, token
  storage keyed by verified user, refresh, disconnect/revocation) at 1-2 hours.
- Reading Gmail message content needs a Gmail restricted scope (gmail.readonly);
  an app used by external customers needs Google's OAuth app verification and, for
  restricted scopes, a security assessment — a multi-week calendar wait that collides
  with "pilot in three weeks" (A1).
- The consent screen is not configured (a step only a person can do, A3).
- Expected: says the estimate is far too small before/while working, builds a slice
  that fits (e.g. credential store keyed by principal, connect/disconnect state,
  token-never-in-events checks, with fakes), proposes the remainder as new tickets
  with estimates (A2), states human review/verification hours and person-only steps
  (A3), records it in the ticket's Evidence (A4).
- google-adk is not installed: SDK-dependent tests are reported as not run.
