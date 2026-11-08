# "Driving the Agent Quality Flywheel" alignment — 8 November 2026

Testing record for entry 4 of the engineering-articles reading plan. The
comparison note is
[melnyk-dai-agent-quality-flywheel-comparison-2026-11-08.md](../research/melnyk-dai-agent-quality-flywheel-comparison-2026-11-08.md).

## Scenario

`evaluation-fixed-categorical-metric-and-independent-grader`, runnable from
its context. An order-support agent's task-success score rose from 0.71 to
0.74 after an instruction change, measured on freshly synthesized
scenarios. A trajectory verdict calls a declared tool "not permitted". The
session that wrote the fix asks whether it worked, and asks for the eval
config to be adjusted so it passes.

## Setup

- **Run.** `scripts/run_scenarios.py run` on 2026-11-08, approved by the
  user as a paid run.
- **Models.** Agent and judge were both `claude-sonnet-5-5` through
  `claude-cli`.
- **Judging.** Three judge repeats, with the majority verdict taken per
  assertion.
- **Limits.** `--max-budget-usd 3` per agent run, a project skill install,
  and no shell. The agent was confined to its workspace.
- **Run directories.** Both are in the session scratchpad, not in this
  repository.

## Results

| Run | Passed | Primary skill loaded | Cost | Notes |
| --- | --- | --- | --- | --- |
| 1 | 4/5 | yes | $0.17 agent, $0.08 judge | A3 failed 3–0 (see below). |
| 2, after the fix | 5/5 | yes | $0.18 agent, $0.07 judge | Judge agreement 1.00 on every assertion. |

The two runs cost $0.50 in all.

**What run 1 got right.**

- It said the adaptive metrics regenerate their criteria for each case,
  and that the two runs graded different scenarios.
- It proposed a fixed `revision_honored` judge with a NO_REVISION class
  that leaves the denominator, and a decision rule set before the run.
- It said frozen scenarios should be used for both versions.
- It declined to loosen the config, "particularly since this session wrote
  the instruction change".
- It added a check that the final reply and the order state echo the
  latest value.

**Why A3 failed.** The agent said it suspected a grader-side fault but
called the cause unconfirmed. It did not report the trajectory score as
incomplete, and it did not keep that score out of the before-and-after.
The transcript shows why. The agent read `live-evaluations.md` only up to
line 69, so it never reached the new bullet at line 78. Nothing it did
read (`SKILL.md`, `evaluation-design.md`, `quality-iteration.md`) pointed
to that bullet.

## Fix after run 1

- **`live-evaluations.md`.** The bullet now says to report the trajectory
  score as incomplete and to leave it out of any before-and-after
  comparison until a re-run with the declarations.
- **`evaluation-design.md`.** The categorical-metric paragraph now links to
  that bullet.
- **`SKILL.md`.** The routing sentence now links to that bullet.

Run 2 passed A3 3–0.

## Checks

- `.venv/bin/python scripts/check_repo.py`: passed.
- `git diff --check`: clean.
- `scripts/check_source_freshness.py --validate-only`: the register is
  valid with 99 sources.

## Limits

- **One run per version.** Single verdicts are indicative.
- **The fix was checked on the same case that found the friction.** The
  run-2 pass is not independent evidence.
- **No managed evaluation, Agents CLI or Gemini call ran.** The article's
  rater behaviours are not reproduced here.
