---
document: regulatory-memo
system: <system name>
version: <design revision or build screened>
status: draft
jurisdictions: [<codes in scope, in the order au, us, eu, uk>]
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
for: <client counsel or AI governance lead>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md, docs/plans/<topic>.md>
---

# Regulatory memo: <system name>

Draft for <client>'s counsel. It records which regimes the jurisdiction
screen found in scope, the facts the design records, and the provisions that
appear relevant in each regime: the EU AI Act classification where the EU is
in scope, and a screen of the existing laws that apply in Australia, the
United States and the United Kingdom, none of which has an AI Act or assigns
a risk tier. Conclusions are proposals for counsel; not legal advice.

<!-- Keep only the regime sections whose code is in jurisdictions, in the
order Australia, United States, EU, United Kingdom. Delete this comment. -->

## Summary

- **Regimes in scope:** <Australia, United States, EU, United Kingdom: those in jurisdictions> (Jurisdiction screen below; counsel: <confirm the screen>).
- **Proposed EU classification, if the EU is in scope:** <prohibited / high-risk (Annex III point) / Article 6(3) derogation argued / transparency obligations only / minimal risk> (counsel: <confirm>).
- **Main obligations in the other regimes:** <one line per regime: for example APP 1.7 privacy-policy entries from 10 December 2026; CPPA risk assessment; UK GDPR Article 22C safeguards> (<IDs>; checked <YYYY-MM-DD>).
- **Proposed roles:** <one line per regime> (Roles below; counsel: <confirm>).
- **Blocking questions:** counsel: <count> questions, listed under Questions for counsel.

## Jurisdiction screen

| Regime | In scope | Trigger facts | Reason |
| --- | --- | --- | --- |
| Australia | <yes / no / yes (gap: fact missing)> | <client establishment, data subjects, consultancy staff access> (<IDs or source:>) | <reason, or n/a: why not> |
| United States | <yes / no / yes (gap:)> | <US client, US residents, federal client> (<IDs or source:>) | <reason, or n/a: why not> |
| EU | <yes / no / yes (gap:)> | <EU establishment, people in the EU, EU market or output use> (<IDs or source:>) | <reason, or n/a: why not> |
| United Kingdom | <yes / no / yes (gap:)> | <UK establishment, people in the UK, central government client> (<IDs or source:>) | <reason, or n/a: why not> |

- **Processing locations:** <hosting region; model processing region from the model page; logs; grounding; abuse monitoring; telemetry; consultancy access from Australia> (<D IDs>, source: <model page>, <YYYY-MM-DD>).
- **Practice profile:** <facts that added a regime, regulator, reviewer or wait, or n/a: no profile bound> (source: practice profile <org>, reviewed <YYYY-MM-DD>).

## System and intended purpose

- **What it does:** <one or two sentences> (<R/C IDs>).
- **Who uses it and who it affects:** <users; people its outputs are about> (<docs/discovery/<topic>.md §n, R IDs>).
- **What the model decides and what code or people decide:** <split> (<D/C IDs>).
- **Effects it can cause:** <reads, drafts, writes, messages, decisions about people> (<C IDs>).
- **Human review of decisions about people:** <where a person decides, share reviewed, override rate> (<C ID, M ID or gap:>).

## Roles

- **Facts:** <who commissions it; whose name it runs under; who changes its purpose; who operates it; what the agency supplies; who handles personal data during build and support> (<D IDs, source:>).
- **Australia, Privacy Act:** <client APP entity? consultancy APP entity in its own right? small business, employee records or State contract exemptions; no processor category in Australian law today> (counsel: <confirm>).
- **United States:** <CCPA business and service provider; state-law controller and processor; Colorado developer and deployer; FEHA agent of the employer; HIPAA business associate> (counsel: <confirm>).
- **EU AI Act:** <client provider and deployer; agency developer under contract, provider only if it markets the system under its own name; Article 25 triggers; Article 25(4) agreement if high-risk> (<D/G IDs>; counsel: <confirm>).
- **EU GDPR and UK GDPR, separately:** <controller, processors, sub-processors> (privacy-impact-input-pack.md; counsel: <confirm>).

