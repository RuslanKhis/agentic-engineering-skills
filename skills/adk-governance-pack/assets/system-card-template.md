---
document: system-card
system: <system name>
version: <build or release the card describes>
status: draft
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md, docs/plans/<topic>.md, evaluation reports>
---

# System card: <system name>

Draft for <client> reviewers. It describes the build named above and nothing
later. Not legal advice. Every statement cites a design, plan or evidence ID,
a dated source, or is marked `assumption:` or `counsel:`.

## Intended use

- **Purpose:** <what the system does, for whom, in which workflow> (<R/C IDs>).
- **Users:** <roles and number; internal / external> (<path §n or source: who, date>).
- **Deployer and provider:** <who puts it into service under whose name> (<classification memo or D ID>).
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

- <where a person reviews, approves or can override; share of outputs reviewed> (<C/SB ID>).
- <how a user contests or corrects an output, and who owns corrections> (<C/D ID>).
- <how the system is stopped or rolled back, and by whom> (<D/G ID>).

## Data

- <data the system reads and stores; personal data categories> (<DPIA input pack or D ID>).
- <screening and retention controls> (<C/SB ID>).

## Contact

- **Owner:** <role and contact> (source: <who confirmed>, <YYYY-MM-DD>).
- **Report a problem:** <channel> (source: <who confirmed>, <YYYY-MM-DD>).
