# Design review: reporting assistant runtime (draft)

Reviews `docs/architecture/reporting-assistant.md` (Kai Moreno, 2026-10-12). Design review only: nothing built, installed, deployed or contacted. Stack unchanged (React, OIDC, PostgreSQL, google-adk on Cloud Run). Status: **draft**, provisional where assumptions below apply.

## Verdict

The proposal does not yet meet the four customer needs. Each of the four fails at least once, and the upgrade plan as written can corrupt live sessions. Nine findings below; F1, F4, F5, F9 are blockers.

## Assumed answers (nobody to ask in this session)

| # | Question I would have asked | Assumed answer | Decisions depending on it |
|---|---|---|---|
| Q1 | Profile? | Production, external customers, real tenant data | all; floor controls kept |
| Q2 | Is an object store (GCS) acceptable for exports? It is not in the "accepted" list. | Yes, as the same GCP project's storage. If no: PostgreSQL large objects, same contracts | F4 |
| Q3 | Is there a legal or contractual deletion promise (retention period, backups)? | Customers have been told history is deleted; true deletion is required | F1 |
| Q4 | Is 2.12's session-format change backward-readable by 2.11? | **Unknown; assumed no** (worst case). Needs release notes and a rehearsal | F9 |
| Q5 | Is a short maintenance window acceptable for the upgrade? | Yes, off-peak, a few minutes | F9 |
| Q6 | Do analysts ever need the same session open in two tabs? | Yes, possible; second send is rejected or queued, not run in parallel | F6 |
| Q7 | Is the warehouse's 50-query limit shared with other tenant workloads? | Yes, so we may use only a share of it | F7 |

## Journey used for checks

A customer asks "revenue by region for Q3, and export it". The agent calls `run_report`, `chart_series`, `export_report`. The customer's laptop sleeps mid-run, they reconnect on another instance, and expect progress, a true result and the full CSV.

## Contracts

| ID | Contract (invariant) | Enforcement | Verdict |
|---|---|---|---|
| C1 | A customer can read, resume, download or delete only their own sessions and exports | Server derives tenant and user from the verified OIDC token; every session, run and download query filters on it; the model never supplies them | Gap: download route takes only a filename |
| C2 | After a deletion request completes, no events, exports or derived copies of that history remain, apart from a stated backup retention | Delete job over session rows, export objects, logs and caches, with a completion record | Gap: nothing deletes anything |
| C3 | Progress shown is true: each tool call shows its own state, and the run is shown successful only if the whole run ended cleanly | Stable call ids; run state held in a durable run record | Gap |
| C4 | A reconnect never starts a second run | Client-generated run id, unique in PostgreSQL; reconnect only observes | Violated by resend |
| C5 | An export offered for download is complete and stays downloadable for its stated lifetime from any instance | Export written to shared storage, row count and checksum verified before the UI says done | Violated by `/tmp` |
| C6 | At most one active run per session across all instances | Database-level constraint plus lease | Violated by per-process lock |
| C7 | Warehouse slots in use by us never exceed our share of 50 per tenant | Counted reservation released on query end or confirmed cancel | Violated by release on disconnect |
| C8 | An upgrade never makes a stored session unreadable or lost, and can be rolled back | Rehearsed migration, version gate | Gap |

## Findings and decisions

**F1. "History deletion" is false (C1, C2, blocker).** `DatabaseSessionService` keeps every event; sending only the last 20 limits what the model reads, not what is stored. Telling customers it is deletion is a misstatement and a privacy risk. Decision: stop using that wording now. Build a real deletion path (session rows, exports, run records, logs/traces, any caches), with a deletion receipt and a documented backup-expiry window. Keep the 20-event window, but call it context trimming. Tradeoff: the 20-event cut can also split a tool call from its result or drop the facts the report depends on; trim on complete exchanges and keep the active report's parameters in state.

**F2. Isolation is not specified (C1).** Nothing says how tenant and user reach the tools. Decision: scope comes from the verified OIDC subject and tenant claim, passed to tools as trusted context; `run_report` cannot take a workspace argument from the model. Same check on the history, stream and download routes. Verify with a two-tenant test across every route, including a guessed session or file id.

**F3. Success is inferred from the wrong signal (C3).** A "final response" event is not run success: a later tool failure, a truncated export, or a stream that dies after it would still read as done. Decision: the server writes a run record (`running`, `succeeded`, `failed`, `cancelled`) and the UI shows the server's state. "Succeeded" requires the export check in F4. Partial answers are labelled partial.

