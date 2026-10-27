# designer-sow-from-plan: what the fixture holds

Base claims-docs only (no overlay): `docs/discovery/claims.md` (outcome measure, baseline 21 min,
target 12 min, counter-metric re-routing 9 %, decider Helen Okafor), `docs/architecture/claims.md`
(R1-R5, C1-C5, SB01/SB03/SB05, D1-D5) and `docs/plans/claims.md`.

Plan facts the SOW must carry (checked with check_schedule.py by the fixture author):
- Phase 1: G01-G06, 21-33 human hours (G01 4-5.5, G02 4-6.5, G03 4-5.5, G04 3-5, G05 3-4,
  G06 3-6.5). At £95 per hour the phase-1 fees are £1,995-£3,135 (21 × 95, 33 × 95).
- Waits: W1 policy API read-only credential from the policy systems manager (Raj Mehta), 5-10
  working days, blocks G02; W2 client security review before the pilot approval, 3-5 working days,
  blocks G06. Both are client dependencies needing an owner and a date (or "<n> working days after
  <event>").
- Resources: Cloud SQL `fm-claims-pilot-sql`, about £1.60 per day idle (pricing read 2026-10-05),
  owned by the cost contract; run cost stated separately from fees. No run-cost ledger exists yet,
  so model and cloud run cost must be stated as an estimate or "to be confirmed", not invented.
- Later list: motor claims, recurring cost review, decommission, production hardening (out of scope
  items for the SOW).

Assertion map: A1 engagement-scoping.md read and the SOW template filled; every deliverable cites
goal IDs and every phase-1 goal (G01-G06) belongs to exactly one deliverable. A2 hours copied from
the schedule (21-33) times £95, no other rate, run cost separate. A3 acceptance criteria with a
comparator threshold, case count, who agreed the cases, method and date (no "answers correctly").
A4 W1 and W2 (and prerequisites such as SME labelling time) as client dependencies with owner and
date; check_sow.py named and, with no shell in the run, reported as not run.
