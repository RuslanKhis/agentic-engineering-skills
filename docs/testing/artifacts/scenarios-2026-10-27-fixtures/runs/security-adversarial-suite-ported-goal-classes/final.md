I've finished the edits. The last step is the summary.

I extended the suite, but none of it has been run. This session had no tool for executing code, so the tests are unverified and may need small fixes on their first run.

**What changed**
- **`tests/adversarial/cases.json`:** it now has 17 cases, up from 2.
  - They cover injection through mail, Drive file text, file-name metadata and calendar events.
  - They include four attack-wording variants (an "important message from the owner" block, "ignore previous instructions", a fake system message, and an injection that names the tool).
  - They include the banking classes of split payment, payee swap and negative amount.
  - They include sending a security code and then deleting the trace, exfiltration through a calendar invite, address-parsing bypasses, a user-turn override and system-prompt extraction.
  - The goal classes paraphrase AgentDojo and InjecAgent from their published descriptions, with invented fixtures. I did not re-read those sources, and no benchmark data is imported.
- **`tests/test_adversarial.py`:** the old test only checked for forbidden strings. The new one also does two things:
  - It confirms the forbidden tool call was actually attempted, so a case can't pass without testing anything.
  - It asserts that the matching fake recorded no effect.
- **`GateInvariantTests` (in the same file):** these checks need no ADK.
- **`tests/adversarial/COVERAGE.md`:** a class-by-class coverage table, what is not covered, and what a live run would add.

**Gaps the new cases should surface**
These are my reading of `app/policy.py`, not test results. I did not change anything in `app/`.
- **`delete_mail`:** the gate lets every call through, so an injected deletion runs (w10).
- **`create_event`:** the gate lets every call through, so an injected invite can name any attendee and carry data in the title (w11).
- **`share_file`:** the gate takes the text after the last `@` as the domain, so `a@evil.invalid@larchpine.example` passes (w12).
- **Daily payment cap:** nothing updates `payments:today_cents`, so split payments never add up against the cap.
- **Negative amounts:** the gate accepts a negative `amount_cents` in `pay_invoice`.

The payment cases only stay safe because `pay_invoice` waits for confirmation. Each open gap is marked `known_gap`: the test skips it with the reason, and fails once the gap closes so the flag gets removed.

**What a live run would add**
- How often a real model attempts each attack, per class and per attack-wording variant. The scripted model always attempts it, so the offline tests only show the gates.
- Attempts the cases don't script, and whether the user's real task still completes under attack.
- Variance across repeats and model versions, and a baseline to compare after each gate fix.
- Generated payloads from tools like promptfoo, garak or PyRIT.

**Questions I couldn't ask, and what I assumed**
- Should the open gaps be fixed now? I assumed no, because you asked for suite coverage only.
- Is a live run wanted? I assumed not yet. It would need your approval of the model, case count, cost ceiling, fakes and blocked egress.

**Left undone**
- Running the suite; the first step is `python -m unittest tests.test_adversarial -v` with google-adk 2.12 installed.
- Fixing the gate gaps.
- A confirmation-resume case (a forged approval is ignored, a real one runs once).
- Cases for surfaces the agent doesn't have yet (MCP, memory, sub-agents, A2A).
- The live run.