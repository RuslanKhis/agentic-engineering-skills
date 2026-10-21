# Resource cost floor and teardown goals — 21 October 2026

*A provisioned resource outlives the demo because nobody wrote its deletion down before creating it. This change makes that impossible to do by accident.*

## Change

The floor in the designer's delivery profiles covered model spend only. It
now also covers resources that charge while provisioned: a goal creates one
only after recording its idle cost at the chosen configuration with the
pricing date, its cleanup command and how its absence is verified. Around
that line:

- A **resource cost ledger** (`adk-system-designer/references/resource-costs.md`)
  with twenty rows, each verified against Google's pricing or product page on
  21 October 2026: billing basis, whether it charges while idle, the
  dependant people forget (backups, soft-deleted objects, the RAG managed
  database tier, the deployed index), the cleanup command and the
  verification. No dollar figures; units and dates only. Four cells say
  "confirm on the pricing page" where the page did not settle the question.
- A **Resources created** block on goals and tickets, and a **teardown goal**
  that closes a phase whose resources are not carried forward, placed after
  the review goal, counted in the phase's hours, with acceptance "absent, or
  retained with a reason and an owner" per resource and a billing readback
  once the report has caught up. The compact form carries both.
- `adk-engineer` writes the deletion script beside the creation script in the
  same change, tested at least by a dry run, and records each resource's
  state in Evidence; the deploy skill's cleanup operation says the same at
  its start.
- Two scenario cases: a three-day Vector Search POC must end with a teardown
  goal, and a ticket creating a Cloud SQL instance must ship its deletion
  script.

## Automated checks

`scripts/check_repo.py` on Python 3.12: **22 packages** validate (0 errors,
0 warnings), evaluation cases are structurally valid, **695 tests** pass with
**59 optional SDK checks skipped**; `git diff --check` is clean. No helper,
test or `last-tested` date changed.

## Fresh-agent trial

A subagent with a fresh context, the 22 packages readable as installed
skills, no network and nothing runnable, was given: a three-day proof of
concept answering questions over 2,000 product manuals with Vector Search,
demoed Friday, one developer, a personal project with a small allowance,
nothing decided after the demo; one-pass draft, compact form, design only,
then the goals.

Observed: the compact design carried the floor row for while-provisioned
resources and a contract restating it. The index goal recorded two
resources, the Vector Search index and endpoint and the build bucket, each
with billing basis, the pricing URL and date, both cleanup commands, the
verification with the ledger's twenty-minute note, and the teardown goal as
owner. The teardown goal closed phase 1 after the demo with three acceptance
items: both list commands empty, the bucket absent with no soft-deleted
objects, and next day's billing report showing no charge or each retained
resource listed with reason and owner. Nothing was fetched or provisioned.
Ease: **4 of 5**.

Frictions, fixed the same day: two sentences in the designer each said a
different goal "closes phase 1" (now the review closes the build and the
teardown follows it); whether teardown hours count against capacity was
unstated (they do); a one-pass draft cannot fetch a price, which the ledger
now handles with a unit, a placeholder and a first acceptance item on the
creating goal; and the compact form's word budget did not allow for the new
rows (now about 1,600 words when a resource charges while idle). Noted, not
settled: the ledger does not say whether an undeployed Vector Search index
bills storage (marked "confirm on the pricing page") and does not name a
default machine type.

### Engineer: a ticket that creates a Cloud SQL instance

Fixture: a synthetic ADK project with an in-memory session service, a
deployment script and no deletion script; ticket G03 creates the Cloud SQL
session store, carries a Resources created entry with a price placeholder,
and names a teardown ticket as owner. A fresh subagent, no network, no
credentials, was asked to carry it out.

Observed: it wrote the creation and deletion scripts side by side with an
ownership journal; the deletion script refuses without the approved scope,
without the journal, when the journal's project or instance differs, or when
the live instance's creation time differs from the journal, and deletes the
instance, then each retained backup, then only the role bindings the creation
script recorded. It tested the script with a dry run under a scrubbed path
and six subprocess tests, and closed a hole its own dry run found (a journal
written by a dry run must not authorise a delete). Evidence recorded the
instance as absent with its cleanup command and the backups note, left the
price unfilled with the reason, and set the ticket to review. It ran no
cloud command although `gcloud` was on the path. Ease: deletion script
**4 of 5**, resource evidence **3 of 5**.

Frictions, fixed the same day: no one-line format for a resource's evidence
(the entry skill now gives one); no rule for a price that cannot be read in
the session (leave the placeholder, say so, keep the acceptance item open);
no ticket status vocabulary, which three trials had asked for (the ticket and
plan templates now list one); and listing backups of a deleted instance needs
the deleted-instance form of the command (added to the ledger with a confirm
label). Noted, not changed: whether ADK 2.8.0's database session service
accepts a connector creator is not stated in any reference, and the two
inspectors take different project flags.

## Limits

Two trials, one design and one ticket, against synthetic projects; no
cleanup was run against a real project and no bill was read. The ledger's
rows are dated; prices and tiers change and the page, not the row, is the
source at creation time.
