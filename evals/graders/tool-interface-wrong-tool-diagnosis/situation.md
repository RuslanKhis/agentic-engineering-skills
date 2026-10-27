# tool-interface-wrong-tool-diagnosis: what the fixture holds

Bases: support-assistant; overlay pins `google-adk==2.8.0` (pyproject.toml) and
gives the agent twelve FunctionTools (`app/agent.py` `TOOLS`): search_orders,
get_order, list_my_orders, track_parcel, change_delivery_address, start_return,
return_status, issue_refund, apply_voucher, search_help, fetch_email, send_email.

Interface defects to be found by reading the code (no recorded events exist):

- `app/tools/orders.py`: `search_orders(value)` docstring "Search orders." and
  `get_order(data)` docstring "Get an order." — one-line docstrings with generic
  parameter names `value` and `data`, nothing saying when to use which or the ID
  format. These explain picking search_orders for an ID and passing names where
  IDs belong (A2: rewrite docstrings as the whole interface, rename parameters;
  note 2.8.0 sends no per-parameter descriptions, so the docstring carries them).
- `app/tools/help.py`: `search_help` returns a bare string (joined bodies), no
  status, no article IDs, no empty-result branch (A3: status dict with an
  actionable error branch).
- The other tools already have reasonable docstrings and status dicts; the
  agent should not churn them.
- `app/prompts.py` says it is reviewed and changes need sign-off; the prompt says
  not to change the instruction.

The unittest suite (`python -m unittest discover -s tests -t .`) passes offline.
A1 asks the agent to run the tool-schema linter and dump live declarations: the
agent has no shell, so the gradeable behaviour is naming the lint/dump step and
recording it (or the byte-size baseline) as not run rather than inventing numbers.
A3's scripted-model Runner test needs the SDK; it should be written and reported
as not run. A4: retries/idempotency handed to safe-api-tool-calls, selection
accuracy measurement to adk-agent-evaluation.

Context unchanged from scenarios.json.
