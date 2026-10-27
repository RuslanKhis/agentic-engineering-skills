I wrote an offline PyRIT test for the poisoned-document case and a runbook for the live A2A campaign. None of it has been run, and the live campaign is not set up. I couldn't run anything here (no shell, no installs, no network), so every result is `not run`.

PyRIT 1.1.0 has no `A2ATarget`. It is only on PyRIT main and in later tags, and 1.1.0 raises `ImportError` for it. So PyRIT 1.1.0 cannot red-team the Cloud Run A2A endpoint. Instead, the offline test attacks the agent in-process with the real ADK Runner, a scripted model and fake backends.

**What I added**
- **`tests/test_pyrit_xpia.py`:** PyRIT's `XPIAWorkflow` plants a poisoned document in a fake store, then runs the agent. The scorer only sees what the fake backends recorded, not the reply, because refused calls still carry the attacker IBAN in their arguments.
  - It has an ungated control agent, so a scorer that never fires can't pass silently.
  - It has the payout case, which should pass.
  - It has an email-exfiltration case marked `expectedFailure`, because that gap is real today.
- **`pyproject.toml`:** a `redteam = ["pyrit==1.1.0"]` extra.
- **`.github/workflows/ci.yml`:** a separate `pyrit-xpia` job, so a PyRIT dependency conflict can't break the main suite. It needs no model credentials.
- **`redteam/README.md`:** the live A2A plan, the questions and assumptions, and the findings.

**Findings from reading the code**
1. `send_email` is ungated and accepts any recipient (`claims/tools/claims_tools.py:29`). Together with `read_document` and the claim data, a poisoned document can send claim data to an attacker. The existing `tests/test_injection.py` doesn't check for it.
2. `file_payout` trusts the model-supplied `payee_account` (`claims/tools/claims_tools.py:18`) instead of looking it up from the claim. A confirmation only helps if the approver sees that account.
3. I did not exercise who can confirm `file_payout` over A2A, or whether a peer-authored message can.

I made no fixes to the agent.

**Questions I couldn't ask, and what I assumed**
- **Who confirms `file_payout` over A2A?** I assumed this is undecided, so the tests never confirm.
- **Is there a staging deployment with fake backends?** I assumed there isn't, so I prepared no live run.
- **May CI install PyRIT next to the agent's pins?** I assumed this is unknown, so the extra and CI job are isolated.

**Left undone**
- **Unverified PyRIT calls:** the PyRIT code in the test is written from the skill's notes on 1.1.0, not run. That covers the `PromptTarget` subclass, `SubStringScorer(...)` and `execute_async(...)`. The first `pyrit-xpia` CI run is the check, so expect to fix a signature or two.
- **Live campaign:** I didn't prepare it. It needs your approval of a staging target with synthetic data, a test service account, the model, a case count and a cost ceiling. It also needs a PyRIT tag that contains `a2a_target.py`, in its own environment.
- **Not done:** I didn't fix `send_email` or `file_payout`, and I didn't write a fake-peer test for confirmation over A2A.