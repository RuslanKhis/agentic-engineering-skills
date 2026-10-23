# Inspect AI alignment — 23 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/inspect-ai-comparison-2026-10-22.md).
In the repository (22 October): the NaN-on-short reducers and `at_least`
in result auditing, Krippendorff's α in judge calibration, the proven
`agent_bridge()` interception in provider compatibility. After the trial
(23 October): two mode-table rows (judge agreement; running under an
external harness), a standard-library recipe for α with the rule for an
under-filled label set and the retired-judge verdict, and how to run an
existing agent under the bridge without editing its module. **One scenario
case** (`evaluation-judge-agreement-and-harness-bridge`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. No helper changed.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK or Inspect installed, on a synthetic project, without the expected
answers; interrupted once by a usage limit and resumed.

### Evaluation: two judges that disagree, and the agent under Inspect

The project: an ADK 2.12 agent, two judge prompts on two models, a labels
file holding 3 of the 60 traces the README describes.

What the agent did: a standard-library α implementation for every rater
pair at the three levels with descriptive companions, validated against a
published worked example and 11 tests, reporting the 3-row file as
incomplete rather than as a result; an Inspect task that copies the agent
onto the bridge model, runs it through the real `InMemoryRunner` inside the
bridge with three epochs and the reducers, carrying the streaming and NaN
limits from the skill, with its tests reported as not run and the package
in a separate dependency group; the retired judge model flagged, not
changed.

Ease rating: **3 of 5**. The guidance existed and was accurate; neither
half was reachable from the mode table.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The bridge guidance lived under a heading routed only for provider rejections | A mode-table row for external harnesses |
| "Calibrate a judge" routed through live evaluations to one sentence at the end of a paragraph | A mode-table row for judge agreement pointing at the section |
| No formula or recipe for α; an under-filled set had no rule | A compact standard-library recipe with the validation and incompleteness rules |
| "Pin it" versus "blocker" for a retired judge | One verdict: a blocker for live reruns until pinned; offline figures stand |
| How to put the agent on the bridge model without editing its module | The factory, or a validated-later `model_copy`, stated |
| The engineer's ticket-oriented paragraphs slow a stand-alone request | Left: a Phase D question |

## What this does not establish

The Inspect task did not run; the α figures are on 3 rows; the
`model_copy` route was not validated against the installed SDK.
