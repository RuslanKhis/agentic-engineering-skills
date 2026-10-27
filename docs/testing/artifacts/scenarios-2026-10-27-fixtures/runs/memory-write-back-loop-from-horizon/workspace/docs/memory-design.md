# Memory write-back design

Code: `fieldline/memory_controls.py` (logic, no SDK), `fieldline/memory_adk.py` (ADK glue),
wiring in `agent.py` and `services.py`. Tests: `tests/test_memory_controls.py`, `tests/test_memory_adk.py`.

## What is saved, and when

Three topics only: `answer_style`, `kit`, `site_note` (a note tagged with a site id). One short
sentence (max 300 chars), saved only when the engineer says it and wants it kept, via the `remember`
tool. Not saved: hazards, access details or codes, anything about other people, entitlements, whole
sessions. Screening rejects secrets/codes, long digit runs, emails and instruction-like text, because
memory is replayed into later prompts. Max 50 facts per engineer; facts expire after 180 days.

`remember` only stages a row in the application's own fact table (an outbox). An `after_agent_callback`
then sends the staged facts to the memory service as one user event each, so the service never sees the
whole session. A failed send stays `failed`, is retried on the engineer's next turns (max 5 attempts)
and is shown by `list_my_memories` as "not saved yet". The callback never raises into the turn.

## Who agreed

Opt-in, per topic, recorded with policy version and time; default is no consent. Consent is read from
the store by the authenticated `user_id`, never from a model argument. `remember` without consent
writes nothing, and the provider is not called. Consent cannot be granted by any tool: `grant_consent`
must be called from an authenticated settings surface (not built, see below). A new `POLICY_VERSION`
invalidates old consent. `stop_remembering` (model-callable, safe direction) withdraws consent: saving and
recall stop at once and unsent candidates are discarded. Audit rows are content-free.

## Isolation

Scope is the authenticated user id only. A site id is a tag, never a scope. Recall shows a fact only if
that engineer's own live, consented, unexpired record matches what the provider returned, and the
text shown is the record's text, so a mis-scoped or leaky provider cannot surface another engineer's note.
Tested with two engineers on NW-0417 against a provider that returns everyone's entries.
Shared site facts (access, hazards) stay in `get_site`, never in personal memory.

## See, correct, delete

Tools `list_my_memories`, `correct_memory`, `forget_memory` act on the signed-in engineer's rows only;
a foreign or unknown id returns `not_found`. Delete and correct take the fact out of recall immediately,
then delete at the provider. If that fails the row stays `delete_pending` (text kept only so the delete can
be retried), is retried on later turns, and is reported as pending, never as done. `erase_user` withdraws
consent, deletes all facts and the user's sessions, and returns `complete: false` while anything is pending.
Not covered by erasure: the visit log (`VISITS`, a business record, needs its own policy), provider
backups and retention, session-DB backups, and the content-free fact rows and audit rows kept so replays
stay blocked.

## When the memory service is down

Writes: staged and retried (above). Recall: `GovernedRecallTool` replaces `PreloadMemoryTool` and tells the
model "memory could not be read" instead of silently continuing, and counts `recall_failed`.
It lives in the agent so it also applies under `adk deploy --memory_service_uri`, which builds its own
memory service and would bypass a wrapper service.

## Horizon recipe verdict

Not adopted wholesale. Used ideas: save through a tool, content screening, small bounded facts, throttled
flush. Not used: whole-session flush (submits unscreened text), a background review agent deciding what
to save (no consent gate, fire-and-forget loses writes), nightly consolidation (needs Memory Bank
generation and revisions, nothing here consents to or verifies it). Reconsider consolidation after consent,
deletion and live checks pass.

## Questions asked (nobody was available) and assumptions used

1. Opt-in or opt-out? Assumed opt-in, because some engineers refuse and the works council is involved.
2. Retention? Assumed 180 days (`MEMORY_FACT_TTL_DAYS`). Needs the works council's answer.
3. Where do engineers grant consent and request erasure? Assumed an authenticated settings surface exists
   or will; only `MemoryControls.grant_consent` / `erase_user` are provided.
4. Should an engineer-correctable record be app-owned? Assumed yes, with Memory Bank as the recall index.
5. Is the visit log in scope for erasure? Assumed no.

## Not done / unverified

- Nothing was executed: the session had no shell. Tests are written but have not been run.
- ADK calls assumed from the skill's 2.8.0 notes and not run: `Context.add_events_to_memory(events=...)`,
  `Context.search_memory(query)`, `BaseTool.process_llm_request`, `llm_request.append_instructions`.
- Provider recall matches by exact normalised text. Memory Bank extracts and rewrites facts, so matching may
  fail and recall return nothing. Check live write-then-read; fallback is to serve recall from the fact table.
- Provider deletion is not wired: `UnsupportedEraser` keeps every delete pending. Memory Bank needs a real
  eraser (find and delete the memory resources for that user), plus TTL and revision settings.
- The control store is sqlite. A multi-instance Cloud Run deploy needs a shared database (Cloud SQL), or a
  withdrawal on one instance is not seen by another. Per-user locks are in-process only.
- No consent/erasure UI or endpoints; no scheduler for `purge_expired`; no metrics export.
