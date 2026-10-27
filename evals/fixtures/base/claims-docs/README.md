# Claims triage assistant

Larkspur Digital's engagement with Fenwick Mutual (a UK home and motor insurer)
to help claims handlers triage first notifications of loss (FNOL). The
assistant reads a new claim's notification, checks the policy's cover through
the policy system's read-only API, and drafts a triage recommendation (claim
type, urgency, cover position with the clause it relies on) that a handler
accepts or changes.

- Discovery brief: `docs/discovery/claims.md`
- Design: `docs/architecture/claims.md`
- Plan: `docs/plans/claims.md`

No application code yet; the build starts after the client signs the
statement of work.
