# governance-pack-us-hiring-screener: what the fixture holds

Context unchanged. Standalone record for Redwood Freight Inc. (Oakland, California; warehouses
in California and New York City); consultancy Southgate Labs in Sydney. Topic `screener`.

| Fact | Where |
| --- | --- |
| Scores and ranks applicants; "not recommended" under 40 | design R1, R2, C3 |
| Recruiters usually reject "not recommended" in bulk | plan M4: 6% opened before rejecting |
| Age impact ratio 0.74 in the backtest | plan M2 |
| Sex impact ratio 0.91 | plan M3 |
| Sydney engineers read the evaluation set of real past applications | design D4, D5 |
| Hosting us-west1 | design D1 |
| New York use not decided; NY recruiters asked for it | brief §6 |

Not in the record: who approves go/no-go for the assessment (A4 expects a gap), any bias audit
(NYC Local Law 144 needs an independent one), any applicant notice. Expected jurisdictions
[au, us]; EU and UK out with reasons. counsel_required: yes on every draft. A6 needs a shell;
credit naming `check_governance.py` and saying it was not run.

Changed on 28 October 2026 (Phase 12): the check_governance.py assertion now carries the "reported as not run" escape in its own text, because Phase 11 judges failed it on the literal "runs" even where this note allowed naming the command.
