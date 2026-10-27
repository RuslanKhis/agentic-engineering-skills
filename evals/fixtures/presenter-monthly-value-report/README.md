# Claims triage assistant

Larkspur Digital's engagement with Fenwick Mutual (a UK home and motor insurer)
to help claims handlers triage first notifications of loss (FNOL). The
assistant reads a new claim's notification, checks the policy's cover through
the policy system's read-only API, and drafts a triage recommendation (claim
type, urgency, cover position with the clause it relies on) that a handler
accepts or changes.

The pilot went live for 14 triage handlers on 2026-08-25.

- Discovery brief: `docs/discovery/claims.md`
- Design: `docs/architecture/claims.md`
- Plan, measurement and incident records: `docs/plans/claims.md`
