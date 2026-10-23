# Phase D: the memo's designer proposals as hypotheses — 23 October 2026

The integration memo proposed eight changes to `adk-system-designer`'s
templates. Each is treated here as a hypothesis: what already exists, what
was prototyped, what two trials showed, and the ruling. The prototype is a
copy of the ticket template with every proposal added
(`ticket-template-B` in the session scratchpad; 590 words against the
current template's 432), used by one designer trial on a synthetic design
while a second designer trial used the current template on the same design;
an engineer trial then carried out one ticket from each. Thresholds the memo
suggested are placeholders and are not written into any skill.

| # | Proposal | Existing equivalent | Prototype | Ruling |
| --- | --- | --- | --- | --- |
| 1 | `reference_patterns` front-matter field | none; "Implementation route" names inspected modules | optional field: source, file, commit, what to copy | declined: "none" on a greenfield project; the route already names inspected modules |
| 2 | `touches`, `parallel_safe`, `constraints`, `docs` fields | `blocked_by` for ordering; supporting skills name the references indirectly; the design's constraints section | four fields; `parallel_safe` derived from `touches` | adopted `touches` (as paths expected to change, implementer adds what it creates), `parallel_safe` (defined on written paths and finished dependencies) and `docs` (the engineer said it cut the reading); declined `constraints` (a third pointer to the design) |
| 3 | EARS wording for acceptance items | free-text A-items naming the contract | `WHEN ... THE <app> SHALL ...`, `IF ... THEN ... SHALL ...`, `... SHALL NOT ...` | adopted as the placeholders (the engineer mapped items one-to-one onto tests), with a `(floor)` tag for items that prove a pin or floor rather than a contract |
| 4 | Automated and manual verification split | one `Verification:` line naming the tier | two lines: automated (command, exit code, tier) and manual (person, check) | adopted, plus the interpreter named and what counts when the SDK is absent |
| 5 | Evidence per acceptance item with command, exit code, commit; `Rulings:` list; `done` only with fresh evidence | Evidence section lists files, commands, per-contract lines, deferred controls, owed review | per-item evidence, `Rulings:`, the `done` rule in the run prompt | adopted (both engineers filled it as a checklist), with "uncommitted" allowed in place of a SHA, a partial-tier wording, and designer rulings given a home in Outcome |
| 6 | Delta contracts | design template: "When a contract is revised, keep its ID, add a one-line note, and update the decisions and goals that cite it" | `contract_deltas` field on the ticket | adopted as an optional field (trial B used it to record a narrowing of C2) |
| 7 | G00 goal writing a project `AGENTS.md` with a `CLAUDE.md` include | none; the engineer's composition reference now names the convention | not in the ticket prototype; tested as a question to the designer trials | declined as a goal of every plan (neither designer reached for it); the handoff reference says where such instructions live and when to write them |
| 8 | Companions table; one lead method per session | composition table rows for Agents CLI and Matt Pocock's process skills | one line in the run prompt: lead method, replacement not addition, `wizard` for human-only steps | adopted as one paragraph in the handoff reference, not in every ticket (the engineer called the per-ticket lines dead weight) |

## Trials

Recorded in the [testing record](../testing/phase-d-designer-trials-2026-10-23.md).

## Rulings

The table's last column. Beyond the memo's eight, both designer trials and
both engineer trials asked for the same repairs to the existing template,
now made: `blocked_by` defined so a dependency-ordered phase can be
ticketed in full; `design:` and `plan:` relative to the repository root;
`calendar_waits` copied from the plan exactly; a `handoff` hours field;
supporting skills with their purpose; usage spend beside provisioned
resources; a status for "implemented, offline green, SDK tier owed"
(`in_progress` with the owed run named) and a rule for ticking boxes;
measurement records pointed at the plan template. The template grew from
432 to 717 words; the prototype's `constraints`, `reference_patterns` and
per-ticket companion lines were dropped to keep it there. Thresholds the
memo suggested are placeholders and were not written into any skill. The
schedule helper's comment parsing on list values, found by trial A, is fixed
with a test.

## Trial A observations (current template, 23 October)

The designer with the current template wrote the plan and four tickets,
ran the schedule helper (fits, four of four contracts cited, exit 0) and
rated the template 3 of 5. Its frictions are about the existing template,
not the memo's proposals, and are fixed or ruled on beside them:

- "Ready" has two meanings (the ticket's `status: ready` and `blocked_by`
  versus the plan's "resolved prerequisites, not new authority"), so a
  dependency-ordered phase cannot yield more than one "ready" ticket.
- Once tickets exist the plan drops its goal entries, but the ticket has no
  home for the implementation route, prerequisites, execution scope or the
  supporting skills' purpose.
- No field for handoff hours or `mentions_only`; no form for usage spend a
  ticket causes without provisioning (a judge run); acceptance items for
  floor constraints have no contract to cite; `design:` and `plan:` paths
  have no stated base.
- The schedule helper reads `mentions_only: [wait]   # reason` as the string
  `"[wait]"` because it checks the closing bracket before stripping the
  comment; the template's own schedule block invites trailing comments.
- The design fixture carried no scope-gate answers, so estimates rested on
  an assumed-answers table with no field to say so.

## Trial B observations (prototype template, 23 October)

The designer with the prototype wrote the plan and four tickets, ran the
schedule helper to a clean exit after four corrective runs, used every
proposed field and rated the template 3 of 5, the same as trial A. What
the proposals did in practice:

- `touches` and `parallel_safe`: filled, but the designer had to decide
  whether a read-only fixture counts as touched and what `parallel_safe`
  means when paths are disjoint but a dependency exists; it set the
  dependent ticket to no. The field needs its definition, not just its name.
- EARS acceptance wording: used for every item without complaint; the one
  gap it exposed is the same as trial A's: an acceptance item for a floor
  constraint or a version confirmation has no contract to cite.
- Automated and manual verification split: used without complaint.
- `Rulings:` inside Evidence: the designer wanted a home for rulings made
  while writing the ticket (two design gaps), and had none; it put them in
  Outcome and Scope.
- `contract_deltas`: used on one ticket to record a narrowing of C2.
- `reference_patterns`: "none" in a greenfield project; the template should
  say that "none: why" is the expected fill, or drop the field.
- `constraints` and `docs`: a third pointer to the design file; `docs` cost
  a grep over eight specialists to fill with real file names.
- The lead-method line in the run prompt: no comment either way.
- G00 project instructions: neither designer proposed one; the design had
  no place to ask for it.
- Shared with trial A: `blocked_by` conflates design readiness with
  dependency order; `design:` and `plan:` have no path base; `calendar_waits`
  must match the plan's value exactly while the hint invites prose; no field
  for handoff hours or `mentions_only`; no measurement-record wording on the
  ticket.

## Engineer trial A observations (ticket from the current template, 23 October)

The engineer carried out G01 from trial A's tickets and rated it 3 of 5.
What helped: primary and supporting skills, contracts, profile and
estimate; a Scope "In" list with paths and signatures; acceptance items
tagged with contracts; the Evidence placeholder's checklist; the Depth
paragraph. What was missing or not actionable: the verification line
assumed an interpreter with the SDK and said nothing about what counts
without it; the status rule left "built, policy tier proven, SDK tier owed"
without a value (it chose `blocked`); one acceptance item was ambiguous
("off-list argument"); which component logs was unstated; the pin's home
(no manifest in scope) and the Python floor were unstated; no wording for a
partial-tier evidence line; whether the agent ticks the boxes was unsaid;
a supporting skill listed without a purpose cost a read that contributed
nothing. The skills' own gaps (the scripted double's code shape; a
greenfield "pre-change run") are fixed beside the rulings.
