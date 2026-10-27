I built the saving side, but none of it has been run. This session had no shell, so the new tests have not been run and no existing test was re-run. The design and the assumptions I made are in `docs/memory-design.md`.

**What I built**
- **What gets saved, and when:** `remember` saves three kinds of fact: answer style, kit and site notes. Each is one short sentence, only when the engineer says it and wants it kept. Facts are screened for codes, emails and instruction-like text. They expire after 180 days. Each fact is staged in an app-owned table, and an after-turn callback sends it to the memory service. A failed send is retried on later turns and shown as "not saved yet".
- **Who agreed:** memory is opt-in per topic, recorded with policy version and time, and defaults to off. Consent is read from the store for the signed-in user, never from a model argument. No tool can grant consent. `stop_remembering` withdraws it immediately.
- **Correct and delete:** `list_my_memories`, `correct_memory` and `forget_memory` work only on the signed-in engineer's rows. A delete takes the fact out of recall at once, then deletes it at the provider. If that fails it stays pending and is retried. `erase_user` removes facts and sessions and reports `complete: false` while anything is pending.
- **Service down:** a failed write is retried and logged without any fact text. For recall I replaced `PreloadMemoryTool` with `GovernedRecallTool`, which tells the model when memory could not be read. It sits in the agent because `adk deploy --memory_service_uri` builds its own memory service and would bypass a wrapper service.
- **Isolation:** scope is the signed-in user id only, and the site id is a tag. A fact is shown only if the engineer's own consented, unexpired record matches what the provider returned. One test has two engineers on the same site against a provider that returns everyone's entries.
- **Horizon recipe:** I did not adopt it wholesale. It flushes whole sessions and has no consent gate. I reused the ideas of saving through a tool, screening content and keeping facts small.

I wrote 28 tests in `tests/test_memory_controls.py` and `tests/test_memory_adk.py`. They cover consent denial, isolation, screening, retry, provider outages, expiry, correction, a delete racing a write, erasure with a control user, replay and audit content.

**Left undone**
- **ADK calls not run:** I assumed `add_events_to_memory(events=...)`, `search_memory(query)`, `BaseTool.process_llm_request` and `append_instructions` from the skill's notes, without running them. The ADK-gated tests may fail on signatures.
- **Recall matching:** recall matches the provider's returned text exactly. Memory Bank rewrites facts, so recall may come back empty. This needs a live write-then-read check. The fallback is to serve recall from the fact table.
- **Provider deletion:** it isn't wired, so every delete stays pending and is never reported as done.
- **Control store:** it is sqlite with in-process locks. A multi-instance Cloud Run deploy needs a shared database, or a consent withdrawal on one instance won't reach the others. I'd treat this as a deploy blocker.
- **Not built:** the settings screen for consent and erasure, a scheduler for `purge_expired`, metrics export, and a policy for the visit log.

**Questions with the assumptions I used**
- Opt-in or opt-out? I assumed opt-in.
- Retention? I assumed 180 days (`MEMORY_FACT_TTL_DAYS`), which the works council should confirm.
- Where do engineers grant consent and request erasure? I assumed an authenticated settings surface will exist.
- Is the visit log in scope for erasure? I assumed no.