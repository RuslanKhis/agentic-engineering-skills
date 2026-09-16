# Diagnose protected-agent operations

Read the matching recipe when setup, startup, provider calls, accounting or
cleanup fails. Keep the target's versions and approved scope. These recipes
carry practical lessons from the dated companion evidence; they do not establish
current cloud access or justify a new deployment. For resource sequencing and
runtime/hosting decisions, use [cloud-lifecycle.md](cloud-lifecycle.md).

Search by symptom: **PermissionDenied / project / ADC**, **SERVICE_DISABLED**,
**TLS / certificate**, **import / nested enum**, **token JSON**, **slow IAM
catalog**, **429**, **budget / retries**, **diagnostic privacy**, **delete None**.

## Project, identity and API failures

**Symptom:** the CLI can see the project but the SDK fails, a project switch
leaves old resources configured, or a template GET returns PermissionDenied.

1. Record the explicit project, CLI account, expected runtime principal, ADC
   source type, ADC quota project, model backend and protection location. Compare
   metadata only; neither `.env` contents nor credential documents belong in the
   report. A UI-selected project or sign-in alias is not principal attestation.
2. Run a bounded CLI project/API read with explicit `--project` and `--account`.
   Separately run the required SDK read using the application's intended ADC.
   Classify failures as unavailable identity, project access, API disabled,
   quota attribution, missing resource, transport, or still unknown. Only a
   typed NotFound means the exact resource is absent.
3. Check the quota project as well as the resource project. For a REST path
   requiring user-project attribution, set the approved target in
   `X-Goog-User-Project`; for relevant gcloud commands use explicit
   `--billing-project`. Confirm `serviceusage.services.use` for that attribution.
   This is command-scoped attribution, not a reason to rewrite saved ADC.
4. If reads fail after a mutation, GET the exact intended IDs and reconcile the
   ownership journal before another write. The September 13 campaign created
   two SDP templates before a verification read failed; a fresh create loop
   would have obscured partial state. IAM propagation was possible, not proven.
5. After a project switch, use a fresh project-bound journal and regenerate
   configuration from that target's resources. Account for resources under the
   old journal separately. Repair only the identified prerequisite within the
   existing authorization; leave dependent work stopped when the cause is unknown.

**Regression:** simulate CLI success/SDK denial, quota-project mismatch,
NotFound versus PermissionDenied, lost create response, stale target journal
and foreign same-named resources. Assert denied reads never cause creation,
activation, ownership adoption or deletion. After a fix, rerun the same bounded
read before paid content acceptance.

**Historical evidence:** September 13 audit, “Access, activation and complete
lifecycle”, lines 131–178; September 15 cleanup recheck, lines 38–43. The latter
fixed DLP request attribution without enabling an API. September 14 preflight
also verified a signed ADC identity token after user-info endpoints returned
USER_PROJECT_DENIED; it did not grant extra permissions or assume an identity.
If using an identity token for attestation, verify its signature, expected
audience, issuer and validity with the trusted library. Decoding claims alone
is insufficient; unavailable attestation stays unverified.

**Symptom:** billing-status lookup returns SERVICE_DISABLED, or APIs appear
enabled yet runtime calls fail.

The failing service matters. A disabled `cloudbilling.googleapis.com` blocks
that status lookup and establishes no billing verdict. Compare the required
API allowlist to the successful enabled-services result. Template read access
does not prove sanitize-use permission, model permission, quota or billing.
Use runtime identity for the eventual minimum synthetic content checks. Record
already-enabled APIs separately from activation actually exercised in this run.
Regression checks should preserve these distinctions in the report.

## TLS trust failure before an HTTP request

**Symptom:** Python raises `SSLCertVerificationError` although gcloud works.

Inspect the selected Python's trust context without loading credentials:

```python
import ssl
context = ssl.create_default_context()
print({"loaded_ca_count": context.cert_store_stats()["x509_ca"],
       "checks_hostname": context.check_hostname,
       "requires_certificate": context.verify_mode == ssl.CERT_REQUIRED})
```

The historical environment loaded zero default CAs. A credential-free TLS
handshake failed with verification code 20 and sent zero HTTP requests; the
already-installed certifi bundle loaded 121 CAs. This was an environment trust
failure, not IAM denial. When the target already uses an approved CA bundle,
configure that client explicitly, preserving hostname/certificate validation:

