The screen and the alignment gate are written, but nothing was run. This session has no shell, so every test below is `not run`. The two runner-based screen tests also skip in this environment because ADK isn't installed.

**Added**
- `contracts/screen.py` is an `after_tool_callback` on every tool.
  - It scans all strings in the result, keys included, with a local classifier in overlapping 384-token windows, so an injection past token 512 or across a window edge is still scored.
  - Only an explicit allow for every window passes. A block, human-review hold, scanner error, exception, timeout, oversize result or missing screen all replace the result with a fixed "withheld" message.
  - Logs carry the decision, score and error type, never the scanned text or the block reason.
- `contracts/prompt_guard.py` is the LlamaFirewall Prompt Guard 2 adapter. It refuses to start unless the weights are already under `$HF_HOME`, so it can't trigger a download or a Hugging Face login.
- `contracts/alignment.py` is a `before_tool_callback` on `send_email`. A missing goal, judge error or timeout refuses the call.
- `agent.py` wires both, `README.md` records them, and `tests/fakes.py` has a fake scanner and tokenizer.
- `tests/test_screen.py` is unit tests for the windowing, the verdict rules, log contents and the alignment gate.
- `tests/test_runner_screen.py` drives the real Runner. It covers a poisoned page withheld and absent from the session, a clean page passing unchanged, a scanner error or exception, and no screen configured.

**Decision for you: alignment check.** I did not use LlamaFirewall's `AlignmentCheckScanner`. It sends the whole trace, tool results included, to a remote endpoint (Together AI by default), which breaks your rule that documents stay in the project. Instead the gate calls an injected judge that sees only the user's message and the proposed call. Assumption I proceeded on: that is what you meant by "its alignment check". If you want the stock scanner pointed at an endpoint inside your project, say so; it would still receive the full trace.

**Left undone**
- **No test has run.** Run `python -m unittest discover -s tests -t .` where ADK is installed.
- **Real detector not tested.** The `llamafirewall` import path and `.tokenizer` attribute in `prompt_guard.py` follow the PurpleLlama source but are unverified against an installed package.
- **Weights and licence.** Prompt Guard 2 weights are gated under the Llama 4 Community License, and no token or network was available. Your project owner has to approve the licence before the live detector is used.
- **Startup wiring.** `configure_screen(load_prompt_guard_screen())` must be called in your Cloud Run entrypoint, which isn't in this repo. Until then every tool result is withheld.
- **No judge configured.** The alignment gate does nothing today. `send_email` is still covered by the allow-list and the confirmation step. A judge on Gemini in your Vertex project would stay inside the project; I haven't built one.
- **Confirmation order unchecked.** I don't know whether ADK runs `require_confirmation` before `before_tool_callback`, so the Runner tests don't assert the judge is called. The gate is tested only directly.
- **Coverage.** The classifier catches explicit instruction-override text, not other attacks, and does nothing for sensitive data. The existing poisoned-page test now passes partly because results are withheld when no screen is configured.