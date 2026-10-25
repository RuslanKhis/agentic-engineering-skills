# Rollout and adoption pack

Read when an agent is about to reach people other than its builders (a pilot
group, a department, customers) and the user asks for the rollout pack, a
user guide, training, launch messages, AI disclosure text or adoption
measures. The pack is documents for users and their managers, written from
the design's contracts and the plan's evidence. It is not a decision
presentation: there is no ask, but the same rule holds that nothing is
promised that the record does not support.

Read the record first, as for a deck (the presenter's first step). Settle
the go-live date against it: when a relative date ("in two weeks") falls
before evidence or a decision the record already holds, or the go-live
decision is not recorded, state the date you assume and why at the top of
the pack. The pack opens with an **Assumptions and gaps** table: each
assumption with what depends on it, and each missing input (no handover
document, no agreed exit thresholds, no recorded decision) with who settles
it.

## Read first

| Source | What the pack takes from it |
| --- | --- |
| Design contracts table (`C1` …) | What the agent will do, will not do, and when a person steps in; each user-facing statement cites its contract |
| Contracts' failure outcomes, deferred controls, open gaps | What users see when it cannot help; the known limits section |
| Discovery brief §4 and §6 | Workflow before and after, users and frequency, counter-metric, people plan, champions, decider and sponsor |
| Plan evidence (`M<n>` measurement records, acceptance results) | Any statement of how well it works, in the measured voice with sample and date; without a record, no accuracy claim |
| Plan goals | Go-live date, hypercare period, the operations handover goal and its support tiers |
| Observability feedback capture (`adk-agent-observability`, `references/feedback-capture.md`) | The feedback record and categories the "report a problem" control writes |

Write the pack to `docs/rollout/<topic>/rollout-pack.md` from the
[rollout pack template](../assets/rollout-pack-template.md); split out the
user guide and the quick-reference card for distribution only after the
pack passes the check.

## What it will and will not do

Turn contracts into user language, one row each, citing the contract:

- **Will:** the journeys the contracts support, in the user's task words
  ("finds the status of a claim from the claims system").
- **Won't:** what the contracts forbid or the design leaves out ("does not
  send anything to a customer; it drafts, you send").
- **Hands over:** when a person steps in, from approval and escalation
  contracts ("refund requests over £500 go to a team lead").

A statement no contract enforces is a hope, not a promise: leave it out or
take it to the designer as a gap. Known limits come from deferred controls
and gaps, stated plainly ("it does not see claims older than 2024").

## User guide and quick-reference card

Write for the task, not the feature list, in the second person, at the
reading level of the frontline audience:

1. Getting started: where it is, how to sign in, the first useful thing to try.
2. Asking well: two or three examples from the real workflow.
3. Checking its answers: what a citation or source looks like, what to
   verify before acting (figures, dates, eligibility), and that the user
   stays responsible for what they send.
4. When it hands over to a person, and what happens next.
5. Reporting a problem: the in-product control and the service desk route.
6. Your data: what not to paste, what is stored, for how long, who can see it.

How well it works goes in only from a measurement record, in the measured
voice: "In testing on 40 claims questions agreed with team leads, 36 answers
were fully correct (October 2026, M3)." Aim for calibrated trust: users who
check the right things, not users who trust everything.

The quick-reference card is one page: three will, three won't, how to check,
how to report, who to call.

## Training

- Train managers and champions first, so the first question a user asks
  their manager has an answer; Prosci's guidance treats managers as the
  people employees take their cue from.
- Practise on the users' own tasks, with the will/won't table and the
  checking steps, not a product tour.
- BCG's 2025 AI at Work survey (over 10,600 workers, 11 countries, press
  release 26 June 2025) found that people who received five or more hours
  of training were significantly more likely to become regular users, and
  only 25% of frontline workers said their leaders gave enough guidance on
  AI. This is a survey association, not a measured effect of your plan;
  use it to argue for training time, not to promise adoption.
- Record who was trained and when: providers and deployers must take
  measures to support their staff's AI literacy (EU AI Act Article 4, as
  amended, consolidated text of 27 July 2026), without having to guarantee
  any level.

## Rollout messages per audience

Write one message per audience, each with sender, send date and channel:

- **Sponsor:** two parts. A briefing to the sponsor: why now, the outcome
  measure and counter-metric in one line each, what success at the end of
  hypercare looks like, and the sponsor's own visible action (using it,
  mentioning it in their next team meeting). Then the short announcement
  the sponsor sends to everyone affected, in their voice.
- **Middle managers:** what changes for their team's workflow, what to do
  in the first week, how to coach, where to send problems, and which
  numbers they will see. State that adoption figures are reported for teams,
  not used to rank individuals, if that is the client's decision; ask, do
  not assume.
- **Frontline users:** what it does for them, what does not change, what it
  will not do, how to check and report, where training is. Address the
  fear directly when the brief records it. Tell them which tool is approved
  and what must not go into other AI tools: in the same BCG survey, 54% said
  they would use AI tools even if not authorised.

