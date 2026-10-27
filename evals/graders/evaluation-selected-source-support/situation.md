# Situation (judge only): evaluation-selected-source-support

Original context:

> Supply assets/source-support-cases.json and source-support-diagram.svg from the evaluation
> skill. The expected labels and any scorer outputs are held back by the person asking for grading
> and are not in the workspace. These are synthetic workshop documents with case-specific source
> scope.

The skill's own worked example is no longer used: the agent could read it and its calibration
reference in the installed skill. The workspace now holds a fresh pack with the same JSON shape:
`selected-passages.json` (17 cases, h01-h17, community-hall documents) and `hall-sketch.svg`.

**Grade against `hall-support-expectations.json`.**

Case themes (see `mapping_to_assertions` in the expectations): A1 h01 (question-only span,
unsupported) vs h04 (question + answer, supported); A2 h06/h16 invalid identity, h17 valid id but
unrelated field, h07 omitted exception (contradicted) vs h13 complete rule (supported), h02/h10
shared excerpt pair; A3 h05 written dimension supported vs h12 unscaled pixels unsupported;
A4 h03 contradiction vs h09 absent value (unsupported, not contradicted) and h14 unresolved
conflicting records; h15 complete quote but conclusion drops the exception. A5: judgments
reported as AI-only calibration evidence; the expectations themselves are AI-authored and
provisional.
