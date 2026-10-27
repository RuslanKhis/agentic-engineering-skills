# European Union: AI and privacy law for the governance pack

*Read 26 October 2026. Research for the EU part of
`skills/adk-governance-pack`: an audit of what the skill says now, and
the gaps. Drafts, not legal advice.*

## Conclusion

The skill's AI Act core holds. I re-read Regulation (EU) 2026/1744 (the
Digital Omnibus on AI) in the Official Journal. The Annex III and Annex I
high-risk dates are right. So are the Article 50 date and its transition,
the new Article 4 wording, Article 27(4) and the new prohibitions. Six
things have moved since the 25 October note, or were never in the skill:

1. **Article 50 has official guidance now, and it reaches agents.** The
   Commission published Article 50 guidelines on 20 July 2026 (C(2026)
   5054). Paragraph 31 says an agent that can interact with people must
   disclose both that it is an AI and *on whose behalf it acts*. It must
   also disclose itself to the person instructing it at key steps.
   Paragraph 63 says agent text that people perceive is synthetic content
   under 50(2) and must be marked. Reasoning steps and web requests are
   not. Paragraph 87 gives a narrow, cumulative B2B exemption. The skill
   still says "counsel on whether chat text is in scope" (`eu-ai-act.md`
   line 151). The Code of Practice has its correct name now, the "Code of
   Practice on Transparency of AI-generated Content". The Commission found
   it adequate for 50(2), (4) and (5) on 8 July 2026.
2. **Article 22 GDPR is underweighted for agents.** SCHUFA (C-634/21) says
   a score that a third party "draws strongly on" is itself an automated
   decision. Dun & Bradstreet Austria (C-203/22) says the data subject is
   owed an explanation of "the procedure and principles actually applied".
   A formula is not enough. On 8 October 2026 the Dutch DPA fined Uber
   EUR 824,990,000 for fully automated deactivations and for not telling
   drivers about them (Articles 22 and 13). The skill treats Article 22 in
   two lines. AI Act Article 86, the right to an explanation for Annex III
   high-risk systems, is missing.
3. **International transfers have no guidance, and the consultancy is in
   Australia.** Australia has no EU adequacy decision. Support access, log
   review or evaluation-set work by Australian staff on EU personal data is
   a Chapter V transfer. It needs Standard Contractual Clauses (SCCs) and a
   transfer impact assessment. The EU-US Data Privacy Framework (DPF) still
   stands. The General Court dismissed Latombe on 3 September 2025. But
   the appeal (C-703/25 P) is pending, and the US Supreme Court removed the
   FTC's independence on 29 June 2026 (*Trump v. Slaughter*). Treat the DPF
   as valid but fragile.
4. **The FRIA is half-described.** Article 27 leaves out Annex III point 2
   systems. It requires the deployer to notify the market surveillance
   authority of the results (27(3)). It applies from 2 December 2027. The
   AI Office template is still to come. The skill has no FRIA crosswalk.
5. **The Omnibus changed the supply-chain contract.** Amended Article
   25(4) requires a written agreement between the provider of a high-risk
   system and any third party that supplies "an AI system, AI model, tools,
   services, components, or processes". Breaching it is now finable under
   Article 99(4)(da). A consultancy building a high-risk system for a
   client is that third party.
6. **The GDPR and ePrivacy Omnibus is still only a proposal.** Its
   procedure is 2025/0360(COD), on COM(2025) 837. The European Parliament
   file is "Awaiting committee decision", with a draft report of 22 June
   2026. The Council reportedly agreed its mandate on 21 October 2026; that
   is secondary, because the Council's site blocked me. No trilogue has
   started. Drafts treat the GDPR and ePrivacy as unamended.

Three more acts matter where their facts apply. The Product Liability
Directive covers software and AI from 9 December 2026, and the developer is
a "manufacturer". The Cyber Resilience Act's reporting duties start on 11
September 2026, but only for *products*, not bespoke SaaS. NIS2 reaches the
consultancy only if it is a medium-sized or larger managed service provider
serving the EU. The AI Liability Directive was formally withdrawn on 6
October 2025.

## Sources

All primary sources were read on 26 October 2026. The EUR-Lex HTML pages
returned a bot challenge, so Official Journal texts came from the
Publications Office by CELEX number
(`http://publications.europa.eu/resource/celex/<CELEX>`), which serves the
same published act. The ELI links below are the citable addresses.

### Primary

