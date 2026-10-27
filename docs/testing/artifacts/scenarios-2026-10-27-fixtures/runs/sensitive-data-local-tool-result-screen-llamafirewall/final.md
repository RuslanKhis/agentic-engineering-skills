Tool results now go through a screening layer, but nothing has been run and the alignment check is not built. I had no shell in this session, so none of the tests have been executed. Treat every result as `not run`.

**What I added**
- **Result screening:** `contracts/screening.py` has a `tool_result_screen` hook that runs on every tool result before the model or the session sees it.
  - It joins every string in the result, keys and nested values included, into one text and checks it against each scanner.
  - Anything other than an explicit allow replaces the result with a fixed notice. That covers a block, an error, a timeout, an unknown type or an oversized result.
  - `llamafirewall_scanner()` runs LlamaFirewall's regex scanner locally. It also runs PromptGuard if you give it a weights directory.
- **Agent wiring:** `build_agent(scanners=None, judge=None)` in `contracts/agent.py` installs the screen. By default it uses LlamaFirewall, so startup fails if `llamafirewall` isn't in the image.
- **Alignment gate:** `alignment_gate(judge)` checks `send_email` calls against the user's goal and fails closed. It is only attached when you pass `judge=`. Without one the gate is off.
- **Tests:** `tests/test_screening.py` has unit tests that need no ADK. `tests/test_runner_poisoned_page.py` has a new real-Runner test checking that the poisoned page text never reaches the second model request or the stored events. `tests/runner_harness.py` now records what the model receives.
- **README:** it now documents all of this.

**What I left undone**
- **Alignment check not built.** LlamaFirewall's stock AlignmentCheck sends the whole trace, contract text and tool results included, to Together AI by default. That breaks your rule that documents stay in the project, so I did not use it. `llamafirewall_alignment_judge` rejects non-Vertex hosts and then raises `NotImplementedError`. The in-project version needs a `CustomCheckScanner` subclass pointed at a regional Vertex AI endpoint. I'd have to write that against the installed package, and I can't here.
- **Alignment check isn't a hard gate.** Even built, it leans towards allow and can't tell a judge outage from a finding, so keep `send_email` confirmation and the allow-list.
- **LlamaFirewall code unchecked.** The `llamafirewall_scanner()` calls (`ScannerType.REGEX`, `Role.TOOL`, `ToolMessage`, `ScanDecision`) are written from memory of its API. They are untested and the package isn't installed. Check them on first run with the package present.
- **Fake-scanner tests only.** Every test uses fake scanners, so they show the wiring and fail-closed behaviour, not LlamaFirewall's detection quality.
- **Runner tests skip.** They skip here because google-adk isn't installed. They also still need a first real run, to confirm that ADK accepts a callback list and that the replaced result is what gets stored.
- **PromptGuard weights.** Meta's weights need a Hugging Face token to fetch. Someone needs to pre-bake them into the image and set `HF_HUB_OFFLINE=1`.
- **Dependency not declared.** I didn't add `llamafirewall` to `pyproject.toml` because I don't know which version to pin.
- **`root_agent` breaks without it.** `root_agent = build_agent()` will now raise on import wherever `llamafirewall` is missing. That is deliberate fail-closed behaviour, but check that `adk web` or deploy tooling can cope.

**Question I couldn't ask:** which in-project endpoint or model should the alignment judge use? I assumed regional Vertex AI in `europe-west3` and left it unwired.