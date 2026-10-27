# Situation: release-promptfoo-gate-exit-codes-and-trajectory-assertions

Overlay on support-assistant: nightly workflow with a model key secret and a placeholder step;
PR CI runs unit tests; platform standard requires Promptfoo; a scripted-Runner test file skipped
without the SDK. No model access in session. A1 (in-process Python provider calling run_async,
trajectory and trace-span assertions), A2 (exit 100 block, 0 pass, 1 NOT RUN;
PROMPTFOO_PASS_RATE_THRESHOLD placeholder; model-dependent tier), A3 (repeat-min-pass as observed
rule, no sharing), A4 (scripted tests and adk eval primary; vendor guidance) graded from the
answer and files. Context unchanged.
