# Expert labelling and the monthly value report — 25 October 2026

## Scope

Two gaps in the delivery chain. `adk-agent-evaluation` assumed labels
already existed (its quality-iteration loop starts from a 5 to 20 case
development set; its judge calibration from human labels), and the
designer's delivery profiles budget 4 to 8 hours of labelling with no
method. `adk-presenter`'s final-results stage needs post-launch numbers,
but nothing produced them on a cadence. This note records the primary
sources read for an expert-review reference with an agreement checker, and
a `value-report` stage with a record checker.

## Sources read (25 October 2026)

| Source | Type | What was taken | What was not |
| --- | --- | --- | --- |
| Hamel Husain and Shreya Shankar, [AI Evals: Everything You Need to Know](https://hamel.dev/blog/posts/evals-faq/) (published 18 September 2026, last modified 21 September 2026) | Practitioner FAQ | Review at least 100 traces and continue until new traces stop revealing failure modes or changing existing ones ("theoretical saturation"); annotate at least the first 30 yourself; open coding then axial coding into a failure taxonomy ("the most important step"); binary pass/fail; a single domain expert as "benevolent dictator" for most small and medium teams; label independently before discussing, then a domain expert decides and records the reason; Cohen's kappa for agreement beyond chance; TPR and TNR with "positive" meaning an error is present; splits of 10 to 20 percent train, 40 to 45 percent dev, 40 to 45 percent test used once; 100 to 200 labelled examples per failure mode, 30 to 50 passes and 30 to 50 fails in each of dev and test; one judge per failure type; correct a judge's estimates once its TPR and TNR are known; criteria drift | No kappa threshold; no correction formula (the formula in the reference is algebra from the TPR and TNR definitions); no fixed saturation block size (the reference's block of 20 is labelled as the project's choice) |
| Shreya Shankar, J.D. Zamfirescu-Pereira, Björn Hartmann, Aditya G. Parameswaran, Ian Arawjo, [Who Validates the Validators?](https://arxiv.org/abs/2404.12272) (arXiv 2404.12272v1, 18 April 2024; HTML version lists UIST, 13 to 16 October 2024, Pittsburgh) | Peer-reviewed HCI paper, qualitative study of nine practitioners | "users need criteria to grade outputs, but grading outputs helps users define criteria"; participants refined and reinterpreted criteria and went back to change earlier grades; criteria depend on the outputs observed; re-grading after criteria updates may improve consistency | The paper does not prescribe criteria versioning; the reference's versioning and re-review rule is this toolkit's operational form of its observation |
| Eugene Yan, [Product evals in three simple steps](https://eugeneyan.com/writing/product-evals/) (November 2025) | Practitioner essay | Binary pass/fail or win/lose labels; at least 50 to 100 failures in 200 or more samples, balanced; organic over synthetic failures; one evaluator per dimension; human inter-rater kappa observed as low as 0.2 to 0.3; his scale of 0.4 to 0.6 substantial and above 0.7 excellent; 75/25 alignment/test split | His kappa bands are his, not a standard; not adopted as thresholds. Not used: criteria drift or domain-expert roles (the essay does not cover them) |
| Hussain Chinoy and Amy Liu, Google Cloud, [Measuring gen AI success: a deep dive into the KPIs you need](https://cloud.google.com/transform/gen-ai-kpis-measuring-ai-success-deep-dive) (26 November 2024) | Vendor guidance | Adoption rate as the percentage of active users, with "consistently low" read as awareness and "high adoption dropping to low" as performance; frequency of use; business-value KPI families | No baselines, measurement windows, reporting cadence or cost-per-outcome definition; its only statistic (a survey of 2,500 leaders) has no findings quoted and is not used |
| Benazir Fateh and Amy Liu, Google Cloud, [The KPIs that actually matter for production AI agents](https://cloud.google.com/transform/the-kpis-that-actually-matter-for-production-ai-agents) (27 February 2026; linked from the first article's editor's note) | Vendor guidance | "Cost per successful task is the metric that matters most"; per-token cost misleading without success rates; human take-over ("output friction") and revert signals; reliability, then adoption, then business value | Its figures ($0.10 a run, 50 percent failure, 80 percent retention) are illustrative and not reused; no stop or scale rule, no cadence |

Secondary statistics on AI project failure (Gartner, McKinsey, BCG) were
not needed and are not cited.

## Decisions

- **Two statistics, two jobs.** Cohen's kappa for two human raters on a
  binary criterion (the FAQ's recommendation); Krippendorff's α, already in
  evaluation design, for more raters or ordinal scales; TPR and TNR on a
  held-out split for a judge against adjudicated labels, because raw
  agreement rewards a judge that passes everything when failures are rare.
- **Thresholds are placeholders.** `label_agreement.py` defaults to kappa
  0.6, TPR and TNR 0.8 and 30 cases per class (the last from the FAQ's 30 to
  50). None of the sources gives a kappa or rate threshold as a standard;
  the reference tells the plan to set them.
- **Criteria drift is checkable.** Each label carries `criteria_version`;
  the checker reports a rater whose labels span versions, turning Shankar
  et al.'s observation into a re-review list.
- **Value report is one page, monthly, not a deck.** Neither Google piece
  prescribes a cadence or a stop rule; the monthly cadence, the seven
  sections and the default call table are this toolkit's choices, labelled
  as such in the reference.
- **The checker reads the plan's records, not the report's prose.** M and I
  records gained a one-line, semicolon-separated shape (added to the plan
  template); the checker reuses `check_deck.py`'s numeric-claim pattern and
  front-matter parser and its exit codes.

## Register

`docs/research/source-register.json` tracks GitHub repositories only
(`owner/name`, pinned commit, licence). None of the sources above is a
repository, so no rows were added; their read dates are recorded here and
in the references' source lines.
