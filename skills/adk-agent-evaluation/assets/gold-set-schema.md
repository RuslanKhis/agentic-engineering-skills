# Gold-set and label file schema

One row per verdict: one rater's pass or fail on one criterion for one case.
Expert labels, adjudicated labels and judge verdicts use the same shape, so
`scripts/label_agreement.py` can read them from one file or several. Store
the files under the project's evaluation data directory with the criteria
file they were labelled against.

| Field | Required | Meaning |
| --- | --- | --- |
| `case_id` | yes | Stable ID of the trace or case; the same ID across raters |
| `criterion` | yes | Criterion ID from the versioned criteria file (`cites_policy`) |
| `rater` | yes | Who gave the verdict: an expert's ID, `adjudicated` for the final verdict, or the judge's name with its version (`judge-cites-policy-v3`) |
| `label` | yes | `pass` or `fail`; fail means the failure mode is present |
| `labeller` | yes on `adjudicated` rows | The person or role who gave the final ruling (the quality decision-maker); on expert rows it may repeat `rater` |
| `critique` | on every fail and borderline pass | One sentence on what is wrong or why it passes; on `adjudicated` rows, the reason for the ruling |
| `criteria_version` | yes on gold rows | Version of the criteria file in force when the label was given (`v01`, `v02`; name versions so that they sort) |
| `labelled_at` | yes on gold rows | ISO date the label was given |
| `split` | yes on gold rows that calibrate a judge | `train` (may appear in the judge prompt), `dev` (judge iteration) or `test` (scored once) |

Keep labeller identity to a role or a pseudonymous ID where the project's
data rules require it; the decision-maker's name lives in the plan. Never
put customer text in `critique` beyond what the trace store already holds
under the same access rules.

CSV, with a header row:

```csv
case_id,criterion,rater,label,labeller,critique,criteria_version,labelled_at,split
claim-0142,cites_policy,underwriter_a,fail,underwriter_a,Quotes the 2024 flood exclusion that was replaced,v02,2026-10-21,
claim-0142,cites_policy,underwriter_b,fail,underwriter_b,Cites a superseded exclusion,v02,2026-10-21,
claim-0142,cites_policy,adjudicated,fail,senior underwriter,Superseded clause cited; both experts agree,v02,2026-10-22,test
claim-0142,cites_policy,judge-cites-policy-v3,pass,,,v02,2026-10-24,
```

JSON Lines, one object per line, the same fields:

```json
{"case_id": "claim-0143", "criterion": "asks_missing_info", "rater": "adjudicated", "label": "pass", "labeller": "senior underwriter", "critique": "Asks for the loss date before deciding", "criteria_version": "v02", "labelled_at": "2026-10-22", "split": "dev"}
```

The judge's own rows need no split: the checker takes the split from the
matching `adjudicated` row.
