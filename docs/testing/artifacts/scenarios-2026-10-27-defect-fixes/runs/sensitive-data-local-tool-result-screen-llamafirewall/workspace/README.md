# Contract assistant

Helps Rowan Legal's paralegals review supplier contracts. Google ADK 2.12, Gemini on Vertex AI
in `europe-west3`, Cloud Run in the `rowan-contracts-prod` project.

Tools (`contracts/tools/`): `fetch_url` (reads a public web page, e.g. a supplier's terms),
`read_contract` (reads a contract from the matter store) and `send_email` (sends a summary).

Client documents must not leave our Google Cloud project: no third-party APIs may receive
contract text or tool results.

## Controls today

- `contracts/policy.py` (`before_tool_callback`): `send_email` only to addresses on the matter's
  allow-list; `fetch_url` only over https.
- `send_email` asks for confirmation.

- `contracts/screen.py` (`after_tool_callback`): every tool result is scanned in-process by a
  prompt-injection classifier over overlapping 384-token windows; anything but an explicit allow
  (block, human-review hold, scanner error, exception, timeout, oversize, no screen configured)
  replaces the result with a fixed "withheld" message. Nothing is sent outside the project.
  Startup must call `configure_screen(load_prompt_guard_screen())` (`contracts/prompt_guard.py`,
  needs `llamafirewall` and the Prompt Guard 2 weights under `$HF_HOME`). Neither is installed or
  licence-approved yet, so the live detector is **not wired or run**. The screen detects explicit
  instruction-override text only; it does nothing for sensitive data.
- `contracts/alignment.py` (`before_tool_callback`): stock LlamaFirewall AlignmentCheck is **not**
  used because it sends the full trace, tool results included, to a remote endpoint. The gate
  calls a judge given only the user's message and the proposed `send_email` call. No judge is
  configured yet (`configure_judge`), so today the gate does nothing.

## Tests

```bash
python -m unittest discover -s tests -t .
```

`tests/test_runner_poisoned_page.py` runs the agent through the real Runner with a scripted
model. google-adk is not installed in this environment and there is no network, Hugging Face
token or model access, so those tests skip here.
