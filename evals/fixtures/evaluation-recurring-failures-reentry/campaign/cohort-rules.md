# Cohort rules, autumn validation (fixed 2026-10-06)

- Cohort A is the six development cases listed on 2026-10-06. Cases are not added, removed or
  re-labelled after that date, and these rules are not changed for batches already run.
- A case passes when the export is produced, the review accepted the draft, and the decision
  matches the officer's label. The denominator is always the six cases.
- A failed attempt stays in the record with its charges; uncertain charges stay uncertain until
  the provider's usage record settles them.
- Ceilings: $0.80 per case end to end; $25 for the campaign. Request timeout 120 s.
- Stop rule: two consecutive failures at the same stage stop the batch.
- Any batch beyond cohort A, or any new route, needs a new approval from the product owner.
