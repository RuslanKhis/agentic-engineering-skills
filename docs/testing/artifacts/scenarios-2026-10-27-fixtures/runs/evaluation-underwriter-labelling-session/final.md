**We can't trust the judge yet, and the current labels can't show whether we can.** I couldn't run a session with the underwriters in a non-interactive run, so I analysed the existing labels and prepared the follow-up session instead.

**Checks.** I had no shell, so I worked out every figure by hand from `labels/experts.csv` and `labels/judge.jsonl`. I did not run `label_agreement.py`. Please re-run the three commands in `docs/evaluation/README.md` to confirm the figures.

**Why the labels can't show it**
- **Agreement between the two underwriters is too low.** Cohen's kappa is about 0.10 for `fraud_flags_correct`, 0.44 for `fast_track_correct` and 0.16 for `note_grounded`. Agreement is 54%, 75% and 58%. If the underwriters disagree this much, there is no stable standard to calibrate the judge against.
- **The criteria changed partway through, and the two raters didn't move together.**
  - uw-mensah used v02 for fraud flags from CLM-4113 on. uw-castillo labelled the same cases under v01, a day after v02 existed.
  - Kappa for `fraud_flags_correct` is about 0.31 on CLM-4101–4112 and about −0.17 on CLM-4113–4124, so part of the disagreement is a version mismatch, not real disagreement.
  - The judge's prompt is v01 only, so it can't catch false flags.
- **The labels carry no usable reasons.** Every critique says "see claim fields", so I can't read patterns in the disagreements. There are also no adjudicated labels and no train/dev/test split, so TPR and TNR are NOT REPORTED for all three criteria. There are only 24 cases, with 5–7 reference failures per criterion, against a minimum of 30 failures and 30 passes.

**Indicative judge results.** I scored the judge only on cases where both underwriters agreed, which leaves out the hard cases, so treat these as a rough guide.
- **`note_grounded`:** the judge fails 4 of 24 cases, against 11 for each underwriter. It missed 4 of the 6 failures both underwriters agreed on, so don't use it for this criterion.
- **`fast_track_correct`:** it caught 5 of 5 failures and passed 13 of 13 passes. That rests on only 5 failures.
- **`fraud_flags_correct`:** it caught 5 of 7 failures and passed 4 of 6 passes.

**Files written**
- `docs/evaluation/README.md`: the findings above and how to reproduce them.
- `docs/evaluation/labelling-session-plan.md`: the follow-up session agenda, a draft invitation (not sent), and the list of disagreements to rule on.

**Questions I couldn't ask, and what I assumed**
1. Who is the final decision-maker on borderline cases? I assumed that is unknown, so I adjudicated nothing and wrote no `adjudicated` rows.
2. Was uw-castillo told about v02? I assumed not.
3. Are the 24 synthetic cases representative of real claims? I assumed not, so the failure types are not shown to be exhausted.

**Left undone**
- Running the checker script.
- The session with the underwriters: independent labelling of a fresh set, ruling on the disagreements, and criteria v03.
- Adjudication, the gold set and its split.
- Rewriting and re-running the judge against the current criteria.
- Re-reviewing uw-mensah's v01 fraud labels.