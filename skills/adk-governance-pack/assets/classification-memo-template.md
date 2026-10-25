---
document: classification-memo
system: <system name>
version: <design revision or build classified>
status: draft
counsel_required: <yes / no / pending>
prepared: <YYYY-MM-DD> by <agency or team>
for: <client counsel or AI governance lead>
sources: <docs/discovery/<topic>.md, docs/architecture/<topic>.md, docs/plans/<topic>.md>
---

# EU AI Act classification memo: <system name>

Draft for <client>'s counsel. It sets out the facts the design records and
the provisions of Regulation (EU) 2024/1689 as amended by Regulation (EU)
2026/1744 that appear relevant. Conclusions are proposals for counsel; not
legal advice.

## Summary

- **Proposed classification:** <prohibited / high-risk (Annex III point) / Article 6(3) derogation argued / transparency obligations only / minimal risk> (counsel: <confirm>).
- **Proposed roles:** <client: provider and deployer; agency: developer under contract> (counsel: <confirm>).
- **Obligations that follow:** <one line each, with the plan goal or gap> (<IDs>).
- **Blocking questions:** counsel: <count> questions, listed under Questions for counsel.

## System and intended purpose

- **What it does:** <one or two sentences> (<R/C IDs>).
- **Who uses it and who it affects:** <users; people its outputs are about> (<docs/discovery/<topic>.md §n, R IDs>).
- **What the model decides and what code or people decide:** <split> (<D/C IDs>).
- **Effects it can cause:** <reads, drafts, writes, messages, decisions about people> (<C IDs>).
- **AI system (Article 3(1)):** <yes, because it infers outputs with a model> (<D ID>; checked <YYYY-MM-DD>).

## Roles (provider and deployer)

- **Facts:** <who commissions it; whose name it runs under; who changes its purpose; who operates it> (<D IDs, source:>).
- **Proposed role of <client>:** <provider and deployer> (counsel: <confirm against the contract>).
- **Proposed role of <agency>:** <developer under contract; provider only if it markets the system under its own name> (counsel: <confirm>).
- **Article 25 triggers to watch:** <name, substantial modification or change of purpose that would move the provider role> (<D/G IDs>).
- **GDPR roles, separately:** <controller, processors> (DPIA input pack; counsel: <confirm>).

## Prohibited practices (Article 5)

| Point | Applies? | Facts | Evidence |
| --- | --- | --- | --- |
| (a) manipulation, (b) exploiting vulnerabilities | <no / counsel:> | <why> | <C IDs> |
| (ba), (bb) generated intimate or abuse material | <no / counsel:> | <why> | <C/D IDs> |
| (c) social scoring, (d) crime prediction by profiling | <no / counsel:> | <why> | <C IDs> |
| (e) facial scraping, (g) biometric categorisation, (h) real-time remote identification | <no / counsel:> | <why> | <D IDs> |
| (f) emotion inference at work or in education | <no / counsel:> | <why> | <C/D IDs> |

## High-risk classification (Article 6 and Annex III)

- **Annex I product:** <no / which product legislation> (<D ID or assumption:>).
- **Annex III area touched:** <none / point and area> (<R/C IDs>).
- **Profiling of natural persons:** <yes / no, with facts> (<C/D IDs>; counsel: <confirm>).
- **Article 6(3) derogation facts, if argued:** <narrow procedural / improves completed human work / detects patterns under human review / preparatory; and why it does not materially influence the outcome> (<C/D IDs>; counsel: <decide>).
- **If high-risk:** <what Chapter III requires of the provider and Article 26 of the deployer; FRIA under Article 27 if the deployer is in scope; the plan goals or gaps for each> (<G IDs or gap:>).

## Transparency obligations (Article 50)

| Paragraph | Applies? | How the design meets it | Evidence |
| --- | --- | --- | --- |
| 50(1) told they interact with AI | <yes / no / n/a:> | <disclosure> | <C ID, G/A> |
| 50(2) machine-readable marking of generated content | <yes / no / counsel:> | <marking decision> | <D ID> |
| 50(3) emotion recognition or biometric categorisation notice | <yes / n/a:> | <notice> | <C ID> |
| 50(4) deepfakes or public-interest text | <yes / n/a:> | <disclosure or editorial review> | <C ID> |

## General-purpose AI model

- **Model and provider:** <model ID, model provider> (<D ID>).
- **Obligations under Articles 53 and 55:** sit with the model provider; <client> relies on its documentation (<source:>, counsel: <confirm>).
- **Fine-tuning or modification:** <none / what> (<D ID>; counsel: <if any>).

## Applicable dates

| Obligation | Applies from | Relevance here |
| --- | --- | --- |
| <obligation> | <date> (<article>, checked <YYYY-MM-DD>) | <why it matters; plan goal> |

- **AI literacy (Article 4):** <training and guidance for users> (<goal ID or gap:>).

## Questions for counsel

- counsel: <question>; facts at <IDs>; needed before <goal or wait ID>.
