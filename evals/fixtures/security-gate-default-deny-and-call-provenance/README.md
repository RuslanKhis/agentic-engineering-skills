# Mail assistant

A personal mail and drive assistant for Pemberton & Hale staff on Google ADK 2.12.

- `mailagent/agent.py`: one agent with `search_mail`, `send_email`, `delete_file` and
  `archive_thread` (added last sprint).
- `mailagent/security/gate.py`: the capability gate (`before_tool_callback`), copied from the
  adk-agent-security skill.
- `mailagent/security/taint.py`: records addresses, URLs and ids found in mail search results so
  the gate can refuse them as egress arguments.
- Egress allow-list: session state `policy:egress_allowlist`, set by the app from the user's
  contacts.

## Tests

```bash
python -m unittest discover -s tests -t .
```

google-adk is not installed in this environment and there is no network; the Runner harness in
`tests/runner_harness.py` skips without the SDK.
