# Evaluation summary: claims triage agent

## 2026-10-27: first labelling batch and the Gemini judge

**Verdict: the judge cannot be trusted yet, and nothing here can show that it can.** There are no
adjudicated labels, no split, 24 cases, and the two experts barely agree with each other. Judge
TPR/TNR is **NOT REPORTED** for every criterion (needs at least 30 reference fails and 30 reference
passes per criterion; we have 5-7 fails).

Evidence tier: `offline`, computed **by hand** from `labels/experts.csv` and `labels/judge.jsonl`.
`label_agreement.py` was not run: this session had no shell. Re-run it to confirm (commands below).

### Expert agreement (24 cases, 2 raters, uw-mensah vs uw-castillo)

| Criterion | Agree | Cohen's kappa | Fail share (mensah / castillo) |
| --- | --- | --- | --- |
| fraud_flags_correct | 13/24 (54%) | ~0.10 | 58% / 46% |
| fast_track_correct | 18/24 (75%) | ~0.44 | 38% / 29% |
| note_grounded | 14/24 (58%) | ~0.16 | 46% / 46% |

All below the checker's placeholder 0.6. The criteria are not yet usable by a second person, so a
judge cannot be calibrated against them.

### Criteria drift (confound, not just noise)

- `fraud_flags_correct` v02 (2026-10-16) fails false flags. uw-mensah used v02 from CLM-4113 on;
  uw-castillo labelled the same cases on 2026-10-17 under **v01**. CLM-4101..4112 are v01 for both.
- Kappa by block: CLM-4101-4112 (both v01) ~0.31; CLM-4113-4124 (mensah v02, castillo v01) ~ -0.17.
  In the second block mensah fails 9/12, castillo 6/12; in 5 of the disagreements mensah fails and
  castillo passes. That fits the v02 rule, but it cannot be confirmed from these labels.
- Mensah's CLM-4101..4112 fraud labels are v01 and need re-review under v02 (the definition changed).
- The judge prompt is v01 (`judge-config.md`, criteria as of 2026-10-13) and every judge row is v01,
  though it ran 2026-10-18, after v02. It cannot be right on false flags by construction.
- Every critique reads "see claim fields". No label has a usable reason, so no disagreement pattern
  can be read from the critiques and there are no few-shot examples for a judge.

### Judge vs experts, indicative only (reference = cases both experts labelled alike)

This leaves out the hard cases and mixes v01/v02 for fraud. It decides only whether the judge is
worth calibrating.

| Criterion | Reference fails / passes | Judge caught fails | Judge passed passes |
| --- | --- | --- | --- |
| fraud_flags_correct | 7 / 6 | 5/7 | 4/6 |
| fast_track_correct | 5 / 13 | 5/5 | 13/13 |
| note_grounded | 6 / 8 | 2/6 | 8/8 |

- `note_grounded`: the judge fails 4 of 24 cases against 11 per expert. It passes almost everything and
  misses 4 of 6 failures both experts agreed on (CLM-4106, 4116, 4119, 4122). Do not use it for this
  criterion.
- `fast_track_correct`: looks good, but it rests on 5 failures. It also passed 3 cases mensah failed
  (4106, 4113, 4121) and failed 4116, which castillo passed.
- `fraud_flags_correct`: misses two agreed failures (4105, 4113) and fails two agreed passes (4111, 4112).

### Open questions and the assumptions I proceeded on

1. Who is the quality decision-maker? Unknown; **not named, so I adjudicated nothing** and wrote no
   `adjudicated` rows. Name them in the session plan.
2. Was castillo told about v02? Assumed no (v01 labels on 2026-10-17). Ask.
3. Are the 24 cases a sample of real traffic or synthetic only? README says synthetic. Assumed they do
   not cover the outcome classes, so saturation is not shown.
4. Did the builder pre-annotate? No record. Assumed not.

### Left undone

- Running `label_agreement.py` (no shell), taxonomy and saturation (24 cases against the ~100 needed),
  adjudication, the split, judge calibration, and expert follow-up hours. The follow-up session is in
  `labelling-session-plan.md`.

To reproduce:

```bash
S=.claude/skills/adk-agent-evaluation/scripts/label_agreement.py
python3 -I $S --labels labels/experts.csv
python3 -I $S --labels labels/experts.csv --criteria-version v01
python3 -I $S --labels labels/experts.csv labels/judge.jsonl --judge judge-gemini --reference consensus
```
