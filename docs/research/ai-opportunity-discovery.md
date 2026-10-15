# How organisations discover where AI belongs and pick a first use case

Primary-source review, 15 October 2026, for the proposed `adk-discovery`
skill. Vendor pages, consulting reports and survey figures change; re-read
each dated URL before relying on it. Some McKinsey, RAND and HBR pages did not
load from the review environment; where a claim rests on a search-index
excerpt or abstract rather than the loaded page, the entry says so.

## Conclusion

The published frameworks agree on more than their branding suggests. Every
credible method starts from a business problem or a user's job, not a
technology; scopes the first effort to one workflow inside one domain rather
than a scattered use-case list; scores candidates on value against
feasibility with data readiness and risk as explicit gates; and insists the
outcome is defined, baselined and guarded before anything is built. The
failure evidence fits: MIT NANDA, RAND and Gartner all attribute stalled
projects to mis-stated problems, workflow misfit and unclear value, not model
quality. What the sources do not establish is a validated scoring formula or
a proven signal that predicts a good first agent; the prioritisation grids are
analyst judgement and the ROI surveys are self-reported. The skill should
borrow the shared structure (problem, domain, workflow, baseline, guardrail,
90-day test) and present the criteria as a checklist to argue through with
the client, not a scoring engine.

## What the sources actually establish

### 1. Vendor adoption frameworks

