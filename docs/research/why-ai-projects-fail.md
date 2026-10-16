# Why AI and agent projects fail for reasons other than the model

Primary-source review, 15 October 2026, for the `adk-discovery` skill. It
extends section 3 of [ai-opportunity-discovery.md](ai-opportunity-discovery.md)
(which already records the MIT NANDA headline figures, Gartner's June 2025
forecast, RAND's five causes, the McKinsey 2025 headline, the BCG 2024 press
release and the Google Cloud ROI study) and does not repeat those entries.
Several McKinsey, RAND, HBR and tribunal pages did not load from the review
environment; each entry says whether it rests on the loaded document, a PDF
mirror, or search-index excerpts.

## Conclusion

The evidence from surveys, interviews, vendor guidance and two public
post-mortems points the same way: projects stall on the organisation around
the model, not the model. The recurring non-model causes are a misframed or
miscommunicated problem, no baseline or outcome measure, AI layered on an
unchanged workflow, no senior owner, no defined point where a human validates
output, data that is poor or inaccessible, cost that is not modelled, absent
risk controls, ignored change management and training, no feedback loop so the
system never learns from corrections, a pilot that never enters the real
workflow, a build-versus-buy choice made on pride rather than fit, and a cost
or quality target that cannot survive model or vendor churn.

Two warnings. Almost all of the evidence is correlational and self-reported:
McKinsey's high-performer practices come from a relative weights analysis of
survey answers, NANDA's 67 versus 33 percent success rates are self-reported
by 52 organisations and NANDA says the gap "does not necessarily prove
causation", and MIT SMR/BCG's odds come from a manager survey. The remedies
converge anyway, across engineers' interviews, executive surveys, a tribunal
ruling and a CEO reversing his own decision, and that convergence is the best
support available. The discovery skill should therefore treat each
countermeasure as a required field or question in the brief, not as a scoring
weight.

## What the sources actually establish

### 1. McKinsey: what the self-reported high performers do differently

