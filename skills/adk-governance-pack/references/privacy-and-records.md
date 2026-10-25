# DPIA inputs and records of processing

Read when writing the DPIA input pack or the records-of-processing rows.
The client, as controller, owns the DPIA and the register; its DPO advises
and signs. The pack supplies the facts the design records, in the order the
DPO needs them, and turns every legal judgement into a `counsel:` question.

Sources, all read 25 October 2026: the GDPR (Regulation (EU) 2016/679,
<https://eur-lex.europa.eu/eli/reg/2016/679/oj>, Official Journal text);
WP29 *Guidelines on DPIA* WP248 rev.01, revised 4 October 2017 and endorsed
by the EDPB (<https://ec.europa.eu/newsroom/article29/items/611236>); EDPB
Opinion 28/2024 on AI models, adopted 17 December 2024
(<https://www.edpb.europa.eu/our-work-tools/our-documents/opinion-board-art-64/opinion-282024-certain-data-protection-aspects_en>);
the Google Cloud pages named below. A GDPR amendment through the Digital
Omnibus was reported as still under negotiation on that date (secondary
sources only); treat Articles 6, 22, 30 and 35 as unamended unless the
Official Journal shows otherwise, and say so in the pack with the date.

## Screening: is a DPIA needed?

Article 35(1) requires a DPIA where processing, "in particular using new
technologies", is likely to result in a high risk to people's rights and
freedoms. Article 35(3) names three cases: systematic and extensive
evaluation including profiling with legal or similarly significant effects;
large-scale special-category or criminal data; large-scale monitoring of
public areas. WP248 adds nine criteria; meeting two usually means a DPIA is
required, and sometimes one is enough:

1. Evaluation or scoring, including profiling and predicting.
2. Automated decision-making with legal or similarly significant effect.
3. Systematic monitoring.
4. Special-category or highly personal data.
5. Large scale (number of people, volume, duration, geography).
6. Matching or combining datasets.
7. Vulnerable data subjects: children, employees, patients, any power imbalance.
8. Innovative use or new technological solutions.
9. Processing that prevents people from exercising a right or using a service or contract.

An agent on a generative model usually meets criterion 8, and any system
used on employees meets 7, so most internal-tool agents touching staff data
reach two criteria. Supervisory authorities also publish national lists
(Article 35(4)); name the client's lead authority and leave the list check
to counsel. Write the screening result as `counsel:`; the DPO decides.

## Map the design into the DPIA's required contents

Article 35(7) requires at least: (a) a systematic description of the
processing and its purposes, including any legitimate interest; (b) necessity
and proportionality; (c) the risks to data subjects; (d) the measures,
safeguards and security mechanisms. The template's sections follow it:

| Article 35(7) | Pack section | Draw from |
| --- | --- | --- |
| (a) description and purposes | Processing description, Data flows, Data subjects and categories | Brief §4 data register and workflow; design data-and-authority table; D-IDs for stores, regions and model endpoint |
| (a) legitimate interest | Legal basis | `counsel:` prompts with the facts that bear on the three-step test |
| (b) necessity and proportionality | Necessity and proportionality, Retention and erasure | Contracts that minimise (removed fields, scoped reads), retention contracts, erasure paths |
| (c) risks | Risks and measures | Brief harms; failure review; I records |
| (d) measures | Risks and measures; Recipients, processors and regions | C and SB IDs with evidence status; sensitive-data controls |

Trace one data flow per path the personal data takes: user input, model
request, tool calls, session and memory stores, logs and traces, evaluation
datasets, backups. A flow the design does not record is a `gap:`, not a
guess. `protect-adk-sensitive-data` evidence (what is masked or rejected
before storage and the model, with its measured detector coverage) is cited
as the measure; write the measured coverage, not "PII is removed".

Article 35(9) asks for data subjects' views where appropriate (for staff,
often the works council or employee representatives); Article 35(11)
requires review when the risk changes. Article 36 requires prior
consultation with the supervisory authority when the DPIA shows a high
residual risk; the authority has up to eight weeks, extendable by six. Both
are calendar waits in the plan.

## Legal basis, special categories and automated decisions

Write candidate bases as questions with the facts beside them; never state
the basis as settled.

- Article 6(1): consent, contract, legal obligation, vital interests,
  public task, legitimate interests. For employees, consent is rarely
  freely given; counsel decides.
- Article 9: special categories (racial or ethnic origin, political
  opinions, religious or philosophical beliefs, trade union membership,
  genetic data, biometric data for unique identification, health, sex life
  or sexual orientation) need a condition. Free-text chat collects them
  whether or not the design asks for them; cite the masking contract and
  its measured coverage.
- Article 22: a decision based solely on automated processing with legal or
  similarly significant effects. Record where a person decides (contract
  ID) and what share of outputs they review (M record); "a human is in the
  loop" without a review rate is not a fact.
- AI Act Article 4a (Omnibus) offers a basis for special-category data used
  to detect and correct bias; see [the AI Act reference](eu-ai-act.md).

## Model provider data use

For Gemini models on Google Cloud (Vertex AI, renamed Gemini Enterprise
Agent Platform; the `aiplatform` APIs remain), these pages were read on 25
October 2026, last updated 22 October 2026:

- Zero data retention:
  <https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/zero-data-retention>.
  Google does not use customer data to train or fine-tune models without
  permission or instruction. Implicit caching is on by default (in memory
  and durable, each deleted within 24 hours) and can be disabled per project
  with `disableCache`. Grounding with Google Search keeps logs up to 3 days
  and Grounding with Google Maps 30 days, neither switchable off; request-
  response logging to BigQuery is off by default; regional endpoints keep
  cached data in location, the global endpoint does not guarantee it.
- Abuse monitoring:
  <https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/abuse-monitoring>.
  For standard Google models, prompts flagged by classifiers can be stored
  up to 90 days in the project's region and may be reviewed by people;
  some model families log all prompts and responses for up to 30 days.
  Customers under a Cloud Master Agreement are exempt by default from some
  of this; others ask their account team.
- Sub-processors: <https://cloud.google.com/terms/subprocessors> (last
  modified 19 October 2026). Cloud Data Processing Addendum:
  <https://cloud.google.com/terms/data-processing-addendum> (Google as
  processor; deletion, locations, sub-processor objection, transfer
  mechanisms).

