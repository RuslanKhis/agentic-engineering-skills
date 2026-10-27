# Workspace assistant

An internal assistant for Larch & Pine's finance and operations staff, on Google ADK 2.12.0.
It reads and sends mail, manages calendar events, reads and shares Drive files, and pays
supplier invoices from the operating account.

- `app/agent.py` builds the agent; `app/tools/` holds the tools; `app/backends.py` defines the
  backend interfaces the tools call.
- `app/policy.py` is the `before_tool_callback`: read-only tools pass, `send_mail` recipients must
  be on the allow-list, `pay_invoice` needs a known payee and stays under the daily cap, and
  `pay_invoice` also asks the user to confirm (`require_confirmation`).
- `tests/adversarial/cases.json` is our injection suite; `tests/test_adversarial.py` runs each
  case through the real Runner with a scripted model (`tests/runner_harness.py`) against the fakes
  in `tests/fakes.py`.

## Tests

```bash
python -m unittest discover -s tests -t .
```

google-adk is not installed in this environment and there is no model access, so the Runner
tests skip; the policy tests run.