| ID | Source | What it settles |
| --- | --- | --- |
| P1 | Regulation (EU) 2026/1744, Digital Omnibus on AI, of 8 July 2026, OJ L 24.7.2026, CELEX 32026R1744, <https://eur-lex.europa.eu/eli/reg/2026/1744/oj> | Read in full: amended Arts 2(7), 4, 4a, 5, 6(1a)-(1c), 10, 25(2) and (4), 27(4) and (5), 50(7), 56(6), 57, 75, 99, 111(2) and (4), 113; Annex VIII B points 7 and 9 deleted; entry into force on the third day after publication |
| P2 | Regulation (EU) 2024/1689, AI Act, CELEX 32024R1689, <https://eur-lex.europa.eu/eli/reg/2024/1689/oj> | Base text: Arts 27, 50, 86, 99, 101, 111, 113 |
| P3 | Commission AI Act page, <https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai> (last update 19 October 2026) | Timeline; political agreement 7 May 2026; list of published guidance |
| P4 | "AI Omnibus enters into force", 27 July 2026, <https://digital-strategy.ec.europa.eu/en/news/ai-omnibus-enters-force> | Summary of changes |
| P5 | Draft high-risk classification guidelines, 19 May 2026, <https://digital-strategy.ec.europa.eu/en/library/draft-commission-guidelines-classification-high-risk-ai-systems>; policy page <https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-high-risk-systems> (last update 19 October 2026) | Still draft; targeted consultation open until 23 July 2026 |
| P6 | Article 50 guidelines, published 20 July 2026, <https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems>; annex C(2026) 5054, <https://ec.europa.eu/newsroom/dae/redirection/document/131215> | Read paragraphs 10 to 13, 30 and 31, 61 to 65, 86 to 91 |
| P7 | Code of Practice on Transparency of AI-generated Content, <https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content> | Final code published 10 June 2026; about 190 signatories by end of July 2026 |
| P8 | Commission opinion on that code, published 9 July 2026, <https://digital-strategy.ec.europa.eu/en/library/commission-opinion-assessment-code-practice-transparency-ai-generated-content> | Adequate for Art 50(2), (4) and (5), concluded 8 July 2026 |
| P9 | GPAI Code of Practice, <https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai> (last update 7 October 2026) | Published 10 July 2025; found adequate; Google listed as a signatory |
| P10 | GPAI scope guidelines, approved 18 July 2025, <https://digital-strategy.ec.europa.eu/en/library/guidelines-scope-obligations-providers-general-purpose-ai-models-under-ai-act>; formal text C(2025) 7719 of 19 November 2025, <https://ec.europa.eu/newsroom/dae/redirection/document/118340> | Paragraphs 59 to 61: the one-third compute test for downstream modifiers |
| P11 | First harmonised standard, 19 October 2026, <https://digital-strategy.ec.europa.eu/en/library/first-harmonised-standard-supporting-ai-act-published-official-journal> | EN 18286:2026 (QMS, Art 17) under Implementing Decision (EU) 2026/2274 |
| P12 | "Supporting the implementation of the AI Act with clear guidelines", <https://digital-strategy.ec.europa.eu/en/news/supporting-implementation-ai-act-clear-guidelines> (last update 31 July 2026) | Pipeline: FRIA template, value chain, substantial modification, joint Commission and EDPB AI Act and GDPR guidelines |
| P13 | Legislative Observatory, 2025/0360(COD), <https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file?reference=2025/0360(COD)> | Stage "Awaiting committee decision"; draft report PE786.818 of 22 June 2026; amendments 27 July 2026 |
| P14 | EDPB-EDPS Joint Opinion 2/2026 on the Digital Omnibus, adopted 10 February 2026, <https://www.edpb.europa.eu/documents/legislative-opinion/edpb-edps-joint-opinion-22026-on-the-proposal-for-a-regulation-as_en> | What the GDPR and ePrivacy proposal contains, with paragraph numbers |
| P15 | EDPB-EDPS Joint Opinion 1/2026 on the Digital Omnibus on AI, 21 January 2026, <https://www.edpb.europa.eu/documents/legislative-opinion/edpb-edps-joint-opinion-12026-on-the-proposal-for-a-regulation-as_en> | Landing page only |
| P16 | GDPR, CELEX 32016R0679, <https://eur-lex.europa.eu/eli/reg/2016/679/oj> | Arts 13(2)(f), 14(2)(g), 15(1)(h), 22 |
| P17 | CJEU, *SCHUFA Holding (Scoring)*, C-634/21, 7 December 2023, <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62021CJ0634> | Operative part; "prohibition in principle" |
| P18 | CJEU, *Dun & Bradstreet Austria*, C-203/22, 27 February 2025, <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62022CJ0203> | Operative part; paragraphs 57 to 62 |
| P19 | General Court, *Latombe v Commission*, T-553/23, 3 September 2025, <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62023TJ0553> | Action dismissed |
| P20 | CJEU, *EDPS v SRB*, C-413/23 P, 4 September 2025, <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62023CJ0413> | Pseudonymised data is not personal data for every recipient |
| P21 | EDPB Opinion 28/2024 on AI models, adopted 17 December 2024, <https://www.edpb.europa.eu/documents/opinion-of-the-board-art-64/opinion-282024-on-certain-data-protection-aspects-related-to_en> | Unchanged |
| P22 | EDPB Guidelines 02/2026 on anonymisation, adopted 7 July 2026, public consultation, <https://www.edpb.europa.eu/documents/guideline/guidelines-022026-on-anonymisation_en>; summary of October 2026 | Entity-relative test; three criteria (no record isolation, no linkage, no inference) |
| P23 | EDPB Guidelines 03/2026 on web scraping in the context of generative AI, 8 July 2026, public consultation, <https://www.edpb.europa.eu/documents/guideline/guidelines-032026-on-web-scraping-in-the-context-of-generative-ai_en> | Controller, processor and joint-controller roles in scraping and fine-tuning |
| P24 | EDPB Guidelines 01/2025 on pseudonymisation, 17 January 2025, consultation closed, still v1, <https://www.edpb.europa.eu/documents/guideline/guidelines-012025-on-pseudonymisation_en> | Not yet final |
| P25 | EDPB Support Pool of Experts, *AI Privacy Risks & Mitigations: Large Language Models*, 10 April 2025, <https://www.edpb.europa.eu/documents/support-pool-of-experts/ai-privacy-risks-mitigations-large-language-models-llms_en> | Written by an external expert; the page says it is not the EDPB's position |
| P26 | EDPB DPF FAQ for European businesses v2.0, adopted 15 January 2026, <https://www.edpb.europa.eu/documents/other-guidance/eu-us-data-privacy-framework-faq-for-european-businesses-version-20_en> | Checking a US recipient's DPF certification |
| P27 | EDPB Work Programme 2026-2027, 12 February 2026, <https://www.edpb.europa.eu/documents/reports-statements-and-letters/edpb-work-programme-2026-2027_en> | Planned EU templates (DPIA, breach, LIA, ROPA, privacy notice); joint AI Act and GDPR guidelines |
| P28 | EDPB national news: Dutch DPA fines Uber, 8 October 2026, <https://www.edpb.europa.eu/news/dutch-dpa-fines-uber-eur-824-990-000-for-unlawful-automated-decision-making-and-insufficient_en> | Arts 22 and 13 enforcement |
| P29 | EDPB Guidelines 3/2025 on the DSA and the GDPR, final 17 September 2026, <https://www.edpb.europa.eu/documents/guideline/guidelines-32025-on-the-interplay-between-the-dsa-and-the-gdpr_en> | DSA note only |
| P30 | EDPB Guidelines 05/2021 on Art 3 and Chapter V (final, 24 February 2023), <https://www.edpb.europa.eu/documents/guideline/guidelines-052021-on-the-interplay-between-the-application-of-article-3-and-the_en>; Recommendations 01/2020 on supplementary measures (18 June 2021), <https://www.edpb.europa.eu/documents/recommendation/recommendations-012020-on-measures-that-supplement-transfer-tools-to_en>; Guidelines 07/2020 on controller and processor (7 July 2021), <https://www.edpb.europa.eu/documents/guideline/guidelines-072020-on-the-concepts-of-controller-and-processor-in-the-gdpr_en>; Guidelines 3/2018 on territorial scope, <https://www.edpb.europa.eu/documents/guideline/guidelines-32018-on-the-territorial-scope-of-the-gdpr-article-3-version-adopted_en> | Landing pages read; these guidelines are long-standing |
| P31 | Commission adequacy decisions page, <https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/adequacy-decisions_en> | Australia is not on the list |
| P32 | Commission EU-US data transfers page, <https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en> | DPF adequacy decision of 10 July 2023 in force |
| P33 | SCC Decision (EU) 2021/914, CELEX 32021D0914, <https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj> | Current SCCs |
| P34 | US Supreme Court slip opinions, October Term 2025, <https://www.supremecourt.gov/opinions/slipopinion/25> | *Trump v. Slaughter*, No. 25-332, decided 29 June 2026 (listing only; opinion not read) |
| P35 | Cyber Resilience Act, Regulation (EU) 2024/2847, CELEX 32024R2847, <https://eur-lex.europa.eu/eli/reg/2024/2847/oj> | Arts 2, 3, 12, 14, 69(3), 71; recitals 11 and 12 |
| P36 | Product Liability Directive, Directive (EU) 2024/2853, CELEX 32024L2853, <https://eur-lex.europa.eu/eli/dir/2024/2853/oj> | Arts 2, 4, 15, 22; recitals 13 and 14 |
| P37 | Data Act, Regulation (EU) 2023/2854, CELEX 32023R2854, <https://eur-lex.europa.eu/eli/reg/2023/2854/oj> | Arts 2, 29, 31, 50 |
| P38 | NIS2, Directive (EU) 2022/2555, CELEX 32022L2555, <https://eur-lex.europa.eu/eli/dir/2022/2555/oj> | Arts 2, 6, 23, 26, 41; Annex I |
| P39 | DORA, Regulation (EU) 2022/2554, CELEX 32022R2554, <https://eur-lex.europa.eu/eli/reg/2022/2554/oj> | Applies from 17 January 2025; Art 30 contract terms |
| P40 | Withdrawal of Commission proposals, OJ C/2025/5423, 6 October 2025, <http://data.europa.eu/eli/C/2025/5423/oj> | AI Liability Directive, 2022/0303(COD), withdrawn |
| P41 | Regulation (EU) 2025/2518 on GDPR enforcement procedure, OJ L 12.12.2025, <https://eur-lex.europa.eu/eli/reg/2025/2518/oj> | Applies from 2 April 2027 |
| P42 | EIOPA, "EIOPA publishes Opinion on AI governance and risk management", 6 August 2025, <https://www.eiopa.europa.eu/eiopa-publishes-opinion-ai-governance-and-risk-management-2025-08-06_en> | Scope excludes high-risk and prohibited AI |
| P43 | MDCG 2025-6 / AIB 2025-1, *Interplay between the MDR and IVDR and the AI Act*, June 2025, <https://health.ec.europa.eu/document/download/b78a17d7-e3cd-4943-851d-e02a2f22bbb4_en?filename=mdcg_2025-6_en.pdf> | Not a Commission position; MDR class IIa or above is high-risk under Art 6(1) |
| P44 | EDPB Coordinated Enforcement Action report on the right to erasure, 18 February 2026, <https://www.edpb.europa.eu/documents/coordinated-enforcement-framework/coordinated-enforcement-action-implementation-of-the-0_en> | Weak anonymisation used in place of deletion; backups; retention periods |

### Secondary (used only where no primary text could be read)

| ID | Source | Used for |
| --- | --- | --- |
| S1 | NicFab, "Digital Omnibus: the Council adopts its position", <https://www.nicfab.eu/en/posts/digital-omnibus-council/>, read 2026-10-26 | Council mandate 21 October 2026 (Coreper), Council document 13886/26, contents. It cites the Council press release <https://www.consilium.europa.eu/en/press/press-releases/2026/10/21/digital-rulebook-council-agrees-position-to-simplify-data-protection-privacy-and-cyber-reporting-rules/>, which returned 403 |
| S2 | IAPP, "EU member states finalize Digital Omnibus negotiating stance", <https://iapp.org/news/a/eu-member-states-finalize-digital-omnibus-negotiating-stance> (search result, 22 October 2026) | Corroborates S1 |
| S3 | Digital Policy Alert, Latombe appeal, <https://digitalpolicyalert.org/event/35459-latombe-filed-appeal-against-general-court-dismissal-of-challenge-to-european-unionunited-states-data-protection-framework-adequacy-decision-in-latombe-v-commission>, read 2026-10-26 | Appeal C-703/25 P lodged 31 October 2025; pending |
| S4 | PPC Land, <https://ppc.land/supreme-court-ftc-ruling-sinks-eu-us-data-deal-noyb-says/>; BBB National Programs, <https://bbbprograms.org/media/insights/blog/trump-slaughter-dpf>; both read 2026-10-26 | noyb's call to withdraw the DPF decision and its planned annulment action; counter-view |
| S5 | A&O Shearman, EBA letter on the AI Act mapping exercise, <https://finreg.aoshearman.com/eba-letter-on-outcome-of-ebas-eu-ai-act-mapping-exercise-against-eu-banking-and-payments-regulation>, read 2026-10-26 | EBA letter of 21 November 2025: no significant contradictions between the AI Act and banking law for credit scoring |
| S6 | activeMind, <https://www.activemind.legal/guides/scc-gdpr-data-importers/>, read 2026-10-26 | Separate SCCs for importers already subject to the GDPR: announced, adoption not found |

### Not verified at a primary source

- **The Council press release and mandate text** for 2025/0360(COD). The
  press release returned 403 and Council document ST 13886/26 returned
  404. The 21 October 2026 date and the contents come from S1 and S2.
- **The CJEU docket for C-703/25 P.** curia.europa.eu serves a JavaScript
  application that could not be read. The status comes from S3.
- **The EBA letter of 21 November 2025** (S5 only).
- **New SCCs for importers subject to Article 3(2).** Nothing adopted was
  found; S6 describes the plan.
