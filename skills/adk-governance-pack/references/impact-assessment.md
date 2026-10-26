# AI system impact assessment

Read when writing the impact assessment. It records who the system affects
and how, beyond the client organisation's own risk, and what the design
does about each impact. It is organised along ISO/IEC 42005 and mapped to
the NIST AI Risk Management Framework so either kind of reviewer can read it.

## Sources and their status (read 25 October 2026)

- **ISO/IEC 42005:2025**, *AI system impact assessment*, first edition
  published 27 May 2025 (metadata from the Standards Council of Canada
  record <https://scc-ccn.ca/standardsdb/standards/8188107>). iso.org could
  not be opened; the topic headings below are paraphrased from ISO's public
  abstract and a law-firm summary, not from the standard. The text is
  copyrighted: use these headings in your own words and tell the client
  that conformity needs their own copy. ISO/IEC 42001:2023 clause 6.1.4
  (an AI system impact assessment process in an AI management system) is
  likewise secondary-only here.
- **NIST AI RMF 1.0** (NIST AI 100-1, January 2023,
  <https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf>), read. Four
  functions with 19 categories: Govern (6), Map (5), Measure (4), Manage
  (4). NIST's page says 1.0 is being revised; no new version was published
  on the read date.
- **NIST AI 600-1**, *Generative AI Profile* (July 2024,
  <https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf>), read. Twelve
  risks; suggested actions keyed like `GV-1.1-001` (function, subcategory,
  sequence; GV, MP, MS, MG). Not superseded on the read date.

## Structure (ISO/IEC 42005 topics, own words)

| Template section | What goes in it | Where the record holds it |
| --- | --- | --- |
| Scope and intended use | System description, functions, intended and unintended uses, the organisation's role, the lifecycle stage and the trigger for this assessment | Brief §4; design purpose and contracts; regulatory memo |
| Interested parties | People affected directly and indirectly, including vulnerable groups and people who never use the system (applicants, customers named in records) | Brief stakeholders and harms |
| System information | Data (sources, quality, provenance), model and algorithm (pinned model, what code decides), deployment environment | Design data and authority table, D-IDs, model lifecycle row |
| Impacts | Actual and reasonably foreseeable benefits and harms per party, with likelihood and severity | Brief harms and cost of a wrong answer; M and I records; failure review |
| Measures | Controls per harm, each as a contract or security rule with its evidence status | C and SB IDs with plan evidence |
| Residual risk and decision | What remains after measures, who accepts it, and the conditions that end acceptance | Design accepted risks and deferred controls |
| NIST AI RMF mapping | The same content indexed by function and GenAI risk | This file |
| Monitoring and review | Measures in operation, owners, review triggers (model change, new user group, new data, incident, change in law) | Observability SLIs; release triggers; I records |

Assess at design, before the production decision, and again on a
significant change. The trigger for this run is a fact with an ID (the
production-approval goal, a model migration, a new market).

## Map to NIST AI RMF functions

| Function | What the pack shows | Evidence to cite |
| --- | --- | --- |
| Govern | Roles and accountability (provider, deployer, owner), policies the system follows, who accepts residual risk, AI literacy measures | Regulatory memo roles; design owners; accepted risks |
| Map | Context, intended purpose, affected parties, regimes and categorisation (jurisdiction screen; AI Act where the EU is in scope), benefits and costs, limits of knowledge | Impact assessment scope and parties; regulatory memo; brief §1 and §4 |
| Measure | Evaluation methods and results, bias and robustness tests, what is not yet measured | M records, evaluation reports, acceptance cases by G/A ID |
| Manage | Controls, incident response, monitoring, decommissioning, third-party (model provider) risk | C and SB evidence; I records; release and rollback decisions |

## GenAI profile risks for an agent

Mark each risk applicable or `n/a:` with a reason; cite the measure.

| NIST AI 600-1 risk | Typical agent exposure | Typical measure in this toolkit |
| --- | --- | --- |
| CBRN information or capabilities | Open-ended assistants | Model provider safety filters; scope instruction; usually n/a for narrow tools |
| Confabulation | Answers about policy, eligibility, facts on a person | Grounding with citation contracts; refusal path; evaluation on gold cases |
| Dangerous, violent or hateful content | Public chat | Content screening (Model Armor) at release |
| Data privacy | Personal data in prompts, memory, logs, training | Sensitive-data controls; retention contracts; privacy impact input pack |
| Environmental impacts | Large volumes, large models | Model choice and token budgets; usually noted, not measured |
| Harmful bias or homogenisation | Decisions about people, ranking, scoring | Adverse-impact measurement; removed proxies; human review |
| Human-AI configuration | Over-reliance, automation bias, unclear disclosure | Disclosure contract; review points; reviewer sampling |
| Information integrity | Published or customer-facing text | Editorial review; Article 50 marking decision |
| Information security | Prompt injection, tool misuse, data exfiltration | Security baseline rules SB10, SB12, SB17, SB18; adversarial suite |
| Intellectual property | Generated content, retrieved third-party text | Source licensing; citation; provider indemnity terms |
| Obscene, degrading or abusive content | Image or open text generation | Screening; usually n/a for text tools on internal data |
| Value chain and component integration | Model provider, MCP servers, retrieval sources | Pinned model and lifecycle date; MCP allowlist; sub-processor list |

## Regime additions

Keep each optional section of the template whose condition holds, and add
the rows the regime asks for. Sources read 26 October 2026 (see
[Australia](australia.md), [United States](united-states.md),
[United Kingdom](united-kingdom.md) and [EU AI Act](eu-ai-act.md)).

- **Adverse impact and equality** (any regime, when the system ranks,
  scores or decides about people): selection or outcome rates by group,
  the ratio to the highest group, the statistical test and sample, proxies
  removed (postcode, name, age signals, language), less discriminatory
  alternatives and the accessibility route. NYC Local Law 144, California's
  FEHA regulations (anti-bias testing is evidence for or against a claim),
  Title VII, the UK Equality Act and Australian anti-discrimination law all
  turn on it, and it is the input to a client's bias audit or, for a UK
  public body, its equality impact assessment. A measured disparity is
  reported with its M ID, never omitted; whether it is justified is
  `counsel:`.
- **NIST AI 600-1 actions** (`us`, and Texas residents in particular):
  Texas TRAIGA gives no liability for a violation found through red-teaming
  or an internal review substantially complying with the Generative AI
  Profile (§552.105(e)). Record the suggested-action IDs actually performed
  and the red-team results; cite AI 600-1 as the most recent version with
  its date.
- **Australia: Guidance for AI Adoption mapping** (`au`, private clients):
  the National AI Centre's six practices, voluntary, published 21 October
  2025. Map at least practices 1 to 3 (decide who is accountable;
  understand impacts and plan accordingly; measure and manage risks).
  Clause 3.1.3 names "data sheets, model cards, or system cards", which the
  system card answers, and clause 2.2 covers contestability.
- **Australia: DTA AI impact assessment inputs** (`au`, non-corporate
  Commonwealth entity): the threshold facts for sections 1 to 4 of the DTA
  tool, the use-case owner and the assessing and approving officers, the
  transparency statement inputs and an AGT.1 to AGT.8 conformance list. The
  agency's officers complete the assessment, due for in-scope use cases by
  15 December 2026 (checked 2026-10-26).
- **EU: FRIA crosswalk** (`eu`, Article 27 deployer): Article 27(1)(a) to
  (f) mapped to pack sections, so the FRIA can cross-reference the DPIA as
  Article 27(4) allows.
- **UK rows:** Consumer Duty outcomes for FCA-authorised clients; the ICO's
  ten agentic risks live in the input pack's risk table.
- **Consumer claims** (`au` and `uk` consumer-facing agents): refund,
  guarantee and retention flows reviewed against the Australian Consumer Law
  and the CMA's AI-agent guidance.

## Judgement the drafter leaves open

Likelihood and severity are provisional until the client's risk owner
scores them: write `assumption:` with the basis. The residual-risk decision
names the person who accepts it; until they do, write
`counsel:` or `gap: acceptance by <role>`. A harm with no measure is a gap
and a proposed goal for the specialist that owns the control.
