# Temporal and DBOS ADK integrations compared with this toolkit — 23 October 2026

## Scope and snapshot

A review of [temporalio/ai-integrations](https://github.com/temporalio/ai-integrations)
`python/google_adk` at commit `bb179c3` (2026-10-21; MIT) and
[dbos-inc/dbos-google-adk](https://github.com/dbos-inc/dbos-google-adk) at
commit `288757e` (2026-05-18; MIT), cloned on 22 October 2026 into their own
directories and read on 23 October, never run; with PyPI metadata for
`temporalio-google-adk` 0.0.1 (2026-10-07, requires `google-adk>=2.8.0,<3`;
the source tree now says `>=2.10.0`) and `dbos-google-adk` 0.1.0 (2026-05-07,
`google-adk>=1.32.0`, `dbos>=2.21.0`), and Google's resume page
(google/adk-docs `docs/runtime/resume.md`, raw, read 2026-10-23). Files read:
the Temporal README, `pyproject.toml`, the test listing with the `Replayer`
calls and the four recorded histories; the DBOS README, `pyproject.toml` and
`tests/test_dbos_plugin.py`.

**Conclusion.** The memo's design fork is right and the sources settle it
with facts rather than opinions: ADK resume is at-least-once and needs a
caller; both engines checkpoint a step's result, so the idempotency key stays
inside the durable step; each engine carries conditions a design must know
(Temporal's MCP toolset needs SDK 1.x, its history records activity
arguments and replays re-record telemetry, HITL re-execution and
continue-as-new; DBOS wants Postgres and a `@DBOS.workflow()`, and declares
an old ADK floor). The workflow skill now states the three-way choice with
the acceptance test; the designer records it as a decision; the safe-API
skill says why the key survives the engine. Both engines' replay tests are
named as the shape of a determinism regression test.

## Method

READMEs, package metadata and tests were read; the ADK resume facts were
taken from Google's page rather than from the vendor posts the memo cites;
each fact is placed with commit, version and date and labelled pre-release
or unverified where the source says so. One scenario case covers the
journey; a fresh-agent trial is recorded in the
[testing record](../testing/durable-execution-alignment-2026-10-23.md).

## Drift corrected

- "Temporal runs each model call and tool as an Activity": model calls yes
  (`invoke_model`); tools as activities through `TemporalMcpToolSet` for
  MCP tools, and the README asks for side effects in HITL re-executed
  bodies to go through activities; plain function tools are not
  automatically activities. The skill says it that way.
- The memo did not note that the Temporal MCP toolset requires MCP SDK 1.x,
  nor the telemetry re-recording on replay; both change a recommendation.
- DBOS's declared ADK floor (1.32.0) predates 2.x; recorded as unverified
  on 2.x.
- The Diagrid post the memo quotes was not used; the at-least-once and
  caller facts come from Google's page.

## Imported, by specialist

- **adk-workflow-design.** The resume-versus-durable-execution section in
  the runtime reference, with both engines' facts and the choice order.
- **adk-system-designer.** The three-way decision and its evidence in the
  design-decisions reference.
- **safe-api-tool-calls.** Why the key survives an engine.

## Routed, not copied

Nothing; engines invoked by their pinned package names.

## Vendored assets

None; the recorded histories are Temporal's test fixtures.

## Left out, with reasons

- Restate and Dapr: named by the memo, not read; no snapshot taken.
- Running either integration: needs a Temporal server or Postgres and the
  SDKs.
- The LangGraph "rules of interrupts" and Pydantic AI's framing: separate
  sources in the memo's list, not reached.

## Limits

Read, not run; Temporal's package is pre-release and its tests were listed,
not executed; the DBOS integration's behaviour on ADK 2.x was not checked.
