# Why AI projects stall, and what the brief does about each cause

Read before filling the stall-checks table in the brief. Surveys of
executives, interviews with the engineers who build these systems, a
tribunal ruling and a CEO reversing his own rollout point the same way: AI
projects stall on the organisation around the model, not the model. The
evidence is mostly correlational and self-reported (sources, figures and
caveats in the repository's research note
`docs/research/why-ai-projects-fail.md`), but the remedies converge across
independent methods, so each one is a field or a rule in the brief, not a
scoring weight.

The magnitudes to calibrate against: among organisations reporting savings
from AI, most report under 10 percent; among those reporting revenue gains,
the commonest level is under 5 percent; measured productivity gains in
controlled studies sit around 15 percent in support work and 25 percent in
software work. A first use case promising more needs a stated reason.

| Cause | What it looks like | What the brief contains |
| --- | --- | --- |
| Problem misframed or miscommunicated (the engineers' most common cause) | The sponsor and the builder describe different problems | The problem in the sponsor's words and in the builder's words, the difference noted, and a frontline user who agrees |
| No baseline or outcome measure | "Improve efficiency"; usage counts as success | Goal metric, current value with source and window, target with units, a threshold sentence; no candidate is ranked above an idea without one |
| AI layered on an unchanged workflow | An assistant beside the old process; desk-level time saved that never reaches a P&L line | The workflow before and after, naming the steps removed, not only assisted; an overlay is scored down; "time saved" is a goal only when the brief says how it converts to a P&L line |
| No senior owner | A lab project with no budget line | A named owner with budget authority and a yes or no to funding one team on this problem for a year |
| No defined human-validation point | "Someone checks it"; a chatbot stating policy nobody verified (a tribunal held the airline liable for its chatbot's answer) | Per action: who validates, when, what share; policy, price and eligibility statements are grounded in a source or routed to a person |
| Data poor or inaccessible | Nobody knows who owns the records; friction is not logged | A data register: source, owner, access path, freshness, logged today or not |
| Cost not modelled per unit | A pilot bill nobody converted to a month; a cost-first rollout reversed when quality fell | Expected volume, a cost ceiling, who pays after the pilot; every cost goal paired with a quality guardrail that can stop the rollout |
| Risk controls absent | Inaccuracy seen but not mitigated; an agent that can act with no permission scope | The top three harms, a guardrail threshold for each, and the agent's permission scope; irreversible actions behind approval |
| Change management and training ignored | Staff hear about the tool at launch; employees already use AI unofficially three times more than leaders think | Who changes what they do, what training, when; the champion found among the unofficial users |
| No feedback loop for corrections | "It doesn't learn from our feedback"; the same context typed in every time | Where a correction is captured, who reviews it, and which artefact changes (prompt, rule, evaluation case, retrieval source) |
| Pilot never embedded in the real workflow | A demo on sample data that never meets live volume | The pilot runs on live volume in the system of record from week one, even for one queue or region, and names the governance sign-off that "scaled" needs |
| Build or buy chosen on pride | A vendor "agent" that neither plans nor acts; an internal build with no process knowledge | Whether a partner already understands the process and learns from feedback; whether the offered agent actually plans and acts |
| Model or vendor churn breaks the target | A prompt that encodes business rules; acceptance defined on a model's behaviour | Deterministic steps are rules, not prompts; acceptance is defined on outcomes so a model swap is re-run against it |

A candidate with no named owner, no data access and no path into the real
workflow is tinkering; the brief does not call it a first use case. Prefer
narrow, back-office or edge-of-workflow work with a low configuration
burden; call summarisation and routing, document automation and repetitive
code succeeded in the field more often than opaque decision support over
proprietary heuristics. Interview frontline staff about their unofficial AI
use; it locates the real friction and the people who will carry the change.
