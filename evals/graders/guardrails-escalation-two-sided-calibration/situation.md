# guardrails-escalation-two-sided-calibration: what the fixture holds

Standalone overlay: `expense_agent/` (ADK agent, `decide_claim`, `escalate_claim`), the
production dashboard `dashboards/escalation-rate.md` (56-61 % escalated, reviewers
bulk-approve, product target under 10 %), `data/recent-claims.jsonl` (40 recent claims,
no lanes or labels), stdlib tests for the tools.

- The travel-category and over-500-EUR must-escalate rules exist only in
  `expense_agent/prompts.py`; `decide_claim` will happily decide a 1,400 EUR flight
  (A1: move them into code — a before_tool_callback refusing `decide_claim` for those
  claims, or `require_confirmation` callable — with a scripted-model Runner test that the
  model cannot bypass; reported not run since google-adk is not installed).
- The instruction also says "when unsure, escalate", "always safer to escalate", "if
  anything looks unusual, escalate" — a likely driver of over-escalation.
- No labelled cases exist (A2: build labelled cases with a reviewed expected lane from
  `recent-claims.jsonl`; report missed-escalation and over-escalation separately).
- A3: missed escalation is the gate; over-escalation the usefulness target; the dashboard
  rate is a drift signal only. A4: live model rates reported as not run (no model access).
