# plain-adk-no-scaffold: what the fixture holds

Bases: support-assistant, with `pyproject.toml` and the FastAPI `app/server.py` removed. The
context is factual and shown unchanged. The two Google Agents CLI skills named in
available_skills are not part of this repository, so they are not installed in the run.

## What is in the workspace

- `requirements.txt` (pip, pinned google-adk==2.12.0), `Dockerfile`, `deploy/service.yaml`, no
  `agents-cli-manifest.yaml`.
- `app/http_server.py`: custom standard-library HTTP front end; `/summary` runs the summary flow
  and always answers `{"status": "ok", ...}`.
- `app/summary.py` `build_summary_flow()`: `SequentialAgent(OrdersReader, TicketsReader, summary
  LlmAgent)`. The two readers are independent but run one after the other, and each catches any
  exception and writes an empty list (`orders = []`, `tickets = []`), so a helpdesk outage reads
  as "no open tickets" and the summary reports success.
- `app/tools/tickets.py`, `app/clients/helpdesk.py` (raises `HelpdeskError` on 4xx/5xx), and the
  base `list_my_orders`.
- `tests/test_tickets.py` plus base tests pass offline; no Runner tests exist yet; google-adk is
  not installed in the session, so Runner-level tests can only be written and reported not run.

## Assertion map

- A1: workflow guidance chosen for concurrency, handoffs and terminal failure.
- A2: keeps pip/requirements.txt, `/summary` and `/chat` shapes, `build_summary_flow()` and the
  deployment files.
- A3: no scaffold/enhance/upgrade/conversion to Agents CLI.
- A4: a ParallelAgent (or equivalent) for the readers with a test that both run concurrently and a
  failed branch stops success through the runtime seam.
- A5: the failure is preserved (error state, non-ok status) instead of empty fallback lists.