**F4. Downloads break across instances (C5, blocker).** `/tmp` is per instance and lost on restart or scale-down; with three instances and no affinity, most downloads after a reconnect return 404, and a path is not an access grant. Decision: write exports to shared durable storage (assumption Q2), keyed by tenant and run id, with an owner check on every download, a short-lived download link or a proxied route, and an expiry. Verify the row count and checksum before reporting success. Tradeoff: one more component (or PostgreSQL large objects if Q2 is no, at DB size cost).

**F5. Reconnect resends the message (C4, blocker).** A resend on a new connection starts a second run: duplicate warehouse slots, a second export, a doubled conversation. Decision: reconnect is observation. The client holds a run id and last event id; the server replays stored events after that id from the run record and attaches to the running work. Only an explicit user "retry" creates a new run with a new id. Because the run must survive a dropped connection, execution cannot be tied to the SSE request; the tool run needs to continue (bounded by a deadline) and write to the record.

**F6. The lock is per process (C6).** Three instances do not share an `asyncio.Lock`. Decision: a unique "one active run per session" row in PostgreSQL with a lease, heartbeat and fencing version, so a stale owner cannot commit. Policy: the second send while a run is active is rejected with a clear message (assumption Q6).

**F7. Capacity is freed too early (C7).** Releasing the slot on browser disconnect, while the warehouse query may keep running, lets us exceed 50 and starve other work; it also contradicts F5, since reconnect resumes the same run. Decision: reserve per tenant in PostgreSQL; release on query completion, on confirmed cancel, or on lease expiry. Abandoned runs are cancelled after a deadline (cancel the warehouse query, then release). Give each tenant a share of 50 and a queue or "busy" message. Count retries and fan-out in the same allowance.

**F8. Tool results are paired by name (C3).** Two `run_report` calls in one turn are indistinguishable. Decision: pair by call id from the ADK function call and response events; test with two simultaneous calls to the same tool. Also test that SSE actually delivers incrementally through the load balancer and Cloud Run (an open connection is not proof), and decide request timeout, heartbeat and slow-client limits.

**F9. The upgrade plan is unsafe (C8, blocker).** The session table format changes in 2.12, yet old and new instances share one database and run together for a day. Either old instances misread or fail on new rows, or new instances migrate under them. Decision: treat it as a schema migration. (a) Read the 2.12 migration notes first; (b) rehearse on a copy of production data: migrate, run both versions, roll back; (c) unless 2.12 is proven readable by 2.11, do a short drain-and-switch (stop new runs, let active ones finish within a bound, back up, migrate, start 2.12 only) instead of a mixed rollout; (d) define the rollback up front, since a migrated table may not go back to 2.11 without a restore; (e) the release moves as one unit (image, prompts, tool schemas) with candidate thresholds decided before traffic. Pin 2.11 until the rehearsal passes. Tradeoff: minutes of downtime versus a day of mixed-version risk.

## Test plan

| Check | Contract | Expected |
|---|---|---|
| Two tenants, every route (history, stream, download, delete), guessed ids | C1 | 403/404, no data |
| Delete a session with exports; inspect DB, storage, logs | C2 | All gone; receipt recorded; backups noted |
| Drop the connection mid-run, reconnect on a different instance | C4, C5 | Same run id, one warehouse query, events replayed without gaps, no duplicate |
| Kill the instance running the tool mid-export | C3, C5 | Run shows failed or resumes, never "done" |
| Download after the exporting instance is restarted | C5 | Full file, row count and checksum match |
| Tool error after the final-response event | C3 | UI shows failed/partial |
| Two parallel `run_report` calls | C3 | Each card shows its own result |
| Two sends to one session from two instances | C6 | One runs, one rejected |
| 60 concurrent runs for a tenant; close tabs | C7 | Never above our share; slots return after queries end |
| Context trim at 20 events with a tool call at the boundary | F1 | Pairs intact, report parameters kept |
| Migration rehearsal: 2.11 and 2.12 side by side, then rollback | C8 | Pass, or the drain-and-switch is the chosen plan |
| SSE through the real load balancer | F8 | Events arrive incrementally, heartbeat holds, timeout handled |

## Unresolved, needing an owner

1. Q4: does 2.11 read 2.12 sessions? Settled by release notes and the rehearsal (platform team).
2. Q3: the deletion promise, backup retention and what customers were told (product and legal; also decide whether to correct earlier statements).
3. Q2: storage choice for exports (platform).
4. Per-tenant share of the 50 queries and the export lifetime (product).

## Not done

No code, infrastructure, dependency or network action. I did not check the 2.12 release notes or ADK APIs (no network); ADK behaviour above is from the proposal and general knowledge, so confirm each against the pinned versions. No independent plan review was run; this draft is unreviewed. No implementation plan, tickets or schedule were written, since you asked only for key decisions and tests.