```python
import ssl
import certifi
verified_context = ssl.create_default_context(cafile=certifi.where())
```

Use the organization's approved trust source where applicable. The snippet is
conditional on that dependency already being present; do not install packages
or rewrite global trust merely to match the old environment. Never use an
unverified SSL context or `verify=False`. If network diagnosis is needed, a
bounded credential-free handshake can separate trust from API authorization;
report it as transport evidence only.

**Regression:** reproduce missing default trust using doubles, require
certificate/hostname checks on the selected context, and reject malformed or
untrusted certificates. Retest one bounded verified connection after the fix.
Source: September 13 audit, “Demonstrated failures and narrow repairs”,
and `audit/resume-20260913/python-tls-trust-store.json` /
`python-tls-handshake.json`; `infrastructure/runtime_identity.py:111–154`.

## Interpreter, typed SDK messages and return contracts

**Symptom:** a shell wrapper fails to import dependencies although another
Python command works.

Check `sys.executable` and selected installed package versions without importing
the application. Inspect the wrapper's interpreter invocation. The historical
Armor wrapper used `exec python`; the September 14 launch initially selected a
different Python and failed before cloud calls. Correct the invocation or
subprocess PATH to the intended existing environment, then run an import/typed
message check. Do not treat that import failure as an API failure or reinstall
the environment to hide interpreter selection.

**Symptom:** a generated snippet uses a nonexistent Model Armor enum/type.

Inspect the installed SDK's generated type declarations and construct the
actual request/template locally. In inspected Model Armor 0.7.1 these were
nested types, not interchangeable top-level names:

```python
from google.cloud import modelarmor_v1 as armor

enabled = armor.MaliciousUriFilterSettings.MaliciousUriFilterEnforcement.ENABLED
uri = armor.MaliciousUriFilterSettings(filter_enforcement=enabled)
rai = armor.RaiFilterSettings.RaiFilter(
    filter_type=armor.RaiFilterType.HATE_SPEECH,
    confidence_level=armor.DetectionConfidenceLevel.MEDIUM_AND_ABOVE,
)
metadata = armor.Template.TemplateMetadata(
    log_sanitize_operations=False,
    ignore_partial_invocation_failures=False,
)
```

No client or credential is required to construct these messages. Use the
installed protobuf's serialization/round-trip and explicit field assertions to
verify the generated request before a cloud mutation. Preserve the pinned
version and adapt to its actual public contract; keep native ADK integration
changes behind [compatibility.md](compatibility.md) and runner regressions.
These type forms are source/contract evidence, not a claim that a nested-enum
failure occurred in the live campaign.

**Regression:** exercise the actual subprocess entry point with the selected
interpreter and real installed SDK message types, replacing only provider
constructors/transports. Check semantic fields after serialization. Relevant
sources: `infrastructure/provision_model_armor.sh:12–16`,
`provision_model_armor.py:14–36`, `scripts/preflight.py:104–115`,
`tests/test_lifecycle_cli.py`; September 14 audit, lines 111–115.

## CLI token shape and bounded permission discovery

**Symptom:** a gcloud token helper rejects otherwise valid output.

The inspected CLI's `auth print-access-token --format=json` returned an object
with exactly one `token` string, rather than a raw JSON string. Match the
installed CLI contract and validate shape in memory. Never stringify arbitrary
JSON as a credential, print a rejected token/value, or include captured stdout
in a parse-error message. Keep any token wholly inside the authorized request
path; do not write a credential probe artifact.

**Regression:** use fake token values for valid exact object, missing/extra keys,
non-string token and malformed JSON; assert diagnostics contain only a fixed
failure classification. Source: `infrastructure/runtime_identity.py:95–109`;
September 13 audit, repair table line 265. This is a historical CLI observation,
not a promise of the output shape of every gcloud release.

**Symptom:** checking a small custom role issues dozens of requests or times out.

