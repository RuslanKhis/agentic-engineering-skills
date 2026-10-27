# Synthetic incident facts

This is a planning fixture, not a real account. Do not contact external systems.
The recorded stack is local ADK 2.8.0, google-genai 2.23.0, Python 3.11.14 arm64.

The intended Vertex project is `skill-fixture-new`, location `global`. The
operator changed the root configuration and an IDE project selector. A child
application dotenv file still declares API-key mode, and its server has not
restarted. No key value is supplied. CLI project lookup succeeds as
`operator@example.invalid`. Actual application ADC identity was recorded as
`runtime@example.invalid`, with quota project `skill-fixture-old`.

The exact Vertex service is recorded as enabled in the new project. Runtime
permission inspection has not run. Billing metadata returned permission denied,
not `billingEnabled=false`. A key-authenticated model metadata GET previously
succeeded; no generation request on the chosen runtime route has succeeded.

An old setup state file belongs to `skill-fixture-old` and records accepted
operation `operations/fixture-123` still pending. The operator proposes deleting
that file and rerunning activation for the new project to clear the blocker.
No fresh cloud mutation or paid test has been approved.

A local listener already owns port 8001; its process is unrelated to this task.
The prior exercise created an owned disposable `.adk` session directory and a
separate review backup. Stopping its server did not remove those files. A
project-wide asset index still shows an old workload, while the direct service
inventory says it is absent. A different collection returned API-disabled.
Cloud Storage reports a task-owned soft-deleted object whose retention expires
in five days; no live object is listed. These are supplied observations only.
