# Invoice agent: dev run 2026-10-27

**Decision accuracy: 36 of 40 (90%).** Target agreed with ops: 88%. Met.

| Field | Extraction accuracy |
| --- | --- |
| supplier_name | 22 / 40 (55%) (worst field) |
| invoice_number | 38 / 40 (95%) |
| total | 39 / 40 (97.5%) |
| po_number | 40 / 40 |
| po_amount | 40 / 40 |

Wrong decisions (agent decision ≠ reviewed decision): dev-011, dev-014,
dev-027, dev-036. All four are decision-stage errors, so the decision prompt
needs work.

Running cost about £0.05 an invoice against £0.90 for a clerk: 18 times
cheaper.

**Next steps (proposed):**

1. Sprint 1: fix supplier-name extraction (lowest field accuracy).
2. Sprint 2: rewrite the `decide_hold` prompt to fix the four wrong
   decisions.
3. Ask the finance director on 20 November to switch off the clerk check
   from January, since we beat the 88% target.