**Google Cloud AI Adoption Framework** (whitepaper; blog 30 June 2020). A
maturity model: people, process, technology and data give six themes (Learn,
Lead, Access, Scale, Secure, Automate) scored as tactical, strategic or
transformational. Its only use-case instruction is to move "toward use cases
that are feasible and designed to deliver business value" and have a central
team "assess the feasibility of new use cases" and "prioritize scarce ML
resources around key business problems". Establishes Google's readiness
vocabulary, not outcomes.
[Whitepaper](https://services.google.com/fh/files/misc/ai_adoption_framework_whitepaper.pdf),
[blog](https://cloud.google.com/blog/products/ai-machine-learning/build-a-transformative-ai-capability-with-ai-adoption-framework).
**Apply here:** use the six themes for the readiness section of the brief,
not as the discovery method.

**Google People + AI Guidebook, "User needs + defining success"** (page
undated; guidebook first published 2019). Replace "Can we use AI to X?" with
"How might we solve X?" and "Can AI solve this problem in a unique way?". AI
is "probably not better" for "maintaining predictability", "providing static
or limited information", "minimizing costly errors" and "complete
transparency". Automate tasks that are boring, repetitive, awkward or
dangerous and where people agree on the correct way; augment where people
enjoy the task, carry personal responsibility, the stakes are high or
preferences are hard to state. Monitoring template: "If { success metric }
for { feature } { drops below / goes above } { threshold } we will { take a
specific action }". Design guidance, not measured evidence.
[Chapter](https://pair.withgoogle.com/chapter/user-needs/).
**Apply here:** adopt the automate-versus-augment test and the threshold
sentence as brief fields; treat the "probably not better" list as a stop
signal for workflows where a wrong answer is costly or irreversible.

**Microsoft Cloud Adoption Framework, AI strategy** (ms.date 26 June 2026,
updated 9 October 2026). "Start with business problems": "repeated manual
effort or slow approvals", "where do results miss expectations", "where do
people spend time on repetitive tasks". Turn each into a statement that
"names the activity and the expected result" and confirm it "happens often
enough to justify the investment". Then ask whether output variation is
acceptable (generative) or "the same input should lead to the same result"
(non-generative), and weigh capabilities, data needed, skills and cost.
[Page](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ai/strategy).
**Apply here:** the activity-plus-result sentence, the frequency check and
the determinism question are the right shape for the candidate-workflow
field.

**OpenAI, "Identifying and scaling AI use cases"** (PDF undated; cites
McKinsey January 2025). Look at "Repetitive, low value tasks", "Skill
bottlenecks" (waiting on another team) and "Navigating ambiguity". An
impact/effort quadrant where "quick wins with strong impact and low effort"
are "often the best place to start building momentum", re-scored quarterly.
Then map department workflows: "break workflows into individual tasks ...
and clearly map each step". Vendor playbook from its own customers.
[PDF](https://cdn.openai.com/business-guides-and-resources/identifying-and-scaling-ai-use-cases.pdf).
**Apply here:** the three "where to look" prompts are interview openers; the
workflow map is the bridge from a task list to an agent spanning steps.

**Amazon Working Backwards / PR-FAQ** (Amazon page undated; book 2021).
"Start by defining the customer experience, then iteratively work backwards";
press release under one page, FAQ under five, with "a clear-eyed and thorough
assessment of how expensive and challenging it will be".
[Page](https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes).
**Apply here:** end the brief with a one-paragraph press release of the
improved journey, in the customer's terms.

### 2. Consulting approaches

**McKinsey, "A generative AI reset"** (McKinsey Quarterly, 2024; page timed
out, quotes from the search index). Scan "domains (that is, customer journeys
or functions)" and prioritise one "to pilot and then scale as part of a larger
sequencing of initiatives". "Launching pilots is (relatively) easy; getting
pilots to scale and create meaningful value is hard because they require a
broad set of changes to the way work actually gets done."
[Article](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/a-generative-ai-reset-rewiring-to-turn-potential-into-value-in-2024).
**Apply here:** in situation A name the domain first, the workflow second,
and list the work changes the first use case implies.

**McKinsey, "The economic potential of generative AI"** (June 2023). 63 use
cases across 16 functions; about 75 percent of modelled value in customer
operations, marketing and sales, software engineering and R&D. An estimate,
not an observation.
[Report](https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier).
**Apply here:** in situation B start the function scan there, then let the
KPI conversation overrule it.

**BCG, "Where's the value in AI?"** (press release 24 October 2024; 1,000
executives, 59 countries). 26 percent "have developed the necessary set of
capabilities to move beyond proofs of concept"; 4 percent generate
significant value consistently; 74 percent show none. Leaders "pursue, on
average, only about half as many opportunities", put "10% of their resources
into algorithms, 20% into technology and data, and 70% in people and
processes", and find 62 percent of value in core functions. Self-reported.
[Press release](https://www.bcg.com/press/24october2024-ai-adoption-in-2024-74-of-companies-struggle-to-achieve-and-scale-value).
**Apply here:** fewer candidates, in the core process, with change cost
budgeted as most of the effort.

**Bain, "AI is transforming productivity; sales remains the new frontier"**
(23 September 2025). Prioritise "the role, then the use case" so the effort
"connects to a measurable effect, such as sales rep productivity"; pick "one
or two domains at the front end of the sales life cycle"; require "data
quality sufficient to move forward"; prefer redesign over automating the
existing flow. Only "a few can measure their success in double digits".
[Article](https://www.bain.com/insights/ai-transforming-productivity-sales-remains-new-frontier/).
**Apply here:** name the role whose metric moves before the feature;
directly relevant to the advertising-sales example.

**Deloitte** (US press release 21 January 2025, 2,773 respondents surveyed
July to September 2024; Luxembourg method page 24 March 2026). 74 percent say
their most advanced initiative meets or exceeds ROI expectations, yet "more
than two-thirds of respondents say that 30% or fewer of their experiments
will be fully scaled in the next three to six months". The method page:
generate ("identify where delays, errors, or manual work block strategic
objectives"), characterise ("replace 'improve efficiency' with 'reduce
invoice processing from 72 hours to 12 hours'"), validate ("time to value
(under 12 weeks), stakeholder readiness, and strategic alignment").
[Press release](https://www.deloitte.com/us/en/about/press-room/state-of-generative-ai.html),
[method](https://www.deloitte.com/lu/en/our-thinking/future-of-advice/first-ai-use-case.html).
**Apply here:** the characterise rewrite (adjective to baseline and target
with units) is the single most useful editing rule for the brief.

**Gartner Use-Case Prisms** (13 May 2024). Plot business value against
feasibility by "framing a domain, defining business value aspects and
evaluating feasibility factors"; quadrant labels and scales are paywalled.
Analyst judgement. [Prism](https://www.gartner.com/en/documents/5426463).
**Apply here:** use the two axes with the client's own definitions; do not
import unseen scores.

**Andrew Ng, AI Transformation Playbook** (December 2018). "It is more
important for your first few AI projects to succeed rather than be the most
valuable AI projects"; not "so small that others would consider it trivial";
"traction within 6-12 months"; "technically feasible" after diligence; "a
clearly defined and measurable objective that creates business value".
[PDF](https://landing.ai/wp-content/uploads/2018/12/AI-Transformation-Playbook-v8.pdf).
**Apply here:** these are the "why this one first" tests in the brief.
Davenport and Ronanki (HBR, January 2018, abstract only, 152 projects) say
the same: "don't start with moon shots".

### 3. Why pilots fail

**MIT NANDA, "The GenAI Divide"** (research January to June 2025; PDF dated
13 July 2025). Method as stated: "a systematic review of over 300 publicly
disclosed AI initiatives, structured interviews with representatives from 52
organizations, and survey responses from 153 senior leaders". "95% of
organizations are getting zero return"; "just 5% of integrated AI pilots are
extracting millions in value, while the vast majority remain stuck with no
measurable P&L impact". For enterprise tools "sixty percent of organizations
evaluated such tools, but only 20 percent reached pilot stage and just 5
percent reached production", failing on "brittle workflows, lack of
contextual learning, and misalignment with day-to-day operations"; "the core
barrier to scaling is not infrastructure, regulation, or talent. It is
learning." Budgets "favor visible, top-line functions over high-ROI back
office"; "external partnerships see twice the success rate of internal
builds"; winners "focus on narrow but high-value use cases ... start at
workflow edges with significant customization, then scale into core
processes". Caveats: small conference-sourced sample; self-reported P&L;
Fortune (18 August 2025) reports different method counts; the sales and
marketing budget share is 50 percent in one takeaway and about 70 percent in
the text.
[PDF](https://www.artificialintelligence-news.com/wp-content/uploads/2025/08/ai_report_2025.pdf).
**Apply here:** ask where the workflow loses context and feedback, prefer a
back-office or workflow-edge foothold, and demand a P&L-linked measure.

**Gartner, agentic AI** (press release 25 June 2025). "Over 40% of agentic AI
projects will be canceled by the end of 2027, due to escalating costs,
unclear business value or inadequate risk controls"; current projects are
"mostly driven by hype and are often misapplied". Use "AI agents when
decisions are needed, automation for routine workflows and assistants for
simple retrieval". A forecast.
[Press release](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027).
**Apply here:** the brief must say why an agent (a decision under
uncertainty) beats a rule or a retrieval assistant; cost ceiling and risk
controls are selection criteria.

**RAND, "The root causes of failure for AI projects"** (13 August 2024; 65
data scientists and engineers interviewed; page blocked, causes confirmed
across summaries). Five causes: the problem is misunderstood or
miscommunicated; inadequate data; technology focus over the problem;
insufficient infrastructure; a problem unsuitable for AI. The "over 80
percent fail" figure is RAND citing prior estimates.
[Report](https://www.rand.org/pubs/research_reports/RRA2680-1.html).
**Apply here:** three of five causes are discovery failures; record who
stated the problem and who agreed.

**McKinsey, "The state of AI in 2025"** (5 November 2025; 1,993
participants, 25 June to 29 July 2025; page timed out, figures from
McKinsey-domain search results). 39 percent "attribute any level of EBIT
impact to AI", mostly under 5 percent; high performers (about 6 percent)
attribute 5 percent or more, are "nearly three times as likely" to have
"fundamentally redesigned individual workflows", and more often set growth or
innovation objectives. An August 2026 edition ("On the road to ROI") exists
and should be read before relying on this.
[Report](https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/the-state-of-ai-2025).
**Apply here:** describe the redesigned workflow, not an overlay; allow a
growth KPI, not only cost.

**Google Cloud ROI of AI study** (4 September 2025; 3,466 leaders already
using gen AI). 74 percent report first-year ROI; 52 percent use agents; top
agent areas are customer service (49 percent), marketing, security
operations (46 percent each) and tech support (45 percent).
Vendor-commissioned, adopters only.
[Press release](https://www.googlecloudpresscorner.com/2025-09-04-Google-Cloud-Study-Reveals-52-of-Executives-Say-Their-Organizations-Have-Deployed-AI-Agents,-Unlocking-a-New-Wave-of-Business-Value,1).
**Apply here:** cite only for where agents are commonly placed.

### 4. Finding friction in an existing journey

**Google HEART, Goals-Signals-Metrics** (Rodden, Hutchinson, Fu, CHI 2010).
"The first step is identifying the goals", then "signals that indicate
success", then metrics; "choose signals that are sensitive and specific to
the goal"; "sometimes failure is easier to identify than success (e.g.
abandonment of a task, 'undo' events, frustration)"; ask "are the relevant
actions currently being logged, or could they be?".
[Paper](https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/).
**Apply here:** start the friction search from failure signals (abandonment,
rework, undo, repeat contact) and confirm they are logged.

**Jobs to be Done** (Christensen et al., HBR, September 2016; abstract).
Customers "hire" products for "the progress that the customer is trying to
make in a given circumstance".
[Article](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done).
**Apply here:** phrase the user's job before the feature, so the agent is
judged on progress.

**Process mining** (IEEE Process Mining Manifesto, 2011). Discover "real
processes (i.e., not assumed processes)" from event logs; task mining extends
to desktop activity. Vendor automation-candidate claims are unvalidated.
[Manifesto](https://tfpm.compute.dtu.dk/resources/manifesto).
**Apply here:** where ERP, CRM or ticket logs exist, pull cycle time and
rework per step before interviewing; otherwise time a handful of cases by
hand. Contact-driver analysis (grouping support contacts by root reason) is
widespread practitioner practice with no primary study found; treat it as a
data source, not evidence.

### 5. Defining the outcome

**Kohavi, Tang, Xu, Trustworthy Online Controlled Experiments** (Cambridge,
2020; chapter abstracts). Goal metrics capture ultimate success but move
slowly; driver metrics are sensitive leading indicators; guardrail metrics
"protect against unintended harm" and must not degrade even when the primary
metric improves.
[Book](https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/).
**Apply here:** every brief carries one goal metric, one or two driver
metrics the agent can move within weeks, and at least one guardrail (refund
rate, complaint rate, error rate, cost per task).

**Impact Mapping** (Adzic, 2012). Why (measurable goal), who (actors), how
(behaviour change), what (deliverable), each link an assumption.
[Site](https://www.impactmapping.org/).
**Apply here:** this is the hypothesis chain: "less effort for actor X on
step Y, so more of behaviour Z, so KPI W moves"; record each arrow as an
assumption the pilot tests.

## Proposed discovery brief

1. **Business and KPI.** What the company sells, the two or three KPIs the
   sponsor answers for, their current value and trend.
2. **Domain and journey.** One customer journey or function, its steps,
   owners and systems of record.
3. **Friction evidence.** Per step: volume, cycle time, abandonment or
   rework, repeat contacts, where people wait, re-key or ask a colleague; the
   data source for each and whether it is logged today.
4. **Candidate workflows (three at most)** as activity plus expected result,
   with frequency, sorted on value, feasibility, data readiness, risk
   (irreversibility, regulation, PII), change cost and time to value.
5. **The first workflow.** Why this one (Ng's tests), why an agent rather
   than a rule or retrieval (Gartner's test), automate or augment (PAIR's
   test), and what changes for the people in it.
6. **Outcome definition.** Impact map, goal metric, driver metrics,
   guardrail metrics, baseline with measurement window, target with units,
   and the threshold sentence that triggers action.
7. **Readiness and risk.** Data owners and access, consent and retention,
   decision rights, cost ceiling, approval points for irreversible actions.
8. **90-day plan and press release.** What ships, how it is measured, who
   reads the result, and the improved journey in the customer's words.

## Discovery interview question bank

- **What does the business sell, to whom, and which KPI is the sponsor judged
  on this year?** Fixes the goal metric everything else is scored against.
- **Walk me through one real case from first contact to money received. Where
  did it wait, bounce back or need re-keying?** Locates friction in observed
  work, not the assumed process (RAND, process mining).
- **Who does this step today and how often?** Sets frequency and the role
  whose metric moves (Bain); rules out trivial or rare tasks (Ng).
- **Which system owns the facts the agent needs, and can we get them today?**
  Data readiness gates every framework; no owner, no use case.
- **What happens when the answer is wrong, and can it be undone?** Decides
  augment versus automate, confirmation points, and whether an agent fits
  (PAIR, Gartner).
- **Must the same input give the same output every time?** Chooses
  deterministic logic over a generative agent (Microsoft).
- **Who decides this today, and what do they look at first?** Separates a
  decision (agent) from routine automation or retrieval.
- **Where does the current process lose context between steps?** NANDA's
  learning gap; defines the memory and integration the agent needs.
- **What is the baseline number now, and how do you know?** Forces the
  characterise rewrite; if nobody can answer, measurement precedes building.
- **Which number must not get worse?** Produces the guardrail metric.
- **What would make you cancel this in six months?** Surfaces cost ceiling,
  risk controls and the real value question (Gartner's three reasons).
- **Who else must change how they work for this to count?** Sizes the
  people-and-process share (BCG) and the sponsor needed.
- **What does success look like in 90 days, in a sentence a customer would
  recognise?** Produces the press-release paragraph and a time-boxed test.
