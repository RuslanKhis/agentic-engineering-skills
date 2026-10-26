---
document: government-form-answers
system: <system name>
status: draft
jurisdictions: [<codes in scope, in the order au, us, eu, uk, nz, sg, ca; must include au>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
for: <the agency officer who completes the official form: assessing officer, accountable use case owner or AIAF Accountable Owner>
form: <official form's name, for example DTA AI impact assessment tool, or NSW AIAF Platform registration>
form_version: <version exactly as the official page or document shows it>
form_url: <https://official page of the form>
form_checked: <YYYY-MM-DD the official page was last read>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md, docs/plans/<topic>.md, regulatory-memo.md, impact-assessment.md, privacy-impact-input-pack.md, system-card.md>
---

# Draft answers for <form>: <system name>

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

This is not the official form. It drafts answers, in the official form's own
order, for <agency>'s officers to check and paste into the official tool,
where they complete, rate and approve the assessment. Each answer cites the
project record, or says who must answer it: `agency:` for what only the
agency can answer, `counsel:` for a legal question. Not legal advice.

<!-- One document per official form: name it
government-form-answers-<form>.md. Take the question order and numbers from
references/au-government-crosswalks.md, never a copy of the form. Re-read the
form's official page first; if its version differs from the crosswalk's,
write a gap: in Form and version and stop until the crosswalk is updated.
If the page cannot be read (no web access, or the form sits behind the
agency's login), take form_version and form_checked from the crosswalk,
which records when the form was last read at the source, and write
"gap: official page not re-read" in Form and version; the checker's 90-day
warning then tracks the true age. Question numbers are written as the form
writes them ("Reg 1", "1.5"), never as bare R1, C1 or M1, which the checker
reads as the design's IDs.
Never fill an officer's name, an approval, a risk rating decision or legal
advice: propose a rating as assumption: with its basis and leave the rest
agency: or counsel:. Delete this comment. -->

## Form and version

- **Form:** <form name> <form_version>, <form_url> (checked <YYYY-MM-DD>).
- **Crosswalk used:** references/au-government-crosswalks.md, verified <YYYY-MM-DD> (source: adk-governance-pack reference, read <YYYY-MM-DD>).
- **Version match:** <the official page shows the version the crosswalk maps / gap: the official page shows <version>; the crosswalk maps <version>>.
- **Rating basis the form uses:** <DTA: inherent risk at section 3, residual at section 12; NSW: intrinsic band under the Operational Policy, residual in the 2024 AIAF> (assumption: <which rating each proposal is>).

## Who completes and approves

| Role in the form | Who | Evidence |
| --- | --- | --- |
| <assessing officer / Accountable Owner> | agency: <name and position, once the agency names them> | <source: or gap:> |
| <approving officer / responsible officers> | agency: <name and position> | <source: or gap:> |
| <external suppliers with responsibilities (the consultancy, the model and cloud provider)> | <consultancy as developer; Google as model and cloud provider> | <regulatory-memo.md Roles; D IDs> |

## Draft answers

| # | Question (paraphrase) | Draft answer | Evidence | Who decides |
| --- | --- | --- | --- | --- |
| <1.1> | <short paraphrase of the official question, never its full text> | <answer drawn from the record> | <C/D/M IDs or pack path> | <agency: approves / counsel: / the record> |
| <3.5> | <privacy risk> | <proposed rating, marked assumption: with its basis; rationale> | <privacy-impact-input-pack.md; IDs> | agency: <the assessing officer sets the rating> |

## Questions for the agency

- agency: <a question only the agency can answer: officer names, the approved products list, its enabling legislation, its records disposal authority, its risk appetite>; needed by <goal or wait ID>.

## Questions for counsel

- counsel: <a legal question the form asks, such as express legislative authority for an automated administrative decision, human rights alignment, use or disclosure>; needed by <goal or wait ID>.

## Review and sign-off

<!-- Only the reviewer fills Decision and Date. Leave both `pending` while
status is draft; the reviewer sets status: reviewed when they sign. One row
per reviewer: the role from `for:` first, then any other reviewer. The
agency's own approval of the official assessment happens in the official
tool, not here. -->

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| <the reviewer named in for:> | <this document, or the sections reviewed> | pending | pending |
