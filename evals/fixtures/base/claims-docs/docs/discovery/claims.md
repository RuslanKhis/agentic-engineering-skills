# Discovery brief: claims triage at Fenwick Mutual

Status: accepted 2026-09-29 by Helen Okafor (Head of Claims Operations)
Prepared by: Larkspur Digital

## The journey today

A first notification of loss arrives by web form or email. A triage handler
reads it, opens the policy in the policy administration system, decides the
claim type and urgency, notes the cover position and routes the claim to a
team. Triage takes a median of 21 minutes per claim (August 2026 sample of 400
claims, claims MI report). 9 % of claims are re-routed after triage because the
first routing was wrong.

## Where it breaks

- Handlers re-read long policy wordings to find the clause that applies.
- Urgent claims (escape of water, uninhabitable home) wait in the same queue as
  routine ones.
- Notes are inconsistent, so the receiving team re-checks cover.

## First workflow and outcome

- **Workflow:** triage of new home claims (motor follows only if home works).
- **Outcome measure:** median triage time per claim, from the claims MI report.
- **Baseline:** 21 minutes (August 2026, 400 claims).
- **Target:** 12 minutes or less on pilot claims.
- **Counter-metric:** re-routing rate after triage must not rise above the
  baseline of 9 %.
- **Threshold to continue:** median at or below 15 minutes after four pilot
  weeks with re-routing at or below 9 %.
- **Decider:** Helen Okafor, Head of Claims Operations.

## Technology fit

An agent with tools (policy lookup) drafting a recommendation for a person to
accept; the decision stays with the handler. Rules alone cannot read free-text
notifications; a single model call cannot check cover without the policy API.

## People

- 14 triage handlers in Leeds; two team leads will label evaluation cases.
- Works council consultation is not required for a decision-support tool
  (HR confirmed 2026-09-24).
- Data owner for the policy system: Raj Mehta (Policy Systems Manager).

## Next

`/adk-system-designer Design the claims triage assistant from docs/discovery/claims.md.`
