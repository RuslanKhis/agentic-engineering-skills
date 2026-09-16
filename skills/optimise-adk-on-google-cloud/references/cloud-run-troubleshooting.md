# Cloud Run deployment and client troubleshooting

Read this when an optimisation fails to reach its deployed revision, a source
build behaves unexpectedly, or the authenticated test client fails. Use
[cloud-run.md](cloud-run.md) for the main workflow and [lifecycle.md](lifecycle.md)
for authority and ownership. Prepare local repairs and exact commands first.
Deployment, IAM changes and paid retries still require the applicable approval;
reconcile an earlier accepted or uncertain operation before proposing another.

These recipes derive from ADK 2.8.0 and, for native source routing, Cloud SDK
572.0.0. Inspect the target's installed signatures, CLI help and supported current
interfaces before adapting them. Historical success does not verify the target.

## Locate the first failed boundary

| Symptom | Inspect first | Completion evidence |
| --- | --- | --- |
| Local change has no hosted effect | Staged files, dependency resolution, generated source, effective revision | Required code/assets/configuration reach the recorded image and revision |
| Native deployment selects Buildpacks or source upload returns 404 | Local Dockerfile detection, bucket selection, object/generation parsing | Real installed CLI boundary test; approved build records the intended source |
| Multiple origins become separate settings | Both build-substitution and deployment-environment parsers | Exact value survives both parsers and application parsing |
| Create succeeded, immediate lookup says absent | Recorded create result and bounded exact-resource reads | Ownership becomes visible without a second create |
| Deleted owned account still returns 403 | Complete project inventory and exact email | Successful authoritative inventory establishes absence |
| UI consent fails while agent answers succeed | Nonroot UID, HOME and writable configuration directory | Actual consent save/reload succeeds under the image's identity |
| Client never receives HTTP | DNS, connectivity, TLS trust and request stage | Verified transport reaches the intended endpoint |
| Private endpoint rejects a token | Credential source, token audience/expiry, caller and invocation policy | Anonymous rejection and intended-caller success through the chosen route |
| Deleted session produces no visible UI error | HTTP status, media type and actual client parser | Visible error, preserved status and no model execution |

## Ship the implementation and its dependencies

Inspect the actual Docker/build context and any separate native staging path.
Packaging a nearby directory or using an editable local installation can hide
missing modules, prompts and other package data. A clean source copy and a clean
dependency environment test different things; identify which was exercised.

Prepare a minimal explicit upload inventory containing the required entrypoint,
agent package, prompt/static assets and dependency declarations. Validate every
required file before cloud mutation, reject symlinks, and exclude `.env*`, private
receipts, local sessions/caches, audit evidence and unrelated projects. When a
change adds a module or prompt, update and test its delivery path too. Derive a
native staging requirements file from the project's existing declaration or lock
workflow; preserve the package manager and version policy rather than keeping an
independent dependency list that can drift.

Cloud upload selection and Docker image selection are distinct boundaries:
`.dockerignore` alone does not protect files sent to Cloud Build. Exercise the
actual uploader's allowlist/ignore behaviour with synthetic secret-marker files
and verify their absence from its archive as well as the image context. Never
test exclusions with real credentials.

Test package discovery and asset loading from an isolated staged copy with the
declared environment. Enumerate and hash the final upload tree. Record accepted
source/build/image identities and compare the effective revision with them.
Declared pins, locally resolved dependencies and dependencies inside a built image
are distinct evidence. An empty build-log extraction proves no installed inventory.

## Native source routing: preserve the actual CLI contract

The historical failure passed a `gs://` archive suffixed with `#GENERATION` to
`gcloud run deploy --source`. Cloud SDK 572.0.0 checked for a Dockerfile through
a local path, selected Buildpacks for that remote input, created its regional
default source bucket, and treated the generation suffix as part of the object
name. Upload then failed before a build or model invocation. A permissive fake
CLI had accepted the incorrect assumptions.

The verified repair supplied ADK's generated **local directory containing its
Dockerfile**, accounted for the SDK-selected regional source bucket, and recorded
the accepted source object generation, build ID and revision. In that version the
normal bucket pattern was `run-sources-PROJECT-REGION`; naming transformations and
length handling made string concatenation an incomplete general implementation.
Inspect the installed SDK's actual selection. If its required bucket already
exists without campaign ownership, preserve it and choose a separately approved
dedicated flow or target; its convenient name grants no right to adopt/delete it.

Before retrying, reproduce source selection and archive contents offline using
the installed CLI implementation with only Storage/provider transport replaced.
Assert Dockerfile detection, bucket, archive file inventory and object handling.
Keep SDK internals confined to a version-specific test: private monkey-patches
are not a portable deployment API. Repeat this check after SDK changes, and mark
an unavailable/skipped SDK test explicitly. For an approved live run, reconcile
the accepted build's exact object/generation and service operation; an empty build
list alone cannot prove an ambiguous submission never happened.

## Preserve configuration across parsers

