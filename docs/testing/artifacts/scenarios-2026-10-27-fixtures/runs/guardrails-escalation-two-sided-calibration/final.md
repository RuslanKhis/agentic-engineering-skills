I lowered the over-escalation, but a rate under 10% can't be reached without changing the written rules. I couldn't run anything: the session has no shell and no model. The tests and the new prompt are unexecuted.

**Why 10% isn't reachable**
- In the 40-claim export, travel (flights, rail, hotel, car hire) or a total over 500 EUR forces 15 claims to review: 10 travel plus 5 over 500, which is 37.5%.
- Those two rules are in the instruction as mandatory, and I haven't touched them. Under 10% would mean dropping or loosening them, which is finance's policy decision, not something to change quietly.
- The observed 56–61% is about 20 points above that floor. That excess is almost certainly the "when unsure, escalate / anything unusual, escalate" clause. I inferred this from the prompt and the export. I haven't measured it, because the export has no outcomes.

**What I changed**
- **`expense_agent/prompts.py`**: removed the blanket "always safer to escalate" language. The agent now escalates only for the two mandatory rules. It also escalates when it can't tell whether a listed rule applies, for example a missing total or attendee count, and it must name the rule in the reason. Anything else it decides.
- **`expense_agent/rules.py`** (new): `mandatory_escalation_reason(claim)` implements the travel and over-500 rules in code.
- **`expense_agent/tools.py`**: `decide_claim` now refuses a claim that falls under those rules. This means that loosening the prompt can't cause required claims to be approved without finance review.
- **`tests/test_tools.py`**: added tests for the guard, including the 500.00 and 500.01 boundary, and a test that the sample has 15 rule-forced claims out of 40. Run them with `python -m unittest discover -s tests -t .`.

**Questions I couldn't ask, and what I assumed**
1. Will product accept about 35–40% or a bit lower? I assumed the realistic goal is "no escalation beyond what the rules require", not 10%.
2. Should a travel claim with no receipt be rejected or escalated? The rules conflict (EXP-26106 and EXP-26122 are examples). I kept the literal current behaviour: travel always goes to review, so the guard blocks a direct reject.
3. Do reviewers approve nearly all of the rule-mandated escalations? If so, finance may want to raise the 500 EUR threshold or exempt rail under some amount. That is their call, and it is the only route to a much lower rate.

**Left undone**
- Measuring the real rate. There are no labelled cases and no model access. I'd label the 40 claims for expected lane, run the old and new prompts, and check both over-escalation and wrongly decided claims.
- Rolling out and watching the dashboard. The rate is only a proxy, so I'd also track how many escalations reviewers approve unchanged and how many decided claims get overturned. I'd roll out gradually.
- Meal-cap and alcohol handling are unchanged.