- **The full *Trump v. Slaughter* opinion.** Only the docket listing was
  read (P34). Its effect on the DPF is commentary (S4).

## Part 1: Audit

### 1.1 AI Act facts re-checked against the Official Journal

| Claim in the skill | Where | Result | Source |
| --- | --- | --- | --- |
| Omnibus is Reg. 2026/1744, OJ L 24.7.2026, in force 27 July 2026 | `eu-ai-act.md` 9-12 | Correct. Adopted 8 July 2026. Art 4 of P1: in force on the third day after publication | P1, P4 |
| Annex III high-risk from 2 December 2027; Annex I from 2 August 2028 | `eu-ai-act.md` 194-195 | Correct. New Art 113(c)(i) and (ii). Art 6(5) is excepted, so the Commission's guideline duty is not deferred | P1 point (40) |
| Art 50 applies from 2 August 2026; 50(2) transition to 2 December 2026 for systems placed on the market before 2 August 2026 | `eu-ai-act.md` 146, 155-158, 192-193 | Correct. New Art 111(4) | P1 point (39); P6 |
| Art 4 replaced from 27 July 2026: "take measures to support"; no individual level guaranteed | `eu-ai-act.md` 172-180, 196 | Correct. New Art 4(2) adds the Commission's duty to publish practical examples; 4(3) adds Board recommendations | P1 point (5) |
| Prohibitions (ba), (bb) from 2 December 2026 | `eu-ai-act.md` 63-64, 190 | Correct. Incomplete: new Art 5(1a) bans *placing on the market* only where generating such material is the intended purpose, or a reasonably foreseeable and reproducible outcome without adequate safeguards. 5(1b) excludes edits that do not increase exposure | P1 point (7) |
| Art 25(2): initial provider hands over documentation, limits, technical access | `eu-ai-act.md` 49-51 | Correct. Missing: the carve-out where the initial provider "clearly specified" the system is not to be made high-risk; the new **Art 25(4) written agreement** with suppliers of AI systems, models, tools, services, components or processes; and Art 99(4)(da), which makes 25(2) and 25(4) finable | P1 points (12), (38) |
| Art 27(4) FRIA may cross-reference or include the DPIA | `eu-ai-act.md` 133-137 | Correct. The FRIA scope statement is incomplete (see 1.4) | P1 point (13); P2 Art 27 |
| Art 4a: bias-detection processing of special categories | `eu-ai-act.md` 139-142; `privacy-and-records.md` 92-93 | Mis-framed as "a legal basis". 4a(1) covers providers of high-risk systems. 4a(2) covers providers and deployers of other systems and models, and deployers of high-risk systems, "strictly necessary" and under all the conditions in 4a(1)(a) to (f). It applies "in addition to" the GDPR. 4a(1)(f) requires the records of processing to state why the processing was strictly necessary. 4a(2) creates no duty to detect bias | P1 point (6) |
| Art 6(3) systems still register (Art 49(2)) | `eu-ai-act.md` 111-112 | Correct. Annex VIII Section B points 7 and 9 are deleted (shorter registration) | P1 recital and point (42) |
| Annex I examples "machinery, medical devices, toys" | `eu-ai-act.md` 87-90 | Stale. The Omnibus deleted Annex I Section A point 1 (Machinery Directive) and added the Machinery Regulation 2023/1230 to Section B. New Art 6(1a) says systems used "solely" for non-safety user assistance, performance optimisation, service efficiency, automation, convenience or quality control are not safety components | P1 points (8), (41) |
| GPAI duties sit with the model provider | `eu-ai-act.md` 163-168 | Correct. Unchanged by the Omnibus. Missing: the GPAI guidelines' one-third compute test for downstream modifiers; Google's signature of the GPAI Code; Commission fines on GPAI providers (Art 101) only from 2 August 2026 | P2 Art 113(b); P9; P10 |
| "General-purpose AI models (Chapter V), governance, penalties: 2 August 2025" | `eu-ai-act.md` 191 | Imprecise. Art 113(b) applies those chapters from 2 August 2025 "with the exception of Article 101", so GPAI fines start 2 August 2026. Models placed on the market before 2 August 2025 comply by 2 August 2027 (Art 111(3)) | P2 Arts 101, 111(3), 113(b) |
| Penalties | not stated | Gap. Art 99(3): up to EUR 35m or 7 % (Art 5). Art 99(4): EUR 15m or 3 %, which covers deployer duties under Art 26, transparency under Art 50 and, since the Omnibus, Art 25(2) and (4). Art 99(5): EUR 7.5m or 1 % for misleading information. SMEs, and now SMCs (Art 99(6a)), pay the lower of the two amounts. Art 101: GPAI providers EUR 15m or 3 % | P2 Art 99; P1 point (38) |
| High-risk systems already on the market are caught only on significant design change; public authority systems by 2 August 2030 | `eu-ai-act.md` 198-202 | Correct. New Art 111(2) | P1 point (39) |

### 1.2 Commission guidance published since

| Instrument | Status on 26 October 2026 | Skill says | Source |
| --- | --- | --- | --- |
| High-risk classification guidelines (Art 6(5)) | **Still draft.** Published 19 May 2026; targeted consultation open until 23 July 2026; policy page updated 19 October 2026 still calls them draft. Final adoption expected, not dated | Draft, 19 May 2026 (`eu-ai-act.md` 112-114). Still right; add that the consultation closed | P5 |
| Article 50 guidelines | **Published 20 July 2026** (C(2026) 5054). Non-binding | Absent | P6 |
| Code of Practice on Transparency of AI-generated Content | Final code published 10 June 2026. **Commission found it adequate on 8 July 2026**; the AI Board followed the next day. Signing it is voluntary; adherence is "not conclusive evidence of compliance" | "voluntary Code of Practice on marking and labelling ... 10 June 2026" (`eu-ai-act.md` 158-159). Wrong name; adequacy missing | P7, P8 |
| GPAI Code of Practice | Published 10 July 2025; found adequate; Google, Anthropic, Microsoft and OpenAI listed as signatories | Absent | P9 |
| GPAI scope guidelines | Content approved 18 July 2025; formal C(2025) 7719 of 19 November 2025 | Absent | P10 |
| FRIA template (Art 27(5)), value-chain and substantial-modification guidelines, joint Commission and EDPB AI Act and GDPR guidelines | In preparation | Absent | P12, P27 |
| EN 18286:2026 (QMS) | First harmonised standard; presumption of conformity with Art 17 | Absent (relevant to high-risk providers only) | P11 |

### 1.3 Digital Omnibus amendments to the GDPR and ePrivacy: status

**Proposed. Not adopted, not in trilogue.** Procedure **2025/0360(COD)**,
proposal **COM(2025) 837** of 19 November 2025. Parliament: joint
ITRE-LIBE committee, stage "Awaiting committee decision", draft report 22
June 2026, amendments tabled 27 July 2026 (P13). Council: negotiating
mandate reported agreed by Coreper on 21 October 2026 (S1, S2; not read
at source). Trilogues can start only once Parliament has a mandate.
Checked 2026-10-26.

| Topic | What the Commission proposed (P14 paragraph) | Council mandate (secondary, S1) | Status |
| --- | --- | --- | --- |
| Personal data definition (Art 4(1)) | New subparagraph: information is not personal data for an entity that cannot identify the person with means reasonably likely to be used *by that entity*; new Art 41a implementing acts on when pseudonymised data stops being personal (P14 paras 11, 22). EDPB and EDPS "strongly urge" co-legislators not to adopt it | Keeps the current definition; adds a provision on pseudonymisation | Proposed |
| Legitimate interest for AI (new Art 88c) | Legitimate interest may be relied on for developing and operating AI models and systems, with an unconditional right to object (P14 paras 39-44). EDPB says Opinion 28/2024 already confirms this under the current text | Clarify, with safeguards | Proposed |
| Special categories in AI (new Art 9(2)(k), 9(5)) | Derogation for incidental and residual special-category data in AI development and operation (P14 section 6.2) | Adds safeguards | Proposed |
| Art 22 | Recast from "right not to be subject to" into an exhaustive list of permitted cases (P14 para 65). EDPB and EDPS want the CJEU's "prohibition in principle" kept (para 66) | No change reported | Proposed |
| DPIA lists (Art 35(4), (5)) | Single EU-level lists prepared by the EDPB and adopted by Commission implementing act; common template and methodology (P14 paras 88-90) | Single EU list plus templates | Proposed |
| Cookies (new Arts 88a, 88b; ePrivacy Art 5(3)) | Terminal-equipment rules for personal data moved into the GDPR; new consent exceptions; machine-readable browser signals (88b) (P14 section 10) | Moves the rules back to ePrivacy Art 5(3); deletes 88b; closed list of six consent-free purposes; four-month wait before asking again after a refusal | Proposed |
| Breach notification (Art 33) | Notify the authority only where the breach is likely to result in a **high** risk; **96 hours**; single EU entry point (P14 paras 73-77) | Same threshold and deadline; national entry points plus an EU information point | Proposed |
| Abusive access requests (Art 12(5)) | Clarifies abuse (P14 section 7.1) | Simplified handling | Proposed |

Already law but procedural only: Regulation (EU) 2025/2518 on GDPR
cross-border enforcement, which applies from 2 April 2027, checked
2026-10-26 (P41). It changes how complaints are handled, not what a DPIA
contains.

