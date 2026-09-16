# Validation procedures

Use the target's existing interpreter and testing tools after checking the tests
for external effects. A mock database does not make an actual model call offline.
Record dependencies from installed distribution metadata without importing the
application. Compare them with declarations and lock resolution; keep target pins.

## Read-only inspection

Set `PYTHON`, `SKILL_DIR` and `TARGET_ROOT` to verified local locations. The skill
may be copied anywhere; none of these values refers to the companion repository.

```bash
"${PYTHON:?}" "${SKILL_DIR:?}/scripts/inspect_project.py" --help
"${PYTHON:?}" "${SKILL_DIR:?}/scripts/inspect_project.py" \
  --root "${TARGET_ROOT:?}" --mode auto --dry-run
```

The inspector requires Python 3.11+ and POSIX directory-descriptor support. It
refuses unsupported platforms instead of relaxing its symlink protections. It
reads bounded `pyproject.toml` and requirement/constraint files, recording only
allowlisted dependency information and configuration-file presence. It does not
read lockfiles, application code or environment-file contents. Source identifiers
are opaque to avoid disclosing project paths. Follow up manually on lockfiles,
unsupported declarations, imported packages and real wiring.

Exit 0 means the inventory completed, **not** that the project is compatible.
`--require-baseline` additionally returns 3 unless the discovered unconditional
runtime ADK declaration is exactly `2.8.0` without conflicting constraints.
Select `--mode agent-runtime` to additionally require AI Platform SDK `1.153.1`
and GenAI `2.19.0`; the known conflicting AI Platform `adk` extra also fails
that gate. `--mode gke` requires ADK and AI Platform SDK at those recorded pins,
without imposing a GenAI pin; the known extra conflict fails this gate too.
`auto` does not infer and enforce a hosting mode's dependency combination.
Ranged, missing, conditional and other pins require inspection, not replacement.
Exit 2 means invalid input, an unsupported platform or a hard inspection limit
was reached. The depth limit is reported in coverage and makes the optional
baseline gate unverified. Narrow the root instead of accepting an incomplete scan.
The inventory limits are 4 directory levels, 4,096 entries, 64 manifests,
128 KiB per manifest and 1 MiB in total. Repetition and `--dry-run` are read-only.

## Test the changed boundary

| Change | Minimum meaningful checks |
| --- | --- |
| Tool or schema path | Actual selected schema/result, denied or unknown inputs, unchanged caller policy, result bounds and explicit provider failure |
| Preview and export | Preview limit, full exported row/value equality, distinct concurrent requests, authorised retrieval and cleanup; verify bounds before expensive materialisation |
| Narrow child or formatter | Inspect outgoing model request: old synthetic marker absent, required current data present; prove the child is registered and reached |
| Independent tool I/O | Record overlapping execution intervals under a controlled test; verify failure/cancellation behaviour and bounded concurrency; separate scripted scheduling from live model selection |
| Output or call budget | Complete expected answer, reject reported errors and token exhaustion, test nested calls and attempt limits at the provider boundary |
| Skills/cache | Actual instruction-loading result; cached-input metadata for reuse; correctness and independent cache cleanup |
| Cloud Run | Real adapter HTTP/SSE contract with model doubles, build/source boundary, authentication, state continuity and effective revision settings; approved live checks must exercise the relevant tools |
| Agent Runtime App/compaction | Actual constructed App reaches Runner; compaction metadata, next-request context and required facts observed separately from retained storage; no hosted claim from local models |
| Managed sessions | Same authorised owner/session across turns, stored event evidence after client exit, explicit retention and recoverable cleanup; identify whether execution is remote or local |
| Runtime streams, persistence and jobs | Valid terminal answer after whole finite stream, byte/admission limits, no loss during an interleaved flush, same immutable payload/key after lost acknowledgement, original call ID in authorised job continuation |
| Runtime lifecycle/capacity | Actual source package and effective settings; owned accepted operations reconciled before retries, including regional DELETE; completed repeats make no mutation; measure capacity instead of inverting sizing recommendations |
| GKE workload | Authoritative rendered manifests, quota/surge/scaling coherence, selectors/ports, shipped image, admitted resources and separate startup/readiness/model acceptance |
| GKE serving | Actual shared backend and replacement continuity, caller-bound sessions, tested drain and final export privacy; partial delivery is independent of completion |

