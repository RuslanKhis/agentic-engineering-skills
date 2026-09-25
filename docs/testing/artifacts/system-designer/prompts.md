# System designer trial inputs — 25 September 2026

These are synthetic requests supplied to independent Codex subagents with the
new skill path and access to its bundled references. The executing agents were
not given the evaluator's expected outcomes, activation labels or source analysis.
They were told to write only documentation in temporary directories, without
cloud changes, application implementation, paid calls or real-user question prompts.
Public documentation lookup was allowed. These are explicit-invocation trials.

## Conversation — first request

I want to build a customer-support agent with Google ADK on GCP. It should
answer questions about customer cases and create escalations. Can you help me
work out the architecture before we code? I am not sure which services I need.

## Conversation — answer to the agent's questions

Customers only. We already have a React app, OIDC login and a PostgreSQL database
containing case ownership and case history. Escalations go to our existing
ticketing API after the customer confirms the exact request. That API has a
create endpoint and lets us search tickets by our own request reference, but
we have not checked whether it deduplicates requests. We want a small first
release, probably 20 concurrent customers, and aim for the first useful answer
within 5 seconds. We have not measured that. Keep cloud costs around $100/month
during the pilot; our team of two already runs services on Cloud Run. Please
produce a first design with explicit assumptions for anything still open,
and no code yet.

## Review — request and supplied proposal

Review the following proposed ADK/GCP architecture and give me a revised one-pass
design. I cannot answer questions today; list assumptions. Keep our React frontend,
existing OIDC login and PostgreSQL database. No coding or deployment.

Browser sends customer_id and session_id to a Cloud Run API. An ADK agent uses
one service account for all tools. A refund tool generates a new UUID for each
HTTP attempt and retries on every timeout. PostgreSQL stores session history so
we assume any failed operation can restart safely. A background coroutine writes
the completed refund receipt after responding to the browser. The UI shows
partial text as success when any final-response event arrives. Billing has a
monthly $100 alert so spending is capped. Peak traffic estimate is 30 requests/sec;
mean processing time 8 sec, two workers run with in-memory per-user locks.
Upstream policy is to delete stored preferences immediately on request; retries
may still be queued. Requirement: users see only their records, one confirmed
business refund must not duplicate, and do not claim cost or latency guarantees
without evidence.

## Interaction refinement

A third fresh subagent used the revised designer. The same documentation-only
constraints applied. It was asked to respond in the conversation, with output
saved verbatim to temporary Markdown files; no provider research was requested.

### First request

We are adding a Google ADK assistant to our lesson-planning application on GCP.
Teachers already use our React app, login and PostgreSQL database. They spend
too long assembling a plan from their own saved notes. They should be able to
ask for a draft, edit it in the app, and reopen it after the chat closes. For
the pilot each teacher works on their own plans. Please help me think through
the first architecture decision in a few short paragraphs. Don't write the
full design or code yet.

### Reply after the first response

Explicit Save draft is right for us. One correction to the pilot: teachers need
to share a saved plan with named colleagues and edit it together. A stale save
must not silently overwrite someone else's edits. Showing a conflict and
asking the editor to resolve it is acceptable for the first release. What
does that change?

## Runtime and release review

A fourth fresh subagent received the updated skill and this request, without
evaluation labels or expected outcomes. It could read the bundled references
and write its response to a temporary file. Application edits, installation,
external calls and cloud actions were excluded. Provider/version questions
could remain explicit verification tasks. The evaluation fixtures and prior
trial reports were not supplied to the executing agent.

Please review this first design for our Google ADK reporting assistant on GCP.
Keep our React UI, existing OIDC and PostgreSQL. We have three serving replicas.
Customers need private conversation continuity and full-result downloads after
reconnecting. We want incremental progress and a truthful outcome, even if a
later step fails. Our proposal keeps conversation events in PostgreSQL but
sends only the last 20 events to the model; we treat that as our history deletion
policy. Full exports go to the serving replica's temporary disk and chat returns
the path. The browser pairs tool results by tool name and marks success on the
first final-response event. Reconnect submits the message again. Each process
has its own per-session lock; browser disconnect releases its work reservation.
SDK upgrades will roll out gradually, including a planned change to session
storage format. Give a concise review with the most important design choices
and planned checks. No implementation or deployment.

## Practical implementation handoff

A fifth fresh subagent received the updated designer and this request. It could
read the skill and bundled resources and write documentation in a temporary
directory. It was not given grading expectations, evaluation fixtures or earlier
trial reports. No application implementation, installation, external calls,
tracker changes or real-user question prompts were permitted; unknown provider
and version facts could remain verification tasks.

We agreed to keep React, our OIDC login, PostgreSQL and Cloud Run for our Google
ADK support assistant. Users should explicitly save a response-language preference,
have it applied in later conversations and be able to forget it. We also want
streamed replies with a clear failed/interrupted state. Verified login supplies
our user ID. Only local development and tests are authorized; we have no cloud
credentials here and haven't chosen the ADK package version. Please produce the
design and a practical plan I can give to another coding-agent session. Include
a first useful implementation goal I can start locally. We may use Matt Pocock's
skills later. One unresolved question is whether a future group-account feature
will allow shared preferences, but individual preferences are the agreed pilot
scope. No coding yet.
