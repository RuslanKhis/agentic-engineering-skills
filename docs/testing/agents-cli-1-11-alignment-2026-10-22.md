# Agents CLI 1.11.0 alignment — 22 October 2026

*The September integration re-checked against the current Agents CLI, with the fact import the Google cloud skills got the day before.*

## Change

See the [comparison note](../research/agents-cli-comparison-2026-10-22.md)
for what was found. In the repository:

- **Drift corrected.** The integration guide, the composition reference and
  five specialists' source citations named versions 1.5 to 1.8; they now
  cite 1.11.0 where the content was re-read, the guide counts the toolkit's
  22 skills, names `agents-cli publish gemini` and the interoperability
  specialist as the registration owner, and lists the changes since
  September that affect how the collections combine. Eleven specialist files
  cite the renamed `google/adk-recipes` repository.
- **Three contradictions settled against the documentation** before any
  text changed: the invoker role for Gemini registration stays as
  documented with the CLI's different name noted; the claim that an Agent
  Gateway binding is set at creation and SDK-only was wrong and is replaced
  by the documented update path and its revision-archiving consequence; the
  Agent Identity baseline role differs between the documentation and the
  CLI and is recorded both ways.
- **Facts imported** into fourteen specialists from the code cheatsheet, the
  evaluation skill and the deployment, observability and publish skills,
  each verified on adk.dev or the Agent Platform pages where it changes a
  statement, otherwise cited to the 1.11.0 snapshot and dated; a
  source-precedence rule in the composition reference says how to settle
  Google's own disagreements.
- **Routing lines** in the exact form used for Google's cloud skills, at the
  decision each serves, and two scenario cases.

## Automated checks

`scripts/check_repo.py` on Python 3.12: **22 packages** validate (0 errors,
0 warnings), evaluation cases are structurally valid, **695 tests** pass with
**59 optional SDK checks skipped**; `git diff --check` is clean. No helper,
test or `last-tested` date changed.

## Fresh-agent trials

Both ran in a subagent with a fresh context, the 22 packages and Google's
seven Agents CLI skills readable as installed, no network, no credentials,
against one synthetic Agents CLI 1.11.0 project (manifest with the Agent
Identity default, an accepted spec, Cloud SQL sessions, generated Terraform,
a `deployment_metadata.json` from an earlier imperative deploy).

### Deployment ticket under Terraform ownership

Observed: the agent named the deploy specialist and the three supporting
skills, quoted the composition rule for the division, kept the dev engine
as retained and never reconciled, created the pilot engine under Terraform
and updated it with the CLI's update-only flag after repointing the
metadata, chose Agent Identity with the documented six-role baseline and
refused the broader role the CLI grants, recorded the content gates in the
environment and the absence of an upload block, wrote every command as not
run, and left the price placeholder open. It found the fixture's own
contract gap (no role for model inference) and recorded it as open. Ease:
**3 of 5**, because Google's skill text, release notes and source disagreed
on the identity default, the dry-run semantics and the manifest key, and
each needed a tie-break. Fixed the same day: the composition reference now
states the precedence (documentation for platform facts, release notes and
source over skill text for command behaviour, divergence recorded beside the
fact), and the Agent Runtime reference names both spellings of the manifest
setting.

### Focused change in the same project

Request: remember each user's preferred response language, keeping the
scaffold, the Cloud SQL backend and the pins, offline tests only. Observed:
the memory specialist led, consulted the code cheatsheet and the
cross-session-memory recipe as our skill directs, chose a deterministic
user-scoped state value written only by trusted code over Memory Bank, wrote
thirteen SDK-free tests and two Runner tests reported as not run, described
them as effect tests rather than the behavioural tests Google's workflow
discourages, and ran no spec phase, scaffold enhance, clone or evaluation
although the installed Google skills asked for each. Ease: **4 of 5**. Fixed
the same day: the composition reference now says a recipe clone is a network
action under the same authorisation as any fetch, and that Google's `uv`
rule does not stop running the project's tests with the interpreter at
hand. Noted, not changed: no skill says what to do when the only interpreter
is older than the project's pin.

## Limits

Two trials against one synthetic project; Google's skills were read as
files, not installed through their CLI; no command of theirs ran. The CLI
and its skills change weekly, and the precedence rule exists because the
snapshot already disagreed with itself.
