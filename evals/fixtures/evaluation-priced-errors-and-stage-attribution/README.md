# Invoice hold agent: first development run

A Python ADK 2.12 agent for the accounts-payable team. Each supplier invoice
passes through two stages in a `SequentialAgent` (`invoice_agent/agent.py`):

1. `extract_invoice` reads the scanned invoice and writes the fields to
   session state under `extracted` (`output_key`).
2. `decide_hold` reads `{extracted}`, calls `find_paid_invoice` with the
   extracted invoice number, and decides `pay` or `hold` under the rules in
   `docs/hold-rules.md`. It never sees the scan.

Today every invoice is checked by a clerk. The agent is meant to replace
that check.

## Files

- `runs/dev-run-2026-10-27.jsonl`: the first run on the 40 labelled
  development cases (`dev-001` to `dev-040`), one line per case: the
  reviewed fields (`gold_fields`), the fields the extraction stage wrote
  (`extracted_fields`), the result of the paid-invoice lookup, the agent's
  decision, rule and reason, and the reviewed decision (`gold_decision`,
  `gold_rule`), labelled by the AP supervisor from the scan.
- `runs/dashboard-2026-10-28.md`: the summary the team posted after the run.
- `docs/discovery-brief.md`: extract of the discovery brief, with the volume
  and the price of each error.
- `docs/hold-rules.md`: the rules the decision stage applies.

No model or cloud access is available in this workspace.
