# Pinecrest delivery assistant

Chat assistant for Pinecrest Grocers' home delivery. Customers book delivery
slots, ask about orders and substitutions. Built on google-adk 2.12.0 with
Vertex AI Memory Bank (memory revisions on, the default) for what customers
tell it about themselves: delivery address and access notes, substitution
preferences, dietary needs.

- `pinecrest/agent.py`: agent with `PreloadMemoryTool`, `book_slot`,
  `order_status`.
- `pinecrest/memory_config.py`: Memory Bank topics and generation settings.
- `jobs/nightly_generate.py`: nightly pass that generates memories from the
  previous day's sessions.
- `eval/memory_gold.jsonl` and `eval/score_recall.py`: the memory gold set and
  its scorer (offline, against saved recall outputs).

```bash
python -m unittest discover -s tests -t .
python eval/score_recall.py eval/memory_gold.jsonl eval/recall_outputs.jsonl
```

## Stale-address and poisoned-memory handling

- Poison cannot be stored: no `account_benefits` topic; the nightly job quarantines sessions whose text
  addresses the assistant (`pinecrest/memory_policy.py`) and exits 1 so it is noticed; every generate call
  keeps revisions on and labels them with `source`, `session`, `run_date`.
- Stale address: the `delivery_details` topic tells consolidation to update, not append; the agent
  instruction makes the current conversation override memory, asks when memories disagree and reads the
  address back before `book_slot`. Newest-wins is enforced by instruction and consolidation, **not** in
  code, because `PreloadMemoryTool` injects recall text and cannot be filtered. The address still lives in
  semantic memory; moving it to a deterministic profile field is a decision for the team, not done here.
- Gold set: `knowledge_update` (g07, g08) and `abstention` (g09-g11, incl. the planted VIP text) cases.
  They have **no saved recall output**; the scorer reports them `no_output` (not a pass) until a live run.
- Repair: `python -m jobs.memory_repair scan ENGINE` and `rollback MEMORY_NAME [--apply]` (dry run by default).

Manual steps (need cloud access and approval; none done):
1. Re-apply `MEMORY_BANK_CONFIG` to the Agent Engine so the benefits topic is dropped there.
2. Run `scan` on the engine (other customers may hold the same planted fact), then `rollback` for each hit,
   dry run first. Rollback restores `m-77a1`'s "prefers paper bags" fact; deleting it would lose that.
   Revisions expire after 90 days (about 21 Dec 2026 for the 22 Sep change).
3. Fix the live address for c-311 (rollback or update the memory) and run the gold set live
   (`eval/recall_outputs.jsonl` is saved output; regenerate it for g07-g11).

Questions I could not ask, and the assumptions used: (a) is the revision from before 22 Sep still within
TTL? assumed yes (90 days); (b) are other customers affected? unknown, hence `scan`; (c) may recall of
entitlement-looking text be blocked? assumed yes, nothing in memory grants authority.

google-adk and the Vertex AI SDK are not installed here; there is no network
or Google Cloud access in this environment.
