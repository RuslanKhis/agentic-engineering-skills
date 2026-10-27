I reviewed the proposal and wrote the review to `docs/architecture/reporting-assistant-review.md`. As it stands, the design misses all four customer needs, and the upgrade plan could corrupt live sessions. Four findings block approval. No code was built, nothing was installed or deployed, and I made no network calls.

**Blockers**
- **Privacy (F1):** The proposal's "history deletion" claim is false. ADK stores every event; the 20-event cap only limits what the model reads. I'd stop using that wording now and build real deletion, covering sessions, exports, run records and logs, with a backup-retention note. I'd also keep tool call/result pairs intact when trimming, since the 20-event cap can split them.
- **Downloads (F4):** Exports are written to `/tmp` on one instance, and there is no session affinity. Downloads after a reconnect would mostly 404, and the download route takes only a filename, so it has no owner check. I'd move exports to shared durable storage, check the owner on every download, and verify row count and checksum before showing "done".
- **Reconnect (F5):** Re-sending the last message starts a second run, which means a duplicate export and a second slot held. I'd have the client send a run id and make reconnect replay stored events and attach to the existing run. That needs a durable run record in PostgreSQL.
- **Upgrade (F9):** Mixed 2.11/2.12 instances share one database whose session format changes. I'd keep 2.11 pinned until a rehearsal on a copy of production data passes. Unless 2.11 can read 2.12 sessions, do a short drain-and-switch with a backup and a defined rollback.

**Other findings**
- Success must come from the server's run state, not from the "final response" event (F3).
- Tool results need pairing by call id, not tool name (F8).
- The per-process lock should become a database-level one-active-run-per-session rule with a lease (F6).
- Warehouse slots should be released when the query ends, not when the browser disconnects (F7).
- Tenant scope must come from the verified OIDC token on every route (F2).

The review also holds the contracts table and a 12-row test plan.

**Questions nobody could answer, and what I assumed**
- Does 2.11 read 2.12 sessions? I assumed no.
- Is GCS acceptable for exports? I assumed yes; the fallback is PostgreSQL large objects.
- Is a short maintenance window acceptable? I assumed yes.
- Do customers have a deletion promise? I assumed yes.
- Is the 50-query warehouse limit shared with other tenant workloads? I assumed yes.
- Do customers ever use two tabs on one session? I assumed they might, so a second send gets rejected.

**Left undone**
- I did not check the 2.12 release notes or the ADK APIs, so every ADK-specific point needs confirming against the pinned versions.
- I wrote no implementation plan, tickets or schedule.
- I ran no independent plan review, so the draft is unreviewed.