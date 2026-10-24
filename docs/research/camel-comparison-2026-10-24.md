# CaMeL compared with this toolkit — 24 October 2026

## Scope and snapshot

A review of [google-research/camel-prompt-injection](https://github.com/google-research/camel-prompt-injection)
at commit `f083b6b` (2025-06-20; Apache-2.0) and the abstract of
"Defeating Prompt Injections by Design" (arXiv 2503.18813, v1 2025-03-24,
v2 2025-06-24), read on 24 October 2026. The code was read, never run.

**Maintenance.** Stale: no commit for 16 months; an unmaintained research
artifact. As agreed, it is cited as a pattern with a dated link, and no code
is used.

**Conclusion.** The review was meant to confirm a citation and found three
problems in our own text. The sample tool gate in the security skill allowed
any tool it did not list and every call when no plan was stored, where
CaMeL refuses any side-effecting tool without a policy. Our wording implied
that matching stored strings gives CaMeL's provenance guarantee; it misses
rewritten values and cannot see that a document steered the decision to
call a tool. And our capability tags recorded only where a value came from,
while CaMeL's also record who may read it, which is what lets a send rule
say "only to people who can already see this". The gate now denies by
default and keeps the plan check for every tool, the taint paragraph says
what it approximates, and two rules were added: readers-based send policies
and a reader that may abstain.

## Method

The policy engine, capabilities and reader were read in source; the
abstract was re-read for the dates. The security skill's existing CaMeL
citation in its sources was updated. One scenario case covers the journey;
the fresh-agent trial is in the
[testing record](../testing/camel-alignment-2026-10-24.md).

## Drift corrected

- The sample `capability_gate` (allow by default) in injection patterns.
- "Taint tracking (CaMeL's capability tags) is how it learns provenance".
- The pattern table's description of capability tags.
- "Not re-fetched" in the sources entry.

## Imported, by specialist

- **adk-agent-security.** The deny-by-default gate, the honest taint
  paragraph, provenance and readers rules per consequential tool, the
  abstaining reader and error redaction for the planner, and the dated
  source entry. After the trial: binding plan steps to the user's words and
  freezing once per invocation (agent callbacks rerun on a confirmation
  resume), many-target steps bound to the user's query, a minimum length
  for substring taint matching, what the plan leaves uncovered, the
  `SequentialAgent` deprecation on 2.12.0, and "archive" as a write verb in
  `inspect_security_surface.py`.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- All CaMeL code and policy files; one policy (`delete_email_policy`)
  inverts its own stated check.
- The custom interpreter as a replacement for ADK's tool loop, its prompt
  wording and its re-planning budget.

## Limits

Only the abstract was read, not the full paper; no CaMeL code was run.
