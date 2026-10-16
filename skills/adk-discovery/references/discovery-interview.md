# The discovery conversation: questions that change the answer

Read before the first question. The published methods (sources and dates in
the repository's research note `docs/research/ai-opportunity-discovery.md`)
share one shape: start from a business problem or a user's job, not a
technology; pick one domain and one workflow inside it; score value against
feasibility with data readiness and risk as gates; define and baseline the
outcome before anything is built. Three of the five root causes of failed AI
projects are discovery failures: the problem misunderstood, the technology
put before the problem, the problem unsuitable for AI.

## Two entry modes

**A rough area** ("introduce AI so we sell advertising more easily"): name
the domain first and the workflow inside it second. The opener is the
abandonment question (row 4 below), asked with the steps named and the
decision it changes:

> Where do advertisers abandon the buying journey today: choosing the
> product, creating the ad, understanding pricing, or completing the booking?
> Is that logged? The answer chooses the first workflow to improve and the
> outcome to measure. If you do not know, the first step is to measure it.

**No use case yet** ("we keep hearing about AI"): the opener is the KPI
question (row 1). Start from the business, then the KPIs the sponsor is
judged on, then the processes that move them.
Scan the functions where the modelled value sits first (customer operations,
marketing and sales, software engineering, research and development) and let
the KPI conversation overrule the scan. Look in three places: repeated manual
effort, waiting on another team, and judgement under ambiguity. Say early
that the answer may be ordinary automation or a process change; the user
asked for a result, not for AI.

In both modes, ask one to three questions per turn, say which decision each
answer changes, and offer a default the user can accept in a word. Infer
what the request already says. When the user cannot answer, record an
assumption with what depends on it, or make measurement the first step.

## The questions, and why each changes the choice

Rows marked **always** are asked unless the request already answered them;
the others are asked when the answer would change the choice, and otherwise
recorded as assumed or "unknown: ask" in the brief.

| | Ask | Why it changes the choice | When |
| --- | --- | --- | --- |
| 1 | What does the business sell, to whom, and which KPI is the sponsor judged on this year? | Fixes the goal metric every candidate is scored against | always |
| 2 | Walk me through one real case from first contact to money received. Where did it wait, bounce back or need someone to re-enter data? | Locates friction in observed work, not the assumed process | always (construct a typical case, labelled assumed, when none exists) |
| 3 | Who does this step today, and how often? | Frequency and the role whose metric moves; rules out rare or trivial tasks | if not inferable |
| 4 | Where do users abandon, retry, undo, or contact support? Is that logged? | Failure signals are easier to find than success; a signal nobody logs needs measuring first | always |
| 5 | Which system owns the facts this would need, and can we reach it this month? | Data readiness is a gate in every framework; no owner, no use case | always |
| 6 | What happens when the answer is wrong, who notices, and can it be undone? | Augment or automate; a person before every effect; whether AI fits at all | always |
| 7 | Does the same input have to give the same output every time? | Deterministic logic over a generative component; the first technology fork | if not inferable |
| 8 | Who decides this today, and what do they look at first? | A decision under uncertainty wants an agent; routine flow wants automation; a lookup wants retrieval | if not inferable |
| 9 | Where does the current process lose context between steps or between days? | The memory and integration an agent would need; the learning gap that stalls pilots | if an agent is a candidate |
| 10 | What is the number now, and how do you know? | Forces the baseline rewrite; no answer means measurement is the first goal | always |
| 11 | Which number must not get worse? | The counter-metric, so a larger basket with more cancellations is not called a win | always |
| 12 | What would make you cancel this in six months? | Cost ceiling, risk controls and the real value question, the three stated reasons agent projects are cancelled | before handoff |
| 13 | Who else has to change how they work for this to count? | Most of the effort is people and process; names the sponsor and the training | before handoff |
| 14 | Who approves the next step, and when? | The decision calendar: the presentation goals the plan must carry | always |
| 15 | What does success look like in 90 days, in a sentence a customer would recognise? | The press-release paragraph and a time-boxed test | before handoff |
| 16 | Who owns this, with what budget, and would they fund one team on it for a year? | A named senior owner is the practice most associated with value; a year is what the engineers say a real problem takes | before handoff |
| 17 | Which steps disappear, and who checks the output, how often? | Redesigned workflows outperform overlays; the validation point is where accuracy risk is caught | before handoff |
| 18 | When the system gets it wrong, where does the correction go, and what changes because of it? | Systems that do not learn from feedback are the users' first complaint | if an agent or LLM is a candidate |
| 19 | Who already uses AI tools for this unofficially? | Employees use AI about three times more than leaders think; they know the friction and will champion the change | if not inferable |

## Rewrites to apply as you go

- **Characterise, do not describe.** "Improve efficiency" becomes "reduce
  invoice processing from 72 hours to 12 hours". Every candidate gets the
  activity, the expected result, the units and the frequency.
- **Job before feature.** "Get a campaign live by Friday without calling a
  rep" before "a chat assistant". The agent is judged on the progress the
  user was trying to make.
- **Automate or augment.** Automate what is boring, repetitive, awkward or
  dangerous and where people agree on the correct way; augment where people
  enjoy the task, carry personal responsibility, the stakes are high or
  preferences are hard to state. Users who say they do not want a task
  automated have answered the question.
- **Stop signals.** Predictability must hold, the information is static,
  a wrong answer is costly or irreversible with no review, complete
  transparency is required: these say the fit is rules, process or nothing,
  whatever the enthusiasm in the room.
- **The threshold sentence.** "If <metric> for <workflow> <drops below /
  rises above> <threshold>, we will <specific action>." Write it for the
  outcome and for the counter-metric; the designer turns both into contracts
  and the presenter puts them on the success-criteria slide.

## The three tests for the first project

The first project must succeed rather than be the most valuable; it must not
be so small that others would call it trivial; and it must show traction
within months on a clearly defined, measurable objective. A bigger idea
waits in the portfolio with the trigger that brings it forward. Fewer
candidates, in the core process, with the change cost budgeted as most of
the effort, is what the firms that report value have in common; treat that
as practice, not proof.

## What the conversation leaves behind

The [discovery brief](../assets/discovery-brief-template.md): the journey
and its friction with sources, the scored portfolio, the first use case with
its measure, baseline, counter-metric and hypothesis chain, the scope-gate
facts the designer needs, the decision calendar, the assumptions, and the
designer's prompt. Read [opportunity portfolio](opportunity-portfolio.md)
for the scoring and the measure, [technology fit](technology-fit.md) for the
`Fit` column, and [handoff](handoff-to-design.md) for what stays with the
designer.
