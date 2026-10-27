# Cohort rules, autumn validation (fixed 2026-10-06)

- Cohort A is the development cases under `cases/dev/` as listed on 2026-10-06. Cases are not
  added, removed or re-labelled after that date.
- A case passes when the export is produced, the review accepted the draft, and the decision
  matches the officer's label.
- A failed attempt stays in the record with its charges; a later continuation is linked to it,
  never written over it.
- Ceilings: $0.80 per case end to end; $25 for the campaign.
- Stop rule: two consecutive failures at the same stage stop the cohort until the cause is fixed
  offline.
- Release needs every cohort case passing on one frozen snapshot plus the full regression suite.
