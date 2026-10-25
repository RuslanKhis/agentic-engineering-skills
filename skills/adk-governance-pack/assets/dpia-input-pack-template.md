---
document: dpia-input-pack
system: <system name>
version: <build or design revision described>
status: draft
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
controller: <client legal entity>; DPO: <name or role>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md, docs/plans/<topic>.md>
---

# DPIA input pack: <system name>

Inputs for <client>'s data protection impact assessment under GDPR Article
35. The controller's DPO writes and signs the DPIA; this pack supplies the
facts the design and plan record and the questions only counsel can answer.
Not legal advice.

## Screening

| Criterion (WP248 rev.01) | Applies? | Why | Evidence |
| --- | --- | --- | --- |
| Evaluation or scoring, including profiling | <yes / no> | <reason> | <C/D ID> |
| Automated decision with legal or similarly significant effect | <yes / no> | <reason> | <C ID> |
| Systematic monitoring | <yes / no> | <reason> | <C/D ID> |
| Special-category or highly personal data | <yes / no> | <reason> | <docs/discovery/<topic>.md §4 data register> |
| Large scale | <yes / no> | <volume> | <path §n or source: who, date> |
| Matching or combining datasets | <yes / no> | <reason> | <D ID> |
| Vulnerable data subjects (employees, children, patients) | <yes / no> | <reason> | <R ID> |
| Innovative use of technology (a generative model) | <yes / no> | <reason> | <D ID> |
| Prevents exercising a right or using a service | <yes / no> | <reason> | <C ID> |

Result: <n> criteria met; counsel: <DPIA required / recommended / not required; confirm>.

## Processing description

- **Purpose:** <purpose in the client's words> (<R ID>).
- **Nature:** <what the agent does with personal data: read, summarise, rank, store, send> (<C/D IDs>).
- **Scope:** <volume, frequency, population, geography> (<path §n or source: who, date>).
- **Context:** <relationship with the data subjects and their expectations> (<docs/discovery/<topic>.md §n>).

## Data flows

| Step | Personal data | From | To (component, region) | Stored? For how long | Screening before it | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| <user prompt> | <categories> | <browser> | <service, region> | <yes / no; period> | <SDP / Model Armor / none> | <C/D/SB IDs> |
| <model request> | <categories> | <service> | <model endpoint, region> | <provider retention> | <control> | <D ID, source:> |
| <tool call> | <categories> | <agent> | <system of record> | <period> | <control> | <C ID> |
| <logs and traces> | <what remains> | <service> | <sink, region> | <period> | <control> | <SB14, D ID> |

## Data subjects and categories

| Data subjects | Categories | Special category or criminal data | Source | Evidence |
| --- | --- | --- | --- | --- |
| <who> | <categories> | <none / which; counsel:> | <system of record> | <docs/discovery/<topic>.md §4 data register> |

## Legal basis

- counsel: <purpose> — candidate basis <Article 6(1) basis>; why it may fit: <facts from the design>.
- counsel: <special category condition under Article 9, if any>.
- counsel: <does any output produce a decision based solely on automated processing (Article 22)?> Facts: <where a person decides> (<C ID>).

## Necessity and proportionality

- <why each data category is needed for the purpose; what was removed or minimised> (<C/D IDs>).
- <less intrusive alternative considered and why rejected> (<D ID>).
- <how data subjects are informed and exercise rights: access, rectification, erasure, objection> (<C IDs>).

## Retention and erasure

| Store | Content | Retention | Erasure path | Evidence |
| --- | --- | --- | --- | --- |
| <session store> | <conversation> | <period> | <how a request reaches it> | <C/D IDs> |

## Recipients, processors and regions

| Recipient or processor | Role | Region | Transfer outside the EEA and mechanism | Evidence |
| --- | --- | --- | --- | --- |
| <Google Cloud> | <processor under the client's agreement> | <region> | <none / mechanism; counsel:> | <D ID, source:> |
| <agency> | <processor during build and support> | <where> | <none / mechanism> | <contract reference or assumption:> |

## Model provider data use

- <model and endpoint used; whether prompts and outputs are used for training; abuse-monitoring logging; caching; zero data retention status> (<D ID>, source: <provider page>, <YYYY-MM-DD>).
- <whether the model was trained on personal data and what the client relies on (provider statements, EDPB Opinion 28/2024)> (counsel: <question>).

## Risks and measures

| Risk to data subjects | Likelihood and severity (provisional) | Measure | Status | Evidence |
| --- | --- | --- | --- | --- |
| <personal data in an answer to the wrong user> | <assumption:> | <per-user scope> | <in place / planned G ID> | <C/SB IDs> |
| <inaccurate output about a person> | <assumption:> | <grounding, human review> | <status> | <C ID, M ID> |
| <personal data retained in logs or traces> | <assumption:> | <screening, log policy> | <status> | <SB14, C ID> |

## Questions for counsel

- counsel: <question>, needed by <goal or wait ID>.
