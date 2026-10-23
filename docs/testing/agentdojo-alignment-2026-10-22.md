# AgentDojo alignment — 22 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/agentdojo-comparison-2026-10-22.md).
In the repository: four attributed synthetic cases and four fixtures in the
security skill's adversarial asset porting the benchmark's goal classes and
its important-instructions envelope; the table row, attribution, end-state
note and the version-conditional live adapter route in the adversarial
testing reference; sources. After the trial (23 October): the confirmation
protocol's wire shape in the evaluation skill's signature list; two harness
readings settled in the reference (a never-confirmed hold satisfies "never
executed"; the allow-list outranks taint for destinations and payees while
taint governs free-text arguments); the asset's key names declared
conventions; the mode row naming which sections of the other references a
suite author needs; the inspector's literal-name limit recorded; a note on
loose annotations for SDK-free policy modules; and the engineer rule that
moving tools out of the agent module is in scope for a testing or security
request. **One scenario case** (`security-adversarial-suite-ported-goal-classes`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean; the asset is data and the full
`check_repo.py` run passed. The inspector's factory-name limit is recorded
as an owed helper change.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK installed, on a synthetic project, without the expected answers.

### Security: extending an injection suite with the benchmarks' attack classes

The project: an ADK 2.12 workspace assistant with mail, drive and payment
tools, no gates, a one-case suite and no harness.

What the agent did: twelve cases (nine attacks, three positive controls)
seeded from the asset and the four ported classes, every fixture synthetic;
a strict scripted-model harness with backend fakes and socket denial; a
capability gate and a taint labeller; `require_confirmation` on the
destructive and payment tools with body re-checks; tools moved to an
SDK-free module; 38 offline tests run on the pin-meeting interpreter and 6
Runner tests reported as not run; the inspector run before and after
(`write_tool_without_gate` 3 to 0); a notes file with the tier table, the
residual trifecta and what a live run adds.

Ease rating: **4 of 5**. Routing and the seed asset fitted the request; the
points lost went to the confirmation protocol's missing wire shape and the
volume of unrelated reference text.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The confirmation resume shape was given nowhere | Stated from the 2.12.0 flow in the evaluation skill's signature list, with end-at-hold marked to confirm on first run |
| Whether the seed's key names are a schema | Declared conventions in the asset and the reference |
| The gate's taint rule conflicted with case a11's allowed payee | The allow-list-outranks-taint reading stated |
| "Never executed" did not admit a never-confirmed hold | Vocabulary and reference admit it |
| 31 KB of references for a 15 percent relevant slice | The mode row names the sections |
| The inspector showed `<unnamed agent>` for a factory-built agent | Recorded in validation with the helper change owed |
| Moving tools out of the agent module looked out of scope; the gate sample imports the SDK for type hints | Both rules stated |
| The engineer's ticket paragraphs for a bare request | Left: a Phase D placement question, now recorded |

## What this does not establish

The Runner tests did not run; the protocol assumptions they encode are
marked for the first SDK run; the trifecta remains and is a follow-up.