The pack states what the design configured (regional endpoint, caching
setting, grounding source, model family) with D-IDs and cites these pages
with the date read; whether the client's agreement exempts it from abuse
logging is a `counsel:` or account-team question. Re-read the pages when the
date is old: they changed name and content during 2026.

EDPB Opinion 28/2024 matters when the client deploys a model trained by
someone else on personal data: a deployer makes an accountability
assessment, scaled to the risk, that the model was not developed unlawfully,
and a model is anonymous only if both extracting training data and
obtaining it through queries are insignificantly likely. For a Gemini model
the client relies on the provider's documentation; write that reliance as a
`counsel:` item, not as a finding. When the project fine-tunes or trains on
personal data, the opinion's legitimate-interest test applies to that step
directly.

## Records of processing (Article 30)

The controller's record (Article 30(1)) holds: (a) controller, joint
controller, representative and DPO contacts; (b) purposes; (c) categories of
data subjects and personal data; (d) categories of recipients, including in
third countries; (e) third-country transfers and safeguards; (f) erasure
time limits where possible; (g) a general description of security measures
where possible. A processor keeps its own record (Article 30(2)) per
controller. The under-250-staff exemption does not apply to processing that
is not occasional, is risky or includes special categories (Article 30(5)),
so agent processing is almost always recorded.

Write one row per purpose in the client's words, not one per component;
the security column cites SB and C IDs; the erasure column cites the
retention contract. The rows go to the DPO for the client's existing
register; the agency does not keep the register.
