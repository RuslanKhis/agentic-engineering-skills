# adk-recipes alignment — 22 October 2026

*What changed, what was checked, and what three fresh agents did with it.*

## Change

See the [comparison note](../research/adk-recipes-comparison-2026-10-22.md).
In the repository:

- **Facts** from google/adk-recipes at commit `be63596` (2026-10-20) went
  into eleven specialists at the decision each serves, every one cited to
  the recipe file and labelled a vendor sample under the repository's "not
  production use" disclaimer: the write-back memory loop and the managed
  RAG recipes (memory), the deterministic-first graph and the callback-chain
  contract (workflow), the repeated-failure signature and headless
  ask-as-deny rules (guardrails), Horizon's guard shape and rubric evalsets
  (security), the evalsets as case templates and the retail plugin's
  rubric-plus-assertion file (evaluation), the Ambient Quality Agent as a
  scheduled production evaluator (release engineering, observability), the
  staged widget emission pattern with its two ADK facts confirmed in the ADK
  source (frontend), the pre-compaction flush (optimise) and Horizon's A2A
  pins (interoperability).
- **Routing.** The `agents-cli-aqua` skill that the AQuA extension installs
  is named in the standard form in adk-release-engineering, mapped in the
  engineer's composition reference and the designer's handoff table, and
  written in a goal as `google/adk-recipes:agents-cli-aqua`.
- **Rules that stay ours** are recorded beside the imported facts: a stop
  uses no extra model call, judge metrics use majority voting, a trajectory
  expectation is graded or removed, a scheduled evaluator's missing run is
  NOT RUN.
- **Three scenario cases** (`release-post-launch-quality-loop-aqua`,
  `memory-write-back-loop-from-horizon`,
  `frontend-tool-widgets-staged-emission`) and one activation case for the
  frontend skill's widened description.

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. The full `scripts/check_repo.py` run
and its counts are recorded in the [testing log](index.md) entry for this date. No helper
script, test or `last-tested` date changed.

## Fresh-agent trials

Each ran in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network and
no ADK SDK, on a synthetic project built for the trial, without the expected
answers. Two of the three were interrupted by a usage limit and resumed from
their saved state; the resumed runs completed and reported normally.

### Release engineering: a post-launch quality loop ticket

Fixture: an Agents CLI project on `google-adk>=2.12.0` writing BigQuery
Agent Analytics rows, a production design with contracts for the CI gate
and weekly production quality, a release manifest, and ticket G07 with
`google/adk-recipes:agents-cli-aqua` among its supporting skills.

Observed: the agent led with adk-release-engineering in production-feedback
mode, recorded the uninstalled AQuA skill as an execution-scope
prerequisite with the pinned extension reference and the recipe disclaimer,
and did not rebuild the evaluator. It wrote the release record with the
rules the reference now states (NEW or RECURRING on the critical slice
blocks, everything else opens a case; a week with no completed investigation
is NOT RUN and blocks as missing evidence; RESOLVED only when a case naming
the insight passes on the candidate), converted the found defect into a
redacted regression case with the observability converter and a project
redaction hook, kept the deterministic C2 check beside the judge metric,
filled the Evidence section with the commands, exit codes, resources,
deferred controls and the two to three hours of human review owed, and left
every live step as not run. Offline: 20 tests passed, 2 SDK or live tests
skipped as NOT RUN. Ease: **4 of 5**; the point lost was that nothing said
how to represent an investigation or an insight locally when the evaluator
is not installed.

Fixed the same day: the production-feedback reference now gives the local
insight row to keep until the installed CLI's JSON fields are known, and
names what the extension deploys for the Resources created line with the
ledger rows that price it; the release skill says its inventory helper reads
ADK's own eval assets and an Agents CLI project's `eval_config.yaml` and
datasets are listed by hand; the observability converter's `--select all`
naming and where the old release's observed output lives are stated; the
evaluation-design ownership example carries `freshness_expires` and
`drift_mode`, which the release reference already required; and
adk-engineer now states the ticket status vocabulary at the finishing step
and what to do when no interpreter meets the project's `requires-python`.

### Frontend: a widget pipeline with three bugs

