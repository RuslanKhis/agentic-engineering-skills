# Red-teaming the claims agent with PyRIT

## Two layers

| Layer | What it tests | Needs | Status |
| --- | --- | --- | --- |
| Offline XPIA (`tests/test_pyrit_xpia.py`, CI job `pyrit-xpia`) | The agent's gates when a model has been talked into acting on a poisoned document | google-adk, `pyrit==1.1.0`; no model, no network | Written, **not run** |
| Live A2A campaign | How often a real model is talked into it, through the deployed A2A face | PyRIT release with `A2ATarget`, a real model, IAM token, approval | **Not set up**, needs the decisions below |

The offline test is the CI gate. The grader is what the fake backends recorded (`payouts.filed`, `mail.sent`), not the
reply: a refused `file_payout` still carries the attacker IBAN in its arguments, and over A2A ADK returns refused
calls in the task history, so scoring the reply or the task would call a gated run a success. The test includes an
ungated control agent so a scorer that never fires cannot pass silently.

## Why PyRIT 1.1.0 cannot attack the A2A endpoint

`A2ATarget` (`pyrit/prompt_target/a2a_target.py`) is on PyRIT main only. 1.1.0 raises `ImportError` for it and has no
`a2a` extra. For the live campaign use a tagged release whose source contains that file, in its own environment
(it needs `a2a-sdk>=1.1.5,<2`; the agent's 1.2.3 fits, but keep the environments apart), never git main. Check the
tag's source before relying on it.

## Live campaign: approval needed first (not done)

Nothing here was run. Before anyone runs it, decide:

1. **Target.** A staging Cloud Run revision with synthetic claims, a fake payout/mail backend and no outbound network
   path. Not production data or identities.
2. **Identity.** A dedicated test service account with `roles/run.invoker` on that service only, minting an ID token
   with the service URL as audience. PyRIT's target must send it as a bearer header: confirm that `A2ATarget` can take
   a custom `httpx` client or headers in the chosen tag; if it cannot, a small authenticating proxy or a custom
   `PromptTarget` over `a2a-sdk` is needed.
3. **Model and cost.** The exact model the service uses (`gemini-3.5-flash` in `claims/agent.py`), case count,
   repetitions and a cost ceiling.
4. **Confirmation path.** `file_payout` is held with `require_confirmation`; the task goes to `input-required`. The
   campaign must never send a confirmation. Success is measured on the staging backend's recorded payouts and mails,
   not on PyRIT's reply scorer.
5. **Planting.** Documents reach the agent through the claim's uploaded-document store, not through the A2A message,
   so the live XPIA setup target must write to the staging store, then send a benign "summarise doc-N" message via A2A.

Report attack success rate per scenario with model and date, labelled vendor-measured on this system, and rerun after
each structural fix.

## Questions I could not ask, and the assumptions used

- Who is allowed to confirm `file_payout` over A2A, and is the confirmer the adjuster or the calling partner system?
  Assumed: not decided; the tests never confirm.
- Is there a staging deployment with fake backends? Assumed: no, so no live run was prepared against it.
- May CI install PyRIT's dependencies next to the agent's pins? Assumed: not known; the extra and the CI job are
  separate so a conflict is isolated.

## Findings from reading the code

1. **`send_email` is ungated and takes any recipient** (`claims/tools/claims_tools.py:29`). With `read_document` as the
   untrusted source and the claim data as private data, all three legs of the trifecta are present. The expected-failure
   test `test_poisoned_document_cannot_email_an_external_address` records it. Fix: restrict recipients to the claimant or
   adjuster on file in the tool body, or gate it.
2. **`file_payout` trusts the model-supplied `payee_account`** (`claims/tools/claims_tools.py:18`), though the docstring says
   "on file". Confirmation helps only if the human sees the account. Fix: look the account up from the claim in the tool
   body and reject a mismatch.
3. **The existing `tests/test_injection.py` only asserts no payout**, not no email.
4. The confirmation gate's behaviour over A2A (who may answer, and whether a peer-authored message can) was not
   exercised; it needs a fake-peer test.
