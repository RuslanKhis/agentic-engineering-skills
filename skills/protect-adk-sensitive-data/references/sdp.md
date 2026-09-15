# SDP: deny, then transform

Use this mode when raw text may reach a model, history, tool or other sink. SDP
means Google Cloud Sensitive Data Protection; the Python package/API still uses
`google-cloud-dlp` / `dlp_v2`. The framework-neutral asset is a controller, not a
detector or Google client. Provider adapters and domain policy remain explicit.

## Choose coverage

Separate **deny** classes (reject the request) from **transform** classes
(replace values while preserving useful intent). Never transform a forbidden
credential into something that accidentally permits the rest of the action.
Ask the owner to resolve ambiguous data policy; do not infer permission to send
raw customer text to a cloud service from permission to write code.

The historical implementation used these exact policies:

| Purpose | Tested configuration |
| --- | --- |
| Credential inspection | `GCP_API_KEY`, `AWS_CREDENTIALS`, `JSON_WEB_TOKEN` |
| PII inspection | `CREDIT_CARD_NUMBER`, `EMAIL_ADDRESS`, `PHONE_NUMBER`, `PERSON_NAME` |
| Inspection behaviour | `min_likelihood=POSSIBLE`, `include_quote=False` |
| Transformation | Replace detected values with info-type labels; transform all findings; transformation error handling `throw_error` |

These lists are a baseline, not comprehensive secret detection. They do not
establish coverage for arbitrary passwords, cookies, bank accounts or an
organisation's own tokens. Inventory those classes and evaluate appropriate
custom detectors with synthetic positive and negative examples. Broad likelihood
settings trade missed findings against false positives. A replacement label or
hash is not proof of anonymisation; re-identification/tokenisation needs its own
access, key, retention and risk design (**production guidance**).

## Wire the reusable controller

Copy [sdp_boundary.py](../assets/sdp_boundary.py) into an appropriate existing
module only when useful. Its two injected async operations are:

- `inspect(text) -> InspectResult`: perform the required credential inspection
  and return the finding count and truncation flag. Adapter transport, parse,
  permission and incomplete-result failures must raise; never manufacture a
  clean result when credentials are missing.
- `deidentify(text) -> str`: return only an accepted transformed result under the
  chosen PII policy. Validate the entire provider response before returning.

Call `await protect_text(text, inspect=..., deidentify=..., max_chars=...,
timeout_s=...)` and use **only its return value** downstream. It enforces one
deadline, input/output bounds and generic failure without logging. It rejects
empty strings; if the target allows an empty message, define that policy before
calling the controller and still validate the rest of the request. Exceptions
withhold the operation. The asset uses one public error for rejected/unavailable
outcomes; projects needing separate HTTP outcomes should introduce safe internal
reason codes without exposing text or provider diagnostics.

The included tests use synthetic replacements and prove controller ordering,
not provider detection accuracy. No Model Armor, authorisation, persistence,
side-effect idempotency or SDK concurrency control is supplied by this asset.

## Adapt the Google provider boundary

Inspect the target's installed SDK before writing calls. In the recorded
`google-cloud-dlp==3.38.0` path:

1. Own one `dlp_v2.DlpServiceAsyncClient` with the selected endpoint and close its
   transport during application shutdown. Bound active calls with a semaphore;
   queue time counts towards the request deadline.
2. Validate the configured security project/location and full template names.
   Use `parent=projects/{project}/locations/{location}`; inspection and
   de-identification templates are trusted configuration, never request fields.
3. `inspect_content` takes an `InspectContentRequest` containing the deny
   `inspect_template_name` and `ContentItem(value=text)`. Disable implicit retries
   for the initial bounded campaign (`retry=None`); set the RPC timeout to no
   more than the remaining budget.
4. Convert `response.result.findings` to a count and retain
   `response.result.findings_truncated`. A finding blocks regardless of
   truncation. An empty truncated list is indeterminate and must not proceed to
   de-identification. Do not use `bool(findings)` as the complete verdict.
5. `deidentify_content` takes the PII `inspect_template_name`,
   `deidentify_template_name` and `ContentItem`. Require a valid text item, check
   every `overview.transformation_summaries[].results[].code` for `SUCCESS`,
   reject failed or malformed summaries, then return `response.item.value`.
   Empty summaries can occur when no transformation was needed; schema validity
   and transport success still matter. Never ignore provider error summaries.
6. Pass the returned text through any required prompt screening before a
   session write or model call. For tool text, preserve the full contract and
   validate again after replacement.

Google documents that truncation can hide additional findings. The decision to
withhold an empty truncated inspection is this skill's fail-closed production
policy. [InspectResult reference](https://docs.cloud.google.com/sensitive-data-protection/docs/reference/rest/v2/InspectResult).
The RPC specification defines transformation error handling, including rejecting
a request on a transformation error. [DLP RPC reference](https://docs.cloud.google.com/sensitive-data-protection/docs/reference/rpc/google.privacy.dlp.v2).

## Required regression cases

Run the relevant cases in [validation.md](validation.md), including findings with
and without truncation, empty truncated results, malformed responses, denied
permissions, timeout, partial transformation failure and transformed output that
no longer fits the domain schema. Check actual model requests and stored events,
not only the user-visible answer.

**Evidence:** the historical adapter/tests support deny-before-transform,
template routing, error handling and concurrency. They do not cover the
empty/truncated case. A later offline probe exposed that gap; the new asset
enforces the stronger rule. See [compatibility.md](compatibility.md), E1–E3.
