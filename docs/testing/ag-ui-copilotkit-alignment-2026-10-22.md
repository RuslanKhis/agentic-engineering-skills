# AG-UI 1.0, ag-ui-adk and the CopilotKit example alignment — 22 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/ag-ui-copilotkit-comparison-2026-10-22.md).
In the repository: the approval-contract section in the frontend skill's
AG-UI reference (both contracts, the enforcement codes, `from_app()` with
resumability, `protocolVersion`, the 0.11.0 state-key rule, `verifyEvents`
against the bundled checker's scope), a line in production, the example's
pins in compatibility, the recipe's header, provenance; one sentence in the
guardrails skill's human-review reference. After the trial (23 October): the
wire shapes the tests need (the `code` field on `RUN_ERROR`, the resume entry,
the accepted tool-message answers, the `from_app` signature and imports, the
constructor default), a probe for which contract a backend emits, the
inspector's `unverified` status on the 1.0 line, the interpreter note on the
frontend skill's helper, and the engineer's import rule extended to the tool
module. No helper changed. **One scenario case**
(`frontend-agui-approval-contract-declared`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. The full `scripts/check_repo.py`
counts are in the README entry for this date.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK or middleware installed, on a synthetic project, without the expected
answers.

### Frontend: a refund approval refused after a client upgrade

The project: an ADK 2.12 refund agent behind ag-ui-adk 0.11.0 with
`require_confirmation` on the refund tool, a CopilotKit app moved to
`@ag-ui/client` 1.0.2 that answers approvals with `useHumanInTheLoop`, and
the symptom that the next turn is refused until the approval is answered
another way.

What the agent did: named the two contracts and the mismatch, chose the
tool-message contract as the smaller change that keeps every pin, declared
it in code on both sides so they cannot drift, moved the backend to
`ADKAgent.from_app` with resumability, moved the tool out of the
SDK-importing module with amount validation, registered the dialog against
the confirmation call, wrote the two prescribed flag-on and flag-off tests
plus a rejection test (SDK-bound, reported as not run), offline tests on both
interpreters and a Node test for the shared declaration, and a notes file
with the fallback to the interrupt contract.

Ease rating: **4 of 5** for finding, **3 of 5** for applying. The section
answered the question; the wire shapes to write the tests were missing.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| No shape for the resume entry, the `useInterrupt` answer or the tool-message content; the error code's field unknown | The AG-UI reference now gives the `RUN_ERROR` `code` field, the resume entry, the accepted tool-message forms and the constructor default, read in the middleware source and the 1.0 pattern page |
| `from_app` signature and `ResumabilityConfig` import path unknown | Both stated from the middleware source and README |
| No probe for which contract a running backend emits; the bundled checker cannot help | The reference names the `RUN_FINISHED` `outcome` probe and says what the checker does not cover |
| Inspector reports every pin on the 1.0 line as unverified | Compatibility says it is a baseline statement, not a finding, and when to skip the tested-stack gate |
| The frontend skill's helper needs Python 3.11 without saying so | One parenthesis pointing at the engineer's interpreter rule |
| The real SDK-import blocker was the tool module, not `__init__.py` | The engineer rule now names the tool module |
| The recipe targets CopilotKit 1.69.0 `/v2`; `useHumanInTheLoop` on 1.79.0 is unaddressed | Left: the recipe records what it exercised; the trial's choice is recorded in the testing record |

## What this does not establish

The three SDK tests and the browser path did not run; the middleware's
default for the flag was read on main after 0.11.0, not on the tag.
