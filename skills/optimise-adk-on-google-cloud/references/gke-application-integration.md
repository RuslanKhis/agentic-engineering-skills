# Connect GKE startup and sessions to the serving application

Read when implementing a session backend, client warm-up, readiness gate or
application lifespan. Use [gke-serving.md](gke-serving.md) for the storage/access
decision and [gke-verification.md](gke-verification.md) for acceptance tests.
This guidance extends the recorded private lab; its isolated examples were not
the deployed application's lifecycle.

## Choose the integration seam before building a helper

Find the object that owns the real request handlers. For ADK's API factory,
follow backend selection through its service factory into the cached Runner.
For a custom server, follow its handlers into the actual `Runner(app=...)` and
service. Preserve the existing server when its supported configuration meets
the requirement; changing to a custom Runner also transfers HTTP, startup and
shutdown responsibilities to the application.

In the recorded ADK 2.8 factory, `session_service_uri` selects the service and
`session_db_kwargs` can supply database constructor options. Inspect their
installed signatures and selected backend before using them. Creating another
`DatabaseSessionService` in a lifespan does not make factory-created handlers
use it. A factory helper returning the same object twice proves that helper's
cache only; capture the service used by an actual request to establish reuse.

The companion selects `SESSION_SERVICE_URI` when its entrypoint imports and
constructs the server. A later environment change cannot reconfigure that
already-created application. Apply configuration before construction and test
alternatives in isolated application instances or fresh processes. Use the
[configuration ledger](application-integration.md#establish-effective-configuration-before-changing-behaviour)
for loader precedence, literal model choices and cached clients.

Keep endpoint decisions separate. A full managed-session URI carries its own
project, region and resource identity; a model configured for `global` need not
place sessions there. The retained ADK service-registry test observes a regional
managed-service constructor even while `GOOGLE_CLOUD_LOCATION=global`. In a
target adaptation, assert both constructor arguments rather than inferring one
service's location from the other's environment variable. Record only approved,
non-sensitive configuration evidence.

## Order ownership and closure explicitly

Use one owner for each Runner, session service, database engine and retained
client. Establish construction, readiness and closing order from the serving
framework, including failure before startup completes.

There is a specific composition hazard in the recorded ADK 2.8 factory: its
services are constructed before the supplied `lifespan` begins, and framework
cleanup closes cached Runners **after** the supplied lifespan exits. Therefore
disposing a service inside that lifespan's exit can precede a Runner flush that
still needs it. The portable [HTTP contract test](../tests/test_gke_http_contract.py)
observes this order while executing the real Runner closure. Recheck the target
version; do not replace the factory's internal lifespan or assume a supplied
callback owns every resource it encounters.

When a custom application deliberately owns the full lifecycle, use this order:

1. Construct each worker's service and retained clients after any worker fork.
2. Prepare necessary local state under bounded startup; publish readiness only
   after preparation succeeds. Build the Runner with the intended ADK `App` and
   that same service, then make it available to the actual handlers.
3. On shutdown, stop admitting new work according to the server's drain policy,
   settle or explicitly fail active work, and close the Runner while its service
   remains available. Then close the owned service/engine and client transports.
4. If construction or preparation fails partway through, close everything
   successfully acquired. Preserve the original startup/request failure when a
   later cleanup also fails; record cleanup failure without sensitive details.

This is an ownership design for a custom server, not a replacement factory
implementation. A context manager around an unused service establishes no
request behaviour. Verify framework-owned resources separately before adding
another close call. In the recorded SDK, Runner flush and database-engine
disposal are distinct boundaries. The relevant tests must observe them both.

## Warm the client the request will actually use

Choose eager or lazy construction from measured demand. A rare tool may benefit
from deferring an expensive import; an essential first-turn client may need
bounded preparation before readiness. Record which work moved from startup to
first use. A smaller startup number alone can hide a slower first useful turn.

Keep the warmed credentials, transport and client attached to the dependency
used by model/tool requests. Test object identity or observable factory counts at
that boundary across two requests; invoking the warm-up helper twice proves
less. Avoid retaining a client across a worker fork or configuration change.
Allow the supported client library to refresh expiring credentials.

The companion's credential example runs `refresh` in a thread and retries every
exception; it supplies neither a deadline for one stalled refresh nor a permanent
error policy. Its retry-success test uses demonstration credentials. A production
adaptation needs transport-level limits as well as the total startup budget,
and transient-versus-permanent classification. Coroutine cancellation alone
does not terminate blocking thread work. Keep readiness a shallow result of
preparation and verify real permissions in the separately bounded smoke path.

## Preserve the API contract when changing construction

Retain application identity separately from answer-author identity. A loader's
application name chooses routes and session storage, while the root agent's
name appears as event author. Verify both after changing loaders or constructing
an ADK `App`; accepting the wrong author can hide an unintended answering agent.

In the recorded ADK 2.8 API, explicit-ID session creation takes the state
dictionary directly. The collection route takes a request containing `state`
and optional `sessionId`. The explicit-ID route is deprecated in that SDK.
Check the selected route's actual schema before adapting a client; wrapping an
already direct state body can silently store an extra `state` layer. Preserve
the intended state and owned session ID through creation, read and invocation.

Choose the developer UI deliberately. `web=False` reduces the served development
surface; it does not establish trusted caller identity. Developer-UI consent
storage is another local capability: the companion tests cover consent-header
validation, persistence on server restart and failure under an unwritable
application home. Those checks neither enable nor verify Cloud Trace export.
Include writable configuration storage only when the selected UI requires it;
keep the image's non-root filesystem behaviour distinct from agent readiness,
session durability and exported telemetry policy.
