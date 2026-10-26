---
document: poc-note
system: <system name>
status: draft
jurisdictions: [<codes in scope, in the order au, us, eu, uk>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
for: <the reviewer who relies on it: counsel, DPO or privacy officer, CISO, risk owner>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md>
---

# Governance note: <system name> proof of concept

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

One page for <client>'s reviewers before the proof of concept runs. Not legal
advice; it says what the full pack must settle before production.

## Classification

- **Purpose and users:** <one sentence> (<R/C IDs>).
- **Australia:** <in scope and why, or n/a: why not> (<IDs or gap:>).
- **United States:** <in scope and why, or n/a: why not> (<IDs or gap:>).
- **EU:** <in scope and why, or n/a: why not; if in scope: Article 5 none identified, Annex III area or none, Article 50 disclosure> (<IDs or counsel:>).
- **United Kingdom:** <in scope and why, or n/a: why not> (<IDs or gap:>).
- **Roles:** <client and agency roles in each regime in scope> (<D ID or counsel:>).
- **Decisions about people:** <none, or what the output feeds and who decides> (<C IDs or counsel:>).
- **Data in the proof of concept:** <synthetic / anonymised / real personal data, scoped how; where staff access it from> (<floor item or D ID>).

## Data flow summary

| Step | Personal data | Component and region | Retention | Evidence |
| --- | --- | --- | --- | --- |
| <user input> | <categories or none> | <service, region> | <period> | <C/D IDs> |

## Questions for counsel

- counsel: <question that blocks the production decision, and who answers it by when>.

Full pack before production: <documents and the goal that writes them>.

## Review and sign-off

<!-- Only the reviewer fills Decision and Date. Leave both `pending` while
status is draft; the reviewer sets status: reviewed when they sign. One row
per reviewer: the role from `for:` first, then any other reviewer. -->

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| <the reviewer named in for:> | <this document, or the sections reviewed> | pending | pending |
