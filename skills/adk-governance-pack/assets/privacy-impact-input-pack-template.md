---
document: privacy-impact-input-pack
system: <system name>
version: <build or design revision described>
status: draft
jurisdictions: [<codes in scope, in the order au, us, eu, uk>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
owner: <client legal entity; for a group, each entity and its role>
for: <DPO, privacy officer or role>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md, docs/plans/<topic>.md>
---

# Privacy impact input pack: <system name>

Inputs for <client>'s privacy assessments of this system: the privacy impact
assessment under the Australian Privacy Principles, the data protection
impact assessment under GDPR or UK GDPR Article 35, and the data protection
or risk assessment US state laws ask for, as the jurisdiction screen found
them in scope. The client writes and signs each assessment; this pack
supplies the facts the design and plan record and the questions only counsel
can answer. Not legal advice.

<!-- Keep only the regime sections, and the regime rows and bullets inside
shared sections, whose code is in jurisdictions. When Australia is in scope
only through the consultancy's own handling, the Australian sections cover
that handling and the inventory feeds the consultancy's own privacy policy.
Delete this comment. -->

## Screening

| Regime | Test | Met? | Why | Evidence |
| --- | --- | --- | --- | --- |
| <EU or UK> | WP248 rev.01: <criterion> | <yes / no> | <reason> | <C/D/R ID> |
| <UK> | ICO list: <item, such as innovative technology including AI> | <yes / no> | <reason> | <D ID> |
| <Australia> | OAIC threshold assessment: <new or changed handling of personal information> | <yes / no> | <reason> | <D ID> |
| <United States> | <CPPA section 7150(b) trigger, or a state data protection assessment trigger> | <yes / no> | <reason> | <C ID> |

Result: counsel: <assessment required / recommended / not required per regime; the DPO or privacy officer decides>.

## Processing description

- **Purpose:** <purpose in the client's words> (<R ID>).
- **Nature:** <what the agent does with personal data: read, summarise, rank, infer, store, send> (<C/D IDs>).
- **Scope:** <volume, frequency, population, geography; approximate number of people> (<path §n or source: who, date>).
- **Context:** <relationship with the people and their expectations> (<docs/discovery/<topic>.md §n>).

## Data flows

| Step | Personal data | From | To (component, region) | Stored? For how long | Searchable by person | Screening before it | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <user prompt> | <categories> | <browser> | <service, region> | <yes / no; period> | <yes / no> | <SDP / Model Armor / none> | <C/D/SB IDs> |
| <model request> | <categories> | <service> | <model endpoint, processing region> | <provider retention> | <n/a: not stored by the client> | <control> | <D ID, source:> |
| <tool call> | <categories> | <agent> | <system of record> | <period> | <yes / no> | <control> | <C ID> |
| <logs and traces> | <what remains> | <service> | <sink, region> | <period> | <yes / no> | <control> | <SB14, D ID> |
| <consultancy access> | <what staff can see> | <client environment> | <consultancy staff, country> | <period> | <n/a:> | <control> | <D ID or gap:> |

## People and data categories

| People (data subjects or individuals) | Categories | Sensitive or special category data (including inferred) | Source (from the person, a third party, or generated) | Evidence |
| --- | --- | --- | --- | --- |
| <who> | <categories> | <none / which; counsel:> | <system of record> | <docs/discovery/<topic>.md §4 data register> |

## Automated decisions

- **Facts:** <where a person decides; who they are, their training and authority to change the outcome; share reviewed and override rate> (<C ID, M ID or gap:>).
- **Explanation the design can produce:** <features used, a counterfactual, who produces it> (<C ID or gap:>).
- counsel: <per regime in scope: APP 1.7 substantially and directly related decision; GDPR Article 22 decision under SCHUFA; UK Article 22A significant decision with no meaningful human involvement; CPPA ADMT and state profiling opt-out; or n/a: no decision about a person>.

## Necessity and proportionality

- <why each data category is needed for the purpose; what was removed or minimised> (<C/D IDs>).
- <less intrusive alternative considered and why rejected> (<D ID>).
- <each re-used dataset: original purpose, whether consent-based, and the regime's re-use test> (<D IDs>; counsel: <compatible?>).
- <how people are informed (notices naming the model provider as recipient, memory retention, transfers, automated decisions, the source of indirectly collected data) and exercise rights: access, correction, erasure (memory, vector stores, backups), objection, opt-out> (<C IDs>).

## Retention and erasure

| Store | Content | Retention | Erasure path | Evidence |
| --- | --- | --- | --- | --- |
| <session store> | <conversation> | <period> | <how a request reaches it> | <C/D IDs> |

## Recipients and regions

| Recipient or processor | Role | Region or country | Transfer or overseas disclosure: mechanism and assessment | Evidence |
| --- | --- | --- | --- | --- |
| <Google Cloud> | <processor or service provider under the client's agreement> | <region> | <none / adequacy, DPF with check date, SCC module, IDTA or Addendum; APP 8 use or disclosure; counsel:> | <D ID, source:> |
| <agency> | <processor or service provider during build and support; APP entity in its own right in Australia> | <where staff access from> | <none / SCC Module 2 or IDTA and transfer-assessment.md; counsel:> | <contract reference or gap:> |

## Model provider data use

- <model and endpoint used; processing region; whether prompts and outputs are used for training; abuse-monitoring logging; caching; zero data retention status> (<D ID>, source: <provider page>, <YYYY-MM-DD>).
- <whether the model was trained on personal data and what the client relies on (provider statements; EDPB Opinion 28/2024 in the EU; the ICO's generative AI positions in the UK)> (counsel: <question>).

## Risks and measures

| Risk to people | Likelihood and severity (provisional) | Measure | Status | Evidence |
| --- | --- | --- | --- | --- |
| <personal data in an answer to the wrong user> | <assumption:> | <per-user scope> | <in place / planned G ID> | <C/SB IDs> |
| <inaccurate output about a person> | <assumption:> | <grounding, human review> | <status> | <C ID, M ID> |
| <personal data retained in logs or traces> | <assumption:> | <screening, log policy> | <status> | <SB14, C ID> |

## Australia: APP compliance check

| APP | Fact in the design | Question or gap | Evidence |
| --- | --- | --- | --- |
| APP 3 collection (3.3 consent for sensitive information; generated or inferred information is collected) | <fact> | <counsel: or gap:> | <C/D IDs> |
| APP 5 notice | <fact> | <counsel: or gap:> | <C ID> |
| APP 6 use and disclosure (primary purpose; secondary use) | <fact> | <counsel:> | <D ID> |
| APP 8 and s 16C overseas recipients | <fact> | <counsel: use or disclosure> | <D ID> |
| APP 10 quality; APP 11 security and destruction | <fact> | <counsel: or gap:> | <C/SB IDs> |
| APP 12 and 13 access and correction (memory, logs, evaluation sets) | <fact> | <counsel: or gap:> | <C ID> |

- **PIA required?** <Commonwealth agency on a high privacy risk project: required; otherwise recommended> (counsel: <high privacy risk?>).

## Australia: Inventory and notice inputs

| Kind of personal information | Purpose | Source (person, third party, generated or inferred) | Usual recipients | Overseas countries | Retention | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| <kind> | <purpose> | <source> | <recipients> | <countries or none> | <period> | <C/D IDs> |

- **Proposed APP 5 notice and privacy-policy additions, including APP 1.8 entries:** <text> (system-card.md; counsel: <confirm>).

## United States: Notice, consent and opt-out

- **States and thresholds:** <states whose residents' data is processed and whether the client meets each threshold> (<source: or gap:>; counsel: <confirm>).
- **Notice and opt-outs:** <privacy-notice text on profiling, the opt-out route and appeal; CPPA pre-use ADMT notice if ADMT> (<C IDs>).
- **Sensitive data:** <opt-in consent, right to limit, or strict necessity, per state> (<C IDs>; counsel: <consent covers free-text chat?>).
- **Level of human involvement:** <solely automated, human reviewed or human involved> (<C/M IDs>).

## United States: Assessment approval

- **Whether the business will proceed:** <go / no-go proposed> (counsel: <decision is the client's>).
- **Approver:** <name, position, approval date> (source: <who>, <YYYY-MM-DD> / gap: approver not named).
- **Contributors:** <names and roles> (source: <who>, <YYYY-MM-DD>).
- **Review cycle and retention:** <review every three years, update within 45 days of a material change, keep five years> (CPPA section 7152, checked <YYYY-MM-DD>).

## EU: Legal basis

- counsel: <purpose>, candidate basis <Article 6(1) basis>; why it may fit: <facts from the design>.
- counsel: <special category condition under Article 9, if any; AI Act Article 4a reasons if special categories are used for bias detection>.

## United Kingdom: Lawful basis and ADM safeguards

- counsel: <purpose>, candidate basis <Article 6(1) basis, including (ea) recognised legitimate interest with its Annex 1 condition or an Article 6(11) example>; facts: <from the design>.
- **Article 22C safeguards, if a significant decision is solely automated:** <information about the decision; how the person makes representations; human intervention route; contest route> (<C IDs or gap:>).
- **Complaints process (DPA 2018 s 164A):** <the client's process and the 30-day acknowledgement> (<source: or gap:>).

## Questions for counsel

- counsel: <question>, regime <regime>, needed by <goal or wait ID>.
