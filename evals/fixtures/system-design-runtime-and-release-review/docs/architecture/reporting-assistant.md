# Proposal: reporting assistant runtime

Author: Kai Moreno (platform team), 2026-10-12. Status: proposed, awaiting design review.

The reporting assistant lets customers of our analytics product ask questions in chat; the agent
runs report tools (`run_report`, `chart_series`, `export_report`) against their workspace and
streams the answer. Customers can download a full export of any report. The stack is accepted:
React SPA, OIDC sign-in, PostgreSQL, Python google-adk on Cloud Run.

## Runtime

- **Replicas.** Three Cloud Run instances behind the load balancer, no session affinity.
- **Sessions.** `DatabaseSessionService` on PostgreSQL stores every conversation event. To keep
  prompts small, the agent sends only the last 20 events of a session to the model. Customers who
  ask us to delete their history are told this "history deletion" already happens because older
  events never reach the model.
- **Streaming.** The browser opens an SSE stream per message. The server forwards ADK events as they
  arrive. The UI shows the run as successful as soon as any event marked final response arrives.
- **Tool results.** The UI pairs each tool call with its result by tool name so it can show "running
  run_report... done".
- **Reconnect.** If the SSE connection drops, the client re-sends the customer's last message on a new
  connection so the answer is not lost.
- **Exports.** `export_report` writes the CSV to `/tmp` on the instance that ran the tool and returns
  a download path `/downloads/<file>`; the download route serves it from the local disk.
- **Concurrency.** A per-process `asyncio.Lock` per session id stops two runs of one session at once.
- **Capacity.** Each run reserves one warehouse query slot (our warehouse allows 50 concurrent
  queries per tenant). The reservation is released when the browser disconnects, so abandoned
  tabs do not hold slots.

## Release

We will move from google-adk 2.11 to 2.12 next month. The session table's storage format changes in
2.12. The plan is a gradual rollout: one new instance at a time over a day, old and new instances
serving traffic together.

## What we want from the review

The key decisions and what we will test. We are not changing the stack and not building anything
yet.