## Australia: Privacy Act and APPs

- **No AI-specific regime:** Australia has no AI Act; the 2024 mandatory guardrails proposal will not proceed, and obligations come from the laws screened here (checked <YYYY-MM-DD>).
- **APPs engaged:** <APP 1, 3, 5, 6, 8, 10, 11, 12 and 13, each with the fact that engages it> (privacy-impact-input-pack.md; <IDs>).
- **Overseas disclosure (APP 8, s 16C):** <model endpoint and processing region, logs, grounding, support or abuse review outside Australia; use or disclosure facts> (<D IDs>; counsel: <use or disclosure>).
- **Notifiable data breaches:** <who assesses within 30 days and who notifies; contract flow-down> (security-questionnaire.md; counsel: <which entity notifies>).
- **Pending, not law:** <tranche 2 exposure draft; Children's Online Privacy Code> (checked <YYYY-MM-DD>).

## Australia: Automated decisions (APP 1.7)

| Decision the agent touches | Solely or substantially and directly related | Human review and its measured share | Effect on the person | Personal information used | Evidence |
| --- | --- | --- | --- | --- | --- |
| <decision, or n/a: no decision about a person> | <which> | <contract ID; M ID or gap:> | <effect> | <kinds> | <C/M IDs; counsel: significantly affects?> |

- **Privacy policy inputs (APP 1.8):** system-card.md, Automated-decision disclosure (<C ID>).

## Australia: Sector, state and government AI policy

- **Sector laws:** <APRA CPS 234 and CPS 230; health records and My Health Records s 77; workplace surveillance notice; Spam Act and telemarketing; Australian Consumer Law ss 18 and 29; or n/a: with the reason> (<IDs>; counsel: <question>).
- **Government AI policy:** <DTA policy and AI impact assessment for a Commonwealth client; state framework; or n/a: private client> (<IDs>; checked <YYYY-MM-DD>).

## United States: Preemption status and FTC claims

- **Federal preemption:** no federal statute preempts the state laws screened below; <court orders staying a state law, for example Colorado> (checked <YYYY-MM-DD>).
- **FTC Act Section 5:** <public claims the client will make about the agent and the M records that substantiate them> (<M IDs or gap:>).

## United States: Automated decisions and state AI laws

- **CPPA ADMT and risk assessment:** <is the client a CCPA business; does the output replace or substantially replace a human in a significant decision; the three-part human review facts> (<C/M IDs>; counsel: <ADMT or not>).
- **Colorado SB 26-189 and other state AI laws:** <consequential decisions about state residents; enforcement status> (<IDs>; checked <YYYY-MM-DD>).
- **Chatbot and companion laws:** <consumer chat disclosure duties; whether a persona or memory brings companion laws in> (<C IDs>; counsel: <exclusion holds?>).

## United States: Privacy, sector and employment laws

- **State privacy laws:** <states whose thresholds the client meets; profiling opt-out; data protection assessment; sensitive-data consent> (<IDs>; counsel: <thresholds>).
- **Employment AI rules:** <NYC Local Law 144, Illinois, California FEHA, Title VII and ADA, or n/a: no employment use> (<IDs>; counsel: <question>).
- **Sector statutes:** <HIPAA, GLBA, FCRA, ECOA Regulation B, TCPA, COPPA, or n/a: with the reason> (<IDs>).

## EU: Prohibited practices (Article 5)

| Point | Applies? | Facts | Evidence |
| --- | --- | --- | --- |
| (a) manipulation, (b) exploiting vulnerabilities | <no / counsel:> | <why> | <C IDs> |
| (ba), (bb) generated intimate or abuse material | <no / counsel:> | <why> | <C/D IDs> |
| (c) social scoring, (d) crime prediction by profiling | <no / counsel:> | <why> | <C IDs> |
| (e) facial scraping, (g) biometric categorisation, (h) real-time remote identification | <no / counsel:> | <why> | <D IDs> |
| (f) emotion inference at work or in education | <no / counsel:> | <why> | <C/D IDs> |

