I've written the plan to `docs/architecture/planning-decision-assistant.md`. It is a design only. Nothing is built, installed or run, and it hasn't been independently reviewed. I also couldn't run the schedule helper, because Bash is disabled here, so the hours are added by hand.

## What I found in the workspace
- **Pack size:** the local plan pack is about 350 words, so retrieval isn't needed. The whole pack goes in the prompt.
- **Where the judgment is:** it is mostly in exceptions and arithmetic. The dev cases include the H3 daylight exception, the T2 parking reduction near a bus stop, and the TPO root protection area.
- **Conditions:** the "begin within three years" condition is on all three dev approvals and none of the refusals. It is not in the plan text, so I treat it as a learned convention and an assumption.
- **Damaged table:** the SPD Table 2 extract is flagged as damaged. The measure says nothing about how well real PDFs would be read.

## The design
- **Shape:** one `LlmAgent` with a structured output, driven by plain Python code.
- **Validation:** code checks that every cited policy ID exists, caps model calls per case and per session, and writes only to `out/`.
- **Scoring:** it is deterministic. It matches the decision, the set of policy IDs cited and the conditions. Wording of reasons is read by hand. There is no LLM judge.
- **Leave-one-out:** each dev case is scored with the other four as exemplars. Otherwise the score would only measure memory.
- **Five contracts, six decisions.**

## Phase 1 (one developer, hours by hand)
| Goal | Hours |
| --- | --- |
| G1 Scaffold, loader, scorer, caps | 0.5–0.75 |
| G2 Agent v0 plus baseline, with safety-net holdout file | 0.5–0.75 |
| G3 Error analysis, hard 30-minute box, at most two changes | 0.5 |
| G4 Holdout regenerated with the final method and config hash | 0.25 |
| G5 Two-page report | 0.5 |

- **Total:** 2.25–2.75 h.
- **Fit:** at 4 hours with a 25% reserve (3.0 h usable) it fits. At 3 hours only the low end fits.
- **Cut order if short:** probe cases first, then G3 down to one change. G2, G4 and G5 are never cut.

## Judgment calls to check
- **Holdout files:** I opened them to see their shape, recorded no predictions, and the design bars tuning against them. The report must disclose this.
- **Coverage gap:** from the pack alone, the dev cases never exercise the front-slope dormer rule, parking with no bus reduction, the splay rule on a classified road, or the detached 6.0 m limit. Optional probe cases I write myself would be author-labelled. They would count as smoke tests, reported separately and not in the score.
- **Small sample:** with five cases, each is worth 20 points. The report gives a per-case table with 3 repeats.

## Questions I couldn't ask, and what I assumed
1. **Model provider and ID for the $25:** unknown. The model lifecycle table isn't in this workspace, so I chose no ID from memory. This blocks G2 only.
2. **Installing `google-adk` in a local venv at build time:** assumed authorized when the build starts. If not, the build stops after G1.
3. **Required report format:** assumed about two pages.
4. **How reasons are judged:** assumed by the policy cited, not the wording.
5. **Standard conditions on every approval:** assumed expected, because the dev labels show them.
6. **ADK structured output may block tools on the same agent:** to confirm against the pinned version.

## Left undone
- Nothing is implemented.
- The design has had no independent review.
- Phase 2 items are listed but not detailed. They are PDF ingestion and retrieval, an expert-labelled gold set, and an officer review flow.

Next prompt:
```text
/adk-engineer Carry out G1 from docs/architecture/planning-decision-assistant.md.
```