**The state of AI in 2025: Agents, innovation, and transformation** (November
2025; 1,993 participants, 25 June to 29 July 2025; read from a PDF mirror, the
McKinsey page timed out). "Nearly two-thirds" have not begun scaling AI; 23
percent are scaling an agentic system, but "no more than 10 percent" are
scaling agents in any one function. High performers (EBIT impact of 5 percent
or more plus "significant" value; about 6 percent, n = 109) are 2.8 times
more likely to have "fundamentally redesigned individual workflows" ("one of
the strongest contributions ... of all the factors tested") and three times
more likely to strongly agree that "senior leaders ... demonstrate ownership
of and commitment to their AI initiatives" (championing over time, role
modelling, continued funding and budget reprioritisation). They are also more
likely to "have defined processes to determine how and when model outputs
need human validation to ensure accuracy", another top factor. The ten leading
practices include a road map by business domain, embedding AI into frontline
processes, a workforce plan, iterative development with guardrails,
role-tailored upskilling, and "tracking KPIs for AI solutions". On risk: 51
percent saw a negative consequence, nearly a third from inaccuracy;
explainability is the second most reported risk "but is not among the most
commonly mitigated". Method caveat in the report's words: "a relative weights
analysis on 31 variables"; "all of the management practices we tested
correlate positively with value". Not a controlled comparison.
[Report](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai),
[PDF mirror read](https://www.rivista.ai/wp-content/uploads/2025/11/1762726272547.pdf).
**Apply here:** the brief names the redesigned workflow (not an overlay), the
senior owner and their budget authority, the human-validation point, the KPI
tracked per solution, and the inaccuracy and explainability controls.

**The state of AI in 2026: On the road to ROI** (August 2026; 1,719
respondents, 4 May to 8 June 2026; PDF timed out, figures from McKinsey-domain
excerpts and The Register's 25 August 2026 coverage). 37 percent attribute any
EBIT impact, flat on 2025; high performers still about 6 percent; 80 percent
say AI improved their individual productivity, which McKinsey contrasts with
the flat enterprise figure (diffuse desk-level gains that never reach the
income statement); 40 percent at firms over 1 billion dollars revenue are
scaling agents, up from 27 percent.
[Report page](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai),
[The Register](https://www.theregister.com/ai-and-ml/2026/08/25/mckinsey-says-enterprise-ai-is-finally-on-the-road-to-roi/5292388).
**Apply here:** reject "time saved per employee" as the goal metric unless the
brief states how the saved time converts to a P&L line (fewer BPO hours,
faster cycle, more throughput per team).

**The state of AI: How organizations are rewiring to capture value** (March
2025; July 2024 survey; page not loaded, figures from search excerpts).
Workflow redesign is described as the attribute most associated with EBIT
impact from gen AI; 21 percent of gen AI users have fundamentally redesigned
at least some workflows; 28 percent have the CEO overseeing AI governance, 17
percent the board; 27 percent review all gen AI output before use.
[Report](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-how-organizations-are-rewiring-to-capture-value).
**Apply here:** ask who reviews output today and what share; the first use
case should state the review rule explicitly rather than inherit "someone
checks it".

**Superagency in the workplace** (January 2025; PDF timed out, figures from
search excerpts of McKinsey-hosted text). Only 1 percent of leaders describe
their gen AI rollout as "mature"; 47 percent of C-suite say their company is
developing gen AI tools too slowly; 48 percent of employees rank training as
the most important factor for adoption; employees report using gen AI for a
third or more of their work at about three times the rate leaders estimate
(13 percent versus 4 percent). McKinsey's framing: employees are ready,
leaders are the bottleneck.
[Report](https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/superagency-in-the-workplace-empowering-people-to-unlock-ais-full-potential-at-work).
**Apply here:** interview frontline staff about their unofficial AI use; it
locates the real friction and the people who will champion the change.

### 2. RAND RRA2680-1: the engineers' view

**The root causes of failure for AI projects and how they can succeed**
(13 August 2024; 65 experienced data scientists and engineers interviewed;
RAND pages returned 403, quotes taken from Asia Financial's and Policy
Commons' reproduction of the summary). Causes and matched remedies: (1)
"misunderstanding or miscommunication about the problem" is "the most
common" cause, so "ensure technical staff understand the purpose of a project
and its context"; (2) inadequate data, so invest in data collection and
governance before modelling; (3) "focus more on using the latest and greatest
technology than on solving real problems", so start from the problem; (4)
inadequate infrastructure to manage data and deploy models, so invest in it
up front; (5) a problem "too difficult for AI to solve", so leaders must
"understand AI limitations and assess project feasibility". The patience
remedy is explicit: "Before they begin any AI project, leaders should be
prepared to commit each product team to solving a specific problem for at
least a year." The "more than 80 percent fail" line is RAND quoting prior
estimates.
[Report](https://www.rand.org/pubs/research_reports/RRA2680-1.html),
[summary read](https://asiafinancial.com/study-suggests-ways-to-overcome-high-failure-rate-in-ai-projects).
**Apply here:** the brief records the problem statement in the sponsor's
words and in the engineer's words and flags any difference; it names the
data owner and the deployment path; and it asks whether the sponsor will
fund one team on this problem for a year.

### 3. MIT NANDA, MIT SMR/BCG and Deloitte: the learning gap and the scale gap

**MIT NANDA, The GenAI Divide** (July 2025; PDF read locally). Beyond the
headline figures already recorded: "The core barrier to scaling is not
infrastructure, regulation, or talent. It is learning. Most GenAI systems do
not retain feedback, adapt to context, or improve over time." Users' stated
barriers: "It doesn't learn from our feedback", "Too much manual context
required each time", "Can't customize it to our specific workflows". For
"complex projects" humans are preferred "by 9-to-1 margins"; 66 percent of
executives want systems that learn from feedback and 63 percent demand
retained context. Successful buyers "act like BPO clients, not SaaS
customers": they "benchmarked tools on operational outcomes, not model
benchmarks", "partnered through early-stage failures", and "sourced AI
initiatives from frontline managers, not central labs", paired "with
executive accountability". External partnerships reached deployment "~67% of
the time, compared to ~33% for internally built tools", with the report's own
caveat that this "does not necessarily prove causation". Categories that
succeeded: call summarisation and routing, document automation, repetitive
code; categories that struggled: "complex internal logic, opaque decision
support, or optimization based on proprietary heuristics". Back-office
deployments "often delivered faster payback periods" despite half of budgets
going to sales and marketing.
[PDF](https://www.artificialintelligence-news.com/wp-content/uploads/2025/08/ai_report_2025.pdf).
**Apply here:** the first use case must say where corrections are captured
and how the system changes because of them; score candidates on an
operational outcome, not a benchmark; prefer narrow, edge-of-workflow,
back-office work with low configuration burden; and decide build versus buy
on whether a partner already understands the process.

**MIT SMR and BCG, Expanding AI's impact with organizational learning**
(October 2020; more than 3,000 managers in 29 industries). "Only 10% of
companies obtain significant financial benefits". Getting the fundamentals
right (data, technology, talent, strategy) lifts the odds to about 20
percent; adding solutions the business actually uses lifts them to 39
percent; "only when organizations add the ability to learn with AI do
significant benefits become likely". Organisations using multiple modes of
human-machine interaction and feedback are described as six times more likely
to amplify success. Self-reported odds, but the same "mutual learning"
mechanism NANDA found five years later.
[Report](https://sloanreview.mit.edu/projects/expanding-ais-impact-with-organizational-learning/).
**Apply here:** the brief states how humans will learn from the system and
how the system will learn from humans, as two separate lines.

**Deloitte, State of Generative AI in the Enterprise, Q4** (21 January 2025;
2,773 director-to-C-suite respondents, 14 countries, July to September 2024).
Regulatory compliance rose from 28 to 38 percent as the top barrier; 69
percent say full governance will take more than a year; "two-thirds of
respondents report that 30% or fewer experiments will fully scale within the
next three to six months"; yet "nearly three-quarters" say their most
advanced initiative meets or exceeds ROI expectations.
[Press release](https://www.deloitte.com/us/en/about/press-room/state-of-generative-ai.html).
**Apply here:** the experiment-to-scale gap is a selection problem; the brief
should say up front what "scaled" means for this use case and which
governance sign-off it needs, so the pilot is designed to pass it.

### 4. Other primary evidence

**Gartner, July 2024 and June 2025 press releases** (both loaded). July 2024:
"at least 30% of generative AI (GenAI) projects will be abandoned after proof
of concept by the end of 2025" because of "poor data quality, inadequate risk
controls, escalating costs or unclear business value"; deployments cost "$5
million to $20 million"; "costs aren't as predictable as other technologies".
June 2025 adds "agent washing" and the estimate that "only about 130 of the
thousands of agentic AI vendors are real". Forecasts and a webinar poll
(3,412 attendees), not outcome data.
[July 2024](https://www.gartner.com/en/newsroom/press-releases/2024-07-29-gartner-predicts-30-percent-of-generative-ai-projects-will-be-abandoned-after-proof-of-concept-by-end-of-2025),
[June 2025](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027).
**Apply here:** model cost per unit of work and the cost ceiling before the
pilot; verify a vendor's "agent" actually plans and acts before buying one.

**HBR** (the October 2025 Verma piece is paywalled; only its introduction
loaded, so it is cited for existence, not content). Davenport and Mittal,
"Stop tinkering with AI" (January 2023, excerpt loaded): initiatives are "too
small and tentative" to create economic value; leaders that succeed "put
people in charge of creating the AI", "rounded up the required data, talent,
and monetary investments" and "moved as aggressively as possible".
[Verma 2025](https://hbr.org/2025/10/why-agentic-ai-projects-fail-and-how-to-set-yours-up-for-success),
[Davenport and Mittal 2023](https://hbr.org/2023/01/stop-tinkering-with-ai).
**Apply here:** a pilot with no named owner, no data access and no path to
the real workflow is tinkering; the brief should refuse to call it a first
use case.

**Stanford HAI AI Index, 2025 and 2026 Economy chapters** (loaded). 2025:
among organisations reporting cost savings "most ... indicate figures less
than 10%"; among those reporting revenue gains the most common level is "less
than 5%" (McKinsey data as reproduced). 2026: 88 percent adoption; "AI agent
deployment was in the single digits across nearly all business functions".
[2025](https://hai.stanford.edu/ai-index/2025-ai-index-report/economy),
[2026](https://hai.stanford.edu/ai-index/2026-ai-index-report/economy).
**Apply here:** set the target in the brief against these typical magnitudes;
a first use case promising 30 percent cost reduction needs a stated reason.

**Google Cloud, five guides to production-ready agents** (6 May 2026, loaded)
and the Next '26 session BRK2-095 (24 April 2026). The guides state the
operational countermeasures: "a misconfigured SaaS tool leaks data passively,
but a misconfigured agent takes bad actions actively"; delegated approval
where "the agent pauses for human review"; per-agent identity, registry and
gateway; hybrid graphs that combine "hard-coded business rules with AI
reasoning". The session promised "a retrospective of recurring failure
patterns identified across more than 70 customer engagements"; the patterns
are not published, so no ADK or Vertex customer story stating what failed
first was found.
[Five guides](https://cloud.google.com/blog/topics/developers-practitioners/five-guides-to-building-and-scaling-production-ready-ai-agents),
[Session](https://www.googlecloudevents.com/next-vegas/session/3913172/from-prototype-to-production-hard-won-lessons-for-advanced-reliable-and-secure-agents-learned-from-70+-deployments).
**Apply here:** the first use case lists its irreversible actions and the
approval point for each, and prefers rules for the deterministic steps.

**Klarna** (press release 27 February 2024, loaded; May 2025 Bloomberg
interview quoted via Entrepreneur). February 2024: "2.3 million"
conversations, "equivalent" to "700 full-time agents", resolution "from 11
minutes to under 2 minutes", satisfaction "on par" with humans, "$40 million"
estimated 2024 profit improvement. May 2025, Siemiatkowski: "As cost
unfortunately seems to have been a too predominant evaluation factor when
organizing this, what you end up having is lower quality"; "it's so critical
that you are clear to your customer that there will be always a human if you
want". The CEO's own account: a single cost metric, no quality guardrail with
teeth, and no retained human path.
[Press release](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/),
[Entrepreneur](https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/491396).
**Apply here:** every cost goal carries a paired quality guardrail with a
threshold that stops the rollout; the workflow keeps a human escalation path.

**Moffatt v. Air Canada, 2024 BCCRT 149** (14 February 2024; tribunal site
and CanLII blocked; quotes from Dentons Data's reproduction). Air Canada
argued "the chatbot is a separate legal entity that is responsible for its
own actions"; the tribunal: "This is a remarkable submission. While a chatbot
has an interactive component, it is still just a part of Air Canada's
website"; "there is no reason why Mr. Moffatt should know that one section of
Air Canada's webpage is accurate, and another is not." Damages 650.88 dollars
plus interest and fees. The finding was negligent misrepresentation; the
failure was an unverified answer about policy given with no grounding check.
[Decision](https://decisions.civilresolutionbc.ca/crt/crtd/en/525448/1/document.do),
[Dentons summary](https://www.dentonsdata.com/airline-ordered-to-compensate-a-b-c-man-because-its-chatbot-provided-inaccurate-information/).
**Apply here:** the brief lists the statements the agent is allowed to make
about policy, price or eligibility, and where each is grounded; anything
else routes to a human or a quoted source.

## Cause to countermeasure

| Non-model cause | Evidence | What the brief or first use case contains |
| --- | --- | --- |
| Problem misframed or miscommunicated | RAND cause 1 ("most common"); NANDA "misalignment with day-to-day operations" | Field: problem statement in sponsor's words and in builder's words, with the difference noted; a frontline user signs it |
| No baseline or outcome measure | McKinsey KPI tracking practice; NANDA "benchmarked ... on operational outcomes"; Stanford typical magnitudes | Field: goal metric, current value, measurement window, target with units; rule: no candidate scores above "idea" without a baseline |
| Workflow not redesigned | McKinsey 2.8x redesign, "strongest" factor; 2026 paradox of desk gains | Field: before and after workflow steps naming what is removed, not just assisted; rule: an overlay on an unchanged process is scored down |
| No senior owner | McKinsey 3x senior ownership; RAND one-year commitment; Davenport "put people in charge" | Field: named owner, budget line, and a yes/no to funding one team for a year |
| No human-validation point | McKinsey "defined processes ... human validation"; Air Canada; Google Cloud delegated approval | Field: per action, who validates, when, and what share of outputs; rule: irreversible or customer-facing policy statements require a validation point |
| Data poor or inaccessible | RAND cause 2; Gartner "poor data quality"; Deloitte data deficiencies | Field: each data source with owner, access path, freshness and whether friction is logged today |
| Cost not modelled per unit | Gartner 5 to 20 million, "costs aren't as predictable"; Klarna cost-first reversal | Field: expected volume, cost per handled unit, ceiling, and who pays for the model bill after the pilot |
| Risk controls absent | Gartner "inadequate risk controls"; McKinsey inaccuracy and unmitigated explainability; Google Cloud governance stack | Field: top three harms, guardrail metric and threshold for each, identity and permission scope of the agent |
| Change management and training ignored | Superagency 48 percent training; McKinsey workforce plan and role-based upskilling; RAND cause 1 | Field: who in the workflow changes what they do, what training they get, and when; the champion from the shadow-AI users |
| No feedback loop for corrections | NANDA learning gap, 66 and 63 percent; MIT SMR mutual learning | Field: where a correction is captured, who reviews it, and what artefact changes (prompt, rule, eval case, retrieval source) |
| Pilot never embedded in the real workflow | NANDA 5 percent to production; Deloitte 30 percent scale; Davenport tinkering | Scope rule: the pilot runs on live volume in the system of record from week one, even if for one queue or one region |
| Wrong build versus buy choice | NANDA 67 versus 33 with its causation caveat; Gartner agent washing and 130 real vendors | Question: does a partner already understand this process and learn from feedback; is the "agent" on offer actually planning and acting |
| Vendor or model churn breaks the target | Gartner cost unpredictability; Google Cloud rules plus reasoning; McKinsey iterative guardrails | Rule: deterministic steps are rules not prompts; the acceptance test is defined on outcomes so a model swap can be re-run against it |

## Discovery brief fields that exist because of this evidence

1. Two-voice problem statement (sponsor and builder) with a frontline
   sign-off (RAND, NANDA).
2. Baseline, window, target and guardrail per metric, with a pass/stop
   threshold sentence (McKinsey KPI tracking, Klarna, Stanford magnitudes).
3. Before-and-after workflow naming removed steps and the validation point
   for each action (McKinsey redesign and human in the loop, Air Canada).
4. Named senior owner, budget line and a one-year commitment answer (McKinsey
   ownership, RAND, Davenport).
5. Data source register with owner, access path and logging status (RAND,
   Gartner, Deloitte).
6. Unit economics: volume, cost per unit, ceiling, post-pilot payer (Gartner).
7. Harm list with guardrail thresholds and the agent's permission scope
   (Gartner, McKinsey risk, Google Cloud).
8. People plan: role changes, training, and the shadow-AI champion
   (Superagency, McKinsey workforce plan).
9. Correction loop: capture point, reviewer, artefact that changes (NANDA,
   MIT SMR).
10. Embedding rule: live volume in the system of record from the start, with
    the governance sign-off named (NANDA, Deloitte).
11. Build-versus-buy question and agent-washing check (NANDA, Gartner).
12. Outcome-defined acceptance test that survives a model swap, with rules
    for deterministic steps (Google Cloud, Gartner).