## EU: High-risk classification (Article 6 and Annex III)

- **Annex I product:** <no / which product legislation> (<D ID or assumption:>).
- **Annex III area touched:** <none / point and area> (<R/C IDs>).
- **Profiling of natural persons:** <yes / no, with facts> (<C/D IDs>; counsel: <confirm>).
- **Article 6(3) derogation facts, if argued:** <narrow procedural / improves completed human work / detects patterns under human review / preparatory; and why it does not materially influence the outcome> (<C/D IDs>; counsel: <decide>).
- **If high-risk:** <what Chapter III requires of the provider and Article 26 of the deployer; FRIA under Article 27 if the deployer is in scope (not Annex III point 2), notified to the market surveillance authority (27(3)); Article 86 explanation; the plan goals or gaps for each> (<G IDs or gap:>).
- **Article 25(4) agreement (if high-risk):** <what the agency supplies; whether the written agreement exists> (<contract reference or gap:>; counsel: <confirm>).

## EU: Transparency obligations (Article 50)

| Paragraph | Applies? | How the design meets it | Evidence |
| --- | --- | --- | --- |
| 50(1) told they interact with AI | <yes / no / n/a:> | <disclosure; for agents, also on whose behalf it acts> | <C ID, G/A> |
| 50(2) machine-readable marking of generated content | <yes / no / counsel:> | <marking decision, or exception relied on: standard editing, no substantial alteration, B2B (guidelines para 87)> | <D ID> |
| 50(3) emotion recognition or biometric categorisation notice | <yes / n/a:> | <notice> | <C ID> |
| 50(4) deepfakes or public-interest text | <yes / n/a:> | <disclosure or editorial review> | <C ID> |

## EU: General-purpose AI model

- **Model and provider:** <model ID, model provider> (<D ID>).
- **Obligations under Articles 53 and 55:** sit with the model provider; <client> relies on its documentation (<source:>, counsel: <confirm>).
- **Fine-tuning or modification:** <none / what> (<D ID>; counsel: <if any>).
- **Downstream modification compute:** <none / compute used versus one third of the original> (<D ID>; counsel: <if any>).

## EU: Other regimes

- <GDPR Article 22 (privacy-impact-input-pack.md), Product Liability Directive, Cyber Resilience Act, NIS2, DORA, MDR, Data Act, DSA: each n/a: with its reason, or counsel: with the facts> (<IDs>).

## United Kingdom: UK GDPR and automated decisions

- **No AI-specific statute:** the UK has no AI Act; the regimes below apply (checked <YYYY-MM-DD>).
- **Regulator:** the Information Commission (formerly the ICO) (checked <YYYY-MM-DD>).
- **Significant decisions (Articles 22A to 22D):** <does an output decide with no meaningful human involvement; special category data; the four Article 22C safeguards> (privacy-impact-input-pack.md; <C/M IDs>; counsel: <significant? meaningful?>).
- **Restricted transfers:** <consultancy access from Australia; endpoints outside the UK; mechanism> (transfer-assessment.md; counsel: <data protection test met?>).

## United Kingdom: Equality, consumer, online safety and sector

- **Equality Act 2010:** <decisions about people; protected characteristics or proxies; public sector equality duty for a public body> (impact-assessment.md; counsel: <justified?>).
- **Consumer law, Online Safety Act, FCA, ATRS:** <each applies or n/a: with the reason> (<IDs>; counsel: <question>).

## Applicable dates

| Regime | Obligation | Applies from | Relevance here |
| --- | --- | --- | --- |
| <regime> | <obligation> | <date in words> (<provision>, checked <YYYY-MM-DD>) | <why it matters; plan goal> |

- **AI literacy (EU AI Act Article 4) and staff training:** <training and guidance for users> (<goal ID or gap:>).

## Questions for counsel

- counsel: <question>; regime <regime>; facts at <IDs>; needed before <goal or wait ID>.
