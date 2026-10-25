# Governance pack: sources and decisions

*Read 25 October 2026. Basis for `skills/adk-governance-pack`.*

Agency engineers building ADK agents for clients are asked, before a pilot
or production decision, for papers the client's counsel, DPO and CISO sign:
an EU AI Act classification, a DPIA, an impact assessment, a system card,
records of processing and security questionnaire answers. The design and
plan this toolkit produces already hold most of the facts (contracts,
decisions, the security baseline, measurement and incident records); the
gap was a skill that drafts those papers from the record without inventing
facts or legal conclusions.

## Primary sources read

Two research subagents read these on 25 October 2026; the coordinator then
grepped the saved Official Journal text of Regulation (EU) 2026/1744 for
the Annex III dates, the Article 50(2) transition, Article 4 and Article
27(4) wording, and its entry-into-force clause. EUR-Lex's HTML pages
returned a bot challenge, so the Official Journal texts were fetched from
the Publications Office by CELEX number
(`http://publications.europa.eu/resource/celex/<CELEX>`), which serves the
same published act.

| Source | Status | What the skill uses |
| --- | --- | --- |
| Regulation (EU) 2024/1689, the AI Act, OJ L 12.7.2024 (CELEX 32024R1689, <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>) | Read in full | Arts. 3(1), 3(3), 3(4), 4, 5, 6, 25, 26, 27, 50, 53, 55, 111, 113; Annex III headings |
| Regulation (EU) 2026/1744, Digital Omnibus on AI, of 8 July 2026, OJ L 24.7.2026, in force 27 July 2026 (CELEX 32026R1744, <https://eur-lex.europa.eu/eli/reg/2026/1744/oj>) | Read in full | Amended Arts. 4, 5, 25, 27, 111, 113; new Art. 4a |
| COM(2025) 836 final, the Omnibus proposal, 19.11.2025 (CELEX 52025PC0836) | Read | Only to show what changed between proposal and final text |
| Commission guidelines on prohibited practices (4 Feb 2025) and on the AI system definition (6 Feb 2025), digital-strategy.ec.europa.eu | Landing pages read | Cited as non-binding aids |
| Draft Commission guidelines on high-risk classification, published 19 May 2026 (<https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems>) | Landing page read; still draft | Cited as draft |
| Code of Practice on marking and labelling AI-generated content, 10 June 2026, and the Article 50 FAQ (digital-strategy.ec.europa.eu) | Read | Art. 50 date and voluntary code |
| GDPR, Regulation (EU) 2016/679 (CELEX 32016R0679) | Read (Official Journal text) | Arts. 6, 9, 22, 28, 30, 35, 36 |
| WP29 Guidelines on DPIA, WP248 rev.01, revised 4 Oct 2017 (<https://ec.europa.eu/newsroom/article29/items/611236>) | Read | Nine screening criteria; two-criteria rule of thumb |
| EDPB Opinion 28/2024 on AI models, adopted 17 Dec 2024 | Executive summary read | Anonymity test; deployer's accountability for a model developed by another |
| NIST AI 100-1, AI RMF 1.0 (Jan 2023) and NIST AI 600-1, Generative AI Profile (July 2024), nvlpubs.nist.gov | Read | Four functions (19 categories); 12 GenAI risks; action ID format |
| NIST AI RMF landing page (<https://www.nist.gov/itl/ai-risk-management-framework>) | Read | 1.0 "being revised"; no new version on the read date |
| Google Cloud: zero data retention and abuse monitoring pages (docs.cloud.google.com/gemini-enterprise-agent-platform/..., updated 22 Oct 2026); sub-processors (modified 19 Oct 2026); Cloud Data Processing Addendum | Read | Training, caching, grounding retention, abuse logging, processor terms |

## Findings that change what a draft says

- **The Omnibus is adopted law.** Regulation (EU) 2026/1744 was published on
  24 July 2026 and entered into force on 27 July 2026. The prior research's
  regulation number was right.
- **High-risk dates are fixed, not conditional.** New Article 113(c):
  Annex III systems from 2 December 2027, Annex I products from 2 August
  2028. The proposal linked these to a Commission decision; the final text
  does not.
- **Article 50 is not delayed.** It applies from 2 August 2026. The only
  transition is new Article 111(4): systems placed on the market before
  that date have until 2 December 2026 for the 50(2) marking duty (the
  proposal said 2 February 2027).
- **Article 4 was narrowed, not removed.** The prior research said AI
  literacy was "softened" into an encouragement duty; that was the
  proposal. The final text keeps an obligation on providers and deployers
  to take measures to support their staff's AI literacy, without having to
  guarantee any individual's level, applying since 27 July 2026.
- **Article 27(4) now allows cross-references.** A fundamental rights
  impact assessment may cross-reference or include the relevant sections
  of the GDPR DPIA where that DPIA already meets an obligation. The DPIA
  input pack is therefore organised to be cited by section.
- **New prohibitions** (Article 5(1)(ba), (bb): non-consensual intimate
  material and child sexual abuse material generation) apply from 2
  December 2026.
- **Article 4a** gives a legal basis for processing special-category data
  to detect and correct bias, relevant to any adverse-impact monitoring.
- **Model provider data use on Google Cloud** has defaults a DPIA must
  state: implicit caching for up to 24 hours unless disabled; grounding
  with Google Search or Maps retains logs (3 and 30 days) and cannot be
  switched off; abuse-monitoring storage of flagged prompts up to 90 days
  for standard models unless the customer's agreement exempts it.

## Not verified at a primary source

- **ISO/IEC 42005:2025 contents.** iso.org returned 403. Publication date
  (27 May 2025) comes from the Standards Council of Canada record; the
  topic headings come from ISO's abstract and a law-firm summary. The skill
  paraphrases headings only and says conformity needs the standard.
- **ISO/IEC 42001:2023 clause 6.1.4** relationship: secondary only.
- **A GDPR Digital Omnibus** (procedure 2025/0360(COD)) was reported as still
  under negotiation; secondary only. The skill treats the GDPR articles as
  unamended and tells the drafter to say so with the date.
- **Commission formal version of the prohibited-practices guidelines**
  (C(2025) 5052) seen only in search results.
- No consolidated version of the AI Act was read; the skill cites the base
  act as amended.

## Decisions

- **Name `adk-governance-pack`.** It names the deliverable (a pack of
  papers) and the reviewers' own word (AI governance), and avoids the words
  the nearby skills own: *sensitive data*, *PII*, *redact* and *screening*
  (`protect-adk-sensitive-data`), *security*, *threat* and *harden*
  (`adk-agent-security`), *release* and *gate* (`adk-release-engineering`).
  Rejected: `adk-compliance` (invites "make our agent compliant", which is
  implementation), `adk-privacy-docs` (too narrow, and collides with the
  sensitive-data skill on "privacy"), `adk-regulatory-review` (sounds like
  it gives legal advice).
- **Drafts, not advice.** Every legal conclusion (role, classification,
  legal basis, DPIA or FRIA requirement, derogation) carries `counsel:`;
  the skill supplies facts with IDs.
- **A small checker, not a legal engine.** `check_governance.py` enforces
  form: required sections, a citation or marker on every statement,
  existence of cited IDs in the sources, a forced counsel flag on Annex III
  trigger phrases, and `checked <date>` on applicability dates. Trigger
  phrases are narrow (for example *database migration* and *model
  performance evaluation* do not trigger) and sections that walk the Article
  5 and Annex III checklists or list out-of-scope uses are not scanned.
- **Profile-sized.** A proof of concept gets a one-page note; an internal
  tool the memo, DPIA inputs and processing rows; a pilot or production the
  full pack. The designer adds a governance goal before the
  production-approval presentation, with sign-offs as calendar waits.
- **Source register.** `docs/research/source-register.json` and
  `check_source_freshness.py` accept only GitHub repositories
  (`owner/name`), and this skill relies on none. The legal and standards
  sources above are dated here instead; re-reading them is a dated
  maintenance task, and the checker warns on `checked` dates older than 180
  days in a client's drafts.
