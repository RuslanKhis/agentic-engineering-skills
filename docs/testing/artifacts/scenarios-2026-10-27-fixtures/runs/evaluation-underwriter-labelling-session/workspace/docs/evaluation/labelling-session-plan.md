# Follow-up labelling session: claims triage agent

Labels already exist, so this is the follow-up agenda from the skill's session plan. Nothing below has
been run with the underwriters; all dates and names are placeholders to fill.

## Invitation (draft, not sent)

> **Subject:** 3 hours to settle what a good claims triage looks like
>
> Last week you and a colleague labelled 24 claims. You disagreed on about half of the fraud-flag and
> note verdicts, and the criteria changed part-way through, so we cannot yet tell whether our automated
> judge is reliable. We need ~3 hours to rule on the disagreements and relabel a fresh set.
> **When:** <date/time>. **What you do:** read each claim in full, mark pass/fail per criterion and write
> one real sentence for every fail. **Data:** synthetic. **Who decides:** <decision-maker>.

## Roles

| Role | Person |
| --- | --- |
| Quality decision-maker (final say) | **<to be named; unresolved>** |
| Second expert (agreement) | uw-mensah / uw-castillo, one of them |
| Facilitator | <developer> |

## Before the session

- [ ] Developer reads all 24 cases alone and notes unreadable or broken claims.
- [ ] Tell both underwriters that `fraud_flags_correct` is **v02** (false flags fail). Relabel under v02.
- [ ] Sample ~100 diverse claims (current 24 are synthetic and few); include hard cases the underwriters name.
- [ ] Choose a fresh overlap (>= 40 cases, expected to include both classes) that neither has seen.

## Agenda

1. Agreement report (15 min): kappa 0.10 / 0.44 / 0.16 for fraud / fast-track / note.
2. Patterned disagreements (40-60 min), one ruling per pattern. Worklist:
   - fraud_flags_correct (11): 4103, 4104, 4107, 4108, 4115, 4117, 4118, 4120, 4121, 4123, 4124.
     First question: do mensah's fails on 4118 and 4120-4124 (castillo pass) come from false flags?
   - fast_track_correct (6): 4106, 4109, 4113, 4116, 4119, 4121.
   - note_grounded (10): 4101, 4103, 4104, 4105, 4108, 4110, 4111, 4113, 4123, 4124. Question: does
     "every statement supported by a claim field" count inference or paraphrase? Both fail rates are
     46% but they fail different cases, so the boundary is unclear.
3. Rule borderline cases, raise the criteria version (probably v03 for note_grounded, a clarified
   fast_track), with a borderline ruling written for each.
4. Independent labelling of the fresh overlap under the new versions (45-60 min), no discussion. Every fail
   gets a specific critique (no "see claim fields").
5. Adjudicate remaining disagreements as rater `adjudicated`, `labeller` = decision-maker, reason in
   critique. Re-review mensah's CLM-4101-4112 fraud labels (v01) under v02.
6. Open coding on new claims to check the taxonomy; record the claim number where each category appeared.

## After the session

- [ ] Gold set in the gold-set schema with `criteria_version`, `labelled_at`, `labeller` and a **split**
      (train 10-20%, dev 40-45%, test 40-45%).
- [ ] Re-run `label_agreement.py`; rerun the judge with a prompt for the current criteria versions and
      one judge per criterion.
- [ ] Judge TPR/TNR on the test split with both class counts, or NOT REPORTED (needs >= 30 fails and
      >= 30 passes in test; at present this implies a few hundred labelled cases per criterion).
- [ ] Record hours per expert against the estimate.
