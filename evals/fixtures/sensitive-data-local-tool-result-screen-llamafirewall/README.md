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

## Tests

```bash
python -m unittest discover -s tests -t .
```

`tests/test_runner_poisoned_page.py` runs the agent through the real Runner with a scripted
model. google-adk is not installed in this environment and there is no network, Hugging Face
token or model access, so those tests skip here.