### 1.4 Statements in the skill that are now wrong, stale or incomplete

Wrong:

1. `references/eu-ai-act.md` line 151, 50(2) row: "counsel on whether
   chat text is in scope". Article 50 guidelines paragraph 63: agent
   outputs that people perceive as text are in scope. Exceptions:
   paragraphs 87 (cumulative B2B and industrial test), 88 (ephemeral
   real-time content) and 90 and 91 (standard editing; no substantial
   alteration) (P6).
2. `references/eu-ai-act.md` lines 158-159: "The Commission's voluntary
   Code of Practice on marking and labelling AI-generated content was
   published on 10 June 2026." Wrong name, and the adequacy finding of 8
   July 2026 is missing (P7, P8).
3. `references/eu-ai-act.md` lines 139-142 and
   `references/privacy-and-records.md` lines 92-93: Article 4a described
   as "a legal basis" or "a basis". It is a strictly-necessary,
   condition-bound permission that applies in addition to the GDPR, and
   it adds a records-of-processing entry (P1).
4. `references/eu-ai-act.md` line 191: penalties dated 2 August 2025
   without the Article 101 exception (P2).

Stale:

5. `references/eu-ai-act.md` lines 87-90: "machinery" as an Annex I
   example needing third-party assessment; machinery is now Section B (P1).
6. `references/eu-ai-act.md` lines 112-114: classification guidelines
   "still a draft on 25 October 2026". Still true; add that the
   consultation closed 23 July 2026 (P5).
7. `references/privacy-and-records.md` lines 14-17: Omnibus "reported as
   still under negotiation ... (secondary sources only)". Now partly
   primary (P13). Name the procedure and add Articles 4(1), 9, 33 and
   ePrivacy 5(3) to the list treated as unamended.
8. `references/eu-ai-act.md` lines 8-16 and `SKILL.md` line 23: read
   dates of 25 October 2026. Move to 26 October 2026 when the edits land.
9. `docs/research/governance-pack-2026-10-25.md` line 32 (code "and the
   Article 50 FAQ"; adequacy missing) and lines 80-82 (GDPR Omnibus
   "secondary only"). Update in the next research note rather than edit.

Incomplete:

10. `references/eu-ai-act.md` lines 131-134, FRIA scope: Annex III point
    2 exclusion, 27(3) notification, start date and template status
    missing (P2 Art 27).
11. `references/eu-ai-act.md` lines 49-53: Article 25(4) written
    agreement and its fine missing (P1).
12. `references/eu-ai-act.md` line 70: 5(1a) conditions missing (P1).
13. `references/eu-ai-act.md` lines 150 and 163-168: agent disclosure
    duty (guidelines paragraph 31) and GPAI modifier test missing (P6,
    P10).
14. `references/privacy-and-records.md` lines 88-91: Article 22 without
    SCHUFA, Dun & Bradstreet, Article 15(1)(h), Articles 13(2)(f) and
    14(2)(g), the Uber fine or AI Act Article 86 (P16-P18, P28).
15. `references/privacy-and-records.md`: no guidance on Chapter V
    transfers or Article 28 terms. The DPIA template has a transfer
    column at line 77 but nothing tells the drafter how to fill it.
16. `references/privacy-and-records.md` lines 129-137: no mention of
    Guidelines 02/2026, 03/2026, 01/2025 or *EDPS v SRB* (P20, P22-P24).

The checker (`scripts/check_governance.py`) has nothing wrong for the EU.
One optional gap: no Annex I trigger for medical-device software (see
Part 2, sector notes).

## Part 2: Gaps

Each item gives status and dates, the facts that trigger it in an agent
project, the paperwork mapped to the pack's documents, and the questions
for counsel.

### 2.1 Article 22 automated decisions, with SCHUFA and Dun & Bradstreet

**Status.** In force since 25 May 2018, checked 2026-10-26 (P16). Case
law: *SCHUFA*, 7 December 2023 (P17); *Dun & Bradstreet Austria*, 27
February 2025 (P18). Enforcement: Dutch DPA, Uber, EUR 824,990,000,
announced 8 October 2026 (P28). AI Act Article 86 (right to an
explanation from the deployer for decisions based on Annex III high-risk
output) sits in Chapter IX, which applies from 2 August 2026. It bites
only on systems that are high-risk, and Annex III classification applies
from 2 December 2027, checked 2026-10-26 (P1, P2). When Article 86 takes
practical effect is a counsel question.

**What the cases add.**

- Article 22(1) is "a prohibition in principle", which applies whether or
  not the person invokes it (*SCHUFA* para 52).
- An automated score is itself the "decision" where a third party "draws
  strongly on" it to establish, carry out or end a contract (*SCHUFA*,
  operative part). An agent that scores, ranks or recommends, with a
  human who usually follows it, can be the decision.
- Article 15(1)(h) gives "a genuine right to an explanation" of "the
  procedure and principles actually applied". Neither a formula nor a
  step-by-step description is enough. Telling the person how a variation
  in their data would have changed the result can be enough (*D&B* paras
  57-62). Trade secrets go to the supervisory authority or court for
  balancing; they are not a ground to refuse (*D&B*, operative point 2).
- The Uber decision found fully automated account deactivations
  unlawful, and the notice to drivers (Article 13) insufficient.

**Triggers.** The agent's output decides, or is usually followed on,
access to a service, a price, a claim, an account, employment, credit or
benefits. Auto-approve or auto-reject paths. Human review that is
sampled, rubber-stamped or unmeasured. Special-category data feeding a
decision (Article 22(4)).

**Paperwork.**

- DPIA input pack: "Legal basis" Article 22 bullet. Add the SCHUFA test
  (does a person decide, and how often do they depart from the output, as
  an M record?), the Article 22(2) exception relied on, and the 22(3)
  safeguards (human intervention, a chance to give a view, contest).
- DPIA input pack: "Necessity and proportionality". Notice content:
  existence of automated decisions, meaningful information about the
  logic, significance and consequences (Arts 13(2)(f), 14(2)(g)). Also
  the Article 15(1)(h) explanation path and who produces it.
- System card: "Human oversight", with the share reviewed and the
  override rate as M records; "Limits".
- Classification memo: Article 86 row where Annex III applies.

**Counsel questions.**

- Is any output a decision under *SCHUFA*, given the measured override
  rate (M ID)?
- Which Article 22(2) exception applies, and does the contract exception
  meet "necessary"?
- Can the explanation the design can produce (features used, a
  counterfactual) satisfy *D&B*?
- When does Article 86 start for this system?

### 2.2 Articles 13 to 15 transparency for AI

**Status.** In force, checked 2026-10-26 (P16). A new transparency
derogation is only proposed (P14 section 7.2).

**Triggers.** Any personal data in prompts, retrieval, memory, logs or
evaluation sets. Data obtained indirectly, such as CRM records the agent
reads about people who never use it, falls under Article 14.

**Paperwork.**

- DPIA input pack: "Necessity and proportionality", rights bullet. The
  notice items: model provider as recipient, memory retention, transfers,
  automated decisions, the source of indirectly collected data.
- Records of processing: recipients and transfers columns.
- System card: "Data".

**Counsel questions.**

- Does the client's existing privacy notice cover the agent's purposes
  and recipients?
- Does any Article 14(5) exemption apply to people named in records?

### 2.3 Chapter V international transfers

**Status, checked 2026-10-26.**

- Australia has no adequacy decision (P31).
- SCCs: Decision (EU) 2021/914 (P33). The separate SCCs for importers
  already subject to the GDPR were announced; no adoption found (S6).
- DPF adequacy decision of 10 July 2023 in force (P32).
- *Latombe*: action dismissed by the General Court on 3 September 2025
  (P19). Appeal C-703/25 P lodged 31 October 2025 and pending (S3).
- *Trump v. Slaughter*, decided 29 June 2026, removed for-cause protection
  for FTC commissioners (P34). noyb asked the Commission to withdraw the
  DPF decision and announced an annulment action (S4). Whether that has
  been filed is unconfirmed.
- EDPB DPF FAQ v2.0, 15 January 2026 (P26).
- EDPB Recommendations 01/2020 (transfer impact assessment and
  supplementary measures) and Guidelines 05/2021 (when a disclosure to an
  importer abroad is a "transfer") (P30).

**Triggers in an agent project.**

- Staff of the Australian consultancy see EU personal data: support,
  log and trace review, evaluation-set curation, incident triage. That is
  a transfer from the EU client (exporter) to a non-adequate country.
- A model endpoint, grounding service or abuse-monitoring store outside
  the EEA. The global endpoint does not guarantee location
  (`privacy-and-records.md` lines 108-109).
- US sub-processors relying on the DPF.
- Observability exporters (traces to a SaaS outside the EEA).

**Paperwork.**

- DPIA input pack: "Recipients, processors and regions". Per recipient:
  country, adequacy or DPF status (with the date the recipient's
  certification was checked), SCC module (Module 2 controller to
  processor; Module 3 processor to sub-processor), transfer impact
  assessment reference.
- Records of processing: column (e) on transfers and safeguards.
- Security questionnaire: "Hosting and region" and "Sub-processors".
- New gap line when no transfer impact assessment exists.

**Counsel questions.**

