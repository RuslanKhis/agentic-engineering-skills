# deepeval, MLflow and Opik alignment — 25 October 2026

Source note: [comparison](../research/deepeval-mlflow-opik-comparison-2026-10-25.md).

## Changed journey

`adk-agent-evaluation`, grading with a third-party scorer and store, with
`adk-agent-observability`'s export paths.

## Fresh-agent trial

A fresh agent with only the skill packages reviewed a nightly MLflow job
(`ToolTrajectory(match_type="EXACT")` over traces, `Hallucination` on
relayed answers, content capture off) whose staging rows were all "no",
with a third empty. It installed google-adk 2.12.0, mlflow 3.17.2, deepeval
4.3.1 and pytest, sent spans over OTLP to a local MLflow server on SQLite,
and ran everything with outbound network denied and every refused
connection logged.

Verdict on staging: every trajectory "no" was a measurement artefact (tool
names read from span names, arguments `"{}"`); the empty rows were NOT RUN
(a merged span for parallel calls raised a validation error);
`Hallucination`'s "no" on relayed answers was an artefact (the judge was
told the agent has no tools). Real failures appeared only in the corrected
job, which joins each trace to its ADK session and calls ADK's evaluators
directly: a wrong argument, an extra call, and invented facts with no
tools; the do-nothing control failed. With MLflow's three switches set,
client and server made no connection attempts.

`pytest`: **8 passed**, with no egress attempts. Ease: 3 of 5.

## Frictions and fixes (same day)

1. No routing row for a third-party scorer. Fixed.
2. "An exception comes back as an error row" was wrong for a judge failure
   inside ADK's evaluator, which arrives as "no". Fixed.
3. "Passes tool names but no tool results" was wrong: neither reaches the
   judge. Fixed.
4. "Supply `actual_tool_calls` or every argument check fails" understated
   it: names fail too. Fixed.
5. mlflow 3.17.2's `ToolTrajectory` needs an explicit threshold with ADK
   2.12.0. Fixed.
6. The merged span for parallel calls. Fixed (checked in 2.12.0 source).
7. The LiteLLM cost-map fetch and MLflow's pytest telemetry gate. Fixed
   (the gate checked in source).
8. No current judge model id. Not changed: the skill does not fill a model
   id from memory; pinning is the project's step.
9. deepeval's default OpenAI client and the hook's extra package. Fixed.
10. Opik is read, not run. Not changed: stated as such.
11. How to join a trace to its session. Fixed: `gen_ai.conversation.id`.

## Limits

No judge model was called; the trial's stand-in judge tested what reaches
a judge, not how well one grades. Opik was not run.
