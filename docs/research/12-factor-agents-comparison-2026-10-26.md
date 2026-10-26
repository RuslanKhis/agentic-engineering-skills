# 12-factor-agents compared with this toolkit — 26 October 2026

## Scope and snapshot

A review of [humanlayer/12-factor-agents](https://github.com/humanlayer/12-factor-agents)
at commit `d20c728` (2025-09-21), cloned on 26 October 2026 into its own
directory and read. The factors the memo named were read at that commit:
5 ("Unify execution state and business state"), 6 ("Launch/Pause/Resume
with simple APIs"), 8 ("Own your control flow") and 9 ("Compact Errors
into Context Window").

**Licence.** The only licence file is an Apache-2.0 `LICENSE` (copyright
line left as the template); the README states that content and images are
CC BY-SA 4.0 and code is Apache, without naming paths; one package declares
ISC. The factor pages are therefore link-only, with no text copied.

**Maintenance.** Stale: no commit for 400 days; not archived.

**Conclusion.** No link. The agreed limit was one link at most, and none of
the four factors adds a decision rule the skills lack. Factors 6, 8 and 9
are already stated more precisely, with ADK mechanisms: the three recovery
choices in `adk-system-designer`'s design decisions, confirmation in code
the model cannot reach and the `adk_request_confirmation` protocol, and
actionable error results with a bounded repeated-failure stop that keeps a
final failure apart from an unknown write. Factor 5, deriving state from
the conversation, contradicts the designer's rule that status comes from
receipts, never from the model's last message.

## Method

Factor titles and content were read at the pinned commit and compared with
`design-decisions.md`, `adk-tool-interface-design`'s results-and-errors
reference and `adk-operational-guardrails`' runtime bounds. No journey
changed, so no scenario case or trial was run.

## Drift corrected

None.

## Imported, by specialist

None.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- All four factors: covered more precisely (6, 8, 9) or contradicting the
  toolkit's receipts rule (5).
- Any text from the factor pages (CC BY-SA).

## Limits

Only the four named factors were read in full.
