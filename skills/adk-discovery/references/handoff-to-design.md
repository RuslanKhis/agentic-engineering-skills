# Handoff to design: what discovery decides, what the designer decides

Read before writing section 9 of the brief. The two skills meet at one
document and must not do each other's work.

## The line between them

| Discovery decides (this skill) | Design decides (`adk-system-designer`) |
| --- | --- |
| Which journey or process, and where it breaks | Which components, contracts and decisions enforce the chosen behaviour |
| The ranked portfolio and the first use case | Nothing about the ranking; it designs the chosen one |
| Technology fit: agent, LLM call, classical ML, rules or process change | The ADK and GCP shape of that fit, or the evidence it is infeasible |
| The outcome measure, its baseline and the counter-metric | The outcome contract, how it is measured in the build and the acceptance case that proves it |
| The hypothesis chain | Which goal tests which link, in which phase |
| Stakeholders, deciders and the decision calendar | Presentation goals at those dates (`adk-presenter`), waits in the schedule |
| Scope-gate facts the user already gave (time, people, money, judge, data) | The delivery profile, depth per concern, floor, capacity check and cut line |
| Assumptions and open questions, each with how to settle it | Which of them block which goal; discovery goals for the rest |

Discovery writes no contracts, no architecture, no goals and no estimates.
When the user asks for those, finish the brief and hand over; the designer
produces them from the brief in its own conversation. The designer does not
reopen the ranking; if it finds the first use case infeasible (no access to
the authoritative system, the measure cannot be observed, the fit was wrong),
it names the finding and the user returns here with it.

## What the brief must contain for the designer to skip its opening

The designer asks only what the brief leaves open, so each of these rows is
either filled in or marked "unknown: ask":

- the first use case in one sentence, its users and what it leaves out;
- the outcome measure, baseline (value, source, date) and counter-metric;
- the technology fit and the nearest alternative rejected;
- the systems that own the facts and who grants access;
- the cost of a wrong answer, the price of each error type with today's
  rates, and whether a person reviews before an effect;
- the scope-gate table (section 5), including who approves the next step
  and when;
- the decision calendar (section 6), so the plan carries presentation goals.

A brief with the measure marked unknown is still a valid handoff: the
designer's first goal becomes measuring the current journey, and the plan
says so.

## The prompt

End the brief and the conversation with the designer's prompt, filled in,
in a copyable block:

```text
/adk-system-designer Read docs/discovery/<topic>.md and design the first use
case it selects (<O-ID>: <one sentence>). Treat its confirmed answers as
settled; ask only what it leaves open. The outcome measure is <metric>
against <baseline>, with <counter-metric> as the guardrail. The sponsor is
<role>; <decider> decides on <decision> on <date>, so plan a presentation
goal for it. Design only.
```

This is the only copy of the prompt; the brief's section 8 holds the filled
version and the closing message repeats it.

When the fit is `process`, the next prompt is not the designer's: say which
role owns the process change and what would be measured, and offer
`adk-discovery` again when that change has run. When the fit is `ml` or
`rules` with no language interface at all, say that the design skill in this
toolkit is for ADK applications and hand the brief to whoever owns that
work; an ML model that an agent will call as a tool still goes to the
designer.

When the user wants the approval presentation before the design exists, the
brief is the only record: `adk-presenter` can draft a proof-of-concept
approval deck from it with every number labelled as the brief labels it, and
the cost and scope slides marked "pending design".