- Is Australian access a transfer under Guidelines 05/2021? Which SCC
  module applies, and who signs as exporter?
- Does the transfer impact assessment for Australia need supplementary
  measures (pseudonymised evaluation sets, EU-only log access)?
- Should DPF-reliant US transfers have SCCs as a fallback given *Slaughter*
  and the pending appeal?
- Does the Google Cloud DPA's transfer mechanism cover every service the
  design uses (grounding, abuse monitoring, support)?

### 2.4 Article 28 processor terms with the consultancy and the model provider

**Status.** In force (P16). Guidelines 07/2020 (P30). Under the Omnibus,
new Art 25(4) AI Act adds a parallel contract for high-risk systems
(P1).

**Triggers.** The consultancy touches personal data during build, test
or support. The client relies on Google Cloud's DPA. Sub-processors,
including MCP servers or SaaS tools the agent calls with personal data.
Any fine-tuning on client data.

**Paperwork.**

- DPIA input pack: recipients table with the contract reference per
  processor.
- Records of processing: the processor record (Art 30(2)) for the
  consultancy.
- Security questionnaire: "Sub-processors".
- Classification memo: roles, plus a row on the Art 25(4) agreement
  where the system is high-risk.

**Counsel questions.**

- Does the consultancy's contract contain every Art 28(3) term, including
  sub-processor approval and deletion or return at the end?
- Is a tool provider a processor or a separate controller?
- Where the system is high-risk, does the contract meet Art 25(4)
  (information, capabilities, technical access, assistance)?

### 2.5 EDPB Opinion 28/2024, LLM guidance and the 2025-2026 guidelines

**Status, checked 2026-10-26.**

- Opinion 28/2024, 17 December 2024, unchanged (P21).
- Guidelines 02/2026 on anonymisation, adopted 7 July 2026, in public
  consultation. Anonymity is assessed per entity. Three criteria: no
  record isolation, no linkage, no inference. "Means" include those
  available through a third party (P22).
- Guidelines 03/2026 on web scraping for generative AI, 8 July 2026, in
  consultation. Scraping and fine-tuning roles: controller, processor,
  joint controllers (P23).
- Guidelines 01/2025 on pseudonymisation: consultation closed, still v1
  (P24).
- *EDPS v SRB*, 4 September 2025: pseudonymised data is not personal data
  for a recipient who cannot re-identify. It stays personal data for the
  controller (P20). The Omnibus definition change would codify it; that
  is only proposed (1.3).
- The LLM report (April 2025) was written by an external expert for the
  EDPB's expert pool and is not an EDPB position (P25). It is useful as a
  risk catalogue for chatbots and assistants.
- Work programme 2026-2027: EU templates for DPIA, breach, legitimate
  interest assessment, records of processing and privacy notices; joint
  AI Act and GDPR guidelines (P27).
- Right-to-erasure enforcement report, 18 February 2026: weak
  anonymisation used instead of deletion; deletion from backups (P44).

**Triggers.**

- An evaluation set or memory store described as "anonymised".
- Fine-tuning or retrieval over scraped or bought web data.
- Erasure from memory, vector stores and backups.

**Paperwork.**

- DPIA input pack: "Model provider data use" (Opinion 28/2024 reliance)
  and "Retention and erasure" (vector stores, memory, backups).
- Data flows: test any "anonymised" claim against the three criteria.

**Counsel questions.**

- Is the evaluation set anonymous for the consultancy under Guidelines
  02/2026 (draft), or only pseudonymised?
- Does the client's accountability assessment for the Gemini model under
  Opinion 28/2024 rest on Google's public documentation alone?

### 2.6 Fundamental rights impact assessment (AI Act Article 27) and the DPIA

**Status.** Article 27 is in Chapter III Section 3, so it applies with
Annex III high-risk obligations from 2 December 2027, checked 2026-10-26
(P1 point (40); P2). The AI Office questionnaire template (Art 27(5),
now also allowing DPIA cross-references) is in preparation (P12).

**Who must do it.** Deployers of Annex III high-risk systems, *except
point 2* (critical infrastructure), that are either:

- bodies governed by public law, or private entities providing public
  services; or
- any deployer of systems under point 5(b) (creditworthiness and credit
  scoring, except fraud detection) or 5(c) (life and health insurance
  risk and pricing).

It is done before first use and updated when the facts change (27(2)).
**The results are notified to the market surveillance authority** with
the template (27(3)).

**How it relates to the DPIA.** The DPIA covers personal data risks to
data subjects. The FRIA covers fundamental rights of affected groups,
including people whose data is not processed. Art 27(4) lets the FRIA
cross-reference or include DPIA sections where they already meet an
obligation. The required FRIA contents (27(1)(a) to (f)) map onto the
pack:

| Art 27(1) | Pack section |
| --- | --- |
| (a) deployer's processes using the system | Impact assessment "Scope and intended use"; DPIA "Processing description" |
| (b) period and frequency of use | DPIA "Processing description" (scope) |
| (c) categories of persons and groups affected | Impact assessment "Interested parties" |
| (d) specific risks of harm, using the provider's Art 13 information | Impact assessment "Impacts"; DPIA "Risks and measures" |
| (e) human oversight measures per the instructions | System card "Human oversight" |
| (f) measures if risks materialise, governance, complaints | Impact assessment "Measures", "Residual risk and decision"; system card contest path |

**Triggers.** Public-sector client, or a utility, education provider,
health provider or other provider of public services. A credit or
life and health insurance use case.

**Paperwork.** Impact assessment, with a new "FRIA crosswalk" table (the
mapping above). Classification memo "If high-risk" bullet. Plan: a wait
`W<n>` for the notification to the market surveillance authority.

**Counsel questions.**

- Is the client a "private entity providing public services"?
- Which DPIA sections can the FRIA cross-reference under 27(4)?
- Which authority receives the 27(3) notification?

### 2.7 Data Act

**Status.** Applies from 12 September 2025. Article 3(1) design duty for
connected products placed on the market after 12 September 2026. Chapter
IV unfair-terms rules for B2B data contracts concluded after 12 September
2025, and from 12 September 2027 for older open-ended contracts. Cloud
switching charges banned from 12 January 2027. All checked 2026-10-26
(P37 Arts 29, 50). Data Act amendments in the Digital Omnibus are
proposed only (P14 part II).

**Relevant only where:**

- the agent is a "related service" of a connected (IoT) product, which
  brings Chapter II data-access duties;
- the client offers the agent to its own customers as a cloud service,
  which brings Chapter VI switching duties. Art 31(1) exempts services
  mostly custom-built for one customer that are not sold at scale;
- a data-sharing contract term is unilaterally imposed (Chapter IV);
- the client wants an exit plan from Google Cloud (switching rights).

A bespoke internal agent usually triggers none of these.

**Paperwork.** Mention only. A `n/a:` line in the classification memo's
questions; an exit-plan answer in the security questionnaire
("Availability and recovery").

**Counsel question.** Is the agent a related service or a data processing
service offered at scale?

### 2.8 NIS2 and the Cyber Resilience Act

**NIS2 status.** Member States apply it from 18 October 2024, checked
2026-10-26 (P38 Art 41). Significant incidents: early warning within 24
hours, then notification within 72 hours (Art 23). Incident-reporting
single entry points are proposed in the Digital Omnibus only (S1).

**When an agent project is in scope.**

- *Client side* (common). The client is an essential or important entity
  (Annex I or II sectors, medium-sized or larger). The consultancy then
  sees supply-chain security clauses (Art 21(2)(d)), and the agent's
  incidents feed the client's 24-hour and 72-hour reports.
- *Consultancy side* (only on these facts). It operates or maintains the
  system for the client after go-live ("managed service provider", Art
  6(39), Annex I "ICT service management (B2B)"), is medium-sized or
  larger, and offers the service in the EU. Then it must designate an EU
  representative (Art 26(3)) and is subject to the Member State where
  that representative is established.

**CRA status.** Applies from 11 December 2027. Reporting duties (Art 14)
apply from 11 September 2026, including to products placed on the market
before 11 December 2027 (Art 69(3)). Notified-body chapter from 11 June
2026. All checked 2026-10-26 (P35 Art 71). Reporting: actively exploited
vulnerability, early warning within 24 hours, notification within 72
hours, final report within 14 days of a fix. Severe incident: 24 hours,
72 hours, final report within one month. All via ENISA's single
reporting platform.

**When an agent product is in scope.** A "product with digital elements"
is software or hardware made available on the market, with its remote
data processing (Art 3). Recital 12: SaaS is a NIS2 matter, not a CRA
one, unless it is the remote data processing of a product. In scope:

- an agent packaged and *sold or distributed* as software (a downloadable
  app, an on-premises install, an SDK or a reusable accelerator the
  consultancy licenses to several clients);
- the cloud back end of such a product.

A bespoke agent hosted for one client is not "made available on the
market" as a product. Products under the MDR and IVDR are excluded (Art
2(2)). High-risk AI systems meeting CRA essential requirements are deemed
to meet AI Act Art 15 cybersecurity (CRA Art 12; AI Act Art 42(3) as
added by P1).

**Paperwork.**

- Security questionnaire: "Incident response", listing the reporting
  clocks that apply (GDPR 72 hours; NIS2 24 and 72 hours; CRA 24 and 72
  hours; AI Act Art 73 for high-risk providers).
