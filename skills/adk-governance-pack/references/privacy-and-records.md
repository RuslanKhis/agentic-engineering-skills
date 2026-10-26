# Privacy assessments, transfers and records

Read when writing the privacy impact input pack, the records-of-processing
rows or the transfer assessment annex. One input pack serves every regime the
[jurisdiction screen](jurisdiction-screen.md) found in scope: the Australian
privacy impact assessment (PIA), the EU and UK data protection impact
assessment (DPIA), and the US data protection or risk assessment. The client
owns each assessment and any register; its DPO or privacy officer advises and
signs. The pack supplies the facts the design records, in the order the
reviewer needs them, and turns every legal judgement into a `counsel:`
question. It never assumes GDPR applies: the regime sections follow
`jurisdictions:`.

Sources, read 25 October 2026 and re-read for the EU changes on 26 October
2026: the GDPR (Regulation (EU) 2016/679,
<https://eur-lex.europa.eu/eli/reg/2016/679/oj>, Official Journal text);
WP29 *Guidelines on DPIA* WP248 rev.01, revised 4 October 2017 and endorsed
by the EDPB (<https://ec.europa.eu/newsroom/article29/items/611236>); EDPB
Opinion 28/2024 on AI models, adopted 17 December 2024
(<https://www.edpb.europa.eu/our-work-tools/our-documents/opinion-board-art-64/opinion-282024-certain-data-protection-aspects_en>);
*SCHUFA* (C-634/21) and *Dun & Bradstreet Austria* (C-203/22) on EUR-Lex;
the EDPB's news item on the Dutch DPA's Uber decision; the Commission's
adequacy and EU-US data transfer pages; SCC Decision (EU) 2021/914;
*Latombe* (T-553/23); *EDPS v SRB* (C-413/23 P); EDPB Guidelines 02/2026,
01/2025 and 07/2020 and Recommendations 01/2020; the Google Cloud pages named
below. Australian, US and UK sources are listed in [Australia](australia.md),
[United States](united-states.md) and [United Kingdom](united-kingdom.md),
all read 26 October 2026.

The GDPR and ePrivacy amendments in the Digital Omnibus (procedure
2025/0360(COD), proposal COM(2025) 837 of 19 November 2025) were not
law on 26 October 2026. Parliament's committee stage was "Awaiting
committee decision"
(<https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file?reference=2025/0360(COD)>,
read 2026-10-26). The Council's mandate was reported agreed on 21
October 2026 (secondary only); no trilogue had started. The proposal
touches Articles 4(1), 9, 12, 13, 22, 33, 35 and new 88a to 88c, and
ePrivacy Article 5(3). Treat all of them as unamended unless the
Official Journal shows otherwise, and say so in the pack with the date.
UK GDPR is a separate text, amended by the Data (Use and Access) Act 2025;
the EU Omnibus caveat does not apply to it.

## Which assessment, under which regime

| Regime | The client's assessment | When it is required | Pack sections that feed it |
| --- | --- | --- | --- |
| Australia | PIA along the OAIC's ten steps | Required for Australian Government agencies on high privacy risk projects; recommended for everyone else | Common sections; "Australia: APP compliance check"; "Australia: Inventory and notice inputs" |
| United States | CPPA risk assessment (California) and state data protection assessments | Before the in-scope processing each law lists | Common sections; "United States: Notice, consent and opt-out"; "United States: Assessment approval" |
| EU | DPIA, GDPR Article 35 | Likely high risk; Article 35(3) cases; national lists | Common sections; "EU: Legal basis" |
| United Kingdom | DPIA, UK GDPR Article 35, with the ICO list | As the EU, with the ICO's list | Common sections; "United Kingdom: Lawful basis and ADM safeguards" |

## Screening: is an assessment needed?

**EU and UK.** Article 35(1) requires a DPIA where processing, "in particular
using new technologies", is likely to result in a high risk to people's
rights and freedoms. Article 35(3) names three cases: systematic and
extensive evaluation including profiling with legal or similarly significant
effects; large-scale special-category or criminal data; large-scale
monitoring of public areas. WP248 adds nine criteria; meeting two usually
means a DPIA is required, and sometimes one is enough:

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
to counsel. The Omnibus proposes single EU-level lists, and the EDPB's
2026-2027 work programme plans an EU DPIA template; neither existed on 26
October 2026. For the UK, screen the ICO's ten-item list beside WP248 (see
[United Kingdom](united-kingdom.md)). Write the screening result as
`counsel:`; the DPO decides.

**Australia.** Use the OAIC threshold assessment: does the project involve
new or changed ways of handling personal information? For an agency, record
the s 12 high-privacy-risk conclusion as `counsel:`.

**United States.** Screen CPPA §7150(b) (selling or sharing; sensitive
personal information; ADMT for a significant decision; inference from
systematic observation of applicants, students, employees or contractors;
training ADMT or biometric identification) and, for each other state whose
threshold the client meets, its data protection assessment triggers
(targeted advertising, sale, sensitive data, risky profiling).

## Map the design into the assessment's contents

Article 35(7) requires at least: (a) a systematic description of the
processing and its purposes, including any legitimate interest; (b) necessity
and proportionality; (c) the risks to data subjects; (d) the measures,
safeguards and security mechanisms. The template's common sections follow it,
and also cover the OAIC's steps 3 to 7 and the CPPA §7152 content:

| Contents | Pack section | Draw from |
| --- | --- | --- |
| Description and purposes (Art 35(7)(a); OAIC step 3; §7152 purpose, categories, approximate number of consumers) | Processing description, Data flows, Data subjects and categories | Brief §4 data register and workflow; design data-and-authority table; D-IDs for stores, regions and model endpoint |
| Lawful basis, collection or notice | The regime sections: EU legal basis; UK lawful basis; APP 3, 5 and 6; US notice, consent and opt-out | `counsel:` prompts with the facts |
| Necessity and proportionality | Necessity and proportionality, Retention and erasure | Contracts that minimise (removed fields, scoped reads), retention contracts, erasure paths |
| Risks (Art 35(7)(c); OAIC step 6; §7152 negative impacts) | Risks and measures | Brief harms; failure review; I records; for the UK, the ICO's ten agentic risks |
| Measures (Art 35(7)(d); OAIC step 7; §7152 safeguards) | Risks and measures; Recipients, processors and regions | C and SB IDs with evidence status; sensitive-data controls |
| Approval (§7152: whether the business will proceed; approver's name, position and date) | United States: Assessment approval | Named by the client; a `gap:` until they are |

Trace one data flow per path the personal data takes: user input, model
request, tool calls, session and memory stores, logs and traces, evaluation
datasets, backups, and consultancy access for support. A flow the design
does not record is a `gap:`, not a guess. `protect-adk-sensitive-data`
evidence (what is masked or rejected before storage and the model, with its
measured detector coverage) is cited as the measure; write the measured
coverage, not "PII is removed". Record per store whether it can be searched
by person: UK subject access is limited to a reasonable and proportionate
search, Australian access requests reach memory and logs, and every regime's
erasure or deletion right needs the path.

Article 35(9) asks for data subjects' views where appropriate (for staff,
often the works council or employee representatives); Article 35(11)
requires review when the risk changes. Article 36 requires prior
consultation with the supervisory authority (in the UK, the Information
Commission) when the DPIA shows a high residual risk; the authority has up
to eight weeks, extendable by six. Both are calendar waits in the plan.
Australia has neither: the nearest are award and enterprise agreement
consultation terms and workplace surveillance notices.

## Lawful basis, collection and consent, by regime

Write candidate bases as questions with the facts beside them; never state
the basis as settled.

- **EU, Article 6(1):** consent, contract, legal obligation, vital interests,
  public task, legitimate interests. For employees, consent is rarely
  freely given; counsel decides.
- **EU and UK, Article 9:** special categories (racial or ethnic origin,
  political opinions, religious or philosophical beliefs, trade union
  membership, genetic data, biometric data for unique identification,
  health, sex life or sexual orientation) need a condition. Free-text chat
  collects them whether or not the design asks for them; cite the masking
  contract and its measured coverage.
- **UK additions:** Article 6(1)(ea) recognised legitimate interests with an
  Annex 1 condition; the Article 6(11) examples (direct marketing,
  intra-group administration, network and information security); Article 8A
  for re-use. See [United Kingdom](united-kingdom.md).
- **Australia: no lawful-basis test.** Never write a GDPR basis in an
  Australian section. The analysis runs APP 3 (reasonably necessary;
  consent for sensitive information under 3.3; generated or inferred
  information is collected), APP 5 (notice) and APP 6 (primary purpose and
  the secondary-use exceptions). See [Australia](australia.md).
- **United States:** no lawful-basis test either. Record notice, opt-in
  consent for sensitive data (California: the right to limit), and the
  opt-outs each state gives. See [United States](united-states.md).
- AI Act Article 4a (Omnibus) permits special-category data for bias
  detection only where strictly necessary and under all its conditions,
  in addition to the GDPR; the records of processing must state why. See
  [the AI Act reference](eu-ai-act.md). It has no UK equivalent: for UK
  bias monitoring, prompt counsel on an Article 9 condition.

## Automated decisions, by regime

The input pack's "Automated decisions" section records the facts once; each
regime reads them differently. Never let a recorded reviewer stand in for a
conclusion: "a human is in the loop" without the review share and override
rate is not a fact.

- **EU, Article 22:** a decision based solely on automated processing with
  legal or similarly significant effects is prohibited in principle unless
  Article 22(2) applies (*SCHUFA*, C-634/21, 7 December 2023). An
  automated score or ranking is itself the decision when the person
  using it "draws strongly on" it. Record where a person decides
  (contract ID), what share of outputs they review and how often they
  depart from the output (M records). "A human is in the loop" without
  those rates is not a fact. Where Article 22 applies, the notice must
  say so and give meaningful information about the logic (Articles
  13(2)(f), 14(2)(g)). On request, Article 15(1)(h) requires an
  explanation of "the procedure and principles actually applied", not a
  formula (*Dun & Bradstreet Austria*, C-203/22, 27 February 2025).
  Write the explanation the design can produce (features used, a
  counterfactual) and its owner. The Dutch DPA fined Uber EUR 824.99
  million on 8 October 2026 for fully automated deactivations and an
  inadequate notice. For Annex III high-risk systems, AI Act Article 86
  adds a deployer duty to explain; see [the AI Act
  reference](eu-ai-act.md).
- **UK, Articles 22A to 22D:** permitted on any lawful basis with the
  Article 22C safeguards (information, representations, human
  intervention, contest), except where special category data is used
  (Article 22B) or the basis is a recognised legitimate interest. "Solely"
  means no meaningful human involvement, and the ICO's draft says ad hoc
  spot-checking is not enough. See [United Kingdom](united-kingdom.md).
- **Australia, APP 1.7 to 1.9 from 10 December 2026 (checked 2026-10-26):**
  wider than Article 22. It covers a program that does "a thing that is
  substantially and directly related to making" a decision, and the OAIC
  says generative AI outputs in significant decisions are generally in
  scope unless subject to "extensive human oversight and control". It
  requires privacy-policy entries, not a prohibition. See
  [Australia](australia.md).
- **United States:** CPPA ADMT (a reviewer who can interpret the output,
  reviews it with other information and has authority to change the
  decision takes it out), Colorado SB 26-189 notices and explanations, and
  state profiling opt-outs. See [United States](united-states.md).

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

The pack states what the design configured (regional endpoint, the model's
processing region as the model page lists it, caching setting, grounding
source, model family) with D-IDs and cites these pages with the date read;
whether the client's agreement exempts it from abuse logging is a `counsel:`
or account-team question. Re-read the pages when the date is old: they
changed name and content during 2026. For Australia, these facts decide the
APP 8 use-or-disclosure question; for the UK, whether Google is a controller
for any part (for example abuse monitoring) is `counsel:` under the ICO's
generative AI positions.

EDPB Opinion 28/2024 matters when the client deploys a model trained by
someone else on personal data: a deployer makes an accountability
assessment, scaled to the risk, that the model was not developed unlawfully,
and a model is anonymous only if both extracting training data and
obtaining it through queries are insignificantly likely. For a Gemini model
the client relies on the provider's documentation; write that reliance as a
`counsel:` item, not as a finding. When the project fine-tunes or trains on
personal data, the opinion's legitimate-interest test applies to that step
directly.

Whether data is anonymous is assessed per entity. EDPB Guidelines
02/2026 (in consultation from July 2026) test record isolation, linkage
and inference. Pseudonymised data can be anonymous for a recipient who
cannot re-identify it while remaining personal data for the controller
(*EDPS v SRB*, C-413/23 P, 4 September 2025). Write "pseudonymised" for
evaluation sets unless the test has been run, and erase from memory,
vector stores and backups rather than "anonymising" on request (EDPB
right-to-erasure report, 18 February 2026).

## International transfers and overseas disclosure

Write one row per recipient in the input pack's recipients table, and one
row per restricted transfer in the
[transfer assessment annex](../assets/transfer-assessment-annex-template.md)
when `eu` or `uk` is in scope. The conclusions are counsel's.

**EU (Chapter V).** Australia has no adequacy decision. When agency staff
outside the EEA view or handle the client's personal data (support, logs and
traces, evaluation sets, incidents), that is a transfer. It needs Standard
Contractual Clauses (Decision (EU) 2021/914: Module 2 client to agency,
Module 3 agency to its sub-processors) and a transfer impact assessment
under EDPB Recommendations 01/2020. Name the module, the exporter and
the assessment reference in the recipients table; a missing assessment
is a `gap:`. The same applies to any model endpoint, grounding service,
abuse-monitoring store or telemetry sink outside the EEA. US recipients
may rely on the EU-US Data Privacy Framework (adequacy decision of 10
July 2023) if certified for the data type; check the certification and
write the date. The General Court upheld the framework on 3 September
2025 (T-553/23). An appeal is pending (C-703/25 P), and the US Supreme
Court's *Trump v. Slaughter* (29 June 2026) removed the FTC's
independence that the decision relies on. Whether SCCs should back up
DPF transfers is `counsel:`. Treat the DPF as valid but fragile.

**UK (Articles 44A to 47A).** There are no UK adequacy regulations for
Australia. Australian staff or systems accessing UK personal data is a
restricted transfer needing the IDTA or the Addendum and a documented data
protection test ("not materially lower"). US recipients may rely on the UK
Extension to the Data Privacy Framework if certified. Every UK pack starts
with a transfer row for consultancy access from Australia, marked `n/a:`
only when the design shows no access.

**Australia (APP 8 and s 16C).** For Australian personal information leaving
Australia (a model endpoint, log sink, grounding service or support desk
offshore), record the use-or-disclosure facts (the contract terms, effective
control, the region) in the recipients table; APP 8.1 reasonable steps and s
16C liability follow a disclosure. No countries are prescribed under APP 8.3.
My Health Record information may not be processed outside Australia at all.

**United States.** State privacy laws follow residents, not servers; US
transfer questions arise only for EU, UK or Australian data, above.

## Processor terms (Article 28)

List each processor and sub-processor with its contract reference: the
agency during build and support, the cloud provider under its Data
Processing Addendum, and any tool or MCP provider that receives
personal data. Article 28(3) terms (instructions, confidentiality,
security, sub-processor approval, assistance, deletion or return,
audits) are counsel's to check; the pack records what exists. A tool
provider that uses the data for its own purposes may be a separate
controller (EDPB Guidelines 07/2020).

In Australia there is no processor category: the consultancy is an APP
entity in its own right unless exempt, and a Commonwealth client flows the
APPs down by contract (s 95B). In the US, service provider and processor
contracts carry the statutory terms, including assistance with the client's
assessments (CPPA §7050(h) for California).

## Records of processing (Article 30)

Written only when `eu` or `uk` is in scope. The controller's record (Article
30(1)) holds: (a) controller, joint controller, representative and DPO
contacts; (b) purposes; (c) categories of data subjects and personal data;
(d) categories of recipients, including in third countries; (e)
third-country transfers and safeguards; (f) erasure time limits where
possible; (g) a general description of security measures where possible. A
processor keeps its own record (Article 30(2)) per controller. The
under-250-staff exemption does not apply to processing that is not
occasional, is risky or includes special categories (Article 30(5)), so
agent processing is almost always recorded. UK GDPR Article 30 is unchanged
in substance; name the UK transfer mechanism (adequacy regulation, IDTA,
Addendum, Article 49) and add the "solely automated significant decision"
column.

Write one row per purpose in the client's words, not one per component;
the security column cites SB and C IDs; the erasure column cites the
retention contract. The rows go to the DPO for the client's existing
register; the agency does not keep the register. A row that uses
special-category data for bias detection under AI Act Article 4a states
why it was strictly necessary (Article 4a(1)(f)).

**Australia** has no Article 30 register. The input pack's "Australia:
Inventory and notice inputs" section replaces it, feeding the APP 1.4
privacy policy, the APP 5 notice and, from 10 December 2026, the APP 1.8
entries. **The United States** has no register either; Minnesota requires a
data inventory and a named privacy lead (Minn. Stat. 325M.18), which the
data-flow rows serve. Keep governance records as long as each law requires:
CPPA risk assessments five years, FEHA automated-decision data four years,
Colorado SB 26-189 records three years (checked 2026-10-26).
