# Portability design principles for ADK agents on Google Cloud — 26 October 2026

## Scope and snapshot

Research behind the principles reference for `adk-portability-planning`.
Pages read 26 October 2026 (see Sources); ISO/IEC 19941 only through its
abstract and an EU summary; ADK classes checked on a cached `google-adk`
1.26.0 wheel, older than the 2.8.0 baseline. Nothing was run.

**Conclusion.** The sources agree. Portability is a cost ("at an acceptable
cost", NIST), not a yes or no, and every provider says to justify multicloud
rather than assume it. Abstraction pays only where it hides real complexity
or a second implementation exists. For an ADK agent the expensive part of a
move is seldom code: it is data (sessions, memories, corpora), behaviour to
re-evaluate (model, retrieval, grounding) and policy (IAM, compliance). Report
each component's cost; recommend few new seams.

## 1. Terms that get conflated, each with a practical test

| Term | Meaning (source) | Practical test |
| --- | --- | --- |
| Portability | "data can be moved from one cloud system to another and ... applications can be ported and run on different cloud systems at an acceptable cost" (NIST SP 500-291r2 §6.4) | Can you name each component's move steps and cost drivers, and has someone accepted that cost? |
| Interoperability | "data can be processed by different services on different cloud systems through common specifications" (same) | Does it exchange data or calls through a published spec (OpenAPI, MCP, A2A, OTLP, Postgres wire protocol) with no custom glue? |
| Cloud-agnostic architecture | No component depends on one provider's services. AWS: building this with containers "often limits them to basic compute and storage" (Tenet 2, translated) | Would the whole system deploy to a second provider with only a configuration change? For a Gemini and Agent Platform build the honest answer is no. |
| Modularity | Parts with defined interfaces that change independently. It says nothing about providers. | Can one module be rewritten without editing its callers? |
| Abstraction | An interface that hides an implementation. Ousterhout: worth it when *deep*, meaning a simple interface over substantial hidden complexity. | Do callers stay unchanged when the implementation changes, and does the interface hide more than it exposes? |
| Loose coupling | How far a change in one part forces changes elsewhere | How many files or teams does a change to this dependency touch? |
| Multicloud deployment | "combines at least two public CSPs" (Google); "using multiple cloud providers concurrently" (Azure CAF) | Are two providers serving production traffic or holding production data *now*? |
| Hybrid | A public cloud plus at least one private environment (Google) | Does any production component run on premises or in a colocation facility? |
| Migration | A one-time move with a decommission date. AWS's 7 Rs: retire, retain, rehost, relocate, repurchase, replatform, refactor. | Is there a date after which the source is switched off? |

ISO/IEC 19941:2017 "specifies cloud computing interoperability and
portability types" and their relationship (IEC abstract). Its contents list
syntactic, semantic-data, behavioural and policy facets (via a search result
and the EU CAMSS summary; full text `unverified`). Two apply to agents: the
same syntax can hide different behaviour (a model, a memory extractor), and
policy (IAM, retention) can differ. Interoperability does not imply
portability: an agent can call Google tools over MCP and still be stuck.

**The distinction to keep.** *Movable later at a known cost* is an exit plan
(classified components, sized drivers, an untested path). *Running on several
providers now* is multicloud (two live implementations, tested and operated).
Deliver the first by default; recommend the second only on a stated need.

## 2. What abstraction costs

- **Under-use and lowest common denominator.** Hohpe: avoiding lock-in "often
  disallows you from using vendor-specific features", and complexity is "too
  often ignored". AWS: "The additional technical effort may not justify the
  portability benefits" (Tenet 2, translated). A common interface over Memory
  Bank, RAG Engine and Search grounding offers only what they share, which
  excludes the reason for choosing each. Hohpe treats switching cost as an
  option's strike price: driving it to zero is "often not the most
  economical" choice.
- **Two implementations mean two burdens.** Each needs contract tests,
  evaluation runs, dashboards and on-call knowledge. A second implementation
  that does not run in CI stops working without anyone noticing (opinion,
  consistent with Fowler's contract-test rationale).
- **Leaky abstractions.** "All non-trivial abstractions, to some degree, are
  leaky" (Spolsky): consistency (read-after-write on a session store),
  transactions (state and event append committing together), IAM semantics
  (principals, role grain, keyless identity), error and quota shapes. A port
  that hides these defers finding them to the migration.
- **Data gravity and egress.** AWS: "Treat data gravity as a primary factor
  in workload placement decisions". Google asks: "Might data movement incur
  significant data transfer charges?" Azure lists "data egress charges
  between clouds". NIST: a petabyte in one database can be easier to move
  than a terabyte shared by thousands of users. Google waived transfer fees
  for full exits from January 2024, with conditions (TechCrunch, secondary;
  terms `unverified`); EU Data Act Art. 29 bans switching charges from
  12 January 2027 (Bundesnetzagentur), reportedly not ongoing parallel-use
  egress (`unverified`). Egress argues more against multicloud than a move.
- **Providers agree.** Google: multicloud "is rarely a goal in itself".
  Azure CAF: "Justify multicloud complexity". AWS FSI: "Avoiding lock-in
  doesn't require a multicloud approach", and full portability between two
  CSPs makes "true portability nearly impossible". Each argues for itself as
  primary, but on this point they all say the same thing.

## 3. Component classification

Ask these questions of every component, in this order.

1. **Shared business logic.** Domain rules, validation, prompts as data,
   tool bodies. No provider SDK imports, enforced by an import test.
2. **Replaceable adapter.** A thin boundary exists or is cheap; a second
   implementation needs no data conversion and no behaviour change. Name the
   port. Exit cost: one module plus a contract-test run.
3. **Intentionally provider-specific.** Accepted for its value; no port. The
   exit rewrites a bounded part (configuration, infrastructure, a few calls)
   with no data to convert and nothing to re-evaluate. Record the reason, the
   exit path and the trigger that would reopen the decision.
4. **Expensive dependency.** The exit needs any of: moving or regenerating
   data, changed semantics, re-embedding or retraining, re-evaluation, or
   repeated contractual or compliance approval. A framework seam does not
   change the class: it makes the code cheap, not the switch. Name the
   drivers and do not promise portability.

| ADK component | Usual class | Why; port or exit path |
| --- | --- | --- |
| Tool function bodies | Shared logic | Pass SDK clients in rather than creating them in the body. `FunctionTool` is ADK's seam. Gemini-tuned docstrings still need re-evaluation on another model. |
| Postgres records (Cloud SQL or AlloyDB) | Adapter | Standard SQL behind a repository module. The Cloud SQL connector and IAM database authentication are provider configuration. Data moves by dump and restore, sized by volume. AlloyDB-only extensions push it to class 3. |
| ADK sessions | Adapter in code; data cost varies | `BaseSessionService` is abstract (`create_session`, `get_session`, `list_sessions`, `delete_session` in 1.26.0). `DatabaseSessionService` runs on Postgres, MySQL or SQLite (adk.dev). `VertexAiSessionService` keeps history in Agent Platform, and its export path is `unverified`. |
| Memory Bank | Expensive | A `BaseMemoryService` seam exists (`VertexAiMemoryBankService`, 1.26.0), but Google generates the memories. Another store extracts different ones, so re-evaluate, regenerate or discard them, and carry the consent and erasure records across. |
| RAG corpus (RAG Engine or Vertex AI Search) | Expensive | Source documents can move; the index and embeddings cannot. Re-chunk, re-embed and re-run retrieval evaluation. |
| BigQuery SQL | Class 3 with a few reviewed templates; expensive with volume, BigQuery ML or Agent Analytics | GoogleSQL dialect, dataset IAM, cost model. Drivers: number of templates, data volume, egress. |
| Gemini grounding (`google_search`) | Expensive | "only compatible with Gemini 2 models", used "by itself", and Search suggestions must be displayed (adk.dev). A replacement search tool gives different results and carries different obligations. |
| The model | Cheap seam, expensive switch | Connectors (LiteLLM, Anthropic, Ollama, vLLM) and routing exist (adk.dev). Google's guide requires code, model-performance and load regression tests even between Gemini versions. |
| IAM and workload identity | Class 3 | Do not wrap it. The exit is re-mapping principals and roles plus a security review: the policy facet. |
| OTel telemetry | Adapter by standard | OTel SDK with an OTLP exporter set in configuration. Cloud Trace dashboards, alerts and BigQuery Agent Analytics are class 3 and get rebuilt. |
| Evaluation sets | Shared asset; baselines expensive | Cases kept as data are portable. Scores belong to a model and judge pair, so a move means re-baselining. A judge on Gemini is a dependency in its own right. |
| MCP and A2A boundaries | Adapter by protocol | Interoperability through open specifications. Server-side auth remains provider-specific. |
| Hosting | Cloud Run or GKE class 3; Agent Runtime expensive | A container image can be rehosted. Agent Runtime's managed sessions, memory and runtime features cannot. |

## 4. When an abstraction earns its place

Add or keep a seam when at least one of these holds:

- **(a) A second implementation is needed now.** Tests count when the fake
  runs in CI and a contract test keeps it honest.
- **(b) The switch is a stated requirement with a date or trigger**, such as
  "EU data off provider X by Q3" or a cost-per-case ceiling.
- **(c) The framework already has the seam** (`BaseSessionService`,
  `BaseMemoryService`, model connectors, MCP, OTLP). Use it; do not wrap it
  again, because a home-made `SessionRepository` over it is a shallow module.
- **(d) It cheaply isolates a volatile vendor API from business logic**, such
  as one module over a preview API. In Ousterhout's terms, it hides change.

Do not add one when:

- the second provider is speculative: record an exit path instead (Hohpe's
  insurance, limiting the scope of change);
- it wraps a managed feature the design relies on (Memory Bank extraction,
  grounding, RAG Engine ranking);
- it forces a lowest common denominator, or has one implementation, no fake
  and an interface as wide as what it wraps (a shallow module);
- it hides semantics that differ (consistency, transactions, IAM): document
  the difference at the boundary instead.

## 5. Effort and risk without invented numbers

Use T-shirt sizes tied to named drivers, never days or money unless a
measured estimate exists. Otherwise write "unknown; needs a spike".

| Driver | Pushes size up when |
| --- | --- |
| Data volume and shape | Large volumes, data shared by many users (NIST's CRM example), embeddings or derived data |
| Integration points | Many callers, tools, dashboards or downstream consumers |
| Semantic differences | Consistency, transactions, quotas or error shapes differ |
| Behaviour re-evaluation | Model, embedding, retrieval, memory or grounding change. Behaviour is not guaranteed to be equivalent, so the evaluation suite must run again. |
| Identity and policy | Principals, roles and secrets need re-mapping |
| Re-approval | Data-processing agreements, residency, AI-governance sign-off or client approval must be repeated |
| Operations rebuild | Alerts, SLOs, runbooks, on-call skills |

**S**: one adapter and its contract tests. **M**: adds a data move or one
round of re-evaluation. **L**: several drivers, or data plus re-evaluation.
**XL**: a project with its own plan. Size by the largest driver, not the sum;
any re-evaluation driver means at least M; show re-approval as a separate
schedule risk outside the team's control. Rate risk on Hohpe's two axes
(switching cost, likelihood): cheap and unlikely needs nothing, costly and
likely needs a plan now, costly but unlikely needs insurance.

## 6. Migration phasing (high level)

- **Strangler fig.** Replace parts behind a façade while the old system
  serves; big-bang rewrites tend to "go down in flames" (Fowler). Azure and
  AWS add: keep the façade from becoming a single point of failure, translate
  through an anti-corruption layer, and skip the pattern for small systems.
  In ADK the façade is often an existing seam (model routing, session
  service, MCP endpoint).
- **Parallel run or shadow.** Return the incumbent's result and compare the
  candidate's out of band. GitHub's Scientist "will always return whatever
  the `use` block returns". For agents, shadow a sample offline through the
  evaluation harness, and never let shadow traffic execute write tools.
- **Data: backfill and change capture, not dual-write.** Azure loads by ETL,
  syncs by CDC and validates before the new store becomes system of record;
  AWS calls synchronised copies "tactical". Dual-write across two stores has
  no shared transaction and can silently diverge (practice, not a citation).
- **Interfaces: expand, migrate, contract** (Parallel Change); finish contract.
- **Cutover and rollback.** Pause writes, finish the sync, validate with
  checksums, not just row counts, then switch. "Retain the source environment
  as a fallback option" (Azure CAF); rollback is cheap until legacy objects
  go, so removal is "a deliberate final step" (Azure strangler-fig page).
- **Pick the R.** AWS calls refactor the most complex and advises moving
  first, modernising later. For an agent: container move = rehost, managed
  store swap = replatform, model or framework change = refactor with a full
  evaluation cycle.

## 7. Testing view

- **Contract tests at each port.** One suite against every implementation,
  the fake included, checking format and behaviour, not exact data (Fowler).
  For sessions: create, append, get, list, delete, state deltas, ownership.
  A suite run only against the fake proves nothing about the move.
- **Evaluation against the alternative.** The frozen set (same cases, same
  judge) on the candidate model or framework, per category, with Google's
  code, model-performance and load regression tests: "It's hard to predict
  these changes without first testing your prompts with the new version."
  Re-run retrieval evaluation after re-indexing, memory after regeneration.
- **Data-migration verification.** Counts and checksums, sample reads through
  the *new* adapter, replayed sessions with state compared, and erasure and
  retention tests on the target: the policy facet does not migrate itself.

## Sources (all read 2026-10-26)

- NIST SP 500-291r2 *Cloud Computing Standards Roadmap*, §6.4 and glossary (PDF text extracted): https://doi.org/10.6028/NIST.SP.500-291r2
- ISO/IEC 19941:2017, abstract only: https://webstore.iec.ch/publication/62163 ; EU CAMSS assessment summary (2024): https://interoperable-europe.ec.europa.eu/sites/default/files/distribution/access_url/2024-06/7744aa5b-d9d5-43a9-a69e-ca7499260c8b/CAMSS_Assessment_Summary_ISO19941_EIF%20Scenario_v1.0.pdf
- Google Cloud, hybrid and multicloud (overview, `/drivers`, `/strategy`, `/other-considerations`): https://docs.cloud.google.com/architecture/hybrid-multicloud-patterns
- AWS Prescriptive Guidance: 7 Rs https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html ; multicloud Tenet 2 (German edition) https://docs.aws.amazon.com/de_de/prescriptive-guidance/latest/strategy-multicloud/tenet-2.html
- AWS FSI anti-patterns and lock-in https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-multicloud-fsi/misconceptions.html and `/vendor-lockin.html` ; strangler fig https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html
- Azure: CAF hybrid strategy (deprecated, removal due 2026-10-30) https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/hybrid/strategy ; CAF execute migration https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/execute-migration ; Strangler Fig https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig
- Hohpe, "Don't get locked up into avoiding lock-in" (2019) https://martinfowler.com/articles/oss-lockin.html ; Fowler, StranglerFigApplication and ContractTest; Sato, ParallelChange: https://martinfowler.com/bliki/StranglerFigApplication.html , https://martinfowler.com/bliki/ContractTest.html , https://martinfowler.com/bliki/ParallelChange.html
- Spolsky, The Law of Leaky Abstractions (2002) https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/ ; GitHub Scientist https://github.com/github/scientist
- ADK https://adk.dev/sessions/session/ , https://adk.dev/agents/models/ , https://adk.dev/integrations/google-search/ ; Google model migration guide https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate
- Exit charges: TechCrunch 2024-01-11 (secondary) https://techcrunch.com/2024/01/11/google-says-itll-stop-charging-fees-to-transfer-data-out-of-google-cloud/ ; Bundesnetzagentur Data Act glossary https://www.bundesnetzagentur.de/SharedDocs/A_Z_Glossar_DataAct_ENG/S/switching-charge.html
- Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), on deep and shallow modules (book; not re-read)

## Limits of this note

- ISO/IEC 19941 was not read in full; its facet names come from a contents
  listing and a secondary EU summary.
- No AWS Well-Architected page on multicloud could be fetched, so AWS's view
  comes from Prescriptive Guidance; Tenet 2 was read in German (English 404).
- The Azure CAF hybrid strategy page is due for removal on 30 October 2026;
  cite its GitHub archive afterwards.
- ADK classes were checked on a cached 1.26.0 wheel; confirm them on the
  pinned version, and whether Agent Platform sessions and Memory Bank export.
- Exit-fee terms change; the Google waiver and the Data Act parallel-use
  reading come from press and commentary, not legal advice.
- The four classes and the T-shirt scale are this note's synthesis.