- Security questionnaire: "Vulnerability management" (CRA Annex I Part
  II, if a product).
- Classification memo: "Questions for counsel".

**Counsel questions.**

- Does any deliverable become a product made available on the EU market?
- Is the consultancy a managed service provider within NIS2 for this
  client, and does it need an EU representative?

### 2.9 Product Liability Directive (EU) 2024/2853

**Status.** Transposition by 9 December 2026. Applies to products placed
on the market or put into service after 9 December 2026. Both checked
2026-10-26 (P36 Arts 2(1), 22).

**What changes.**

- "Product" includes software (Art 4(1)). Recital 13 names "AI systems"
  and covers software "supplied through a software-as-a-service model".
- "Manufacturer" includes whoever "develops" the product, whoever has it
  designed and puts their name on it, and whoever develops it for their
  own use (Art 4(10)). Both the consultancy and the client can be
  manufacturers.
- Liability cannot be limited or excluded by contract towards the
  injured person (Art 15).
- Damage is to natural persons: death, personal injury including
  medically recognised psychological harm, damage to property, and
  destruction or corruption of data not used for professional purposes.
- Lack of software updates needed for safety defeats a later-defect
  defence.
- Substantial modification, including through continuous learning,
  makes a new product.
- Free and open-source software outside commercial activity is excluded
  (Art 2(2)).

**Triggers.**

- A consumer-facing or patient-facing agent put into service after 9
  December 2026.
- An agent whose actions can cause injury, property damage or loss of
  personal (non-professional) data.
- Any agent the consultancy reuses across clients.

Internal staff tools carry less exposure, because professional data and
property are excluded.

**Paperwork.**

- System card: intended use, out-of-scope use, limits, update and
  rollback ownership. These are evidence on "defectiveness".
- Security questionnaire: "Vulnerability management" and "Secure
  development".
- Impact assessment: harms to natural persons.

**Counsel questions.**

- Who is the manufacturer between the consultancy and the client?
- What indemnities and insurance cover joint and several exposure that
  cannot be excluded towards the injured person?
- Who is obliged to supply safety updates after hand-over?

### 2.10 AI Liability Directive

**Status.** Proposal 2022/0303(COD) withdrawn. Approved by the Commission
on 16 July 2025; notice published in the Official Journal on 6 October
2025, checked 2026-10-26 (P40). There is no EU-level fault-based AI
liability rule; national tort law applies.

**Paperwork.** Mention only. Remove any reference to it.

### 2.11 Digital Services Act

**Relevant only where** the agent is part of an intermediary service:
hosting user content, an online platform, or a very large online platform
or search engine. The AI Omnibus gives the AI Office exclusive competence
over AI systems that are or are integrated into very large online
platforms or search engines (new AI Act Art 75(1)(b), P1). The EDPB's
final DSA-GDPR guidelines are dated 17 September 2026 (P29).

**Paperwork.** Mention only, as an `n/a:` line in the memo unless the
client is a platform.

### 2.12 Sector notes

**Insurance.** EIOPA Opinion on AI governance and risk management, 6
August 2025 (P42). It covers AI under the Insurance Distribution
Directive and Solvency II. It excludes high-risk and prohibited AI under
the AI Act (life and health pricing is Annex III 5(c)). It expects data
governance, record-keeping, fairness, cybersecurity, explainability and
human oversight.

**Banking.** The EBA letter of 21 November 2025 on its AI Act mapping
found no significant contradictions between the AI Act and banking law
for creditworthiness AI (S5; primary not read). DORA applies to financial
entities from 17 January 2025, checked 2026-10-26 (P39). Article 30 sets
mandatory terms for ICT third-party contracts, which reach a consultancy
supplying or operating the agent.

Paperwork for financial-sector clients:

- Classification memo: Annex III 5(b) and 5(c) checks; FRIA for 5(b) and
  5(c) deployers.
- Impact assessment: the EIOPA principles as measures.
- Security questionnaire: DORA contract and incident answers.
- Counsel: does the client classify the consultancy as an ICT third-party
  service provider supporting critical or important functions?

**Health.** Under MDCG 2025-6 / AIB 2025-1 (June 2025, not a Commission
position), medical-device software in MDR class IIa, IIb or III needs
notified-body assessment. Such AI is therefore high-risk under AI Act Art
6(1), with obligations from 2 August 2028, checked 2026-10-26 (P1, P43).
An agent intended to give information used for diagnostic or therapeutic
decisions can be medical-device software. The CRA does not apply to
MDR and IVDR products (P35 Art 2(2)). New AI Act Art 6(1a): convenience
or efficiency features that serve no safety function are not safety
components (P1).

Paperwork for health clients: classification memo "Annex I product" row,
plus a counsel question on MDR qualification and class.

Optional checker change: add an Annex I trigger area (`medical device`,
`in vitro diagnostic`, `diagnos(is|tic) decision`) to `ANNEX_III` in
`scripts/check_governance.py` lines 73-95, so these drafts force
`counsel_required: yes`.

## Ranked list for the EU

**Must cover**

1. AI Act Art 50 with the July 2026 guidelines. Agent disclosure of AI
   nature and principal; text marking with the paragraph 87 B2B test;
   the code's adequacy.
2. GDPR Art 22 with *SCHUFA*, *D&B*, Arts 13 to 15 and the Uber fine;
   AI Act Art 86 where Annex III applies.
3. Chapter V transfers: Australian access, SCCs, transfer impact
   assessment, DPF fragility.
4. Annex III classification and Art 6(3) facts (existing), draft
   guidelines status, Art 25(4) supply contract.
5. FRIA scope, 27(3) notification and DPIA crosswalk.
6. Omnibus status line: AI Omnibus adopted; GDPR and ePrivacy Omnibus
   proposed (2025/0360(COD)).
7. Art 28 processor terms and sub-processors (consultancy, Google, tool
   providers).

**Should cover**

8. Art 4a framing and the records-of-processing entry it requires.
9. EDPB anonymisation (draft), pseudonymisation and *SRB*, and erasure
   from memory and backups.
10. Product Liability Directive from 9 December 2026 for consumer- or
    patient-facing agents and reusable products.
11. Penalties summary (AI Act Art 99 and 101; GDPR Art 83).
12. GPAI: one-third compute test for fine-tuning; Google's GPAI Code
    signature.
13. Sector screens: finance (FRIA for 5(b) and 5(c), EIOPA, DORA
    contracts) and health (MDR class IIa or above, high-risk from 2
    August 2028).
14. NIS2 client-side supply-chain duties and reporting clocks.

**Mention only**

15. CRA (only if a product is made available on the market; reporting
    from 11 September 2026).
