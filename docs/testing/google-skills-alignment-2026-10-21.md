# Google skills alignment — 21 October 2026

*What changed, what was checked, and what two fresh agents did with it.*

## Change

Google's [skills collection](https://github.com/google/skills) was compared
with every specialist (see the
[comparison note](../research/google-skills-comparison-2026-10-21.md)).
Two kinds of change followed:

- **Routing.** A goal or ticket may list a Google product skill as
  `google/skills:<name> (purpose)` in its supporting skills. The engineer's
  composition reference carries the specialist-to-product-skill table and the
  rule for a missing one (install command or Google's router, continue local
  work, record the product step as a prerequisite); the designer's handoff
  carries the same mapping by implementation route; the plan and ticket
  templates show the syntax; each specialist names the product skill to
  consult at the decision it serves.
- **Facts.** Nineteen specialist packages gained facts that change an ADK
  decision, each cited to the official page that confirmed it or labelled
  "vendor guidance, confirm against current docs" when only Google's skill
  stated it. The largest: the Agent Identity mechanism for Agent Runtime
  replaces a sentence that said a dedicated runtime identity was not
  implemented.

## Automated checks

`scripts/check_repo.py` on Python 3.12: all **22 packages** validate
(0 errors, 0 warnings), evaluation cases are structurally valid including the
two new scenario cases, and the offline suites run **695 tests** with
**59 optional SDK checks skipped**. `git diff --check` is clean. No helper
script, test or `last-tested` date changed; no SDK or cloud behaviour was
exercised.

## Fresh-agent trials

Both trials ran in a subagent with a fresh context, the 22 packages readable
as installed skills, no Google product skill installed, no credentials and no
network. Neither was given the expected answers.

### Engineer: a ticket naming two uninstalled product skills

Fixture: a synthetic ADK project (tools, agent, FastAPI health route,
Dockerfile, pinned requirements, three-contract design, plan, and ticket G04
"deploy privately on Cloud Run behind the existing load balancer" with
`supporting_skills` naming `google/skills:cloud-run-basics` and
`google/skills:iam-helper-for-policy-management`).

Observed: the agent opened with "Specialist: deploy-adk-on-google-cloud,
because ...", reported both product skills as not installed with the exact
`npx skills@latest add google/skills --skill <name>` command each, said the
specialist still decides what the service needs, and continued. It ran the
deploy inspector, fixed the Dockerfile per the validation reference, added a
health-route test (3 of 3 tests pass offline), wrote a deployment script that
refuses to run without an approved scope, planned `--ingress
internal-and-cloud-load-balancing --no-allow-unauthenticated` with the
dedicated service account, recorded the service creation, the two role
bindings and the Docker build as not run, and filled the Evidence section per
contract. It used the ingress facts the deploy skill had imported rather than
guessing the product skill's content, and labelled the two facts it could not
confirm as vendor guidance. It found two defects in the fixture's own design
(a contract that forbids the model-access role the agent needs; a server that
never mounts the agent) and proposed a follow-up ticket instead of widening
scope. Ease for the product-skill entries: **4 of 5**; the one cost was
reading two files for the two halves of the rule, so the entry skill now
states the whole rule in one sentence. Pre-existing gap noted, not changed
here: no status vocabulary is prescribed for a ticket.

### Designer: a one-pass production design

Request: a production warranty assistant on Cloud Run with an existing Cloud
SQL database and a return-request tool, two developers, six weeks, real
customer data, an organisation with a landing zone and an external load
balancer with IAP; one-pass draft, design only, then the plan. Google's
`finding-google-skills` router was readable but fetching was forbidden.

Observed: the agent wrote the design (contracts C1 to C11, decisions, grids,
open decisions) and a sixteen-goal phased plan. Product-skill lines appeared
on the goals whose routes need a product operated: foundation (`gcloud`,
`cloud-sql-basics`, `iam-helper-for-policy-management`), the CI gate
(`cloud-build-basics`), deployment (`cloud-run-basics`,
`google-cloud-global-frontend-configuration`,
`google-cloud-slo-alert-configuration`, `cloud-run-alert-configuration`),
budgets (`gcloud`), and phase 2 (traffic split, backups). It fetched and
installed nothing and kept this toolkit's specialist as primary on every
goal. Ease: **4 of 5**. Gaps it hit, fixed the same day: no mapping row for
Model Armor, Sensitive Data Protection or quotas (now a `gcloud` row with
the rule that the specialist supplies the settings); the Well-Architected
pillar skills were cited in a reference but absent from the handoff table
(now a row); rows listing several names with no distinguishing text (now one
row per trigger for the IAM helpers and the monitoring skills); and the
conflict between Google's router rule "never name a skill you have not seen
in the catalogue" and our dated table (the handoff now says the table is a
dated reference and the name is confirmed against the current catalogue when
the router is present). Pre-existing gaps it noted, not changed here: the
shape of a wait entry in the schedule block is shown only in the delivery
profiles reference, and the presentation-goal multiplier has no field in the
template. One clarification was added: a one-pass draft hands over
unreviewed and says so.

## Limits

Two trials, one host client, no real Google product skill installed, so the
path where the skill *is* present and its commands are proposed was not
exercised. The facts imported from Google's skills were checked against
documentation, not run. Google's catalogue changes weekly; the names in the
mapping are dated 21 October 2026.
