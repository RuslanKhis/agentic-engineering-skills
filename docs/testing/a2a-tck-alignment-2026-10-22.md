# A2A TCK alignment — 22 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/a2a-tck-comparison-2026-10-22.md).
In the repository: the scoped TCK run, requirement ids, limits and companion
skills in the interoperability skill's A2A contracts reference; the
origin-pinning rule for raw SDK clients with agents-cli's note; the planned
A2A acceptance in the designer's handoff row; sources. After the trial
(23 October): the 2.12.0 `to_a2a` signature with its new `security_schemes`
and `default_skill_security` parameters, a 1.0 card example generated from
the pinned SDK beside the 0.3 template, an inbound-authentication recipe for
an exposed agent with the executor's principal rule, the TCK ids as a table,
the card checker accepting the 1.0 `securityRequirements` key and leaving
scheme names untouched (with tests), the exact standard-library test
command, and a skip note for platform registration. **One scenario case**
(`interoperability-expose-a2a-with-tck-acceptance`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean; the interoperability package's tests
re-run after the checker change. The full `scripts/check_repo.py` counts
are in the README entry for this date.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK or a2a-sdk installed, on a synthetic project, without the expected
answers.

### Interoperability: exposing a triage agent over A2A with acceptance checks

The project: an ADK 2.12 agent with a2a-sdk 1.2.3 pinned, a partner that
will call with an OAuth client-credentials token, nothing exposed or
registered yet, no Node on the CI runner.

What the agent did: a curated 1.0-shaped card with one skill and a
client-credentials scheme, a standard-library bearer boundary (claims,
401/403/503 split, public card only) with a pluggable verifier and a
PyJWT-based one left uninstalled as an owner decision, the `to_a2a` server
behind that middleware with served-origin substitution, the tool moved out
of the SDK-importing module, 43 offline tests run on both interpreters and
5 SDK tests reported as not run, the card checker run (exit 0, two review
items about registration fields), and an acceptance ticket with twenty-four
checks by tier, deferred controls with triggers and the next run prompt.

Ease rating: **3 of 5**. Routing and the checker, template and checklist
were directly usable; the 1.0 wire shape and the inbound-auth side were
missing.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| No 1.0-shaped card example; where `protocolVersion` and the security wrappers sit was guessed | A 1.0 example asset generated from a2a-sdk 1.2.3 and the shape stated in the reference |
| Inbound authentication for an exposed agent had no owner recipe | A producer-auth recipe in the A2A contracts reference, with the ownership split stated |
| Principal to ADK user id on 2.12.0 unresolved | The request converter's rule from the 2.12.0 source: an authenticated call-context user's name, otherwise `A2A_USER_<context_id>`, with the unauthenticated name ignored |
| The checker camelCased scheme names and read only the 0.3 `security` key | Fixed with tests: map keys under schemes and requirements are kept; `securityRequirements` accepted |
| The standard-library test command was not given | The exact command in the engineer's interpreter rule |
| `to_a2a` stated for 2.8.0 only | The 2.12.0 signature with its two new parameters beside it |
| The TCK paragraph buried the acceptance-relevant ids | A table of ids with level, applicability and authenticated-run notes |
| Platform registration mandatory reading when not registering | The mode row says to skip it until registering |

## What this does not establish

The TCK was not run; the SDK-bound tests and any live exchange did not run;
the 1.0 card example was generated from the SDK's serialiser, not served.
