---
document: system-card
system: <system name>
version: <build or release the card describes>
status: draft
jurisdictions: [<codes in scope, in the order au, us, eu, uk>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
for: <the reviewer who relies on it: counsel, DPO or privacy officer, CISO, risk owner>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md, docs/plans/<topic>.md, evaluation reports>
---

# System card: <system name>

> **Drafting aid output, not legal advice.** Prepared to support the
> reviewer named in `for:`, never to replace the client's lawyer. It is not
> reviewed until that reviewer records a decision in Review and sign-off at
> the end; counsel decides every legal conclusion in it.

Draft for <client> reviewers. It describes the build named above and nothing
later. Not legal advice. Every statement cites a design, plan or evidence ID,
a dated source, or is marked `assumption:` or `counsel:`.

## Intended use

- **Purpose:** <what the system does, for whom, in which workflow> (<R/C IDs>).
- **Users:** <roles and number; internal / external> (<path §n or source: who, date>).
- **Deployer and provider:** <who puts it into service under whose name> (<regulatory memo or D ID>).
- **Decisions it informs:** <what a person decides with its output; what it may change itself> (<C IDs>).

## Out-of-scope use

- <use the system is not designed or evaluated for> (<C/D ID or assumption:>).
- <reasonably foreseeable misuse and the control that limits it> (<C/SB ID>).

## Limits

- <known failure mode, from evaluation or incidents> (<M/I ID>).
- <inputs, languages or populations not evaluated> (<gap: or assumption:>).
- **Model:** <pinned model ID and its retirement date> (<D ID>, source: <lifecycle table>, <YYYY-MM-DD>).

## Evaluation results

| Measure | Result | Baseline or threshold | Sample and window | Build | Evidence |
| --- | --- | --- | --- | --- | --- |
| <quality / safety / bias / cost measure> | <value> | <value> | <n, dates> | <build> | <M ID or report path> |

Not yet measured: <measure>, measured by <goal ID> (<gap:>).

## Human oversight

- <where a person reviews, approves or can override; share of outputs reviewed; override rate> (<C/SB ID, M ID>).
- <how a user contests or corrects an output, and who owns corrections> (<C/D ID>).
- <how the system is stopped or rolled back, and by whom> (<D/G ID>).

## Automated-decision disclosure

<!-- Facts for the client's privacy policy, notices and explanations; write n/a: with the reason when no output decides, or feeds a decision about, a person. Delete this comment. -->

- **Kinds of personal information used:** <kinds, in plain language> (<C/D IDs>).
- **Decisions made solely by the system:** <kinds, or none> (<C IDs>).
- **Decisions where the system does something substantially and directly related:** <kinds: ranks, scores, recommends, drafts> (<C IDs>).
- **Meaningful information about the logic:** <features used and how the output is used; the explanation the design can produce on request> (<C/D IDs>).
- **Human review, representations and contest:** <route and owner> (<C IDs or gap:>).
- **Opt-out or appeal, where offered:** <route, or n/a: none required by the regimes in scope> (<C ID or counsel:>).

## AI disclosure and hand-off

- **Disclosure that the user is talking to an AI:** <when and how; how it answers "are you a human?"; on whose behalf an acting agent says it acts> (<C ID with its test>).
- **Hand-off to a person:** <route, hours, and the measured time to connect> (<C ID, M ID or gap:>).
- **Persona, memory of the user or relationship features:** <none, or what; the disclosure cadence and self-harm protocol if present> (<C/D IDs>).
- **Public claims about the system:** <each capability or accuracy claim the client will make and the M record behind it> (<M IDs or gap:>).

## Data

- <data the system reads and stores; personal data categories> (<privacy impact input pack or D ID>).
- <screening and retention controls> (<C/SB ID>).

## Contact

- **Owner:** <role and contact> (source: <who confirmed>, <YYYY-MM-DD>).
- **Report a problem or make a privacy complaint:** <channel> (source: <who confirmed>, <YYYY-MM-DD>).

## Review and sign-off

<!-- Only the reviewer fills Decision and Date. Leave both `pending` while
status is draft; the reviewer sets status: reviewed when they sign. One row
per reviewer: the role from `for:` first, then any other reviewer. -->

| Reviewer (role) | Scope reviewed | Decision | Date |
| --- | --- | --- | --- |
| <the reviewer named in for:> | <this document, or the sections reviewed> | pending | pending |
