# Rollout pack: <assistant name>

Go-live: <date> · Hypercare: <start> to <end> · Release: <build tag>
Assigned population: <N users, teams>
Built from: design <path> (contracts), plan <path> (evidence, go-live
goals), discovery brief <path> (workflow, people plan, counter-metric),
operations handover <path> (support tiers)

## 0. Assumptions and gaps

| Item | Assumption or gap | What depends on it | Who settles it |
| --- | --- | --- | --- |
| A1 | <assumed go-live date and why> | <dates below> | <decider> |
| G1 | <missing input, e.g. no handover document> | <support routes> | <role> |

## 1. What it will and will not do

Each statement cites the contract that enforces it. A statement with no
contract is left out or raised with the designer as a gap.

| Statement for users | Contract |
| --- | --- |
| Will: <task in the user's words> | C1 |
| Won't: <what it never does> | C2 |
| Hands over: <when a person steps in, and to whom> | C3 |

Known limits (from deferred controls and gaps): <one line each>.

## 2. User guide

### Getting started

### Asking well

<two or three examples from the real workflow>

### Checking its answers

<what a source looks like; what to verify before acting; you remain
responsible for what you send>

### When it hands over to a person

### Reporting a problem

<the in-product control; the service desk for harm, a wrong action or
exposed data>

### Your data

<what not to paste; what is stored, how long, who can see it>

How well it works (only from measurement records): <"In testing on <n>
<cases> agreed with <role>, <k> were <result> (<month year>, M<n>)." or
"not yet measured">

## 3. Quick-reference card

One page: three will, three won't, how to check, how to report, who to call.

## 4. Training plan

| Session | Audience | Minutes | Objectives | Practice on | Trainer | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Managers and champions | <team leads, n> | 60 | <coach the first week; answer the top questions> | <their team's real tasks> | <role> | <YYYY-MM-DD> |
| Users | <team, n> | 90 | <use, check, hand over, report> | <own tasks> | <champion> | <YYYY-MM-DD> |

Attendance is recorded (AI literacy, EU AI Act Article 4).

## 5. Rollout messages

### Sponsor

Briefing to the sponsor (from <role>, <date>): <why now, measure,
counter-metric, success at hypercare exit, their visible action>

Announcement the sponsor sends (sender: <sponsor>, <date>, <channel>):

<message>

### Middle managers

Sender: <role> · Date: <date> · Channel: <channel>

<message>

### Frontline users

Sender: <role> · Date: <date> · Channel: <channel>

<message>

## 6. AI disclosure

Status: applies / not legally required: <reason> / verify
Text: "<exact words shown to users>"
Shown: <first screen before the first message; about page; voice greeting>

## 7. Adoption metrics

| Metric | Definition | Source | Target | Window |
| --- | --- | --- | --- | --- |
| Active user | <distinct user_id with at least 1 completed invocation> | <analytics table> | <n% of assigned> | <7 days rolling> |
| Weekly active rate | <active users ÷ assigned population> | | | |
| Outcome measure | <the brief's measure> | | | |
| Counter-metric | <the brief's counter-metric and threshold> | | | |
| Negative feedback share | <negative ÷ rated invocations> | <feedback table> | | |

Figures reported go into the plan as measurement records (M<n>).

## 8. Feedback channel

| User action | Record category | Route | Owner | Response |
| --- | --- | --- | --- | --- |
| Wrong or made-up answer | wrong_answer | <POST /feedback → sink → feedback table> | <role> | <weekly triage> |
| Could not do the task | tool_failed | | | |
| Too slow | too_slow | | | |
| Unsafe or inappropriate | unsafe | <also service desk, incident> | | |
| Something else | other | | | |

## 9. Hypercare exit test

Agreed with <sponsor> on <YYYY-MM-DD> (or `Status: proposed` until agreed; list it under gaps).

| Criterion | Threshold | Window | Source | Owner |
| --- | --- | --- | --- | --- |
| Severity 1 or 2 incidents open | 0 | 10 consecutive working days | <incident log> | <role> |
| Weekly active rate | ≥ <n>% of assigned | last 2 weeks | <analytics> | <role> |
| Counter-metric | ≤ <threshold> | last 4 weeks | <source> | <role> |
| Negative feedback share | ≤ <n>% of rated invocations | last 2 weeks | <feedback table> | <role> |
| Tickets resolved by client tiers | ≥ <n>% | last 2 weeks | <service desk> | <role> |
| Operations handover acceptance | passed | at exit | <handover document> | <role> |

If the test fails on <end date>: <extend by n weeks with the named fix / rollback decision by decider>.
