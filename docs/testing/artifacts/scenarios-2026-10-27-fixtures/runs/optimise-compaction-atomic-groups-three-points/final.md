I fixed the trimmer so it can no longer separate a function call from its result. I haven't run anything, because this session has no shell tool. Treat the fix and its tests as unverified until you run `python -m unittest discover -s tests -t .`.

**Cause.** `trim_contents` in `app/plugins/trimming.py` cut the request to the newest 24 items by count. That cut could land between a model's function call and the user content carrying its result, so the model received a call with no result. That matches the rejections you describe.

**What I changed**
- **`app/plugins/trimming.py`:** the cut now moves earlier to the nearest turn start, meaning a user content with no function response. `max_items` is now a minimum. If there is no turn start before the cut, nothing is dropped, so the current turn is always sent whole.
- **`tests/test_trimming.py`:** three new tests. They cover every cut size on a history containing calls, the minimum and current-turn rules, and a history with no turn start.

**When compaction runs.** I wrote this up in `docs/compaction.md`. There are two separate mechanisms:
- **Inside a run:** `HistorySummariserPlugin` trims what is sent to the model on every call where the request holds more than 24 items. It changes only the outgoing request, not what Postgres stores.
- **After an invocation:** `EventsCompactionConfig(compaction_interval=6, overlap_size=1)` runs once 6 new invocations have built up since the last compaction. It appends a summary event and leaves the raw events in Postgres.

Compaction triggers on invocation count only, because no token threshold is set. A few very large tool results can bloat requests long before the sixth invocation. No summarizer is set, so each compaction is an extra call to the agent's own model.

**Not done or not verified**
- **ADK behaviour:** the ADK package isn't installed here, so the trigger description comes from the skill's notes on 2.8.0 and 2.12.0, not from the installed source.
- **Real-stack checks:** I didn't test compaction through `DatabaseSessionService` on Postgres or capture a real outgoing request. There is no model access, so summary quality wasn't tested. The checklist is at the end of `docs/compaction.md`.
- **Plugin wiring:** I didn't add a Runner-level test that no request carries a split pair. The plugin still needs the ADK `Runner` to exercise it.
- **Assumption:** I assumed keeping more than 24 items in a request is acceptable. If you need a hard cap on request size, a token-threshold compaction setting is the better lever. I didn't change that without measurements.