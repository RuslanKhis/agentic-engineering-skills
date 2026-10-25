# Postmortem: <short title>

Date: <incident date> · Authors: <roles> · Status: draft / reviewed by
<reviewer outside the responding team> on <date> / actions complete
Plan incident record: I<n> · Severity: <Sev n>

Blameless: describe systems, prompts, controls and decisions; assume people
acted well on what they knew.

## Incident note

| Field | Value |
| --- | --- |
| Alert or report | <alert policy, feedback record, service desk ticket> |
| Trace ID | |
| Invocation ID | |
| Session ID | |
| Build, model and prompt version | |
| Root-cause category | model / tool / dependency / infrastructure / telemetry / instruction / control gap |
| Fix | |
| Regression case ID | |

## Summary

<two or three sentences: what happened, to whom, how it ended>

## Impact

- **Affected invocations and users:** <count> invocations, <count> users,
  between <start> and <end>; selected by: `<query against agent_events or the
  session store>`
- **Harm category:** wrong information acted on / unauthorised action / data
  exposure / unsafe or discriminatory content / financial / service only
- **Harm severity and reach:** <what happened to people; did any effect reach
  people outside the organisation; can it be undone, and was it>
- **Contracts breached:** C<n> <how>

## Notification decision

| Question | Answer |
| --- | --- |
| Personal data involved? | |
| Risk to people likely? High? | |
| Who decided, when | <controller's DPO or role, date and time> |
| Regulator notified? | <authority, yes with date / no with reasoning> (UK ICO, or the EU lead supervisory authority under GDPR Art. 33: without undue delay, within 72 hours where feasible, when a risk is likely) |
| Individuals informed? | <yes, how / no, reasoning> (when the risk is high) |
| Processor told the controller? | <date> (GDPR Art. 33(2): without undue delay; verify the contract's period) |
| Other duties (sector regulator, contract, AI Act for high-risk systems) | |

## Root causes

<contributing causes; why the controls did not stop it>

## Trigger

## Resolution

## Detection

<how it was found; how long after it started; would an alert have caught it
sooner; did the monitoring work>

## Regression case

- Case ID and file: <evalset path, case ID>, converted with
  `events_to_eval_set.py` and reviewed for redaction
- `fail_to_pass`: <tests reproducing the defect>
- `pass_to_pass`: <neighbouring tests the fix could break>
- Base-commit run: <fails as expected, date> · Fix run: <passes, date>

## Action items

| Action | Kind (prevent / detect / mitigate) | Owner | Due | Tracker |
| --- | --- | --- | --- | --- |

## Lessons learned

### What went well

### What went wrong

### Where we got lucky

## Timeline

| Time (UTC) | Event |
| --- | --- |

## Supporting information

Links: traces, dashboards, the session export (redacted), related contracts
and plan goals.
