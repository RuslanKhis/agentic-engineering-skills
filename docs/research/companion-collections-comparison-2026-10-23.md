# Companion collections and conventions compared with this toolkit — 23 October 2026

## Scope and snapshot

Read on 23 October 2026, never run: google/adk-docs
`docs/tutorials/coding-with-ai.md` at commit `0ac7ec6` (sparse checkout
repaired that day); [agentsmd/agents.md](https://github.com/agentsmd/agents.md)
at commit `d001185` (MIT; `README.md`); [obra/superpowers](https://github.com/obra/superpowers)
at commit `2ce8aa1` (MIT; `skills/using-superpowers`,
`subagent-driven-development`, `verification-before-completion`);
[mattpocock/skills](https://github.com/mattpocock/skills) at commit `5beb35b`
(MIT; `skills/engineering/implement-spec`, `wizard`, `to-tickets`); and
Kiro's public specs pages (overview, best practices, correctness,
feature specs; fetched 2026-10-23; no snapshot). Phase B's agents-cli review
already covered google/agents-cli.

**Conclusion.** Two facts entered the engineer's composition reference as
routing context: Google's three channels for giving a coding agent ADK
context, and the `AGENTS.md` convention with its `CLAUDE.md` pairing. The
rest is Phase D input, recorded here so the designer trials can test it:
Superpowers' rule that only four things stop an executing agent
(irreversible or destructive operations, security-sensitive actions, side
effects outside the worktree that norms say to ask about, and a plan so
broken that every path is a guess), its "no completion claims without fresh
verification evidence" rule with the red-green check for regression tests,
and its "process skills first" bootstrap, which is why it is an alternative
lead method rather than a layer; Matt Pocock's ticket graph with "Blocked by"
edges and `ready-for-agent` status, per-ticket worktrees with a merger
subagent and a final review, and the wizard for steps only a person can do.
Kiro's pages, as fetched, give one EARS template (`WHEN [condition/event]
THE SYSTEM SHALL [expected behavior]`) and the bugfix form `WHEN [condition]
THEN the system SHALL CONTINUE TO [existing behavior]`, define a property as
"a universal statement about how your system should behave" derived from
such requirements and checked by generated property-based tests, and say
plainly that passing tests "raise confidence but do not guarantee the
absence of bugs" and that a weak or wrong property passes while behaviour
is still wrong.

## Method

Each collection's relevant skill files were read; nothing was installed or
run; the memo's proposals that rest on them are tested in Phase D against
the designer's existing templates rather than adopted from this reading.

## Drift corrected

- The memo attributed `parallel_safe` and `touches` front-matter fields to
  Matt Pocock's `implement-spec`; the collection's `to-tickets` template
  carries "Blocked by" and a status, not those fields. They remain the
  memo's own proposal and are tested as such.
- The memo's EARS forms with `IF ... THEN ... SHALL ...` and `SHALL NOT`
  were not on the fetched Kiro pages; only the two templates above were.
  The designer trials test the wording on its merits, cited to Kiro only
  for the `WHEN ... SHALL` form.
- The concepts page the memo cites returned 404 on 2026-10-23.

## Imported, by specialist

- **adk-engineer.** The three context channels and the `AGENTS.md`
  convention in the composition reference.

## Routed, not copied

The collections are companions a ticket may name; the composition table's
existing rows for Agents CLI and Matt Pocock's process skills stand.

## Vendored assets

None.

## Left out, with reasons

- Superpowers and Matt Pocock's remaining skills: process skills for other
  workflows.
- Kiro's bugfix, plan and quick-spec pages beyond the quoted lines.

## Limits

Read, not run; Kiro's pages were fetched through a summarising fetch, so
quotes are limited to what it returned verbatim.