Fixture: a shopping agent whose three tools each called `render_ui_widget`
inline, two of them with the same widget id, and an after-agent refresh
callback that rendered without writing state; BUGS.md described duplicate
cards, a refresh that never reached the browser and a "show again" that
re-ran the search.

Observed: the agent routed to adk-frontend-integration (confirmed by
grepping for the function name, because no routing row named widgets),
read the new "Widgets emitted by tools" section, moved every render into one
emitting callback with a declared order, per-widget state keys for
parallel-merge safety, a byte-identical suppression and an emitted flag
written as the state delta, answered "show again" from the stored picks,
kept the tools' names and result shapes, added a test that fails on any
second render call site, and wrote a Runner regression for all three bugs
reported as not run without the SDK. Offline: 25 tests passed on the only
interpreter with pytest (3.9, below the project's pin, which it recorded).
Ease: **4 of 5**; the paragraph named both ADK facts and the remedy, and
everything else cost routing time.

Fixed the same day: the adk-engineer routing table and the frontend skill's
description and mode table now name interface widgets that tools render;
the frontend skill says the widget section applies to a bug fix; the
workflow callbacks reference states that every callback in a stage shares
one `CallbackContext` and one state delta (confirmed in `base_agent.py`);
the workflow runtime reference states how parallel function responses are
merged (deep merge, later value wins, widgets concatenated unchecked) and
that a `temp:` delta is readable later in the same invocation and never
persisted (confirmed in `base_session_service.py` and `_batch_executor.py`
on main, labelled for confirmation on the pinned version), with a pointer
from the memory skill's state-prefix sentence.

### Memory: the write-back side of cross-session memory

Fixture: a `google-adk==2.8.0` field-engineer agent with `PreloadMemoryTool`,
Memory Bank in deploy and `InMemoryMemoryService` in tests, a
`DatabaseSessionService`, two tools, and a request to design and implement
what is saved, when, under whose consent, how it is corrected and forgotten,
and what happens when the memory service is down, with one engineer's
preference never surfacing for another.

Observed: the agent led with adk-memory-architecture in Memory Bank mode and
built the write-back side as the reference's contracts require: a topic
allowlist with sizes and lifetimes, consent carried as `RunConfig.custom_metadata`
and rechecked at the write boundary (consent false means zero provider
calls), candidates staged per function call in `temp:` state and written by
one after-agent callback as event deltas with policy metadata, a SQLite
ledger with accepted, failed and indeterminate outcomes reconciled by search
before any resubmission, a recall filter for foreign scope, topic, tombstone
and expiry, forget as tombstone-then-delete, erasure that blocks writes,
settles the ledger, deletes by scope and verifies zero with a control user,
and a recall outage that fails open with a log. It kept the shared-site
guarantee by scoping memory to the verified engineer and routing shared
facts to the visit record, named the Horizon loop as the pattern and listed
what it lacks, and left the pin at 2.8.0. Offline: 61 tests passed, the one
SDK Runner test reported as not run. Ease: **3 of 5**; the reference stated
the right contracts but read as an audit of someone else's code, so the
mechanism had to be inferred from its warnings, and the context accessor
names and the absence of a delete surface on the memory service had to be
guessed without the SDK.

Fixed the same day: the memory-bank reference now carries a six-step minimal
write-back sequence on 2.8.0 with the accessor names and memory methods read
in `agents/context.py` and `memory/base_memory_service.py` (no delete method
on the service; tombstone first, then the provider's API), and the
shared-subject rule (scope stays app and user, the subject is a tag and a
recall filter, shared facts belong to the owning record); the
integration-recipes reference says that on 2.8.0 `ToolContext` and
`CallbackContext` are one `Context` class with the same accessors and guards
the `thought` attribute; the memory skill's inspect step carries the
interpreter rule; and the failure-recovery reference says at the top that
write outcomes live in the memory-bank reference. Not changed: the
`VertexAiMemoryBankService` delete and scope-filter call shapes, which the
agent could not verify offline and this review did not read either.

## Limits

Three trials on three synthetic projects, one host client, no recipe
executed and no SDK installed, so every Runner test the trials wrote is
reported as not run. Google's AQuA skill was not available, so the path
where its commands are proposed was not exercised. The two resumed trials
lost no files, but their first halves ran before the usage limit and their
reports after it; the ratings are the agents' own.
