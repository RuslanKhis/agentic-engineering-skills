# The A2A TCK compared with this toolkit — 22 October 2026

## Scope and snapshot

A review of [a2aproject/a2a-tck](https://github.com/a2aproject/a2a-tck) at
commit `5daf014` (2026-10-20), latest tag v0.2.5, cloned on 22 October 2026
into its own directory and read (Apache-2.0, no NOTICE), with the A2A
specification `CHANGELOG.md` already verified in Phase B (1.0.0 of
2026-03-12, 1.0.1 of 2026-05-26) and `a2a-sdk` 1.2.3 on PyPI. Files read:
`README.md` (run command, levels, transports, reports),
`run_tck.py` (level semantics), `tck/requirements/auth.py`,
`agent_card.py` and `versioning.py` (requirement ids, titles and levels),
`scenarios/core_operations.feature` (scripted `messageId` prefixes),
`tck/transport/jsonrpc_client.py` (headers sent) and `AGENTS.md` (companion
skills). Two related items: google/agents-cli's `_a2a_pinning.py` was fetched
raw and read for its origin-pinning note; a2aproject/a2a-samples was listed
by its HEAD commit only.

**Conclusion.** The TCK is the right acceptance tool for an exposed agent's
card and versioning requirements and the wrong one for everything else on a
real agent, exactly as the memo said: its core-operation scenarios drive a
scripted system under test and its client sends no authentication header. So
the interoperability skill now carries the scoped MUST run, the requirement
ids a ticket can name, what the toolkit's own card checker does not yet
cover, and the companion skills; the designer's handoff writes the A2A
acceptance as a planned verification whose first step is the spike. It was
not run: the kit is not published to PyPI and this programme's rules forbid
executing code from a downloaded repository, so every command above is
version-conditional until a team runs it on its pinned a2a-sdk.

## Method

Facts were read from the kit's source rather than its prose where the two
could differ (levels from `run_tck.py`, headers from the transport client,
prefixes from the feature file), classified, and written at the decision in
the A2A contracts reference with the citation and the "not run" label. One
scenario case covers the journey; the fresh-agent trial is in the
[testing record](../testing/a2a-tck-alignment-2026-10-22.md).

## Drift corrected

- The memo's "`AUTH-SERVER-002` ('Server must authenticate every incoming
  request')" and "`VER-SERVER-003` (an empty version header means 0.3)" match
  the requirement titles. The card requirements the memo summarised
  (signing, caching, extended-card auth) map to `CARD-SIGN-001`, `-002`,
  `CARD-CACHE-001` to `-003` and `CARD-EXT-001`; `CARD-CACHE-*` are SHOULD,
  not MUST, which the scoped `--level must` run will therefore not score.
- "The TCK's lack of an auth-header option was established by grep": the
  transport client was read and sends `A2A-Version` and `Content-Type` only;
  a pytest hook could still inject one, which the reference leaves to the
  team.

## Imported, by specialist

- **adk-agent-interoperability.** The scoped command, card discovery path,
  level semantics, report files, the scripted-SUT and no-auth limits, the
  requirement ids, the three checks `agent_card_check.py` lacks as manual
  items, the companion skills, the origin-pinning rule for raw SDK clients
  with agents-cli's note, and the a2a-samples names pinned by commit.
- **adk-system-designer.** The A2A acceptance item as a planned verification
  with the spike first.

## Routed, not copied

The TCK's `run-tck`, `learn-requirement` and `diagnose-failure` skills are
named as companions a ticket may list; they live in the kit's repository,
not in a published collection, so no standard routing line.

## Vendored assets

None.

## Left out, with reasons

- New rules in `agent_card_check.py` for signing, caching headers and
  extended-card authentication: a helper change that should be validated
  against a TCK run, which this review could not perform; recorded as the
  next change for the helper.
- The gRPC and HTTP+JSON transports, the SUT generators, push-notification
  and streaming requirements: no decision here depends on them.
- a2a-samples contents: not read.

## Limits

Read, not run. Requirement ids and levels are as of v0.2.5 and the kit's
own README calls its tags alpha; a team runs the scoped command on its
pinned a2a-sdk and records the exit code before relying on the wording.
