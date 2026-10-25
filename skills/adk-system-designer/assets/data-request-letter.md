# Data and access request: <engagement name>

To: <client role, e.g. data owner or IT lead> · From: <supplier role>
Date: <date> · Statement of work: <path, version>, dependencies CD<n>

To start <goal IDs> on <date>, we need the items below. Each lists what we
will do with it and what we will not. Please tell us if a smaller scope or
synthetic data would do; we will use the least that meets the purpose.

## Data

| Item | Purpose (goal) | Minimum scope | Format and route | Personal data? | Retention and deletion | Approver | Needed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <claims export> | <G02 retrieval test> | <last 6 months, closed claims, no free-text notes> | <CSV via shared bucket in the client's project> | <yes: names, policy numbers; pseudonymised by the client before transfer?> | <deleted at teardown G0n or on request; evidence of deletion provided> | <DPO / data owner> | <date> |

We will not use this data to train or improve any model, copy it outside
the agreed location, or keep it after the engagement unless you instruct
us in writing.

## Access

| Grant | Principal | Scope and role | Why | Expires or reviewed | Approver | Needed by |
| --- | --- | --- | --- | --- | --- | --- |
| <GCP project with billing linked> | <supplier engineers' group> | <project-level roles listed> | <G04 deployment> | <end of engagement> | <client cloud admin> | <date> |
| <read access to the tracker API> | <service account> | <read only, one project> | <G03 tool> | <end of engagement> | <system owner> | <date> |

## People and decisions

| Need | Who | Hours or date |
| --- | --- | --- |
| Subject-matter experts to agree gold cases and judge output | <role> | <n hours per week from date> |
| Product owner for questions and acceptance | <role> | <named by date> |
| Review decisions (presentation goals) | <decider> | <dates> |

## Access checklist (supplier side, before first use)

- [ ] Each grant matches the row above, no broader; principals are groups or service accounts, not personal keys.
- [ ] No credential arrives by email or chat; secrets go to Secret Manager in the client's project.
- [ ] Data lands only in the agreed location; logging of content is off or redacted.
- [ ] Each item has a deletion step recorded in the teardown or handover goal.
- [ ] The DPO or data owner's approval is recorded with its date.
