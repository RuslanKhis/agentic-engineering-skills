# Postmortem: <short title>

Copy to `docs/operations/claims-intake/postmortems/<YYYY-MM-DD>-<slug>.md`.
Pre-filled for the `claims-intake` agent (Cloud Run, `kestrel-claims-prod`, europe-west2). Items in angle brackets are filled per incident. Items marked `unverified` depend on things that do not exist in the repo yet (see the handover, sections 2 and 8).

Date: <incident date> · Authors: <roles, not names of those at fault> · Status: draft / reviewed by <reviewer outside the responding team> on <date> / actions complete
Plan or tracker incident record: <ID> · Severity: <Sev1 / Sev2 / Sev3, per the handover's severity table>

Blameless: describe systems, prompts, controls and decisions ("the instruction forbade payout promises but nothing checked the draft"), not people. Assume everyone acted well on what they knew. The review is not complete until someone outside the responding team has read it and every action item has an owner, a due date and a tracker link.

Write the review within <N> working days of resolution (Kestrel to set).

## When to write one (agreed triggers)

Write a review if any applies: user-visible degradation past the alert threshold; any rollback or on-call intervention; resolution slower than <target>; a monitoring failure (an alert that should have fired did not, or reached nobody); the agent made or implied a payout promise or an outside action it should not have; personal data of a policy holder or claimant, or a credential, appeared in an answer, log or trace; a sustained quality drop; harmful or discriminatory output reached a user; cost overran past the stop.

## Incident note

| Field | Value |
| --- | --- |
| Alert or report | <alert policy name, handler report, service desk ticket> |
| Trace ID | |
| Invocation ID | |
| Session ID | |
| Cloud Run revision, `google-adk` version, model ID, instruction version | <revision name>, 2.12.0, `gemini-2.5-flash` or its replacement, <commit> |
| Root-cause category | model / tool / dependency / infrastructure / telemetry / instruction / control gap |
| Fix | |
| Regression case ID | |

## Summary

<Two or three sentences: what happened, to whom, how it ended.>

## Impact

- **Affected invocations and users:** <count> invocations, <count> claims handlers, between <start UTC> and <end UTC>. Selected by the query below, not estimated.
- **Harm category** (one or more): wrong information acted on (for example a wrong cover answer used in a notice of loss) / unauthorised action / data exposure (policy holder or claimant data) / unsafe or discriminatory content / financial (for example a payout promised) / service only.
- **Harm severity and reach:** <what happened to people; did any effect reach claimants or anyone outside Kestrel; can it be undone, and was it>.
- **Contracts breached:** C1 never promise a payout; C2 cover statements come from `check_cover`; C3 no personal data in logs or traces (C2 and C3 are proposals until Kestrel accepts them; see the handover). <how each was breached>

### Affected-users queries

No analytics table exists today, so use the source that exists. Run the query, record the text, the count and the window in this section.

Request-level (Cloud Logging, project `kestrel-claims-prod`; works now, `unverified` until run):

```
resource.type="cloud_run_revision"
resource.labels.service_name="claims-intake"
timestamp>="<start>" AND timestamp<="<end>"
httpRequest.status>=500
```

Count distinct callers from the request logs' identity field, if the load balancer logs one; if not, state that users cannot be counted and report invocations only.

Session-level (needs a session store that survives restarts; `unverified: from the repo`, see handover section 2): list sessions with events in the window and, per session, `invocation_summary.py --session <export> --format json` from the adk-agent-observability skill for tool errors and model errors.

Once a BigQuery analytics table exists (adk-agent-observability, BigQuery Agent Analytics), replace the above with: `SELECT COUNT(DISTINCT session_id), COUNT(DISTINCT invocation_id) FROM <dataset>.agent_events WHERE timestamp BETWEEN <start> AND <end> AND <condition>`. Column names depend on the table version; check the schema before using this text.

Content-based harms (a payout promise, a wrong cover answer) cannot be found from status codes. State the selection rule used (for example, drafts containing "will pay" or "you will receive") and its limits, and say how many sessions were read by a person.

## Notification decision

The controller decides; this review records the decision and never makes it. Kestrel is the controller and Brightlane (agency) is, while it operates the agent, a processor. Confirm both roles against the contract.

| Question | Answer |
| --- | --- |
| Personal data involved? | |
| Risk to people likely? High? | |
| Who decided, when | <Kestrel DPO or named role, date and time> |
| Regulator notified? | <ICO (UK), yes with date / no with reasoning> (UK GDPR: without undue delay, within 72 hours where feasible, when a risk to people is likely; record every breach even if not reported) |
| Individuals informed? | <yes, how / no, reasoning> (when the risk is high) |
| Processor told the controller? | <date> (Article 33(2): without undue delay; check the contract's own period) |
| Other duties | <financial services regulator, contract terms with claimants or reinsurers; the DPO names them. A payout promise may also raise a conduct or complaints-handling duty.> |

Kestrel's regulator, DPO contact and any sector regulator duties are not in the repo; Kestrel to fill them once here and keep them current.

## Root causes

<Contributing causes, and why the controls did not stop it. Name the layer: instruction, tool, model, deployment, alerting, access.>

## Trigger

## Resolution

<What stopped the harm, what restored service, who approved any action with outside effects.>

## Detection

<How it was found; how long after it started; would an alert have caught it sooner; did the monitoring work. Include whether the alert reached a Kestrel channel.>

## Regression case

- Case ID and file: <evalset path, case ID>, converted with `events_to_eval_set.py` from the saved session and reviewed for redaction (the case must not contain policy holder data)
- `fail_to_pass`: <tests reproducing the defect>
- `pass_to_pass`: <neighbouring tests the fix could break; at least the `tests/test_policy.py` cases>
- Base-commit run: <fails as expected, date> · Fix run: <passes, date>
- No evaluation set exists yet, so the first incident review also creates it (hand over to adk-agent-evaluation).

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

Links: traces, dashboards, the redacted session export, alert policy, Cloud Run revision, related contracts. Do not paste personal data or secret values.
