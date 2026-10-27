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
- `contracts/screening.py`: every tool result goes through local LlamaFirewall scanners
  (`after_tool_callback`); anything but an explicit allow replaces the result with a fixed notice.
  Agent startup fails if `llamafirewall` is not in the image. Set `HF_HUB_OFFLINE=1` and bake
  PromptGuard weights into the image before enabling `prompt_guard_weights_dir`.
- Alignment check: `alignment_gate` is wired when `build_agent(judge=...)` gets an in-project judge.
  LlamaFirewall's stock AlignmentCheck sends the whole trace to Together AI and is **not** used.
  The in-project variant is not built yet (`llamafirewall_alignment_judge` raises).

## Tests

```bash
python -m unittest discover -s tests -t .
```

`tests/test_runner_poisoned_page.py` runs the agent through the real Runner with a scripted
model. google-adk is not installed in this environment and there is no network, Hugging Face
token or model access, so those tests skip here.
