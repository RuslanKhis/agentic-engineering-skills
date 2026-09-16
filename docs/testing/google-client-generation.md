# Google coding-client generation trial

*16 September 2026 · One local implementation exercise, with separate acceptance checks.*

## Result

**Antigravity IDE 2.5.5, using Gemini 3.8 Flash (Medium), successfully used
`safe-api-tool-calls` to repair a synthetic refund adapter.** Its 21 project tests
and nine independent acceptance tests passed. No implementation repair was
needed after review; a follow-up corrected one sentence in its generated README.

Gemini CLI 0.60.0 was also attempted, but its preflight exited **41** because no
authentication method was configured. Its normal Google sign-in flow was opened;
model generation remains pending authentication. Antigravity's separate app and
`agy` CLI were not exercised. The IDE result does not establish results for them.

| Evidence | Result |
| --- | --- |
| Antigravity IDE reads the named skill | Observed `safe-api-tool-calls/SKILL.md` read |
| Relevant supporting instructions | Observed `writes-and-confirmation.md` and `validation.md` reads |
| Generated implementation | `service.py`, additional tests and a README |
| Project tests | 21 passed: one preserved original test and 20 added tests |
| Independent acceptance | 9 passed, kept outside the client project during generation |
| Required file preservation | `provider.py` and `CONTRACT.md` unchanged; original test class preserved |
| Review follow-up | README wording corrected; tested code and test hashes unchanged |
| Gemini CLI generation | Blocked at authentication preflight; no code generated |

## Exercise and method

The [seed project](artifacts/google-coding-agents/live/seed/CONTRACT.md) contains a
small standard-library Python adapter and an entirely local synthetic provider.
Its defects include generating a new replay key on each retry, accepting invalid
money inputs, ignoring confirmation and misreporting uncertain outcomes.

The [generation prompt](artifacts/google-coding-agents/live/prompt.txt) asks the
client to use the named skill, preserve the public interface and fixed provider
contract, implement the repair, add tests and explain the limits. All twelve
skill packages were copied into the disposable project's `.agents/skills/`
directory. The skill's text was not pasted into the chat.

The Antigravity IDE trial used a new window and an owned temporary project,
with trust granted only to that project. The existing account session was used.
The selected model during both generation and the editorial follow-up was
**Gemini 3.8 Flash, Medium**; the previous client model preference was restored
afterward. Local test and read-only status commands received one-time approvals.

The observed client actions include skill/reference reads, file edits, actual
test output and a completed final response. The final response additionally
named `reads-and-deadlines.md`; that name alone is not proof of reading it, so it
is not included in the confirmed reference-read list. A `git status` command
failed because the disposable directory was not a Git repository; generation
and testing continued normally.

The [nine independent checks](artifacts/google-coding-agents/live/acceptance/test_acceptance.py)
were written before generation and retained outside the project. Eight of their
nine test methods fail against the seed, demonstrating that the original happy
path test is insufficient. They cover single-effect recovery after a lost reply,
cached repeats, changed payloads, uncertainty after a later rejection, exact
money, invalid inputs, confirmation and terminal rejection.

The parent independently ran both suites against the generated code with
**Python 3.11.4**. Repeated executions are not counted as new coverage. Imports
and test entrypoints were inspected; these suites use the standard library and
synthetic calls, with no provider I/O or cloud dependencies.

## Review and scope

Review found no implementation defect within the specified contract. The
generated README initially described every `confirmed=False` call as cancelled.
The implementation and its tests instead return the stored outcome for an
already-dispatched operation. Antigravity corrected that wording to distinguish
new operations from repeated ones. Only the README hash changed afterward.

This is one functional smoke test of one specialist in Antigravity IDE. It does
not test every skill, automatic skill selection without naming it, routing via
`adk-engineer`, or live ADK/Google Cloud integrations. The refund provider
guarantees valid receipts and deduplication within its lifetime; malformed
receipts, restart persistence and worker concurrency are outside this exercise.
The coding client used a real hosted model; the generated application made no
real refund, ADK provider or cloud deployment calls.

## Reproduce the offline checks

From this repository's root, with Python 3.11 or later:

```bash
python3 -m unittest discover -s docs/testing/artifacts/google-coding-agents/live/antigravity-final -v
PYTHONPATH=docs/testing/artifacts/google-coding-agents/live/antigravity-final python3 -m unittest discover -s docs/testing/artifacts/google-coding-agents/live/acceptance -v
```

## Evidence

- [Initial generated files](artifacts/google-coding-agents/live/antigravity-initial/service.py)
  and [final README](artifacts/google-coding-agents/live/antigravity-final/README.md).
- [Commands, results and hashes](artifacts/google-coding-agents/live/antigravity-results.json).
- [Project test output](artifacts/google-coding-agents/live/antigravity-generated-tests.txt)
  and [independent test output](artifacts/google-coding-agents/live/antigravity-acceptance-tests.txt).
- [Selected observed UI events](artifacts/google-coding-agents/live/antigravity-observations.json),
  transcribed from the client interface; these are not a full conversation export.
- [Failing seed results](artifacts/google-coding-agents/live/baseline-results.json)
  and [editorial follow-up prompt](artifacts/google-coding-agents/live/editorial-followup.txt).
- [Gemini authentication preflight error](artifacts/google-coding-agents/live/gemini-preflight.stderr.txt).

See the earlier [installation and discovery checks](google-coding-agents.md) for
all twelve packages, and the [Google client setup guide](../integrations/google-coding-agents.md)
for installation and invocation instructions.
