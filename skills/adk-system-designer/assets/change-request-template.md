# Change request CR<n>: <short title>

Status: draft / submitted <date> / approved <date> by <role> / rejected
Statement of work: <path, version> · Raised by: <role> · Trigger: <the
SOW §8 trigger or assumption that fired, or "new request">

## What changes and why

<two or three sentences: the request or event, and what the client gets>

## Changes by ID

Update the design and plan first, rerun `check_schedule.py`, then fill these
rows from the diff. Use `none` where nothing changes; mark goal IDs that do
not exist yet as `new`.

| Kind | IDs | Change |
| --- | --- | --- |
| Contracts | C3 (revised), C9 (new) | <one line each; the plan's change-table row> |
| Goals | G04 (re-estimated), G11 (new) | <what each now delivers> |
| Acceptance criteria | AC2 | <new threshold or cases> |
| Client dependencies | CD2 | <new date or owner> |
| Deliverables | DL1 | <scope change> |

## Estimate change

From the schedule check run `<command>` on <date>:

| | Before | After | Difference |
| --- | --- | --- | --- |
| Human hours | <low>-<high> | <low>-<high> | <low>-<high> |
| Fees at <rate per hour, supplied by the user> | | | |
| Run cost per month (estimate) | | | |
| Finish (working days) | | | |

## Effect if not approved

<what the current SOW still delivers, and any risk accepted>

## Approval

| Party | Name and role | Decision | Date |
| --- | --- | --- | --- |