For Part 1 implementation depth, use
[part1-verification.md](part1-verification.md): actual ADK transport doubles,
component/integration acceptance, exact preview/export checks, aggregate budgets
and cleanup-only recovery. Use
[cloud-run-troubleshooting.md](cloud-run-troubleshooting.md) for installed
packaging/CLI, environment parser, TLS/authentication and UI boundary tests.

For Part 2 startup, compaction, streaming, buffering and continuation changes,
use [runtime-verification.md](runtime-verification.md). It includes actual-framework
checks and controlled failure interleavings; the optional finite stream consumer
validates decoded answer completion separately from tool-result semantics.

For GKE release, server/session, streaming or telemetry changes, read
[gke-verification.md](gke-verification.md). It separates renderer and SDK contracts
from admission, real storage, authenticated delivery and provider cleanup.

For a proposed performance improvement, retain the baseline workload, model and
configuration, measure successful comparable requests, record errors and sample
counts, and separate cold starts, cache state and client/network effects. A
functional pass or a change in configuration is not a measured speedup.

## Check a saved tool-and-answer run

`check_run.py` validates a **small, explicit smoke contract** against a saved JSON
array. It does not fetch an endpoint or parse SSE. Collect the entire stream using
the target's tested client, preserve provider errors and completion metadata, and
protect raw artefacts according to their contents. Do not truncate collection at
the first answer. Capture provenance separately; edited JSON can satisfy any
offline checker.

Create an expectation file for the actual tool and final author. This complete
example expects one schema tool call and two nonblank streamed text events:

```json
{
  "schema_version": 1,
  "answer_author": "catalogue_agent",
  "tools": [
    {
      "name": "get_schema",
      "result_equals": {"/status": "success"},
      "result_contains": {"/result": ["user_id", "revenue"]}
    }
  ],
  "answer_contains": ["user_id", "revenue"],
  "require_cache_hit": false,
  "min_partial_events": 2
}
```

```bash
"${PYTHON:?}" "${SKILL_DIR:?}/scripts/check_run.py" --help
"${PYTHON:?}" "${SKILL_DIR:?}/scripts/check_run.py" \
  --events "${EVENTS_FILE:?}" --expect "${EXPECT_FILE:?}" --dry-run
```

The pointers address fields in `functionResponse.response`, with JSON Pointer
escapes `~0` and `~1`. `result_equals` compares scalar values with strict types;
`result_contains` tests nonempty substrings in the chosen string field. Each tool
needs at least one assertion. Assert the tool's actual success predicate as well
as its data; custom status semantics cannot be inferred by this helper.
Prefer exact structured values for currency or
numeric data. `answer_contains` checks expected text, not semantic correctness;
add domain-specific assertions in the target's own tests.

The checker requires exactly one invocation, one correlated call/response per
declared tool, no other completed tool calls and one visible `STOP` answer from
the selected author after all required results. It rejects repeated submissions,
reported errors, failed result envelopes, non-STOP finish reasons, interrupted
events, late tool activity and subsequent text from that author. Tool call IDs
and invocation IDs must be present. Snake-case and camelCase SDK serialisation
are accepted; conflicting aliases are rejected.

This deliberately excludes arbitrary multi-agent trajectories, repeated calls to
the same tool and outputs without completion metadata. Adapt a target-specific
validator when these are legitimate requirements; do not strip adverse events to
make the smoke contract pass. Missing cache usage means unknown; zero means no hit
observed. A positive count supports reuse in the supplied data only. The reported
maximum is neither a token total nor a billing estimate.

The supported Part contract contains text, thought/signature metadata and the
declared named function calls/responses. Non-null code-execution, server-side tool,
media and unknown payload fields return unsupported input, including when they
occur after an apparent answer. The same restriction applies to nested tool media,
partial arguments, continuation and scheduling fields. It does not inspect
ordinary business keys within the declared JSON args/response as protocol fields.
Null SDK defaults are allowed. Additional protocols need an explicit
target-specific verifier; accompanying text is not a substitute.

Inputs are bounded to 8 MiB/2,000 events and a 64 KiB expectation file. Duplicate
JSON keys, nonfinite numbers and nonregular or symlink input files are rejected.
Only counts and fixed reason codes are printed. Exit 0 means accepted saved data,
2 means invalid/unsupported input, and 3 means acceptance failed. All invocations,
including `--dry-run`, make zero network calls and writes.

## Check this package after adaptation

