I've stopped before making any changes. Permission to read `app/tools/tickets.py` and `app/tools/orders.py` was denied, so I haven't edited anything.

**Why I need those files.** `OrdersReader` and `TicketsReader` call `list_my_orders` and `list_open_tickets` as plain blocking functions. Running them at the same time means pushing them onto worker threads, which only works if they're thread-safe. I can already see one problem in `app/store.py`. `Store` opens `sqlite3.connect(path)` with the default `check_same_thread=True`, so a read from a worker thread would raise `ProgrammingError`. I can't tell from here what `tickets.py` and `orders.py` do. They might use the shared `Store`, the helpdesk HTTP client, or both. Guessing at that could give you a version that looks parallel but fails, or one that doesn't actually overlap.

**What I plan to do once I can read them.**
1. Replace the two sequential readers with a `ParallelAgent` of the two readers, followed by the `LlmAgent` summary step in the same `SequentialAgent`. `build_summary_flow()` keeps its signature.
2. Remove the `except Exception: orders = []` and `tickets = []` fallbacks in `app/summary.py`, which currently turn a failed read into an empty result that is reported as success. A failure will propagate, so the summary step never runs.
3. Make `run_summary` and `Handler` in `app/http_server.py` return a non-200 error body (for example 502 with `{"status": "error"}`) when a read fails. The success shape `{"status": "ok", "summary": ...}` stays the same.
4. Add offline unittest cases with a scripted model. One checks that both reads overlap, using a barrier or event. One checks that a failure in either read means no summary and no `ok`.

**Assumptions I'd proceed on.**
- A failed read should return an error response rather than a summary with a gap in it.
- If the tools use the shared `Store`, the smallest safe change is `check_same_thread=False` plus a lock inside `Store`. That edits `app/store.py`, which isn't a public interface, deployment or dependency file, but I'd like your OK.

**Decision for you.** Either allow reads of `app/tools/orders.py` and `app/tools/tickets.py` so I can continue, or tell me whether those tools use the shared SQLite `Store` and a blocking HTTP client. I haven't run any tests or installed anything.