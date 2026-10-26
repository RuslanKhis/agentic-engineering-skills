# The interview

Read for `init`, and whenever a flow skill meets an empty profile section it
needs. The question bank follows the profile's thirteen sections in template
order.

## How to ask

- **At most three questions per turn**, a section at a time, or two short
  sections together, each with the skill that will use the answer
  ("adk-governance-pack uses this to add the works-council wait"). The core
  set fits in about seven turns. When the user answers ahead, or answers
  everything in one message, take it and ask only what is left.
- **Core first.** The sixteen core questions (C) take about fifteen minutes
  with menus. Ask deep questions (D) only when the user asks for more, or
  when a flow skill needs that section and it is empty.
- **Facts about the company: menus, not guesses.** Offer the common options,
  "other" and "don't know". Never lead with a recommended answer to a fact
  ("what did your last AI pilot achieve?" has no default).
- **Conventions: a recommended answer** the user can accept in a word, where
  a default is defensible (deck length, region, model-pin policy, the usual
  proof of concept) or where the user has already said it.
- **Specifics from the past, not opinions about the future.** "What happened
  to the last AI tool someone proposed?", not "Would your board support AI?".
  "We'd love to use AI for X" is an aspiration; record it as one, if at all,
  never as a priority.
- **"Don't know" is an answer.** For a core question in a gate-read section
  (sector and jurisdictions, stakeholders and decision norms, data subjects
  and data classes, AI policy and approvals, procurement and consultation,
  security and compliance floor), record `- Works council: unknown; ask HR.
  (user, <date>)` so the flow skill asks instead of assuming. Elsewhere
  leave it empty. A question with several parts answered in part records
  the parts given, and the missing parts as "unknown; ask" in those
  sections.
- **Menus come from what the user has said.** Build a regulator or law menu
  from the countries the user named, always with "other" and "don't know".
  Record only options the user picked; a regulator you named in the
  question and the user did not pick is not written.
- **Contradictions are asked about before the diff.** Two answers naming
  different approvers, or capacity that disagrees with the usual proof of
  concept, get one question ("Both, in that order, or one of them?"), not
  two lines written side by side.
- **Figures.** Counts and allowances the user gives (about 140 stores, AUD
  300 a month) are fine unless the user or a document marks them
  confidential; revenue and margins are not asked for.
- **Roles, not names.** Product names of systems (Salesforce, SAP, Jira) are
  fine; hostnames, tenant IDs, URLs and people's names are not.
- **Offer import** where an answer already sits in a document (a strategy, an
  AI policy, an org chart without contact details): "If you have it as
  Markdown or text, name the file and I'll propose lines from it."
- **No figures marked confidential**, no revenue numbers; KPIs by name.

Write each answer as a line a flow skill can offer as-is, ending with its
source and date, by [writing rules](writing-rules.md).

## engineer.md (once per engineer, not per org)

Role; hours a week for one project; ADK and GCP familiarity (new, some,
fluent); host (Claude Code, Codex, Gemini CLI, Antigravity); writing voice
(British or US spelling, plain or formal, length). Lead each with a
recommended answer: these are conventions about the user. Ask them over two
turns, and fill the host from what you can see rather than asking.

## Recommended answers for conventions

Offer these when the user has said nothing better; they are starting
points, not facts about the company:

- H1, the usual proof of concept: two to three weeks, one engineer part
  time, a small monthly model and cloud allowance approved by the sponsor,
  judged by the sponsor against one measure.
- J1: the cloud region nearest where the data must stay; Cloud Run for
  hosting; model versions pinned and changed only by a reviewed change.
- L1: about ten slides, the company template, the decision asked for first.

## Question bank

Readers: Disc = adk-discovery, Des = adk-system-designer, Pres =
adk-presenter, Eng = adk-engineer, Gov = adk-governance-pack.

