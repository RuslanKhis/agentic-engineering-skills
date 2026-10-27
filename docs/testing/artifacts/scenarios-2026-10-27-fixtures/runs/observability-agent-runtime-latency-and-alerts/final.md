I turned telemetry on in the deploy config and wrote the SLO and alert design, but nothing is deployed and nothing was run. I had no shell, so I couldn't run the helper scripts or the unit tests.

**What I changed**
- **`deploy/agent_engine.env`:** I added `GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true` and `ADK_EXPERIMENTAL_TELEMETRY=true`. The second is what produces the token metrics.
- **Prompts out of traces:** I also set `ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false` and `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT`. In 2.8.0 prompts and tool arguments go into spans by default, so the first one matters.
- **`docs/observability.md`:** this is new and holds the attribution design, the draft SLO, draft alert queries, the approvals list and my assumptions.
- **No application code changed:** ADK 2.8.0 already emits model and tool spans and duration metrics.

**What the saved session suggests**
- One invocation took 11.8 s. Tools were about 60% of that and the model about 40%.
- The `issue_refund` call alone took 6.8 s, which is 57% of the invocation. That is a payments-provider HTTP call.
- This is one sample, so it's a lead. It needs confirming across many traces.
- Session loading can't be seen in the export. I attribute it as a residual: host request latency minus agent duration. It is inferred, not measured.

**The SLO and alerts**
- The provisional SLO is 95% of invocations within 12.8 s over 28 days. That 12.8 s is a placeholder, because I had no baseline numbers. Replace it with the pre-regression p95 plus headroom.
- I drafted fast-burn and slow-burn latency alerts, plus alerts for telemetry stopped, slow tools, and model errors. The PromQL is unverified until the real metric names are visible in your project.
- `issue_refund` returns `{"status": "error"}`. ADK doesn't treat that as a tool error, so refund failures won't show up in the tool-error alert. Changing the return shape would change what the model sees, so I left it for you to decide.

**Left undone, needs your approval**
- Enabling `telemetry.googleapis.com`. Don't redeploy with the new env file before this is on, or exports fail quietly.
- Granting the runtime identity `roles/telemetry.writer` and `roles/logging.logWriter`.
- Redeploying.
- Creating the alert policies and choosing notification channels.
- Checking live that spans arrive without content and that the metric names match.
- Running `invocation_summary.py`, `events_to_eval_set.py`, an in-memory exporter test, and the repo unit tests.

**Questions I couldn't ask, and what I assumed**
- **p95 before and after:** I assumed it's unknown, which is why the 12.8 s target is a placeholder.
- **Which host serves production:** the README says Cloud Run and you said Agent Runtime. I assumed Agent Runtime. `app/server.py` (Cloud Run) is not instrumented.
- **Who gets paged:** I assumed it's undecided, so no channel is referenced.
- **What changed at the time of the regression:** unknown. Prompt tokens grow by about 100–180 per call in the session, so context growth is worth checking too.