16. NIS2 consultancy-as-managed-service-provider test.
17. Data Act (connected products, SaaS switching, B2B unfair terms).
18. DSA (platforms only).
19. AI Liability Directive withdrawn.
20. GDPR procedural Regulation 2025/2518 (from 2 April 2027).
21. EN 18286 (high-risk providers' QMS).

## Screening checklist

| Trigger fact (from the design or brief) | Law | Pack document and section |
| --- | --- | --- |
| Agent talks to people (chat, voice, email, calls) or acts for a person towards others | AI Act Art 50(1); guidelines paras 30-31 | Classification memo "Transparency obligations", 50(1) row: disclosure of AI nature and principal, at first interaction and key steps |
| Agent output reaches people as text, audio, image or video | AI Act Art 50(2); guidelines paras 61-65, 87-91; Art 111(4) | Memo 50(2) row: marking decision or exception relied on |
| Generated content published to inform the public, or deepfakes | AI Act Art 50(4) | Memo 50(4) row; editorial review contract |
| Emotion or biometric analysis of people | AI Act Art 5(1)(f), 50(3); Annex III 1 | Memo "Prohibited practices", "Transparency obligations" |
| Image or video generation open to users | AI Act Art 5(1)(ba), (bb), 5(1a), from 2 December 2026 | Memo "Prohibited practices" (ba), (bb) row |
| Output decides or is usually followed on access, price, claim, account, job, credit or benefit | GDPR Art 22, 13(2)(f), 15(1)(h); *SCHUFA*; *D&B*; AI Act Art 86 | DPIA "Legal basis", "Necessity and proportionality"; system card "Human oversight" (override rate M ID) |
| Use in employment, education, credit, insurance, public services, migration or justice | AI Act Annex III; Art 6(3); Art 26 | Memo "High-risk classification"; `counsel_required: yes` |
| Annex III deployer is a public body or provides public services, or the use is credit or life and health insurance | AI Act Art 27 | Impact assessment FRIA crosswalk; memo "If high-risk"; plan wait for 27(3) notification |
| Consultancy supplies components or tools for a high-risk system | AI Act Art 25(4) (Omnibus) | Memo "Roles"; counsel question on the written agreement |
| Special-category data used to test or fix bias | AI Act Art 4a; GDPR Art 9 | DPIA "Legal basis"; records of processing (4a(1)(f) reasons) |
| Consultancy staff outside the EEA access personal data (support, logs, evaluation sets) | GDPR Chapter V; SCCs 2021/914; EDPB Recs 01/2020 | DPIA "Recipients, processors and regions"; records of processing transfers column |
| Model, grounding, abuse logging or telemetry outside the EEA, or US sub-processors | GDPR Chapter V; DPF; *Latombe* appeal | Same; security questionnaire "Hosting and region", "Sub-processors" |
| Any processor or tool provider handles personal data | GDPR Art 28 | DPIA recipients table; records of processing processor record |
| Data called "anonymised" or "pseudonymised" | GDPR Art 4(1), 4(5); *EDPS v SRB*; EDPB Guidelines 02/2026 (draft), 01/2025 | DPIA "Data flows", "Retention and erasure" |
| Fine-tuning or training on personal or scraped data | EDPB Opinion 28/2024; Guidelines 03/2026 (draft); GPAI guidelines paras 59-61 | DPIA "Model provider data use"; memo "General-purpose AI model" |
| Consumer- or patient-facing agent put into service after 9 December 2026, or a reusable product | Product Liability Directive | System card "Intended use", "Limits"; impact assessment harms to natural persons |
| Deliverable distributed as software (app, on-premises install, SDK, licensed accelerator) | CRA (Art 14 from 11 September 2026) | Security questionnaire "Incident response", "Vulnerability management" |
| Client in a NIS2 sector, or consultancy operates the system after go-live | NIS2 Arts 21, 23, 26 | Security questionnaire "Incident response"; memo "Questions for counsel" |
| Client is a bank, insurer or other financial entity | DORA Art 30; EIOPA Opinion; EBA mapping; Annex III 5(b), 5(c) | Security questionnaire; impact assessment "Measures"; memo |
| Agent informs diagnosis or treatment | MDR; MDCG 2025-6; AI Act Art 6(1) | Memo "High-risk classification" (Annex I product) |
| Agent is a related service of a connected product, or offered as SaaS at scale | Data Act Chapters II and VI | Memo "Questions for counsel" (`n/a:` otherwise) |
| Agent embedded in an online platform | DSA; AI Act Art 75(1)(b) | Memo `n/a:` unless a platform |
| Website or app front end sets non-essential cookies | ePrivacy Art 5(3) (national law; Omnibus changes proposed) | DPIA "Data flows" (front end) |

## Exact corrections to the existing files

Every new applicability date below carries `checked 2026-10-26`, because
the references are copied into drafts the checker reads.

### `references/eu-ai-act.md`

**Lines 8-16.** Change "read in the Official Journal text on 25 October
2026" to "on 26 October 2026", and "copy `checked 2026-10-25`" to "copy
`checked 2026-10-26`".

**Lines 49-53.** Replace from "Since the Omnibus, Article 25(2)" to the
end of the paragraph with:

> Since the Omnibus, Article 25(2) also says what the original provider
> must hand over in that case (documentation, known limits and failure
> modes, targeted technical access), unless it clearly specified that its
> system is not to be changed into a high-risk system. New Article 25(4)
> requires the provider of a high-risk system and any third party that
> supplies "an AI system, AI model, tools, services, components, or
> processes" used in it to agree in writing the information, technical
> access and assistance the provider needs. Article 99(4)(da) makes 25(2)
> and 25(4) finable. An agency building a high-risk system for a client
> is such a third party. State the facts (who commissions, whose name,
> who changes the purpose, what the agency supplies) with their IDs and
> write the role and the 25(4) agreement as `counsel:` to confirm.

**Line 70**, row (ba), (bb), "Where an agent could get near it" cell.
Replace with:

> Any open image or video generation. Placing on the market is banned
> only where this is the intended purpose, or a reasonably foreseeable and
> reproducible outcome without adequate safeguards (Art 5(1a)); a
> deployer's use is banned when it uses the system for that purpose.

**Lines 87-90.** Replace "(machinery, medical devices, toys and others;
rare for agency agents)" with:

> (medical devices, toys, lifts and others; machinery moved to Section B
> under the Omnibus; rare for agency agents). Since the Omnibus, Article
> 6(1a) says systems used solely for non-safety user assistance,
> performance optimisation, service efficiency, automation, convenience
> or quality control are not safety components.

**Lines 111-114.** Replace from "and still registers" to the end of the
paragraph with:

> and still registers it (Article 49(2)), with the shorter Annex VIII
> Section B the Omnibus introduced. The Commission's guidelines on
> classification (Article 6(5)) were still a draft on 26 October 2026:
> published for consultation 19 May 2026, targeted consultation closed 23
> July 2026. Cite them as draft
> (<https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-high-risk-systems>).

**Lines 131-137.** Replace from "A fundamental rights impact assessment"
to "written to be cited by section." with:

> A fundamental rights impact assessment (Article 27) is required, before
> first use, of deployers of Annex III systems other than point 2 that are
> bodies governed by public law or private entities providing public
> services, and of any deployer of Annex III points 5(b) (credit) and 5(c)
> (life and health insurance). The deployer notifies the market
> surveillance authority of the results on the AI Office template
> (Article 27(3)); the template is not yet published. Article 27 applies
> with the Annex III obligations from 2 December 2027 (Art. 113(c),
> checked 2026-10-26). Since the Omnibus, Article 27(4) lets the FRIA
> cross-reference or include the relevant parts of the GDPR DPIA, so the
> [DPIA input pack](../../skills/adk-governance-pack/references/privacy-and-records.md) is written to be cited by
> section, and the impact assessment carries the FRIA crosswalk (Article
> 27(1)(a) to (f) to pack sections).

**Lines 139-142.** Replace with:

> Article 4a (added by the Omnibus) lets providers of high-risk systems
> (4a(1)), and providers and deployers of other AI systems and deployers
> of high-risk systems (4a(2)), exceptionally process special categories
> of personal data where strictly necessary to detect and correct bias.
> All of conditions (a) to (f) apply: other data, including synthetic or
> anonymised data, would not do; re-use limits and pseudonymisation;
> access controls; no transmission to others; deletion once the bias is
> corrected; and the records of processing state why it was strictly
> necessary. It applies in addition to the GDPR, not instead of it, and
> imposes no duty to run such checks. A bias-monitoring contract such as
> an adverse-impact check names it as `counsel:`, with the Article 6 basis
> and the Article 9 condition alongside.

**Line 150**, 50(1) row, "Typical agent design evidence" cell. Replace
with:

> The chat discloses it is an AI (a C-ID with a UI test). An agent acting
> for someone towards others also discloses on whose behalf it acts, and
> discloses itself to its instructing user at key steps (Commission
> guidelines of 20 July 2026, paragraph 31)

**Line 151**, 50(2) row, last cell. Replace with:

> Marking decision (watermark, metadata, provenance) for every output
> people perceive, agent text included (guidelines paragraph 63);
> intermediate steps and web requests are out of scope. Exceptions:
> standard editing or no substantial alteration (paragraphs 90 and 91);
> narrow B2B or industrial use meeting all three paragraph 87 conditions.
> The exception relied on is `counsel:`

**Lines 155-159.** Replace from "Systems placed on the market" to the end
of the paragraph with:

> Systems placed on the market before 2 August 2026 have until 2 December
> 2026 for 50(2) (Article 111(4), added by the Omnibus, checked
> 2026-10-26). The Commission's Article 50 guidelines were published on
> 20 July 2026 (C(2026) 5054,
> <https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems>).
> The Code of Practice on Transparency of AI-generated Content (final
> text 10 June 2026) was found adequate for Article 50(2), (4) and (5) by
> the Commission on 8 July 2026. Signing is voluntary and is not
> conclusive evidence of compliance; non-signatories show equivalent
> means
> (<https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content>).

**Lines 163-168.** Append to the paragraph:

> The Commission's GPAI guidelines (C(2025) 7719) treat a downstream
> modifier as a model provider when the compute used for the modification
> exceeds a third of the original model's training compute (paragraphs 59
> to 61); ordinary fine-tuning by an agency rarely reaches it. Record the
> compute used as a fact. Google is a signatory of the GPAI Code of
> Practice (published 10 July 2025, found adequate), which the client can
> cite as the provider's compliance route
> (<https://digital-strategy.ec.europa.eu/en/policies/contents-code-gpai>,
> read 2026-10-26).

**After line 180**, add a section:

> ## Penalties
>
> Member States set penalties within the caps in Article 99. Prohibited
> practices: up to EUR 35 million or 7 % of worldwide turnover. Most
> operator duties, including deployers under Article 26, transparency
> under Article 50 and, since the Omnibus, Article 25(2) and (4): EUR 15
> million or 3 %. Misleading information to authorities: EUR 7.5 million
> or 1 %. SMEs and, since the Omnibus, small mid-caps pay the lower of the
> two. The Commission fines GPAI model providers up to EUR 15 million or
> 3 % (Article 101), from 2 August 2026 (Art. 113(b), checked
> 2026-10-26). GDPR fines under Article 83 run alongside.

**Line 191**, the table row. Replace with:

> | General-purpose AI models (Chapter V), governance, penalties (except Art. 101) | 2 August 2025 | Art. 113(b) (checked 2026-10-26) |
> | Commission fines on GPAI model providers (Art. 101) | 2 August 2026 | Art. 113(b) and general date (checked 2026-10-26) |
> | GPAI models placed on the market before 2 August 2025 | 2 August 2027 | Art. 111(3) (checked 2026-10-26) |

**After line 195**, add:

