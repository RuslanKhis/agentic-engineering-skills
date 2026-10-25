# WrenAI compared with this toolkit — 25 October 2026

## Scope and snapshot

A review of [Canner/WrenAI](https://github.com/Canner/WrenAI) at commit
`86fcca2` (2026-10-23), cloned on 25 October 2026 into its own directory
and read, never run. WrenAI is now an engine, a CLI (`wren` 0.16.0) and an
MCP server; the earlier chat application moved to a `legacy/v1` branch.

**Licence.** The root `LICENSE` maps licences by path: `core/`, `sdk/`,
`skills/` and `examples/` are Apache-2.0 (no NOTICE file); `docs/` is
CC BY 4.0; an AGPL-3.0 text ships for future modules but covers no path
today; the `legacy/v1` branch is AGPL-3.0 as a whole; the Wren names and
logos are trademarks outside every licence. The skill paraphrases code
behaviour with a link and copies nothing from `docs/` or `legacy/v1`.

**Maintenance.** Active; releases on 2026-10-23.

**Conclusion.** The memo's "semantic layer as reviewable files" is
confirmed: models, relationships, measures and examples are committed YAML
and Markdown, and the compiled manifest is generated. The useful import is
the file shape plus two gaps in WrenAI's own gate, not the tool: its
validator only warns on a relationship without a join condition or type,
proves nothing about the live schema, and its re-check of expanded SQL
lets a parse failure through.

## Method

The validator's warning levels and `--strict` exit, the expansion comment
and the fail-open docstring in `policy.py` were confirmed in the snapshot
before editing. One scenario case covers the journey; the fresh-agent trial
is in the [testing record](../testing/wrenai-alignment-2026-10-25.md).

## Drift corrected

None; the skills did not mention WrenAI.

## Imported, by specialist

- **adk-sql-agent-engineering.** In `implementation.md` (semantic domains):
  a reviewed-file layout for the map, a CI check that fails rather than
  warns on an incomplete relationship, an unknown name or a missing key,
  and a live-schema comparison plus a duplicate-key fixture. In
  `execution-safety.md`: run the read-only policy on SQL expanded from the
  map and fail closed when it does not parse, with a write-in-definition
  fixture asserting zero jobs. After the trial: what WrenAI's validator
  accepted when run, where domains and metrics go, the `join_type`
  mapping, a drift rule with type-name normalisation, the key check on a
  schedule, a routing row and a rule for few-shot examples saved from
  traffic, the Python floor for ADK 2.12, and the function-node context
  fields.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- Storing every successful query as an approved example by default, which
  WrenAI's usage guide does and labels as user-sourced; the skill already
  treats a successful trace as a candidate for review.
- `strict_mode: False` as the default table-scope gate; the skill's
  trusted-scope binding stays mandatory.
- Agent-applied "auto-pilot" enrichment of definitions; metric owners
  settle meaning.
- WrenAI as executor or MCP server; not evaluated.
- The Ossie interchange draft; not verified upstream.
- Any `docs/` text, `legacy/v1` code, and the Wren names and logos.

## Limits

Nothing was run; the validator's exit codes come from reading the source.
The planner's fallback path when strict mode is off was not traced.
