# Portability principles for ADK agents on Google Cloud

<!-- verified: 2026-10-26; re-check every 90 days -->

Read before classifying components, proposing a boundary or sizing effort.
The four classes and the effort scale are a synthesis of the sources below.

**The short version.** Portability is a cost, not a yes or no. For an ADK
agent the expensive part of a move is seldom code: it is data (sessions,
memories, corpora), behaviour to re-evaluate (model, retrieval, grounding)
and policy (IAM, compliance). Report each component's cost; recommend few
new seams.

## Terms and their practical tests

| Term | Meaning | Practical test |
| --- | --- | --- |
| Portability | Data and applications can be moved and run elsewhere "at an acceptable cost" (NIST SP 500-291r2 §6.4) | Can you name each component's move steps and cost drivers, and has someone accepted that cost? |
| Interoperability | Data is processed by services on different clouds "through common specifications" (same) | Does it exchange data or calls through a published spec (OpenAPI, MCP, A2A, OTLP, the Postgres wire protocol) with no custom glue? |
| Cloud-agnostic | No component depends on one provider. AWS: doing this with containers "often limits them to basic compute and storage" (Tenet 2, read in German) | Would the whole system deploy to a second provider with only a configuration change? For a Gemini and Agent Platform build, no. |
| Modularity | Parts with defined interfaces that change independently; says nothing about providers | Can one module be rewritten without editing its callers? |
| Abstraction | An interface hiding an implementation; worth it when *deep* (Ousterhout): a simple interface over substantial hidden complexity | Do callers stay unchanged when the implementation changes, and does the interface hide more than it exposes? |
| Loose coupling | How far a change in one part forces changes elsewhere | How many files or teams does a change to this dependency touch? |
| Multicloud | At least two public providers used concurrently (Google; Azure CAF) | Are two providers serving production traffic or holding production data *now*? |
| Hybrid | A public cloud plus a private environment (Google) | Does any production component run on premises? |
| Migration | A one-time move with a decommission date; AWS's 7 Rs: retire, retain, rehost, relocate, repurchase, replatform, refactor | Is there a date after which the source is switched off? |

ISO/IEC 19941:2017 separates syntactic, semantic-data, behavioural and
policy facets of portability (abstract and an EU summary only; full text
`unverified`). Two matter for agents: the same API syntax can hide different
behaviour (a model, a memory extractor), and policy (IAM, retention) differs.
Interoperability does not imply portability: an agent can call Google tools
over MCP and still be stuck.

**Keep this distinction in every assessment.** *Movable later at a known
cost* is an exit plan: classified components, sized drivers, an untested
path. *Running on several providers now* is multicloud: two live, tested and
operated implementations. Deliver the first by default; recommend the second
only on a stated need with a date or trigger.

## What abstraction costs

- **Lowest common denominator.** Hohpe: avoiding lock-in "often disallows you
  from using vendor-specific features". AWS: "The additional technical effort
  may not justify the portability benefits." A common interface over Memory
  Bank, RAG Engine and Search grounding offers only what they share, which
  excludes the reason each was chosen. Hohpe treats switching cost as an
  option's strike price; driving it to zero is "often not the most
  economical" choice.
