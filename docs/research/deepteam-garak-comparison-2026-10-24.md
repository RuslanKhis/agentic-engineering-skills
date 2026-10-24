# deepteam and garak compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [NVIDIA/garak](https://github.com/NVIDIA/garak) at commit
`d6a8be1` (release 0.17.1, 2026-10-16; Apache-2.0) and
[confident-ai/deepteam](https://github.com/confident-ai/deepteam) at
`6306f0f` (PyPI 1.0.10, 2026-10-16; Apache-2.0), cloned on 24 October 2026
into their own directories and read, never run. garak 0.17.1 was installed
from PyPI into a scratch environment and run offline against its test
generator and a scratch Python function; deepteam 1.0.10 was installed,
introspected and called once without a key, which it refused before any
request.

**Maintenance.** Both active. deepteam's GitHub releases page still shows
1.0.9 from November 2025 while PyPI has 1.0.10, so pin from PyPI.

**Conclusion.** Our security skill said garak "probes model endpoints, not
agents"; its `function` generator wraps any Python callable, so it can
attack the agent through the `Runner`. The spike and the trial found what
matters for CI: garak exited 0 on a clean pass, on detected hits and on most
errors (a function that raised exited 1), so a gate must read its report;
and garak's detectors read text only, so a gate must also read a record of
the tool effects that actually ran. Its `agent_breaker` probe and deepteam's OWASP Agentic
preset are both model-graded and model-paid, so they belong in the approved
live campaign with pinned models; deepteam also sends telemetry unless two
variables opt out, labels findings `ASI_01` rather than `ASI01`, and does not
import on a fresh 1.0.10 install without `sentry-sdk`.

## Method

Facts were read from source and confirmed by the garak spike (seven runs,
exit codes and report rows recorded) and the deepteam introspection. One
scenario case covers the journey; the fresh-agent trial is in the
[testing record](../testing/deepteam-garak-alignment-2026-10-24.md).

## Drift corrected

- "garak probes model endpoints, not agents", in the adversarial-testing
  reference and the sources list.
- The memo said deepteam's titles match ours; they differ for ASI04 and
  ASI08.

## Imported, by specialist

- **adk-agent-security.** In the live campaign: garak's `function`
  generator command and its contract (last message only, list return, no
  `name` parameter, deprecated flags), the report-based CI gate,
  `agent_breaker`'s models, judge and old OWASP tags; deepteam's preset
  invocation, default models, telemetry opt-outs, label normalisation and
  the install gap.

- **From the trial.** The effects sidecar as the grader, the corrected exit
  codes and report path, the stale-prefix trap, `nones`, the generation and
  detector defaults, the Python floor, deepteam's Gemini model class,
  callback signature, case count, `RedTeamer` defaults and result upload.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- deepteam's titles, default models, exposure scoring and platform upload.
- garak's OWASP tags as finding ids; the `agent_breaker` judge as a grader.
- garak's default report location under the user's home in CI.

## Limits

`agent_breaker` and deepteam attacks need model keys and were not run;
garak's `function` generator was not tried with an async `Runner` under
parallel attempts.
