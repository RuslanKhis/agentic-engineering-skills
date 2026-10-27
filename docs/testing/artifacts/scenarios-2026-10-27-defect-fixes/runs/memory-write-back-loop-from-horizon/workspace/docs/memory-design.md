# Memory write-back: design

Status: implemented and unit-tested offline against a fake backend; SDK-dependent code and everything live are **not run**.

## What is saved, and when

Only what an engineer explicitly asks the assistant to remember, one short line, in one of three topics:
`answer_style`, `kit`, `site_note` (a site note carries a site id and is stored as "At site NW-0522: ...").
Nothing is inferred from conversation and no whole session is ever sent (`add_session_to_memory` is ignored by the
governed service). Codes, passwords, 4+ digit runs, emails and URLs are refused (access arrangements live in
`get_site`, the owning record). Facts expire after `MEMORY_RETENTION_DAYS` (default 180).

Flow: `remember` tool stages a row in the ledger (durable, keyed by user + invocation + call id, so retries are
idempotent) -> `after_agent_callback` rechecks consent, claims the row, writes it to the backend with
`add_events_to_memory`, records `accepted` / `failed` / `indeterminate`. The reply to the engineer says "will be
saved"; only `list_my_memories` showing `accepted` means saved.

The Horizon recipe was reviewed (see `docs/memory-wishlist.md` ask) and **not adopted**: its background judge and
whole-session flush save things nobody asked to be saved, and its consolidation needs a live Memory Bank engine. Its
useful ideas are used: after-turn callback, delta writes, retry without blocking the reply.

## Who agreed

Opt-in, default off. Consent is a row per engineer (state, policy version, time, source). It is granted and withdrawn
through `fieldline.memory_admin` / the app settings screen, never through a model tool. Bumping `POLICY_VERSION`
makes old consent stale until re-granted. Consent is checked at stage, at write claim, and at recall.

## See, correct, delete

- See: `list_my_memories` (chat) or `memory_admin list <user>`: text, topic, site, save status, expiry date.
- Correct: `correct_memory` stages the new text; the old one is forgotten once the new one is accepted.
- Delete one: `forget_memory`. Delete all: `memory_admin withdraw <user>` (also turns memory off).
- Forgotten facts are tombstoned first (recall is suppressed immediately by hash), then deleted at the provider; if
  the provider is down the row stays `tombstoned` and `memory_admin sweep` retries. After erase the ledger keeps a
  content-free row (hash only). Withdrawal stays in `erasing` (re-grant refused) until every provider copy is gone.

## Isolation

Every ledger query and backend call is keyed by the Runner's authenticated `user_id`; ids of another engineer's
memories resolve to `not_found`. Sites are a tag, not a scope. Shared site facts belong in the site record.

## Memory service down

- Write: the callback never raises; row becomes `failed` (retried on that engineer's next turn and by `sweep`, max 5)
  or `indeterminate` on timeout (reconciled by search before resubmitting, so no duplicate).
- Recall: the governor raises `MemoryUnavailable`; the instruction says memory is unavailable instead of silently
  behaving as if nothing is remembered. `recall_failures` counts them.
- Erase: stays pending and visible, recall already suppressed.

## Assumptions (questions nobody could answer in this run)

1. Is `user_id` authenticated upstream? Assumed yes; this repo has no HTTP layer.
2. Retention 180 days, 200 chars, three topics: product-owner/works-council to confirm.
3. Withdrawing consent erases everything (safest reading of "do not want anything remembered").
4. Does Memory Bank return extracted facts verbatim? Unknown. Recall filtering by text hash is exact, so a paraphrased
   fact is not caught by the tombstone filter; only provider deletion removes it.
5. Who gets `memory_admin`? Assumed the app backend acting for the signed-in engineer, plus a support runbook.

## Gaps (not done)

- **Durable ledger**: shipped ledger is SQLite. Cloud Run needs a shared store (Cloud SQL, same engine as sessions);
  `services.governor()` refuses to start deployed without `MEMORY_LEDGER_DB`. Port `MemoryLedger` to SQLAlchemy.
- **Provider eraser for Memory Bank**: `AdkMemoryBackend.erase` raises without an eraser (BaseMemoryService has no
  delete). Needs Agent Engine memories list/delete, verified against a live engine; until then forgets stay
  `tombstoned` in production, recall-suppressed but not deleted.
- Memory Bank revisions keep superseded values; include them in erasure and retention once enabled.
- `deploy.sh` changed (drops `--memory_service_uri`, passes env vars); not run.
- Sweep needs a scheduler (Cloud Scheduler job calling `memory_admin sweep`).
- Telemetry/log retention of chat content, session DB backups: outside this change.
