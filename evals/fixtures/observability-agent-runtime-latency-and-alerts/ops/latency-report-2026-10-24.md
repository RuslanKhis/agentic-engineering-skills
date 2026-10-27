# Latency, week of 2026-10-20

From the Agent Runtime console's request latency chart (the only latency view we
have): p95 rose from about 4.2 s (weeks of 2026-09-29 to 2026-10-13) to about 8.6 s
since 2026-10-20. p50 moved from 1.9 s to 2.4 s. No deploy happened on 2026-10-20;
the payments provider announced maintenance that week. Nobody can say whether the
time goes to the model, the tools or loading the session.

No traces: nothing appears in Cloud Trace for the engine. Support pasted one slow
session export into `exports/` (session sess-7f31, 2026-10-23, 11.8 s end to end).
