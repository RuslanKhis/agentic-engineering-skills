# Operations handover and agent incident review

Read when an ADK agent built by one team (often an agency) is to be run by
another (the client's IT team, a platform team), or when an incident needs
a written review beyond the incident note in the
[debugging runbook](debugging-runbook.md#5-close-the-loop). The handover
decides who owns each signal, alert, credential and recurring task after the
builders leave; the commands that grant a role, move a secret or relink a
billing account belong to `deploy-adk-on-google-cloud` and
`adk-tool-auth-and-secrets`, and the Google product skills they name.

The structure follows Google's SRE book: the launch coordination checklist
(Appendix E: monitoring including "monitoring the monitoring", alert
management, a defined release process, graceful degradation of external
dependencies, standard operating procedures) and postmortem culture
(chapter 15, John Lunney and Sue Lueder: triggers agreed in advance,
blameless review, "an unreviewed postmortem might as well never have
existed"), read 25 October 2026.

## What makes an agent handover different

A service handover transfers uptime. An agent handover also transfers
quality: the service can be healthy while the agent answers wrongly, takes
an unapproved action, or drifts after a provider changes the model. So the
receiving team needs, beyond a runbook:

- the contracts and their evidence (what it must never do, and how that is
  checked), not only the architecture;
- owners for the recurring quality tasks: evaluation-set refresh from
  production samples (`adk-release-engineering`), judge and model migration
  before a retirement date, cost review against the cost contract;
- the model-retirement calendar for the pinned model and judge, copied from
  `adk-model-and-output-contracts`' dated lifecycle table
  (`assets/model-lifecycle-*.json`) with the date it was read; the table is
  refreshed from the provider's pages, never from memory. Use the date for
  the platform actually serving the model (`vertex_retirement` on Vertex AI,
  `shutdown` on the Gemini API). Without web access, copy the table's dates
  with its `checked_on` date and mark them `refresh before relying`; a
  retirement inside the engagement or hypercare is a blocker, not a note;
- a route for quality complaints (the feedback channel in
  [feedback capture](feedback-capture.md)) as well as outages.

## Write the handover document

Write `docs/operations/<topic>/handover.md` from the
[handover template](../assets/handover-template.md). Fill it from what
exists: the design's contracts and deferred controls, the plan's resources
and cost contract, the alert policies and dashboards actually deployed, the
secrets and service accounts actually present (names only, never values).
Mark anything planned but not deployed as such.

### Support tiers and RACI

Default three tiers, adjusted to the client:

| Tier | Who | Handles |
| --- | --- | --- |
| 1 | Client service desk | User reports, the "report a problem" route, known-issue answers from the user guide, triage by the severity table |
| 2 | Client IT or platform team | Alerts, restarts and rollbacks by runbook, access and quota requests, cost alerts, first look at quality complaints |
| 3 | Agency (during hypercare or under a support contract) or the client's own ADK engineers | Code, prompt, tool and model changes; incident root cause; evaluation re-runs |

Write one RACI row per recurring activity (incident response by severity,
release and rollback, model migration, evaluation-set refresh, cost review,
access review, feedback triage, postmortem). Each row has exactly one
Accountable person or role; a row with none or two is the gap the
handover exists to close. Name the date tier 3 moves from the agency to
the client, usually the hypercare exit.

### Alert ownership

List every alert policy actually deployed (or, without project access,
those the design names, marked `unverified: from the design`): name, condition, severity,
notification channel, owning tier, runbook entry. An alert whose channel
reaches nobody after handover (an agency mailing list, a builder's phone)
is moved before go-live. Include the alert that tells someone telemetry
itself stopped arriving.

### Transfer of access

One row per credential or grant: IAM roles on the project, service accounts
and their keys (prefer none: workload identity), Secret Manager secrets and
their rotation owner, OAuth clients and their consent screen, the billing
account link and budget alerts, the source repository, CI secrets, the
domain and certificate, the model provider account if not Vertex AI. Each
row records from whom, to whom, the date, how it is verified (the new owner
performs the action once; `gcloud projects get-iam-policy` shows the grant)
and when the agency's access is removed and verified absent. The agency
keeps no standing access after the transfer date unless the support
contract says so, with an expiry.

### Runbook entries

One entry per alert and per routine task: symptom, first check, the
[debugging runbook](debugging-runbook.md) step that applies, safe actions
tier 2 may take (roll back to the previous release, disable a tool by
configuration, switch to the fallback model, turn off a feature flag), when
to escalate, and who must approve an action with outside effects. Each
entry is rehearsed once by tier 2 before hypercare exit; record the date.

### Known limits and hypercare exit

Copy the design's deferred controls and open gaps as known limits, each with
its trigger. The operations exit criteria join the rollout pack's hypercare
exit test (`adk-presenter`); when no rollout pack exists yet, list it as a
blocker with the rollout goal that owns it. The exit criteria are: every RACI row has one accountable owner,
every alert routes to a client channel, every access row is verified on both
sides, every runbook entry is rehearsed, and the model-retirement calendar
and cost review have owners and dates.

## Agent incident review (blameless postmortem)

Agree the triggers before go-live and write them in the handover. Beyond
the SRE book's (user-visible degradation past a threshold, data loss, an
on-call intervention such as a rollback, resolution time past a threshold,
a monitoring failure), an agent adds:

- an action with outside effect that the contracts forbid or that lacked
  approval;
- exposure of personal data or credentials in an answer, a log or a trace;
- a sustained quality drop (an Online Monitor or feedback share past its
  threshold for a window), even with the service up;
- harmful, discriminatory or unsafe output reaching a user;
- a cost overrun that the cost contract's stop did not stop.

Asked for "the postmortem template", write a project copy to
`docs/operations/<topic>/postmortem-template.md`, pre-filled with this
agent's contracts, harm categories from the brief, the affected-users query
against its own analytics table, and the notification route (controller,
supervisory authority); write a review of a past incident only when asked.
Write each review from the [postmortem template](../assets/agent-postmortem-template.md)
to `docs/operations/<topic>/postmortems/<date>-<slug>.md`. It starts from
the incident note's fields and adds:

- **Affected users and invocations** by query, not estimate: the BigQuery
  or session query that selected them, the count, and the window.
- **Harm assessment:** category (wrong information acted on, unauthorised
  action, data exposure, unsafe content, financial), severity, whether any
  effect reached people outside, and whether it can be undone.
- **Notification decision:** who decided and when. For a personal data
  breach, the controller decides: the UK ICO's guide says to notify the
  regulator without undue delay and, where feasible, within 72 hours when a
  risk to people is likely, to tell individuals directly when the risk is
  high, and to record every breach with the reasoning when not reporting.
  For EU data subjects the same duty runs to the controller's lead
  supervisory authority under the EU GDPR (Article 33; for example Ireland's
  Data Protection Commission for an Irish establishment; verify on
  EUR-Lex). Sector regulators (financial services, health) may add their own
  deadlines; the controller's DPO names them. An agency acting as processor tells the controller without undue delay (GDPR
  Article 33(2); verify against the contract's own notice period). The EU AI
  Act's serious-incident reporting applies to high-risk systems only. The
  review records the decision; it never makes it on the client's behalf.
- **Regression case:** the evaluation case added from the session, with its
  `fail_to_pass` and `pass_to_pass` lists and the base and fix runs
  (`adk-agent-evaluation`, incident regressions), converted with redaction
  by `events_to_eval_set.py`, and its case ID.
- **Plan record:** the incident record `I<n>` in the plan (date, severity,
  effect, response, fix) so the results review can cite it.

Blameless means the review names systems, prompts, controls and decisions,
not people at fault: "the approval gate checked the draft, not the
recipient list" rather than "the engineer forgot". Action items each have
an owner, a due date and a tracker link. The review is not complete until
someone outside the responding team has reviewed it and its action items
are tracked.