- **Two implementations, two burdens:** contract tests, evaluation runs,
  dashboards and on-call knowledge each. One that does not run in CI stops
  working unnoticed (practice, consistent with Fowler's contract tests).
- **Leaky abstractions.** "All non-trivial abstractions, to some degree, are
  leaky" (Spolsky): read-after-write consistency on a session store,
  transactions (state and event append committing together), IAM semantics,
  error and quota shapes. A port that hides them defers finding them to the
  migration.
- **Data gravity and egress.** AWS: treat data gravity "as a primary factor in
  workload placement decisions"; Google and Azure list transfer charges
  between clouds. Egress argues more against multicloud than a one-time move.
  Google waived transfer fees for full exits from January 2024, with
  conditions (press report; terms `unverified`). The EU Data Act bans
  switching charges from 12 January 2027 (Bundesnetzagentur), reportedly not
  ongoing parallel-use egress (`unverified`). Neither is legal advice.
- **Providers agree.** Google: multicloud "is rarely a goal in itself"; Azure
  CAF: "Justify multicloud complexity"; AWS FSI: "Avoiding lock-in doesn't
  require a multicloud approach."

## The four classes

Ask these questions of every component, in this order, and stop at the first
class that fits.

1. **Shared logic.** Domain rules, validation, prompts as data, tool bodies.
   No provider SDK imports, which an import test can enforce. Exit cost:
   none beyond re-running tests.
2. **Replaceable adapter.** A thin boundary exists or is cheap; a second
   implementation needs no data conversion and no behaviour change. Name the
   port. Exit cost: one module plus a contract-test run.
3. **Provider-specific by choice.** Accepted for its value; no port. The exit
   rewrites a bounded part (configuration, infrastructure, a few calls) with
   no data to convert and nothing to re-evaluate. Record the reason, the exit
   path and the trigger that would reopen the decision.
4. **Expensive dependency.** The exit needs any of: moving or regenerating
   data, changed semantics, re-embedding, re-evaluation, or repeated
   contractual or compliance approval. Name the drivers; never promise
   portability.

**Cheap seam, expensive switch.** A framework seam (`BaseSessionService`,
`BaseMemoryService`, the model connectors) makes the *code* cheap to change.
It does not downgrade an expensive dependency whose data or behaviour must be
regenerated or re-evaluated: the model, Memory Bank, a RAG corpus. Write both
facts in the row: the seam in "Exit path", the class from the switch.

| ADK component | Usual class | Why; port or exit path |
| --- | --- | --- |
| Tool function bodies | shared logic | Pass SDK clients in rather than creating them in the body; `FunctionTool` is ADK's seam. Gemini-tuned docstrings still need re-evaluation on another model. |
| Postgres records (Cloud SQL, AlloyDB) | replaceable adapter | Standard SQL behind a repository module; the Cloud SQL connector and IAM database auth are configuration. Data moves by dump and restore, sized by volume. AlloyDB-only extensions push it to class 3. |
| ADK sessions | replaceable adapter; data cost varies by service | `BaseSessionService` is abstract (`create_session`, `get_session`, `list_sessions`, `delete_session`, checked on 1.26.0). `DatabaseSessionService` runs on Postgres, MySQL or SQLite. `VertexAiSessionService` history lives in Agent Platform; its export path is `unverified`. |
| Memory Bank | expensive dependency | `BaseMemoryService` seam exists, but Google generates the memories. Another store extracts different ones: regenerate, re-evaluate or discard them, and carry consent and erasure records across. |
| RAG corpus (RAG Engine, Agent Search) | expensive dependency | Source documents move; the index and embeddings do not. Re-chunk, re-embed, re-run retrieval evaluation. |
| BigQuery SQL | provider-specific by choice; expensive dependency with volume, BigQuery ML or Agent Analytics | GoogleSQL dialect, dataset IAM, bytes-billed cost guards. Drivers: template count, data volume, egress. |
| Gemini grounding (`google_search`) | expensive dependency | "Only compatible with Gemini 2 models", used by itself on its agent, and Search suggestions must be displayed (adk.dev). A replacement search tool returns different results under different terms. |
| The model | expensive dependency; cheap seam, expensive switch | Connectors (native Claude and OpenAI, LiteLLM, Ollama, vLLM) exist. Google's own migration guide asks for code, model-performance and load regression tests even between Gemini versions. |
| IAM and workload identity | provider-specific by choice | Do not wrap it. The exit re-maps principals and roles and repeats the security review: the policy facet. |
| OTel telemetry | replaceable adapter; by standard | OTel SDK with an OTLP exporter set in configuration. Cloud Trace dashboards, alerts and BigQuery Agent Analytics are class 3 and get rebuilt. |
| Evaluation sets | shared logic; the cases move, baselines are re-run | Cases kept as data move. Scores belong to a model and judge pair, so a move means re-baselining; a judge on Gemini is a dependency of its own. |
| MCP and A2A boundaries | replaceable adapter; by protocol | Interoperability through open specifications; server-side auth stays provider-specific. |
| Hosting | provider-specific by choice; Cloud Run or GKE (Agent Runtime is an expensive dependency) | A container image rehosts. Agent Runtime's managed sessions, memory and runtime features do not. |

## When an abstraction pays

Propose or keep a seam only when at least one holds:

- **(a) A second implementation is needed now.** A fake that runs in CI under
  a contract test counts.
- **(b) The switch is a stated requirement with a date or trigger**, such as
  "EU data off provider X by Q3" or a cost-per-case ceiling.
- **(c) The framework already has the seam** (`BaseSessionService`,
  `BaseMemoryService`, model connectors, MCP, OTLP). Use it and do not wrap it
  again: a home-made `SessionRepository` over it is a shallow module.
- **(d) It cheaply isolates a volatile vendor API** from business logic, for
  example one module over a preview API. In Ousterhout's terms, it hides
  change.

Otherwise record an exit path instead (Hohpe's insurance). Skip a seam that
serves a speculative second provider; wraps a managed feature the design
relies on (Memory Bank extraction, grounding, RAG Engine ranking); forces a
lowest common denominator or has one implementation, no fake and an
interface as wide as what it wraps; or hides semantics that differ
(consistency, transactions, IAM), which belong documented at the boundary.

## Effort and risk without invented numbers

Size each item with the vocabulary **small | medium | large | very large |
unknown**, tied to named drivers. Write days, hours or money only when a plan
measurement record (`M<n>`) supports the figure, or label it `assumption`.
"unknown; needs a spike" is allowed and better than a guess.

| Driver | Pushes the size up when |
| --- | --- |
| Data volume and shape | Large volumes, data shared by many users, embeddings or derived data |
| Integration points | Many callers, tools, dashboards or downstream consumers |
| Semantic differences | Consistency, transactions, quotas or error shapes differ |
| Behaviour re-evaluation | Model, embedding, retrieval, memory or grounding changes; the evaluation suite runs again |
| Identity and policy | Principals, roles and secrets need re-mapping |
| Operations rebuild | Alerts, SLOs, runbooks, on-call skills |

**small**: one adapter and its contract tests. **medium**: adds a data move
or one round of re-evaluation. **large**: several drivers, or data plus
re-evaluation. **very large**: a project with its own plan.

Size by the **largest** driver, not the sum. Any item that needs
re-evaluation (model, framework, retrieval) is at least medium. Contractual
or compliance re-approval (data-processing agreements, residency, AI
governance sign-off, client approval) is a separate schedule risk outside
the team's control, never folded into effort.

Rate risk on Hohpe's two axes, switching cost and likelihood: cheap and
unlikely needs nothing; costly and likely needs a plan now; costly but
unlikely needs insurance (an exit path and a trigger).

## Phasing patterns

- **Strangler fig.** Replace parts behind a façade while the old system
  serves; big-bang rewrites tend to "go down in flames" (Fowler). Keep the
  façade from becoming a single point of failure, translate through an
  anti-corruption layer, and skip the pattern for small systems (AWS, Azure).
  In ADK the façade is often an existing seam: model routing, the session
  service, an MCP endpoint.
- **Parallel run or shadow.** Serve the incumbent's result and compare the
  candidate's out of band; GitHub's Scientist "will always return whatever
  the `use` block returns". For agents, shadow a sample offline through the
  evaluation harness, and never let shadow traffic execute write tools.
- **Data: backfill plus change capture, not dual-write.** Load by ETL, sync by
  CDC and validate before the new store becomes the system of record (Azure);
  AWS calls synchronised copies "tactical". Dual-write across two stores has
  no shared transaction and can diverge silently (practice).
- **Interfaces: expand, migrate, contract** (Parallel Change); finish contract.
- **Cutover and rollback.** Pause writes, finish the sync, validate with
  checksums, not only row counts, then switch. "Retain the source environment
  as a fallback option" (Azure CAF); removing it is "a deliberate final step".
- **Pick the R.** Container move = rehost; managed store swap = replatform;
  model or framework change = refactor with a full evaluation cycle.

## Testing a move

- **Contract tests at each port.** One suite runs against every
  implementation, the fake included, checking format and behaviour rather
  than exact data (Fowler). For sessions: create, append, get, list, delete,
  state deltas, ownership. A suite run only against the fake proves nothing
  about the move.
- **Re-run the evaluation sets.** The frozen set (same cases, same judge) on
  the candidate model or framework, per category, plus code, performance and
  load regression tests: "It's hard to predict these changes without first
  testing your prompts with the new version" (Google). Re-run retrieval
  evaluation after re-indexing and memory evaluation after regeneration.
- **Verify the data migration.** Counts and checksums, sample reads through
  the *new* adapter, replayed sessions with state compared, and erasure and
  retention tests on the target: the policy facet does not migrate itself.

## Sources

All read 2026-10-26 unless noted.

| Topic | URL |
| --- | --- |
| NIST SP 500-291r2, §6.4 and glossary | https://doi.org/10.6028/NIST.SP.500-291r2 |
| ISO/IEC 19941:2017 abstract; EU CAMSS summary | https://webstore.iec.ch/publication/62163 ; https://interoperable-europe.ec.europa.eu/sites/default/files/distribution/access_url/2024-06/7744aa5b-d9d5-43a9-a69e-ca7499260c8b/CAMSS_Assessment_Summary_ISO19941_EIF%20Scenario_v1.0.pdf |
| Google hybrid and multicloud patterns | https://docs.cloud.google.com/architecture/hybrid-multicloud-patterns |
| AWS 7 Rs; multicloud Tenet 2 (German edition) | https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html ; https://docs.aws.amazon.com/de_de/prescriptive-guidance/latest/strategy-multicloud/tenet-2.html |
| AWS FSI misconceptions and lock-in; AWS strangler fig | https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-multicloud-fsi/misconceptions.html ; https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-multicloud-fsi/vendor-lockin.html ; https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html |
| Azure CAF hybrid strategy (page due for removal 2026-10-30) | https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/scenarios/hybrid/strategy |
| Azure CAF execute migration; Azure strangler fig | https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/execute-migration ; https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig |
| Hohpe, "Don't get locked up into avoiding lock-in" | https://martinfowler.com/articles/oss-lockin.html |
| Fowler: StranglerFigApplication, ContractTest; Sato: ParallelChange | https://martinfowler.com/bliki/StranglerFigApplication.html ; https://martinfowler.com/bliki/ContractTest.html ; https://martinfowler.com/bliki/ParallelChange.html |
| Spolsky, leaky abstractions; GitHub Scientist | https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/ ; https://github.com/github/scientist |
| ADK sessions, models, Google Search tool | https://adk.dev/sessions/session/ ; https://adk.dev/agents/models/ ; https://adk.dev/integrations/google-search/ |
| Google model migration guide | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate |
| Exit fees (TechCrunch, secondary); EU Data Act switching charges | https://techcrunch.com/2024/01/11/google-says-itll-stop-charging-fees-to-transfer-data-out-of-google-cloud/ ; https://www.bundesnetzagentur.de/SharedDocs/A_Z_Glossar_DataAct_ENG/S/switching-charge.html |

Ousterhout, *A Philosophy of Software Design*, 2nd ed. (2021), on deep and
shallow modules: book, not re-read. ADK classes were checked on a cached
`google-adk` 1.26.0 wheel; confirm them on the project's pinned version.
