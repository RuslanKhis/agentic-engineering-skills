# Govern approved reference knowledge with RAG

Use this reference when designing, reviewing or implementing retrieval of approved documents. Use semantic memory for remembered preferences and a scoped structured-data tool for owned records; neither establishes the current approved policy.

## 1. Choose the retrieval boundary

- Establish the requested mode: in a review, trace and report existing behaviour; in an implementation, change the requested boundary; in validation, execute only the authorised checks. A design request does not authorise corpus creation or promotion.
- Inspect the target's installed ADK, model provider, retrieval SDK, root-agent construction, tools and content-protection hooks. Retain its supported interfaces and dependency conventions rather than transplanting example imports or replacing its root agent.
- Prefer explicit application retrieval when passages must pass entitlement, provenance or content checks before model consumption. Trace the exact order from authenticated request to released answer.
- Consider model-service retrieval only when its inspection boundary and tool composition meet the requirement. Verify the exact SDK/model path: an application before-model hook cannot inspect passages fetched later inside the model service. A separate agent can address composition without creating that missing inspection point.
- For metadata filtering, verify enforcement in the selected API, backend and deployment mode. A stored tenant field is not an access control. Use separate collections where required isolation cannot be established.

Complete this decision with the chosen retrieval path, the checks it permits, and the target files or components that own them.

## 2. Inspect authority and release state

- Find the trusted mapping from authenticated subject to retrieval entitlement. Resolve tenant, role/classification and collection scope on the server; keep them out of model-supplied tool arguments.
- Separate read-only serving authority from document ingestion, publication and retirement. Verify permissions using the serving workload identity, including required metadata reads; operator success proves a different access path.
- Identify how a request resolves its active release and whether a cache exists in code. Record cache expiry, invalidation and behaviour during an unavailable registry; a configuration variable alone does not establish implemented caching.
- Require approved content to have stable document identity, release/version, access scope, reviewed-byte digest and useful location metadata. Treat effective date, publication time and active release as different facts.
- Trace each retrieved source back to the selected release's manifest or equivalent trusted registry. Reject unknown sources and mismatched release/scope metadata before evidence reaches the model.

Complete inspection with a concrete authority and provenance chain, plus any missing enforcement points.

## 3. Implement the serving contract

1. Accept a bounded question and only the business arguments the model needs. Use the target's supported context injection to obtain trusted identity; do not manufacture ADK context from request text.
2. Resolve the caller's entitlement, then the active release and its pinned manifest/index version. An empty scoped search must remain empty; it must not widen to another tenant or unapproved collection.
3. Retrieve within that scope, map source metadata and recheck passage classification and ownership. Retrieval similarity selects candidates; it does not authorise access or establish answer support.
4. Project an explicit evidence schema. Preserve passage text with document, release/version and available section/page metadata. Represent unavailable locations honestly rather than inventing them.
5. Apply required content protection before publishing the complete tool result. Treat retrieved instructions as evidence, never as authority to change scope or invoke otherwise forbidden actions. On an incomplete protection check, release no partly screened passages.
6. Set a total deadline covering entitlement lookup, registry reads, retrieval and required screening. Bound question size, candidate count, passage size and complete serialised UTF-8 payload; top-k alone does not bound bytes. Choose limits from the target workload and quota budget.
7. Drop complete evidence units or return a safe no-answer outcome when bounds cannot be met. Preserve text/citation association and avoid truncating an exception into a contradictory claim.
8. Where internal source locations must remain private, issue opaque invocation-bound citation IDs and retain their source/passage mapping server-side. Validate answer citations against that invocation before release. Separately evaluate whether the cited evidence supports the claim; valid identifiers do not prove semantic support.

Define a stable public unavailable/no-supported-answer contract that does not reveal inaccessible collections. Keep safe internal reason codes for absent evidence, denied scope, registry inconsistency and dependency failure. Make the agent decline unsupported claims instead of reconstructing policy from memory.

## 4. Implement publication only when in scope

- Admit approved sources through a separate ingestion identity. Inspect/classify them under the target policy and quarantine incomplete checks. A credential-pattern scan or self-declared `clean` manifest does not establish full privacy or hostile-content review.
- Preserve document structure needed to understand headings, tables and exceptions. Evaluate chunking and overlap against representative questions rather than copying fixture settings.
- Stage immutable source/index versions and bind review to their bytes. Associate the evaluation artefact with the exact candidate digest, collection and release; reject mismatches or stale results.
- Promote with a compare-and-swap or generation precondition on the active pointer. On conflict, re-read and report the competing state rather than overwriting it blindly.
- Define cutover semantics. An atomic pointer change does not revoke evidence already resolved by in-flight requests; caches can extend visibility. Preserve release provenance and implement stronger admission/release checks only where required.
- Record accepted import and other long-running operation handles before retrying uncertain work. Resume or reconcile the known operation instead of creating an untracked replacement.
- Define retirement separately for inactive collections, source/staging objects, index versions, caches and evaluation copies. Read [operations-validation.md](operations-validation.md) when planning authorised cleanup; deleting a collection is not proof that retained copies or regional backend capacity are gone.

## 5. Validate the selected guarantees

- Test an authorised request, another tenant/role, a missing mapping, an inactive release, unknown source metadata, and an empty result. Assert that none of the negative cases broadens retrieval.
- Test hostile passages and screening timeout/unavailability at the actual pre-model boundary. Assert no raw or partly protected content is released.
- Exercise payload overflow, missing location metadata, fabricated/cross-invocation citations and claims unsupported by an otherwise valid citation.
- Test failed/stale candidate evaluation, concurrent promotion and a request spanning promotion. Assert the documented release and cache behaviour.
- Measure retrieval independently from generation: expected document/section recall, irrelevant and unanswerable questions, scope negatives, citation support and bounded work. A positive document-hit fixture does not establish answer quality.
- Use deterministic doubles for boundary failures, then authorised live checks with the actual serving identity for provider behaviour. Label unexecuted or blocked gates explicitly; a historic pass does not validate a changed target.

## Completion and evidence limits

Report the target decision, changed components, observed validation and unresolved release conditions. The source companion demonstrates explicit scoped retrieval, manifest-backed provenance and candidate-gated pointer promotion. It does not establish a full production ingestion pipeline, opaque citation renderer, complete payload caps or one end-to-end retrieval deadline. Implement and test those controls where required before describing them as delivered.