```bash
"${PYTHON:?}" -m unittest discover -s "${SKILL_DIR:?}/tests" -v
```

The standard-library tests exercise malformed inputs, secret-safe output,
read-only repetition, pin preservation and false-positive smoke results.
`test_adk_contract.py` additionally serialises real ADK 2.8.0 events offline when
that distribution is installed. `test_runtime_contract.py` triggers compaction
through real ADK with deterministic model doubles and contrasts App versus
agent-only construction. Both explicitly skip if that SDK baseline is absent;
a skip is not an SDK compatibility pass. No test calls a provider model or
creates a cloud resource.

`test_runtime_token_compaction.py` additionally exercises the real ADK 2.8.0
token path: synthetic observed usage, an oversized first input reaching the model,
and a retained function-call/response pair outside the compacted prefix. It skips
on another SDK baseline. This establishes neither real token usage nor summary
quality, hosted configuration or a hard input admission limit.

`test_finite_answer_stream.py` checks the optional standard-library async consumer
through late errors, strict aliases/types, thought/tool exclusion, UTF-8/count/time
bounds, provisional delta/snapshot updates, cancellation and independent closure
failure. Its interoperability cases use real ADK 2.8 event JSON serialisation and
skip explicitly if that baseline is absent; the other consumer tests need no ADK. The consumer
does not validate application-specific tool results or perform transport decoding.

`test_gke_http_contract.py` keeps ADK 2.8's actual FastAPI, Runner, session routes
and event serialisation while replacing the model. It tests session body shapes,
application versus author identity, streaming selection, late errors after HTTP
200 and framework closure order. `test_gke_session_contract.py` tests real SQLite
history selection/disposal, the managed adapter with its API client doubled, and
native span export to memory. The latter intentionally demonstrates that capture
flags leave a raw conversation identifier. These tests skip missing required
SDKs; neither file establishes GKE delivery, PostgreSQL behaviour or telemetry
privacy after a production export policy. The saved-run checker's real SDK
regression also rejects code-result narration as unsupported input.

`test_formatting_contract.py` exercises the optional Pydantic 2 preview asset:
strict plain JSON cells (including rejection of Decimal-to-float coercion), exact
UTF-8 limits, cross-field shape, safe public errors, input preservation and
revalidation after mutation. It skips when Pydantic 2 is absent. This is an input
contract test, not a formatter integration or query/authorisation test.

`test_part1_adk_budget.py` uses real ADK 2.8.0 Runner, `AgentTool` and session
orchestration with deterministic model doubles. It demonstrates that the root's
framework call limit is not an aggregate child-call limit, and that shared
logical-generation admission can reject a continuation before model dispatch.
It also checks that a content-free error can be marked final. Socket/DNS paths
are blocked and another ADK version skips explicitly. The test-only counter does
not provide durable coordination, provider-attempt accounting or a live budget.

`test_gke_observation.py` uses the bundled optional session-observation component
and real OpenTelemetry in-memory export. It checks preserved service results and
exceptions, fixed safe attributes and negative controls for default exception
recording and an unfiltered parent. It skips explicitly if the SDK is absent;
this is not a whole-application privacy or external export test.

## GKE-specific acceptance

Run the inspector with `--mode gke --require-baseline --dry-run` for its two-pin
declaration gate. It does not validate Kubernetes YAML. Trace and render the
actual generator, then check selectors, private/public exposure, source staging,
image digest, probes, resources, quota/replicas/surge and session-backend wiring.
Exercise changed rendering or application behaviour with target-local tests.

For an approved deployment, bind context/project/cluster/namespace and inspect
current-generation conditions, admitted Pod resources, actual image IDs and Ready
endpoints. Verify the intended complete tool result and stored-event continuity
through a different replacement Pod UID. Check authorised session absence after
each test independently of model success. Public auth/tenant isolation, HPA
scale-out, multi-node resilience, graceful drain, database migrations, exported
privacy and browser partial delivery each require their own actual-boundary test;
a private functional smoke cannot stand in for them. Read
[gke-serving.md](gke-serving.md) and [gke-lifecycle.md](gke-lifecycle.md) only for
the selected integration and lifecycle details.

Use [forward-cases.json](../tests/forward-cases.json) to exercise an agent on
independent temporary fixtures. Judge the resulting files, commands and reports,
not whether the response repeats this document. Package validation results and
their environment limits are recorded in [skill-validation.md](skill-validation.md).
