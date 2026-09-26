# Make a review contract solvable

Read this when a structured critic repeatedly fails coverage/identity checks, or
when a review schema combines decision claims with an issue register. Establish
expressibility before changing prompts, model effort or live sample size.

## Worked failure: decision claims cannot carry every issue

The synthetic draft refuses a venue because its only exit is obstructed. A
separate sign-colour issue is resolved and acceptable. The original checker
requires each issue to appear either in a real decision-claim review or an
unresolved gap. It permits neither a fabricated draft claim nor a resolved gap.

| Reference or transformation | Broken checker | Required behaviour |
| --- | --- | --- |
| Exit issue and its supported refusal claim | Accept | Accept |
| Add acceptable sign colour; retain the honest exit-only claim | Reject coverage | Accept an independent issue disposition |
| Put resolved sign colour in the gap list | Reject resolved gap | Preserve that rejection; represent the issue elsewhere |
| Invent a sign-colour refusal claim | Reject claim identity | Preserve that rejection |
| Attach sign-colour ID to the exit claim without assessing its evidence | Accept | Reject invented association; require independent assessment |

The missing disposition is a representational defect. A validator pass obtained
by inventing a relationship is not a positive control. Retain the broken checker
as a reproducer, construct an honest accepted reference, then retain both the
honest transformation and the misleading association as regressions. The
[executable fixture](../tests/test_review_contract.py) demonstrates all five
paths; its test-only `broken_claim_only_checker` intentionally preserves the bug.

## Optional server-owned frame

The [stdlib example](../scripts/review_contract.py) demonstrates an application
pattern, not an ADK class or required architecture. The server compiles a frame
from its current draft, issue registry and evidence. Existing, reviewed
claim-to-issue/source associations stay server-owned. Every issue has a separate
disposition slot, whether or not it contributes a draft claim. Each claim/issue
slot has its own evidence judgments because one passage can support one
assertion and fail to support another.

The model receives text plus short slots (`c1`, `i1`, `s1`) and assesses support,
contradiction, relevance/uncertainty and issue disposition. It cannot add IDs or
rewrite known associations. Complete required evidence slots are assessed
explicitly; merely attaching a source never grants support. An empty evidence
map can honestly accompany `no_relevant_evidence`; it cannot justify publication.
The deliberately small schema omits free-text rationale/remedies. Add those to
the application's model judgment when needed, and test their actual size and
downstream use; keep established control IDs and release obligations authoritative.

`compile_frame` binds draft revision, claim text, associations, controls, issue
materiality and evidence contents to a fingerprint. `consume_review` recompiles
from trusted current state, checks the exact JSON slots and rejects stale
responses after any correction. Rebuild the request/schema after a correction;
do not mechanically relabel an old response with the new fingerprint. A hash is
not authentication: fetch state under the verified caller/session, and perform
an atomic revision check when committing a release to prevent a concurrent
draft update between validation and publication. Those application boundaries
are intentionally outside this side-effect-free helper.

### Shape acceptance and publication are separate

An honest report of uncertainty should be representable. It need not authorize
a final decision. The example returns `accepted`, `publishable`, `blockers` and
`warnings`; callers must retain all four, rather than treating accepted JSON as
successful release. No actual publication occurs in the helper.

| Synthetic reference | Shape accepted | Publication result |
| --- | --- | --- |
| Supported decisive refusal plus separately acceptable issue | Yes | Allowed |
| Supported approval with the registered required barrier control | Yes | Allowed |
| Same approval with the control removed, even if labelled acceptable | Yes | Blocked |
| Unresolved outcome with no relevant evidence | Yes | Blocked; no invented support |
| Material contradictory/unsupported/uncertain issue | Yes | Blocked |
| Nonmaterial uncertainty alongside an independent supported refusal | Yes | Allowed with a retained warning |
| Registered contradictory evidence labelled acceptable | Yes | Blocks approval; cannot disappear behind a nondecisive disposition |
| Extra issue/source association, missing slot, duplicate key, stale frame | No | Rejected before publication policy |

These are explicit toy policy choices. In particular, registered contrary
observations conservatively remain unresolved until an upstream adjudication
changes the issue registry and frame. A target application may permit a
reasoned resolution, but must encode and verify that resolution instead of
allowing a disposition to silently bypass contradictions. Materiality and
necessary approval controls must come from the application's established
policy, not an untrusted response that can downgrade its own obligations.

## Adapt and verify at the actual boundary

1. Run the retained reproducer and positive references locally. Add the target
   application's important outcome classes, including control deletion and
   adding an independently acceptable issue without changing decision claims.
2. Map references through the **actual** response schema and checker. Then send
   the same references through the real Runner or served route with a controlled
   model boundary. Inspect the stored draft/revision, selected final output,
   failed correction and publication gate. The bundled helper is not that test.
3. Inspect the serialized schema/request, frame and largest realistic response.
   Measure bytes and the target route's token/output limits; fixed slot IDs can
   reduce copying without proving provider compatibility. Test limits before
   asserting the new contract fits. A real provider canary remains a separate
   authorized observation on the exact model/adapter/schema route.
4. Check support independently on fixed evidence. The model's `supports` or
   `acceptable` label is a judgment, not independent evidence that the passage
   proves the claim. This fixture tests contract solvability and consumption,
   not recommendation quality, retrieval completeness or factual correctness.

Run from this skill directory with Python 3.11 or later:

```bash
python -m unittest discover -s tests -p 'test_review_contract.py' -v
```

The fixture uses only invented observations, makes no network/model calls and
requires no SDK installation. It exercises `consume_review` with serialized
JSON, including exact byte-boundary rejection, rather than checking documentation
wording. `sizes_bytes` reports UTF-8 frame/schema/response sizes for the actual
consumed reference; these counts do not establish token use or production fit.
Dependency pins and the skill's SDK compatibility record are unchanged.
