I can't get the escalation rate under 10% without dropping escalations the company rules require, so I haven't tried to. I added the rules in code instead, and nothing has been run, because this session has no shell.

**Why 10% is out of reach**
- In `data/recent-claims.jsonl`, 15 of 40 claims (37.5%) must be escalated under the travel and over-500 rules. That is 10 travel claims plus 5 non-travel claims over 500 EUR.
- No agent change gets below 37.5% unless the policy owner relaxes those rules. That decision is theirs, not mine. It also means the 10% target is unreachable as stated.
- Of the 60% rate on the dashboard, about 22 points come from the model escalating on its own (the "if unsure / anything unusual, escalate" lines in the prompt). That is the part that could be reduced.
- The 40-claim sample is small, so 37.5% is a rough figure. Please recompute it from the claims table.

**What I changed**
- `expense_agent/policy.py` (new): `forced_escalation_reason()` holds the travel and over-500 rules in code. It fails closed, so a missing or unreadable category or total forces review.
- `expense_agent/agent.py`: a `before_agent_callback` sends forced cases to review without a model call. Before this, a model that did nothing left them unrouted.
- `expense_agent/tools.py`: `decide_claim` now refuses a forced case, so the model can't approve something the rules say must go to review.
- `tests/test_policy.py` (new): covers the rules, the 500 boundary, fail-closed inputs, the `decide_claim` refusal, and the 15-of-40 floor on the sample data.

The prompt is unchanged.

**Left undone**
- I ran nothing. There is no shell here, and the README says `google-adk` isn't installed and there's no model access. The new tests and the callback wiring are unexecuted, and the callback is written from the ADK 2.12 docs, not tested.
- The model's own escalations are the lever for bringing the rate down. I did not touch the "when unsure, escalate" wording, because without labelled cases I can't tell whether trimming it removes needless escalations or required ones. The dashboard rate can't tell those apart. The next step is a labelled sample of 100–200 claims, measured for both missed and unnecessary escalations. Any prompt change should be judged on that, not on the dashboard number.
- The effect on the rate is unmeasured. The expected result is a floor of about 38% plus whatever the model still escalates.

**Questions I can't ask, and what I assumed**
- Is 10% a hard target, or should finance review the 37.5% floor? I assumed the required rules stay.
- Should a travel claim with no receipt be rejected or escalated? The prompt rules conflict. I assumed escalate, because the travel rule is the stricter one.
- Reviewers bulk-approving the queue is a control problem in its own right. Cutting routine items from it should help, but I haven't addressed it directly.