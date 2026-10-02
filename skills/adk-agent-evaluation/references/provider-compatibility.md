# Check the response shapes actually sent

Read for dynamic structured-output schemas, provider/adapter changes or schema
rejections. Compatibility belongs to the exact provider, endpoint, model, adapter
version, request mode and serialized request. No example here establishes a
restriction for all ADK or OpenAI-compatible routes.

Qualify [contract solvability](contract-qualification.md) offline first. Keep native
Pydantic/custom validation, provider-enforced wire schema and semantic source checks
as separate gates; local parsing and an OpenAI-compatible endpoint prove neither
keyword enforcement nor factual correctness on the selected route.

## Populate the compatibility matrix

Generate requests through the application's pinned SDK/adapter and intercept the
final transport offline. Preserve a sanitized synthetic request and schema hash
after adapter conversion, including effective output settings. Inspect nested
schemas rather than only the application's Pydantic model. Record resolved SDK
versions separately; retain existing dependency pins.

| Actual workflow shape | Representative content | Offline observation | Authorized live observation |
| --- | --- | --- | --- |
| Source selection | Realistic enum count/length; literal multiline quotation and short-ID alternatives | Native serialized enum and escaping; reject the problematic shape in a controlled transport | Exact route accepts/rejects this schema |
| Structured review | Required claim/source slots, nested arrays and nullable/no-evidence branches | Missing/duplicate slots rejected; null branch survives conversion | Valid complete response within configured output limit |
| Visual evidence | Image input plus the actual review schema | Media part, MIME/size and permitted source mapping reach transport | Actual route accepts this combination |
| Largest planned frame | Longest expected draft, enum cardinality and source set | Request/schema bytes and expected response size measured | Truncation/finish status and complete parsed response retained |

Mark unsupported or unused shapes explicitly; do not mark untested rows passed.
Bytes are not tokens. Measure tokens with the target's available tokenizer/usage
facility, or record the token estimate as uncertain. A large frame that cannot fit
the existing output limit needs a contract/workload decision before the cohort.

For exact quotations, a short selection ID can keep full immutable text server-side
and reduce schema size. Validate selections against the draft/source revision and
resolve them on the server. This changes wire format, not whether the passage
supports a claim; run grounding calibration separately.

## Controlled rejection and route binding

The optional [schema evidence helper](../assets/provider_schema_probe.py) compares
exact synthetic wire requests with observation records. Its
[tests](../tests/test_provider_schema_probe.py) use an offline transport that
rejects a multiline enum nested in a schema. They verify that a rejection blocks
the gate, and that a successful observation for a different route or a smaller
request cannot substitute. The helper sends no requests and does not understand
provider schemas or enforce budgets.

Adapt the controlled rejection to the real adapter seam: capture its emitted
bytes, force the matching request to fail and assert no cohort dispatch follows.
Test SDK retries at that seam too. Local serialization acceptance, controlled
transport behavior and remote observations are three different evidence levels.
Retain every response/error and its level; keep authorization headers and private
content out of exported artifacts.

## Budget a representative remote canary

When remote evidence is needed, include the actual generated schemas and media
shape in the exact approved account/model/route envelope. Reserve its sends,
retries, output and deadline alongside the cohort, with a declared failure gate.
Use existing authorization within scope. A canary rejection stops the conditional
cohort; diagnose the request rather than silently switching routes. For a fixed
already-approved cohort, preserve its declared protocol.

Check parsing, required slots, finish/truncation status and actual usage as well as
HTTP success. Retain unresolved charges on a missing receipt. A tiny JSON answer
or another provider's success is not evidence for the dynamic request being tested.