The historical gcloud testable-permission listing made 58 HTTP attempts before
a 45-second timeout because filtering occurred after catalog pagination. Where
the required permission set is known, prefer the current documented bounded
query interface. The inspected implementation used IAM
`POST /v1/permissions:queryTestablePermissions`, pages of 1,000, and stopped as
soon as all seven required names were found. It checked custom-role support/API
availability, bounded response bytes, reserved each request before sending,
rejected repeated page tokens and redirects, and disabled retries.

This is a fragile wire-accounting path: verify current method and paging
contracts before adapting it. A wrapper that counts gcloud commands, or counts
HTTP diagnostics only after each command completes, cannot enforce an exact
pre-send cap on gcloud's internal pagination/retries. Report observed and
reserved attempts separately, including a reserved TLS failure that sent no
HTTP. Stop further discovery when the bound is reached.

**Regression:** multiple pages, early completion, duplicate/malformed entries,
repeated cursor, unavailable permission, request/response size bounds, exhausted
budget and TLS failure before send. Source: `runtime_identity.py:43–185`;
September 13 audit, lines 264 and 277–286. That campaign did **not** establish
compliance with a universal management-wire cap.

## HTTP 429 and safe provider classifications

**Symptom:** real Gemini calls return 429 after successful setup or after a
billing change elsewhere.

Stop the bounded test at its agreed failure condition. Record backend,
credential/quota project, model, region, HTTP code, allowlisted SDK status,
allowlisted `google.rpc.ErrorInfo.reason` and whether `QuotaFailure` is present.
Use already-parsed SDK data; do not consume a streaming response again merely
for diagnostics. Withhold content and retain a generic public failure.

Distinguish quota restrictions from temporary capacity only when response
classification supports it. The September 13 error body was not retained, so
its cause remained unknown. Twenty-seven successful Vertex requests on
September 14 did not establish that an AI Studio payment caused the improvement.
Backend billing and quota paths must match the actual request.

If quota metadata is relevant, use the currently documented route with bounded
pagination. The historical Service Usage `v1` route returned 404; `v1beta1`
consumerQuotaMetrics worked. Missing limits/dimensions and sentinel values such
as `-1` are not a measured model request capacity. Record incomplete or ambiguous
metadata explicitly. A larger quota, alternate model/region or new paid cycle
is a separate decision, not an automatic diagnostic retry.

**Regression:** malformed/unknown error detail, allowlisted reason,
QuotaFailure-only response, streaming errors and raw secret text in exception
messages. Assert generic release failure and metadata-only diagnostics.
Sources: `scripts/live_campaign.py:218–248,310–327`; September 14 audit,
“Investigation of the previous 429”; `audit/resume-20260914/quota-summary.json`.

## Live budget and retry accounting

Use this only for an approved bounded acceptance campaign; it is not a demand
to monkey-patch a production SDK. The companion isolated version-specific
instrumentation in its campaign harness. Ordinary application request limits
and a smoke helper do not enforce a campaign-wide provider budget.

The implementation needs these properties before the first paid call:

1. A private, durable journal holds the immutable service ceilings and absolute
   deadline. Reserve each attempt under a cross-process lock **before** transport;
   atomically save and keep failed/cancelled/reserved attempts charged to the
   budget. Refuse journal reset, repeated once-only test commands, and silent
   deadline extensions on restart.
2. Count direct protection clients **and** native plugin calls at their common
   transport boundary. Disabling GAPIC retries alone does not disable gRPC-core
   retries; inspect both. For GenAI, inspect retries and the selected HTTP
   transport for streaming and nonstreaming paths. Fail setup if instrumentation
   does not cover the installed version, rather than claiming a hard cap.
3. Validate model host/path/project/location and bound serialized request bytes
   including schema/history, protection payload bytes and output tokens. Clip
   each RPC timeout to remaining campaign time. Count actual generation attempts
   separately from gateway requests, which can make several model/tool turns.
4. Account management, credential-refresh and paid-content calls separately.
   A transport hook covering generation does not cover all management traffic.
   Expose any wire-count gap in the final evidence instead of implying a global
   hard cap. Reserve time and permitted operations for cleanup after paid stop.
5. Keep automatic paid retries disabled for the diagnostic run. A positively
   classified transient read may receive a separately bounded retry; an
   uncertain mutation first requires exact-ID reconciliation. A tool side
   effect requires its own idempotency contract before retry.

