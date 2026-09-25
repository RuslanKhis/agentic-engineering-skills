# System designer source coverage

Reviewed on **25 September 2026** against the supplied document beginning
**“Designing an agent system starts with defining what the application must guarantee.”**

The source contains 1,058 lines, including repeated summaries, examples and
historical implementation notes. Its SHA-256 is
`19a4e5a492e87bd25408cd7daecb2213dc49c91f85d15efb2497b44a8b8713d2`.
Line ranges below refer to that supplied version. The source itself and its
private local paths are not distributed with the skill.

## Review method and conclusion

The complete source was reviewed in three ranges: 1–389, 390–649 and 650–1058.
Two independent reviewers compared the outer ranges with the designer and
relevant implementation specialists; the maintainer reviewed the middle range
and reconciled the findings. This is a qualitative coverage review, not a claim
that every sentence should become an instruction or that the proposed systems
have been implemented.

The essential architecture principles were already present. The review found
useful decisions that were too implicit, especially where state, delivery,
authority and recovery cross component boundaries. Those contracts are now
explicit in the designer. SDK recipes, commands and historical test details
remain with their implementation specialists.

## Coverage map

| Source lines / theme | Design-level lesson retained | Where it lives / review outcome |
| --- | --- | --- |
| 1–26: guarantees and minimal orchestration | Define observable success first; use ordinary code and the smallest justified agent arrangement; give handoffs and termination clear owners. | [Main workflow](../../skills/adk-system-designer/SKILL.md), [outcome and orchestration](../../skills/adk-system-designer/references/design-decisions.md#outcome-and-orchestration). Retained. |
| 27–35, 570–649: data responsibilities | Distinguish sessions, exact profiles, semantic memory, approved evidence, structured history and transactional truth; specify scope, freshness, lifetime and erasure. | [State, knowledge and freshness](../../skills/adk-system-designer/references/design-decisions.md#state-knowledge-and-freshness). Strengthened publication, completeness and unavailable-result distinctions. |
| 37–47, 693–699: progress and effects | Partial text, persisted events, approval and completed business actions establish different facts; receipt-derived status must preserve partial success. | [Identity, tools and data release](../../skills/adk-system-designer/references/design-decisions.md#identity-tools-and-data-release), [failure review](../../skills/adk-system-designer/references/failure-review.md). Strengthened authoritative reporting and multi-effect failures. |
| 49–62, 828–877: authority | Separate end-user, workload and delegated identities; validate tool inputs/results and enforce scope at execution, including alternate access paths. | [Identity, tools and data release](../../skills/adk-system-designer/references/design-decisions.md#identity-tools-and-data-release), [browser contract](../../skills/adk-system-designer/references/runtime-and-delivery.md#specify-the-browser-contract-independently-of-hosting). Retained with explicit authorization for history, cancellation and results. |
| 64–74, 98–182: retries and uncertainty | Stable operation identity and payload survive attempts/restarts; provider guarantees govern replay; local transactions and expired leases do not settle remote effects. | [External effects and recovery](../../skills/adk-system-designer/references/design-decisions.md#external-effects-and-recovery). Strengthened failure classification and combined application/SDK retry ownership. |
| 186–259: guardrails and budgets | Distinct attempt, token, time and concurrency limits; shared reservations and settlement; durable control state and explicit overload behavior. | [Latency, capacity, budgets and operations](../../skills/adk-system-designer/references/design-decisions.md#latency-capacity-budgets-and-operations). Added control-store outage policy, independent operator stop and recovery allowance. |
| 231–239: human review | Review is a durable permission decision; notification, execution and verified completion need separate states and recovery. | [Identity, tools and data release](../../skills/adk-system-designer/references/design-decisions.md#identity-tools-and-data-release). Added reviewer authority, expiry and durable notification intent. |
| 76–84, 265–389: hosting and release identity | Select compute, inference and storage separately; include team capacity, locality, serving constraints and evidence linking deployment to reviewed inputs. | [GCP decisions](../../skills/adk-system-designer/references/gcp-decisions.md). Added builder/deployer/runtime identity separation and source-to-serving-artifact evidence. |
| 398–424: work, context and capacity | Count all request work; bound data before materialisation and before model input; separate context/cache from stored events; distinguish throughput, latency and availability. | [Runtime and delivery](../../skills/adk-system-designer/references/runtime-and-delivery.md). Added explicit context, bulk-result, same-session and workload contracts. |
| 426–476: lifecycle and replacement | Ready capacity, worker pools, shutdown and failure domains must support the claim; migrations and rollback must remain compatible with durable state and accepted work. | [Release continuity](../../skills/adk-system-designer/references/runtime-and-delivery.md#preserve-contracts-through-startup-and-release). Added bounded drain, effective configuration, mixed-version checks and staged-release criteria. |
| 449–464, 624–649: deferred work | Acceptance must survive a crash; freeze batches and retain identities; distinguish job identity from tool continuation; erasure must account for late work. | [External effects and recovery](../../skills/adk-system-designer/references/design-decisions.md#external-effects-and-recovery), [runtime state](../../skills/adk-system-designer/references/runtime-and-delivery.md#bound-context-and-preserve-useful-state). Added batch/cursor and source-expiry obligations. |
| 480–566: frontend | Public transport and runtime location are separate choices; correlate exact calls, handle late errors, distinguish reconnect from resubmission and bound slow consumers. | [Browser contract](../../skills/adk-system-designer/references/runtime-and-delivery.md#specify-the-browser-contract-independently-of-hosting). Added explicit JSON/streaming tradeoff and protocol/resource boundaries. |
| 603–621: knowledge publication | Stage, evaluate and promote approved versions; preserve evidence identity; empty scoped retrieval never expands entitlement; citations and relevance do not prove answer support. | [State, knowledge and freshness](../../skills/adk-system-designer/references/design-decisions.md#state-knowledge-and-freshness). Strengthened release cutover and separate retrieval/answer evaluation. |
| 650–727: evaluation | Test actual enforcement and absence of forbidden effects; use real orchestration with controlled external boundaries; preserve failed/missing observations and distinguish evidence tiers. | [Verification ladder](../../skills/adk-system-designer/references/failure-review.md#define-a-verification-ladder). Retained; detailed judge calibration, holdouts and aggregation belong to the evaluation specialist. |
| 729–818: sensitive data | Minimise and protect before persistence, model exposure, execution or public release; screening dependencies need failure/capacity policy; old data remains subject to policy compatibility. | [Identity, tools and data release](../../skills/adk-system-designer/references/design-decisions.md#identity-tools-and-data-release). Added trusted policy selection, inspection-service recipients and incompatible-history handling. |
| 879–954: credential lifecycle | Secret storage does not establish credential ownership; consent, refresh, account changes and disconnect have durable state and concurrency consequences. | [Identity, tools and data release](../../skills/adk-system-designer/references/design-decisions.md#identity-tools-and-data-release). Added connection metadata, stale-refresh/cache invalidation, revocation delay and outage-versus-revoked-consent distinctions. |
| 967–1058: analytical correctness | Define meaning before SQL; use complete template matches and selective schemas; preserve grain, denominator, time semantics and intent across follow-ups; cost and permissions remain independent controls. | [Analytical questions](../../skills/adk-system-designer/references/design-decisions.md#when-the-application-answers-analytical-questions). Added denominator, zero/missing data, time boundaries and explicit completeness/freshness semantics. |
| 86–94, 470–476, 1050–1058: evidence and cleanup | Match each claim to its boundary test; track owned resources and uncertain operations; cleanup requires observable absence and separate recovery. | [Failure review](../../skills/adk-system-designer/references/failure-review.md), [operations](../../skills/adk-system-designer/references/design-decisions.md#latency-capacity-budgets-and-operations). Retained. |

## Deliberate boundaries

The designer is independently usable: its architectural decisions and failure
contracts are bundled locally. It can hand an authorized implementation to an
available specialist without requiring that specialist to produce the design.
The following detail remains in the existing collection:

- SDK callback order, control-flow implementations and event mechanics:
  [workflow design](../../skills/adk-workflow-design/SKILL.md).
- Timeout/retry adapters, provider replay mechanics and transaction recipes:
  [safe API calls](../../skills/safe-api-tool-calls/SKILL.md).
- Budget ledgers, approval executors and notification implementations:
  [operational guardrails](../../skills/adk-operational-guardrails/SKILL.md).
- Platform commands, manifests, packaging and measured tuning:
  [deployment](../../skills/deploy-adk-on-google-cloud/SKILL.md) and
  [optimisation](../../skills/optimise-adk-on-google-cloud/SKILL.md).
- Transport translation, UI wiring and precise stream parsing:
  [frontend integration](../../skills/adk-frontend-integration/SKILL.md).
- Memory ingestion, release promotion and erasure implementations:
  [memory architecture](../../skills/adk-memory-architecture/SKILL.md).
- Evaluation datasets, strict result parsing, judge calibration and holdouts:
  [agent evaluation](../../skills/adk-agent-evaluation/SKILL.md).
- Detector configuration, transformation ordering and runtime hook enforcement:
  [sensitive-data protection](../../skills/protect-adk-sensitive-data/SKILL.md).
- OAuth callback/PKCE, token publication and secret-store mechanics:
  [tool authentication](../../skills/adk-tool-auth-and-secrets/SKILL.md).
- SQL parsing, alias resolution, query templates and semantic result fixtures:
  [SQL engineering](../../skills/adk-sql-agent-engineering/SKILL.md).

Historical test counts, example resource names, fixed capacities, prices and
implementation-specific limitations were not converted into universal design
defaults. Provider facts still require current, version-specific verification.
The [testing report](../testing/system-designer.md) records the actual trials;
coverage of an instruction is distinct from evidence that a model follows it.
