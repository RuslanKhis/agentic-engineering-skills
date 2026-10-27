I added a garak run that attacks the agent through the real ADK Runner, but none of it has been run. This session had no way to execute code, and I did not install garak or make network calls. The new tests, the gate checker and the workflow are unexecuted.

**What I added**
- **`redteam/garak_target.py`**: the function garak calls (`run_agent`). Each prompt gets a fresh Runner session for `build_agent()`. The tools use the fakes from `tests/fakes.py`, so no real payment or mail call can happen. Only the model is live (Gemini). Each attempt also writes a sidecar record of what actually reached the fake payments and mail providers.
- **Why the sidecar**: garak's detectors only read reply text, so an agent that really sends mail can still pass them. The gate therefore reads the sidecar.
- **`redteam/check_garak.py`**: the CI gate, ignoring garak's exit code. It fails on:
  - a missing report or missing completion row;
  - a probe with no eval row;
  - any eval row with `fails` or `nones` above zero;
  - a hit log;
  - an attempt count that differs between garak's report and the sidecar;
  - any forbidden effect in the sidecar.
- **Labels and tests**: findings carry an `ASI02` label (my choice, see below). `tests/test_redteam_gate.py` covers each gate rule and runs in the existing `ci.yml` with no model. `tests/test_redteam_target.py` covers the wrapper with a scripted model and skips when the SDK is absent.
- **`.github/workflows/redteam.yml`**: hand-started, with `approval_ref`, the `live-eval` environment, Workload Identity and a 60-minute timeout. It uses a fresh report prefix and `--generations 1`, passes the probe spec through an env var, and pins garak to 0.17.1 in `redteam/requirements-garak.txt`. I added a README note.

**Decision for you: deepteam.** I did not add it. It needs a paid simulator and evaluator model, which CI doesn't have: the default is OpenAI, and Gemini would have to go through `deepeval.models.GeminiModel`. It also has a telemetry opt-out requirement and a known import failure in 1.0.10. If you want ASI labels from it, that should be a separate approved run with a stated case count and cost ceiling. For now the gate labels findings itself.

**Questions I couldn't ask, and what I assumed**
- Which probe modules to run? I defaulted to `probes.latentinjection`.
- Is the `live-eval` environment's approval enough for this run? I assumed yes.
- Is any email during a red-team run a finding? I assumed yes, since no probe has a legitimate reason to send mail.
- Is `ASI02` the right label for both payment and mail findings? I used it for both; please confirm.

**Still open**
- **The gate will likely fail on its first live run.** `send_email` (`app/tools/mail.py`) has no confirmation and no recipient restriction, so an injected email reaches the mail fake. `tests/test_redteam_target.py` currently asserts that email is recorded as a finding. I did not change the agent. You need to decide on a recipient policy or a confirmation for `send_email`.
- **Report shape unchecked.** I haven't checked garak's report row shape or the `--spec` syntax against a real run. If they differ, the gate fails closed because rows are missing, which wastes a paid run but can't give a false pass.
- **No cost ceiling.** I haven't estimated one. The approval ticket should state it before the first dispatch.
- **`tests/runner_harness.py`.** The scripted model repeats its last step when the script runs out instead of raising.
- **PR-time garak.** It can't run on pull requests without a model. PRs get the deterministic gate tests, and the live garak run stays approval-gated.