Historical example: 48 Gemini, 160 SDP, 240 Armor and 20 gateway attempts;
32 KiB provider requests and 2,048 model output tokens; paid stop after 75 minutes
with cleanup targeted by minute 90. September 14 used 27/59/92/20 respectively,
with no paid retry. These are campaign evidence, not recommended universal
defaults. A US-dollar estimate also depends on tokens, bytes, allowances and
current prices; request ceilings are not a hard billing cap.

**Regression:** concurrent reservation, failure after reservation, journal
reopening, deadline expiration, duplicate test command, extra tool turns,
SDK/gRPC retry attempts, oversized schema/history and wrong model target.
Exercise actual transport entry points with offline doubles before live use.
Sources: `scripts/live_campaign.py:47–173,184–215,261–357`;
`audit/EXTERNAL_CAMPAIGN.md`, “Bounded execution and acceptance”;
September 14 audit, lines 242–268. Its private SDK hooks required inspected ADK
2.8.0 / GenAI 2.23.0 and are not a portable production integration recipe.

## Failure diagnostics can become a sensitive-data sink

Provider exception messages, pytest assertion representations and HTTP debug
logs can contain the very prompt, tool value or credential the boundary is
protecting. Emit an allowlisted record such as operation, error class, approved
reason/domain/service, status, elapsed time and counts. Omit arbitrary provider
messages/metadata, URLs, headers, principal strings and payload excerpts.

If raw failure details are truly needed, use a separately authorized private
artifact path: directory `0700`, exclusive non-symlink file creation with mode
`0600`, outside version control and exported evidence. Capture test output so
tracebacks cannot also escape to ordinary terminal/CI logs. Retain only the
minimum necessary and follow the target's retention policy. A file called
“audit” or “metadata” is not automatically safe to publish.

The companion's live-test failures could create private `.failure.txt` files
while the public journal held assertion outcomes only. Its gcloud wrapper
captured HTTP logs transiently to count requests, disabled file logging and
discarded the raw buffer; copying those debug logs would violate the intended
evidence boundary. Prefer transport counters when available.

**Regression:** inject secrets into exception text, ErrorInfo metadata and
pytest failure details; assert they are absent from stdout/stderr/public JSON.
Check private file permissions, symlink/existing-file refusal and export
exclusion. Sources: `infrastructure/lifecycle.py:25–63`,
`runtime_identity.py:63–108`, `scripts/live_campaign.py:499–528`;
`README.md:461–477`.

## Cleanup fails after the first successful delete

**Symptom:** deletion removed one resource, then raised an AttributeError on
`.result()` and left the rest.

Inspect the pinned SDK's method return contract. The historical Model Armor
delete returned `None`; treating it as a long-running operation caused exactly
this partial cleanup. Record intent, call the synchronous delete, then GET the
exact ID and accept typed NotFound as absence. Continue cleanup of independent
owned resources after a failure, aggregate unresolved outcomes and preserve the
journal. A retry begins by reading/reconciling current state, since the failed
local line may follow a successful cloud deletion.

**Regression:** synchronous `None` return, already absent resource, one delete
failure followed by successful independent cleanup, denied verification read,
lost response, foreign marker, missing journal and repeated cleanup. Keep the
installed SDK request types real in offline tests. Source: initial independent
audit, repair table line 134; `infrastructure/cleanup_gcp.py:26–53`.

For IAM tombstones, shared APIs, incomplete inventory and billable retained
storage, finish with [owned teardown and retained state](cloud-lifecycle.md#owned-teardown-and-retained-state).

## Evidence scope

All companion paths above are optional provenance within the revision pinned
by [compatibility.md](compatibility.md). The instructions here are standalone;
do not require those paths or private audit files at runtime. “September 13”
and “September 14” refer to the public
`audit/INDEPENDENT_AUDIT_2026-09-13.md` and
`audit/INDEPENDENT_AUDIT_2026-09-14.md`; the initial report is
`audit/INDEPENDENT_AUDIT.md`. The cleanup recheck is
`audit/CLEANUP_RECHECK_2026-09-15.md`.

Historical fixes and regression evidence explain these recipes. A newly adapted
adapter, environment, hosted service or budget harness needs its own applicable
offline tests and separately authorized live evidence; none is implied by a
successful historical run.
