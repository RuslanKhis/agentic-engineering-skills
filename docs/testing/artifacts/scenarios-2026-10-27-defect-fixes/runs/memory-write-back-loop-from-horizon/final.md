I built the saving side, but none of it has been run. Bash was disabled in this session, so I couldn't run any tests and I only walked the unit tests through by hand. google-adk isn't installed here either.

**What it does**
- **What gets saved:** only what an engineer explicitly asks to be remembered. It's one short line in one of three topics: `answer_style`, `kit` or `site_note`. Nothing is inferred from conversation, and no whole session is ever sent. Codes, passwords, long digit runs, emails and URLs are refused.
- **When it's saved:** a `remember` tool stages the fact in a durable ledger. An after-turn callback then rechecks consent and writes it. The assistant says "will be saved". Only `list_my_memories` showing `accepted` means it was.
- **Who agreed:** memory is opt-in and off by default. Consent is a recorded row per engineer with a policy version, a time and a source. It's granted and withdrawn only through `python -m fieldline.memory_admin`, never by the model. A new policy version makes old consent stale until it's granted again.
- **Correct and delete:**
  - **In chat:** `list_my_memories`, `correct_memory` and `forget_memory`.
  - **Outside chat:** withdrawing consent turns memory off and erases everything.
  - **Order of deletion:** a forgotten fact is suppressed from recall immediately, then deleted at the provider and retried if that fails.
- **Isolation:** every ledger query and backend call uses the signed-in `user_id`. Another engineer's memory id returns `not_found`. A site is only a tag, so a site note belongs to the engineer who wrote it.
- **Memory service down:** writes never break the reply. They are retried up to 5 times, and a timeout is checked by search first so nothing is saved twice. If recall fails, the agent is told memory is unavailable rather than seeing an empty result.

**Decisions**
- **Horizon recipe:** I didn't adopt it. Its background judge and whole-session flush would save things nobody asked to be saved.
- **Recall path:** I replaced `PreloadMemoryTool` with a governed instruction provider. `adk deploy --memory_service_uri` builds its own memory service for the Runner, so a tool reading from it would skip consent and forgotten-fact filtering.
- **`deploy.sh`:** I dropped `--memory_service_uri` and added the memory env vars. That change is untested.

**Files**
- **New code:** `memory_ledger.py`, `memory_governor.py`, `memory_tools.py`, `memory_adk.py`, `memory_admin.py` under `fieldline/`.
- **Changed:** `agent.py`, `services.py`, `deploy/deploy.sh`, `README.md`.
- **New docs:** `docs/memory-design.md` has the full design, assumptions and gaps.
- **Tests:**
  - **Governor tests:** `tests/test_memory_governor.py` runs against a fake backend. It covers consent denial, cross-user access, replay, correction, forgetting, a write in flight during an erase, expiry, outages, timeout reconciliation and log leakage.
  - **Runner tests:** `tests/test_memory_runner.py` uses a scripted model and skips without the SDK. It was never executed, so expect fixes on first run.

**Not done**
- **Durable ledger:** the ledger is SQLite. Deployed, it needs a shared store such as Cloud SQL, and `services.governor()` refuses to start without `MEMORY_LEDGER_DB`.
- **Memory Bank deletion:** `BaseMemoryService` has no delete method and I had no live engine to check one against. In production a forgotten fact stays recall-suppressed but isn't deleted until a provider eraser is written.
- **Sweep scheduler:** the retry and expiry sweep needs a scheduler such as Cloud Scheduler calling `memory_admin sweep`.
- **Provider paraphrasing:** if Memory Bank paraphrases saved facts, the hash-based recall filter won't catch them. Only provider deletion would.

**Questions I couldn't ask, and what I assumed**
- Is `user_id` authenticated upstream? I assumed yes, since this repo has no HTTP layer.
- Are 180-day retention, 200 characters and the three topics right? I assumed so, pending the product owner and works council.
- Should withdrawing consent also erase everything? I assumed yes.
- Who runs `memory_admin`? I assumed the app backend acting for the signed-in engineer, plus a support runbook.