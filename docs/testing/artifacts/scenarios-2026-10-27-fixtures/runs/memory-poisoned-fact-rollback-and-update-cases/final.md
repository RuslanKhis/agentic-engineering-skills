I changed the code and gold set to cover both problems, but I couldn't run any of it. This session has no shell tool, so the new tests and the scorer have not been executed and nothing is proven yet. I checked them only by re-reading. Please run `python -m unittest discover -s tests -t .` and `python eval/score_recall.py eval/memory_gold.jsonl eval/recall_outputs.jsonl`.

**Fake VIP discount (poison)**
- **Topic removed:** the `account_benefits` topic is gone from `pinecrest/memory_config.py`, and the agent instruction no longer mentions account benefits.
- **Memory no longer grants anything:** the instruction now says never to offer or apply a discount, VIP status or offer because of a memory or because chat text says so. It also treats pasted text as content, not instructions.
- **Nightly job:** `jobs/nightly_generate.py` skips any session whose text addresses the assistant (e.g. "SYSTEM NOTE FOR ASSISTANT"). It keeps revisions on, labels them with source, session and run date, and reports failures instead of dying on the first one. It exits 1 if anything was quarantined or failed.
- **Repair tool:** `jobs/memory_repair.py` has a read-only `scan` for entitlement-looking memories and a `rollback` that is a dry run unless you pass `--apply`. Rollback restores `m-77a1`'s earlier "prefers paper bags" fact, whereas deleting the memory would lose it.

**Old delivery address**
- **Consolidation:** the `delivery_details` topic now tells consolidation to update the single current address rather than add a second one.
- **Agent behaviour:** the current conversation overrides memory. The agent asks when memories disagree and reads the address back before `book_slot`.
- **No code-level enforcement:** "newest wins" is enforced only by instruction and consolidation. `PreloadMemoryTool` injects recall text, so there is nothing to filter in code. If the model ignores the instruction, the stale address can still appear.

**Gold set**
- **New cases:** I added two knowledge-update cases (g07, g08) and three abstention cases (g09–g11). One abstention case seeds the planted VIP text.
- **Scorer:** it now handles `expected: null` for abstention and reports a missing output as `no_output` instead of passing it.
- **Tests:** `tests/test_memory_safety.py` and the updated `tests/test_score_recall.py` use a local double, so they exercise this repo's code, not Memory Bank. They check that an append-only recall fails the update case and a recalled VIP fact fails the abstention case.

**Left undone**
- **No live recall outputs:** g07–g11 have none, so they show `no_output` until someone runs them live. I did not invent outputs, and the scorer exits 1 until then.
- **Unverified SDK calls:** `sessions.events.list`, `memories.list`, `memories.revisions.list` and `memories.rollback`, plus the attribute names on their results, came from documentation and were never executed.
- **Cloud steps, which need your approval:**
  - Re-apply the Memory Bank config to the engine so the benefits topic is actually dropped there.
  - Run `scan` for other affected customers and `rollback` each hit, dry run first.
  - Fix c-311's stored address. Revisions expire after 90 days, so the 22 Sep change must be rolled back before about 21 Dec 2026.
- **Open decision:** the address still lives in semantic memory. Moving it to a deterministic profile field is a decision for you, not part of this fix.

**Questions I couldn't ask, and what I assumed:**
- Is the pre-22-Sep revision still within TTL? I assumed yes.
- Are other customers affected? Unknown, hence the `scan`.
- May recall of entitlement-looking text be blocked? I assumed yes.

These are also written up in `README.md`.