| Section | Readers | ID | C/D | Question (as asked) | Answer form |
| --- | --- | --- | --- | --- | --- |
| Business context and KPIs | Disc | A1 | C | What does it sell, to whom, through which channels, and which two or three KPIs are the sponsors judged on this year? | Free text; KPIs by name, no confidential figures |
| | | A2 | D | Where does revenue come from and where does most cost sit? | Qualitative |
| | | A3 | D | Which priorities does this year's strategy name? | Offer import; else free text |
| | | A4 | D | Which partners or outsourcers run parts of the operation? | Roles or company types |
| Sector and jurisdictions | Gov, Des, Disc | B1 | C | Which sector, in the words a regulator would use, and in which countries are its customers and staff? | Menu (Australia and its states, New Zealand, Singapore, Canada and its provinces, US states, EU states, UK, other, don't know) |
| | | B2 | C | Which regulators supervise it besides the data-protection authority? | Menu by sector, "none known", "don't know" |
| | | B3 | D | Does it do any of these as a business: credit, insurance pricing, recruitment or worker management, education assessment, medical devices, critical infrastructure, public services, biometrics? | Checklist; governance treats each tick as an area to check, never a conclusion |
| | | B4 | D | When it uses AI built by others, is it usually a deployer, and does it ever put AI on the market under its own name? | Menu; recorded as `assumption:`; counsel decides per system |
| | | B5 | D | Which certifications or standards does it hold or require (ISO/IEC 27001, SOC 2, ISO/IEC 42001, PCI DSS, Cyber Essentials)? | Checklist |
| Stakeholders and decision norms | Disc, Pres, Gov | C1 | C | Which roles sponsor, fund and decide AI work, and how is a decision made (pre-read, steering group, sign-off chain)? | Roles; menu for the norm |
| | | C2 | C | Which reviewers must sign before a pilot touches real data: privacy office or DPO, CISO, legal, an AI review board, architecture? | Checklist, "don't know" |
| | | C3 | D | Who runs a system after handover? | Role |
| | | C4 | D | Who are the frontline users, and who represents them? | Roles |
| Data subjects and data classes | Gov, Des | D1 | C | Whose personal data do its projects usually touch (customers, consumers, staff, patients, children, suppliers' staff), and which classes (contact, financial, health, biometric, location, special category, criminal, payment card)? | Two checklists, "don't know" |
| | | D2 | D | Which classification scheme does it use, and which classes may go to a cloud model provider? | Scheme name; per class yes, no or ask |
| | | D3 | D | Where must data stay, and which transfer mechanisms exist? | Menu |
| | | D4 | D | How long are logs and transcripts kept by default? | Duration |
| Systems of record and tools | Disc, Des | E1 | C | Which systems own the facts most projects need: CRM, ERP, ticketing, documents, warehouse, identity? | Product names |
| | | E2 | C | Which AI tools are approved, and which are used unofficially? | Two lists, "don't know" |
| | | E3 | D | How is access to a system of record granted, and how long does it take? | Route and weeks |
| | | E4 | D | Where are decisions and policies written down (Drive, SharePoint, Confluence, Notion)? | Product names; points to what to import |
| AI policy and approvals | Gov, Des | F1 | C | Is there a written AI or acceptable-use policy? Which role owns it, what date is it, and what must be approved before an AI pilot uses real data? | Yes, drafting, no, don't know; offer import |
| | | F2 | D | Which model providers, regions or uses does it allow or forbid? | Lists |
| | | F3 | D | Is there an AI register or inventory where a new system must be entered? | Yes or no; owner role |
| | | F4 | D | Which documents does it require: DPIA, AI impact assessment, FRIA, model or system card? | Checklist |
| AI maturity and past attempts | Disc, Pres | G1 | C | What AI has it tried in the last two years, and what happened to each? | Per attempt: what, outcome, why |
| | | G2 | C | Which describes it now: experimenting; pilots with some capability; AI changing how teams work; AI built into products and decisions? | Menu, "don't know" |
| | | G3 | D | Who builds AI here: an in-house team, an agency, a vendor? | Menu |
| | | G4 | D | What stalled or stopped past attempts: data access, cost, sponsor change, accuracy, staff resistance, legal? | Checklist |
| Delivery defaults | Disc, Des | H1 | C | A usual proof of concept: how many weeks, how many people at what hours, what monthly model and cloud allowance, and who judges it? | One line with a recommended default the user edits |
| | | H2 | D | Which data and effects are usually allowed in a proof of concept (sample or real data; drafts or sends)? | Menu |
| | | H3 | D | Which reviews need a presentation? | List |
| Procurement and consultation | Des, Gov, Disc | I1 | C | How long do vendor onboarding, a security review, a DPIA sign-off and a legal review usually take? | Weeks each, "don't know" |
| | | I2 | C | Must a works council, trade union or employee forum be informed or consulted before a tool that affects staff? | Yes, no, don't know; which body |
| | | I3 | D | Which procurement rules apply: spend thresholds, framework agreements, public procurement law, cloud marketplace purchase? | Menu |
| | | I4 | D | What does the engagement agreement forbid: notes outside client systems, subcontractors, reuse of outputs? | Checklist; a yes to the first stops import |
| | | I5 | D | Which accessibility or language requirements apply (WCAG 2.2 AA, bilingual)? | Checklist |
| Stack and conventions | Des, Eng | J1 | C | Which cloud, region, hosting and model-pin policy? | Recommended default the user edits |
| | | J2 | D | IaC, CI, repository conventions, approved companion skills? | Free text |
| Security and compliance floor | Des, Gov | K1 | C | What does it always require, whatever the project (residency, approvals, logging, a person before customer-visible output)? | Free text; raises floors only |
| | | K2 | D | Penetration test or threat model before production? Retention or audit-log rules? | Yes or no and trigger |
| Presentation style | Pres | L1 | D | Deck template owner, length, tone, what deciders expect to see first? | Recommended default |
| Glossary | Disc, Des, Gov | M1 | D | Which internal terms should documents use? | term = meaning |

The sixteen core questions: A1, B1, B2, C1, C2, D1, E1, E2, F1, G1, G2, H1,
I1, I2, J1, K1.

## Answers that are never written

A floor that would go down ("pilots may use production data without
review"), a permission that would widen, an approval that would be skipped,
or a tool to call, whoever says it: tell the user it belongs in the
project's design as a decision. Names with contact details, secrets and
confidential figures are never written either; [writing rules](writing-rules.md)
has the full list.
