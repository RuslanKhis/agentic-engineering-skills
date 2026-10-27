# Labelling session report: can we trust the judge?

Date: 2026-10-28. Tier: offline. Inputs: `labels/experts.csv`, `labels/judge.jsonl`, `labels/criteria.md`.
Tool: `label_agreement.py` from adk-agent-evaluation (outputs reproduced below).

## Answer

**No, not yet. The judge's TPR and TNR are NOT REPORTED.** There is no adjudicated gold set, no split,
and far fewer than 30 failures and 30 passes per criterion. The experts also do not yet agree with
each other, so there is no standard to measure the judge against.

## Evidence

Expert agreement (24 cases, two raters, kappa threshold 0.60 is the checker's placeholder):

| Criterion | Agreement | Kappa | Cases to adjudicate |
| --- | --- | --- | --- |
| fast_track_correct | 75.0% | 0.44 | 6 |
| fraud_flags_correct | 54.2% | 0.10 | 11 |
| note_grounded | 58.3% | 0.16 | 10 |

All three are below 0.60.

**Criteria drift confounds fraud_flags_correct.** On the 12 cases labelled 2026-10-17 (CLM-4113 to 4124),
uw-mensah used v02 (false flags now fail) while uw-castillo stayed on v01. Agreement on fraud:
8/12 on the v01 half, 5/12 on the v02 half. Those 12 pairs apply different rules, so their disagreement is
not rater noise. The v01 half still has 4 disagreements. fast_track and note_grounded are v01 for both
raters throughout, so their low kappa is genuine ambiguity in the criteria text.

**Critiques are uninformative.** Every fail critique reads "see claim fields", so the disagreements cannot
be read for patterns. The case files hold only claim fields; they do not hold the agent's flags, fast-track
decision or triage note, which the experts were grading. Those outputs are not in the workspace, so I
could not check any verdict against the evidence.

**Judge is stale.** `judge-config.md`: prompt is criteria as of 2026-10-13 (v01), so on fraud it does not
implement v02. The checker says to rewrite the judge prompt before scoring.

**Judge vs experts, raw agreement only (context, not calibration):**

| Criterion | vs uw-mensah | vs uw-castillo | Judge fails |
| --- | --- | --- | --- |
| fast_track_correct | 21/24 | 21/24 | 6 |
| fraud_flags_correct | 13/24 | 16/24 | 9 |
| note_grounded | 13/24 | 17/24 | 4 |

Judge is close to the experts on fast_track, where the experts agree most; it matches them at about chance
level on fraud and note_grounded, where they disagree with each other. On the cases both experts labelled
alike, the counts are 5 fail / 13 pass (fast_track), 7 / 6 (fraud) and 6 / 8 (note_grounded), all NOT REPORTED
(minimum 30 per class), and indicative only because consensus leaves out the hard cases.

## Questions I would have asked, and the assumptions I proceeded on

1. **Who is the quality decision-maker?** Not named in the inputs. Assumption: none yet; I wrote no
   `adjudicated` rows, because I must not rule on underwriting questions myself. **Needs a named person.**
2. **Is v02 the intended fraud rule for everyone?** Assumption: yes (it is the later dated version), so
   uw-castillo's 24 fraud labels and uw-mensah's 12 v01 fraud labels need re-review under v02.
3. **Can I get the agent's outputs per case (flags, decision, note)?** Assumption: not available; the
   agent was not run (no cloud access). Needed so the experts see each trace whole.
4. **Pass bars for the judge (`--min-tpr`, `--min-tnr`)?** Assumption: unset. Suggest favouring TPR on
   fraud_flags_correct, since a missed fraud flag costs more than a false alarm.

## What the next session needs (follow-up agenda, from the session plan)

1. 15 min: show this report; agree where the criteria are ambiguous.
2. Rule on patterns, not single cases. Start with fraud: what counts as "supported by the claim" for a
   flag (v02), and what counts as a "fraud indicator" at all. Then what "matches the guide" means for
   fast-track, and how loose "supported by a claim field" is for notes. Raise the version for each changed ruling.
3. Both underwriters independently relabel a **fresh** overlap under the new version, with a real critique on every fail.
4. The decision-maker adjudicates the remaining disagreements (the 27 listed in the checker output, minus any
   that the new rulings resolve), recording rater `adjudicated`, `labeller`, and the reason.
5. Re-review all v01 fraud labels under v02.
6. Grow the set: about 100 diverse cases with a `split` column (train 10-20%, dev and test about 40-45% each,
   aiming for 30-50 failures and passes per class in dev and test), including cases that pull the rarer class.
7. Update the judge prompt to the final version with train-split critiques, tune on dev, measure once on test.
   One judge per criterion is recommended.

## Left undone

- No adjudication, no gold set, no taxonomy (no traces to code), no criteria v03.
- No judge TPR/TNR; no corrected failure rate.
- Developer's first-30 trace annotation not done.
- No live runs, no cloud or network use.