## AI disclosure

EU AI Act Article 50(1): a system intended to interact directly with people
is designed so they are informed they are interacting with an AI system,
unless that is obvious to a reasonably well-informed person; 50(5): clear
and distinguishable, at the latest at the first interaction, and accessible.
It has applied since 2 August 2026 (Article 113; not postponed by the
Digital Omnibus on AI; consolidated text of 27 July 2026 on the
Commission's AI Act Service Desk). The duty sits with the provider, the
party putting the system into service under its own name; the statement of
work's AI terms say who that is.

Set the pack's disclosure status to one of: `applies` (EU users or
EU-facing), `not legally required: <reason>` (still recommended), or
`verify` when the jurisdiction or role is unsettled. Give the exact text and
where it shows: the first screen before the first message, the about page,
and any channel where the agent speaks (a voice line says it first).
Example: "You are chatting with an AI assistant. It can make mistakes;
check figures and dates before acting. A person reviews anything it sends
outside the team."

For an internal staff tool, disclose anyway: the "obvious" exception is a
judgement a one-line label makes unnecessary. Article 50(2) separately
requires providers of systems that generate synthetic text to mark outputs
in a machine-readable way, with exceptions (for example an assistive
editing function); whether drafts a person edits and sends fall under it is
a question for counsel: mark it `verify` in the pack rather than deciding.

## Adoption metrics

Define before go-live, from data the agent already records:

| Metric | Definition (default; adjust to the brief's usage frequency) |
| --- | --- |
| Assigned population | Users given access, N, by team |
| Active user | A distinct opaque `user_id` with at least one completed invocation (a final response, not an error or an abandoned turn) in a rolling 7-day window; 28 days for monthly work |
| Weekly active rate | Active users ÷ assigned population |
| Activation | Share of assigned users with a first completed invocation within 14 days of access |
| Retention | Share of last week's active users active again this week |
| Depth | Completed tasks per active user per week |
| Outcome measure | The brief's measure, against its baseline |
| Counter-metric | The brief's counter-metric with its threshold; a rollout that pushes usage while this worsens is failing |
| Quality signal | Negative feedback share of rated invocations; hand-over rate |

Log-ins, messages and conversations are vanity counts: report them only in
an appendix. Source the figures from the analytics rows (`user_id`,
invocation completion) and the feedback table, and write each reported
figure into the plan as a measurement record so the results review can cite
it.

## Feedback channel

Do not invent a second channel. Map the in-product "report a problem"
control onto the feedback record defined in `adk-agent-observability`'s
feedback capture reference (keyed by `session_id` and `invocation_id`, with
a bounded score and a category):

| User sees | Record category |
| --- | --- |
| Wrong or made-up answer | `wrong_answer` |
| It could not do the task | `tool_failed` |
| Too slow | `too_slow` |
| Unsafe or inappropriate | `unsafe` |
| Something else | `other` |

Free text is optional and de-identified before storage. Anything involving
harm, a wrong action or exposed data goes to the service desk as an
incident, routed by the operations handover's support tiers, not only to
the feedback table. Promise users a response rhythm you can keep (weekly
"you said, we changed" notes during hypercare).

## Hypercare and its exit test

Hypercare is the period after go-live with extra support: daily triage of
feedback and incidents, a named agency contact, and a fixed end date. Agree
the exit test with the sponsor before go-live, as thresholds over a window,
for example:

| Criterion | Threshold | Window |
| --- | --- | --- |
| Severity 1 or 2 incidents open | 0 | 10 consecutive working days |
| Weekly active rate | ≥ the agreed share of the assigned population | last 2 weeks |
| Counter-metric | within the brief's threshold | last 4 weeks |
| Negative feedback share | ≤ the agreed share of rated invocations | last 2 weeks |
| Tickets resolved by the client's tiers without the agency | ≥ the agreed share | last 2 weeks |
| Operations handover acceptance | passed (handover document) | at exit |

Mark the table `Agreed with <sponsor> on <date>` once agreed; until then
`Status: proposed`, and list it under gaps. When no operations handover
exists yet, use the default tiers from `adk-agent-observability`'s
operations handover reference, mark them assumed, and list the handover as
a gap with its goal.

When the test fails at the end date, extend hypercare by a fixed period with
the named fix, or take the rollback decision to the decider; do not let
hypercare end silently.

## Check

```bash
python3 "$SKILL_DIR/scripts/check_rollout.py" --pack docs/rollout/<topic>/rollout-pack.md \
  [--design docs/architecture/<topic>.md]
```

Exit 0 means every will/won't/hands-over statement cites a contract (that
exists, with `--design`), there is at least one of each, the disclosure has a
status and text, "active user" is defined with a window and a counter-metric
is named, the feedback rows map to record categories with an owner, every
hypercare exit criterion has a numeric threshold and a window, all three
audiences have a message, and no template placeholders remain. It checks
structure and citations, not whether the writing is clear; read the guide
aloud to one frontline user before sending.