> | FRIA (Art. 27) and deployer duties (Art. 26) for Annex III systems | 2 December 2027 | Art. 113(c)(i) as replaced by Reg. 2026/1744 (checked 2026-10-26) |
> | Right to explanation (Art. 86) | 2 August 2026 (Chapter IX); in practice tied to Annex III classification from 2 December 2027, counsel to confirm | Art. 113 (checked 2026-10-26) |

Then change every remaining `checked 2026-10-25` in the table to `checked
2026-10-26`; I re-verified each row against P1 and P2.

### `references/privacy-and-records.md`

**Lines 14-17.** Replace from "A GDPR amendment" to "with the date." with:

> The GDPR and ePrivacy amendments in the Digital Omnibus (procedure
> 2025/0360(COD), proposal COM(2025) 837 of 19 November 2025) were not
> law on 26 October 2026. Parliament's committee stage was "Awaiting
> committee decision"
> (<https://oeil.secure.europarl.europa.eu/oeil/en/procedure-file?reference=2025/0360(COD)>,
> read 2026-10-26). The Council's mandate was reported agreed on 21
> October 2026 (secondary only); no trilogue had started. The proposal
> touches Articles 4(1), 9, 12, 13, 22, 33, 35 and new 88a to 88c, and
> ePrivacy Article 5(3). Treat all of them as unamended unless the
> Official Journal shows otherwise, and say so in the pack with the date.

**Lines 41-43.** Append: "The Omnibus proposes single EU-level lists,
and the EDPB's 2026-2027 work programme plans an EU DPIA template; neither
existed on 26 October 2026."

**Lines 88-91.** Replace the Article 22 bullet with:

> - Article 22: a decision based solely on automated processing with legal
>   or similarly significant effects is prohibited in principle unless
>   Article 22(2) applies (*SCHUFA*, C-634/21, 7 December 2023). An
>   automated score or ranking is itself the decision when the person
>   using it "draws strongly on" it. Record where a person decides
>   (contract ID), what share of outputs they review and how often they
>   depart from the output (M records). "A human is in the loop" without
>   those rates is not a fact. Where Article 22 applies, the notice must
>   say so and give meaningful information about the logic (Articles
>   13(2)(f), 14(2)(g)). On request, Article 15(1)(h) requires an
>   explanation of "the procedure and principles actually applied", not a
>   formula (*Dun & Bradstreet Austria*, C-203/22, 27 February 2025).
>   Write the explanation the design can produce (features used, a
>   counterfactual) and its owner. The Dutch DPA fined Uber EUR 824.99
>   million on 8 October 2026 for fully automated deactivations and an
>   inadequate notice. For Annex III high-risk systems, AI Act Article 86
>   adds a deployer duty to explain; see [the AI Act
>   reference](../../skills/adk-governance-pack/references/eu-ai-act.md).

**Lines 92-93.** Replace with:

> - AI Act Article 4a (Omnibus) permits special-category data for bias
>   detection only where strictly necessary and under all its conditions,
>   in addition to the GDPR; the records of processing must state why. See
>   [the AI Act reference](../../skills/adk-governance-pack/references/eu-ai-act.md).

**After line 137**, add two sections:

> ## International transfers (Chapter V)
>
> Australia has no adequacy decision. When agency staff outside the EEA
> view or handle the client's personal data (support, logs and traces,
> evaluation sets, incidents), that is a transfer. It needs Standard
> Contractual Clauses (Decision (EU) 2021/914: Module 2 client to agency,
> Module 3 agency to its sub-processors) and a transfer impact assessment
> under EDPB Recommendations 01/2020. Name the module, the exporter and
> the assessment reference in the recipients table; a missing assessment
> is a `gap:`. The same applies to any model endpoint, grounding service,
> abuse-monitoring store or telemetry sink outside the EEA. US recipients
> may rely on the EU-US Data Privacy Framework (adequacy decision of 10
> July 2023) if certified for the data type; check the certification and
> write the date. The General Court upheld the framework on 3 September
> 2025 (T-553/23). An appeal is pending (C-703/25 P), and the US Supreme
> Court's *Trump v. Slaughter* (29 June 2026) removed the FTC's
> independence that the decision relies on. Whether SCCs should back up
> DPF transfers is `counsel:`.
>
> ## Processor terms (Article 28)
>
> List each processor and sub-processor with its contract reference: the
> agency during build and support, the cloud provider under its Data
> Processing Addendum, and any tool or MCP provider that receives
> personal data. Article 28(3) terms (instructions, confidentiality,
> security, sub-processor approval, assistance, deletion or return,
> audits) are counsel's to check; the pack records what exists. A tool
> provider that uses the data for its own purposes may be a separate
> controller (EDPB Guidelines 07/2020).

**Lines 129-137.** Append:

> Whether data is anonymous is assessed per entity. EDPB Guidelines
> 02/2026 (in consultation from July 2026) test record isolation, linkage
> and inference. Pseudonymised data can be anonymous for a recipient who
> cannot re-identify it while remaining personal data for the controller
> (*EDPS v SRB*, C-413/23 P, 4 September 2025). Write "pseudonymised" for
> evaluation sets unless the test has been run, and erase from memory,
> vector stores and backups rather than "anonymising" on request (EDPB
> right-to-erasure report, 18 February 2026).

**Lines 141-149.** Append to the records paragraph: "A row that uses
special-category data for bias detection under AI Act Article 4a states
why it was strictly necessary (Article 4a(1)(f))."

### Templates

**`assets/classification-memo-template.md`**

- Line 39, after the Article 25 triggers bullet, add: `- **Article 25(4)
  agreement (if high-risk):** <what the agency supplies; whether the
  written agreement exists> (<contract reference or gap:>; counsel:
  <confirm>).`
- Line 58: change "FRIA under Article 27 if the deployer is in scope" to
  "FRIA under Article 27 if the deployer is in scope (not Annex III point
  2), notified to the market surveillance authority (27(3))".
- Line 64, 50(1) row, column 3: "<disclosure; for agents, also on whose
  behalf it acts>".
- Line 65, 50(2) row, column 3: "<marking decision, or exception relied
  on: standard editing, no substantial alteration, B2B (guidelines para
  87)>".
- After line 73, add: `- **Downstream modification compute:** <none / compute used versus one third of the original> (<D ID>; counsel: <if any>).`
- Before "Questions for counsel", add a short "Other EU regimes" list:
  GDPR Art 22 (DPIA input pack), Product Liability Directive, CRA, NIS2,
  DORA, MDR, Data Act, DSA. Each line is `n/a:` with a reason or
  `counsel:`. Keep it optional, so `REQUIRED` in
  `scripts/check_governance.py` line 49 does not change.

**`assets/dpia-input-pack-template.md`**

- Line 61: replace with `- counsel: <does any output produce, or is it
  usually followed for, a decision with legal or similarly significant
  effect (Article 22; SCHUFA)?> Facts: <where a person decides; review
  share and override rate> (<C ID, M ID>); explanation available under
  Article 15(1)(h): <what and who> (<C ID>).`
- Line 67: replace with `- <how data subjects are informed (Articles 13
  and 14, including automated decisions and model-provider recipients)
  and exercise rights: access, rectification, erasure (memory, vector
  stores, backups), objection> (<C IDs>).`
- Line 77: rename the column to "Transfer outside the EEA: mechanism
  (adequacy, DPF with check date, SCC module) and transfer impact
  assessment".
- Line 80, agency row: `| <agency> | <processor during build and
  support> | <where staff access from> | <none / SCC Module 2 and TIA
  ref; counsel:> | <contract reference or gap:> |`.

**`assets/processing-records-template.md`, line 20.** Add to the "Legal
basis" cell: "<; AI Act Art 4a reasons if special categories are used for
bias detection>".

**`assets/impact-assessment-template.md`.** After "Residual risk and
decision", add an optional section `## FRIA crosswalk (AI Act Article 27,
if required)` with the six-row table from 2.6. Its rows cite the
classification memo for the requirement, `counsel:`, and pack sections.
Keep it optional, so the checker's `REQUIRED` stays as it is.

**`assets/security-questionnaire-template.md`, line 38.** Replace the
incident response answer placeholder with "<alerts, owner; notification
clocks that apply: agency to client without undue delay (GDPR Art
33(2)), client to authority within 72 hours (Art 33(1)); NIS2 24 and 72
hours if the client is in scope; CRA 24 and 72 hours if a product; AI
Act Art 73 if high-risk>".

### `SKILL.md`

- Line 23: `sources-reviewed: "2026-10-26"` once the reference edits land.
- Lines 97-102, step 2: add "and the transfers and processor sections"
  after "read [privacy and records](../../skills/adk-governance-pack/references/privacy-and-records.md)".
- Line 124: change "whether a DPIA or FRIA is required" to "whether a
  DPIA or FRIA is required, whether Article 22 applies, the transfer
  mechanism".

### `scripts/check_governance.py` (optional)

- Lines 73-95: add an area `"Annex I product (medical devices)":
  (r"medical device", r"in vitro diagnostic", r"\bMDR\b")`. Check the
  `ANNEX_PATTERNS` case rule at line 96, which only spares patterns
  starting `\bCV`. `\bMDR\b` would then match case-insensitively; give it
  the same case-sensitive treatment.
- Add a test in `tests/test_check_governance.py` for a draft mentioning
  "medical device software" with `counsel_required: no`, expecting the
  error.
