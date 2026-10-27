**The rejection of PA-2026-0177 comes from the checker, not the reviewer model or the writer.** I traced `pipeline/coverage_check.py` by hand, because shell access was unavailable and I couldn't run it.

In `pipeline/stages.py:40-42` any checker finding forces `verdict = "reject"`, whatever the model says. The checker produced two findings on this draft, and both are wrong:

1. **"Gaps listed although every source is accounted for."** This treats "every document cited" as "nothing unresolved". The gap is real: the tree survey says the stem diameter was not measured and the root protection area was not calculated (TS lines 3–4).
2. **"LP-ENV3 is cited but not applicable."** The checker only looks for "root protection area" in the application form, design statement and agent letter. This tree survey is a protected oak 3.5 m from the new wall, so the tree policy clearly applies. The accepted case (PA-2026-0152) passed only because its application form happens to contain that phrase.

The review model's "revise to approve" just repeats the checker. Its prompt has the checker's findings appended, so its own accuracy can't be read from this run.

A paid retry would be wasted. Any honest draft of this case that keeps the gap or cites ENV3 gets the same forced reject. The only draft that would pass is one that hides the unresolved tree issue.

**Writer concerns I did not adjudicate:**
- **R1 may be unsupported.** The planning policy needs the extension to be "subordinate in scale and height", and no cited document gives dimensions. The reviewer marked it supported. The accepted case has the same weakness.
- **Refusing on R2 is a judgement call.** ENV3 speaks of an absent tree survey, and here the survey exists but is incomplete. The schema also has no "request more information" option. This needs a planning officer or tree specialist.

**Done:**
- Read the runs, case sources, plan and checker.
- Wrote `analysis/findings.md` with the evidence table, the assumptions I proceeded on and recommended next steps.
- Wrote `analysis/replay_checks.py`, a read-only script that replays the checker on both drafts.
- Made no provider calls and changed nothing under `runs/`, the checker, the tests or the ledger.

**Not done:**
- **Not run:** `analysis/replay_checks.py` and the unit tests, so the traces are hand-derived. Please run `python -I analysis/replay_checks.py` to confirm them.
- **Not changed:** the checker fix and regression tests, since you wanted the diagnosis first.
- **Not measured:** the accuracy of the reviewer or the writer. Two cases show the checker's logic faults and say nothing about rates.

**Questions I couldn't ask:**
- **Tree survey:** I assumed it counts as an applicant document. The conclusion doesn't depend on this, because the protected-tree order triggers ENV3 either way.
- **Refusal:** I assumed whether "refuse" is the right call is for the planning officer.
- **Checker edits:** I assumed you don't want them yet.