Trace each changed setting through environment loading, build substitutions,
deployment arguments, revision configuration and application interpretation. The
historical origin allowlist crossed two dictionary parsers: Cloud Build
`--substitutions` and Cloud Run `--set-env-vars`. Commas in the value could become
new dictionary entries at either boundary.

Use the installed CLI's help and
[dictionary-flag escaping rules](https://docs.cloud.google.com/sdk/gcloud/reference/topic/escaping)
when preparing these arguments; shell quoting alone does not stop the CLI's
own comma splitting.

Use supported structured input or an explicitly selected delimiter at **both**
boundaries, and reject a reserved delimiter in values before creating resources
or a submission receipt. Test at least two comma-separated origins end to end,
then assert the exact runtime string and parsed origin list. Test profile and
call-budget propagation similarly. Inspect only non-secret effective fields;
keep secret values out of build substitutions, routine logs and evidence.

## Recover delayed visibility without replaying mutations

After an acknowledged create, poll the exact resource read and ownership marker
within a short bounded budget. Retry confirmed absence only; permission and
transport errors need diagnosis. Keep attempted/unconfirmed receipt state if the
budget expires. Resume the same operation's reconciliation when visible instead
of submitting another create. The lab's brief read delays are observations, not
a provider consistency guarantee or a universal retry interval.

For deletion, IAM sometimes returned 403 for a previously confirmed owned service
account after it had been deleted. The verified recovery required a **successful,
complete project-scoped inventory** containing no exact email match. Apply that
alternative only to the account and ownership recorded in the receipt. A failed
or truncated inventory, wrong scope, or still-listed account leaves absence
unproven. Preserve the receipt and resume later. Test denied GET plus empty,
nonempty and failed inventories; verify setup/cleanup repetition does not create
new resources or remove pre-existing grants.

## Make intentional developer UI state writable

ADK 2.8.0's developer UI saved telemetry preference in `$HOME/.adk/config.json`.
The nonroot image initially lacked a writable home, so consent POST failed with
HTTP 500 even while model answers worked. Inspect the actual image UID and HOME;
provide a narrowly writable home/configuration directory. Running the service as
root is not the repair.

Exercise actual consent routes under the nonroot identity: initial state, required
request header, save, reload and an unwritable-directory negative control. The
recorded Docker repair passed offline and live. A saved preference remains shared
within that container and ephemeral across replacement; it does not establish
per-user consent or durable synchronisation. For production-facing APIs, retain
the deliberate UI decision described in [cloud-run.md](cloud-run.md).

## Diagnose TLS and authentication separately

A certificate failure before HTTP does not implicate Cloud Run IAM. For a Python
client on macOS, inspect the already selected interpreter's CA support locally:

```bash
"${PYTHON:?}" - <<'PY'
import importlib.metadata
import ssl
from pathlib import Path
import certifi

bundle = Path(certifi.where())
if not bundle.is_file():
    raise SystemExit("CA bundle is unavailable")
ssl.create_default_context(cafile=str(bundle))
print("certifi", importlib.metadata.version("certifi"), "CA bundle loads")
PY
```

If the existing environment provides an appropriate CA bundle, configure
`SSL_CERT_FILE` for the intended client process using the path resolved by that
same interpreter. Preserve TLS verification and the environment's dependency
policy; an unavailable `certifi` is a prerequisite to report, not an implicit
installation request. This local check makes no network request and does not
verify the remote endpoint. The recorded repair succeeded before any paid request
had been submitted; establish that stage before deciding whether retry is safe.

For an HTTP rejection, distinguish token type/audience/expiry, credential source,
verified caller and invocation authority. The lab observed anonymous 403 and an
unsupported token audience returning 401. The same account could obtain tokens
from different OAuth clients, so matching the email alone was insufficient.
An explicitly selected user-ADC path refreshed its credential and verified
signature, issuer, expiry, client audience and expected verified email; that
specific route then passed live. It is not a generic service-account token recipe.

Choose the supported route for the actual credential type without silently
switching accounts, broadening IAM or publishing the service. Keep token material
out of argv diagnostics and exception output. A refreshing proxy and a proxy
given one fixed token have different expiry behaviour; verify renewal and bind
development proxies to loopback. Stop their processes/listeners after use.

## Preserve an error the actual streaming client can display

In the recorded ADK 2.8.0 UI, `/run_sse` parsing consumed SSE `data:` frames before
checking HTTP status. A missing-session HTTP 404 JSON body was therefore invisible
to that client. The narrow repair returned an SSE error frame only for POST
`/run_sse`, status 404 and exact `Accept: text/event-stream`, retaining status and
exception headers. Inspect current client behaviour before copying that predicate.

Test the actual adapter/client contract: deleted session displays an error and
restores input without executing a model; ordinary JSON clients, other routes
and statuses retain their contract; valid streams still complete. The repair was
verified offline and live. Simulated provider-timeout presentation was verified
offline only, and established neither real network timeout enforcement nor an
independent deadline in the browser client.
