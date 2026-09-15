# Delegated OAuth lifecycle

Read this reference when the requested work involves user consent, account linking, reconnect, token refresh or disconnect. Apply the requirements to the selected provider and deployment. A mock provider can demonstrate transaction mechanics without proving real browser or account security. Use [compatibility-and-evidence.md](compatibility-and-evidence.md) to separate existing evidence from required production behaviour.

## 1. Establish the connection identity

Trace the verified application principal through the credential index, token store and cache. Record the provider, trusted provider-account identifier, OAuth client, granted scopes, active credential reference, connection status and revision. Derive the principal from validated issuer/project, tenant where applicable, and subject. An application UID does not automatically identify the provider account selected during consent.

Complete this step when every credential lookup has an explicit owner and every lifecycle update can distinguish the connection revision it acts upon. On review tasks, report missing fields and protections rather than claiming they exist.

## 2. Bind and consume consent transactions

Start consent through an authenticated application action. Store a random, short-lived, single-use transaction bound to the initiating principal and browser, provider, client, requested scopes and exact configured redirect URI. Retain a pending session/action only when the application supports continuation, and verify its ownership. Keep the transaction-specific PKCE verifier server-side; apply the provider's supported code-flow contract.

Establish browser continuity through a protected transaction cookie or equivalent server-validated mechanism. With cookies, use HTTPS, Secure, HttpOnly and a SameSite policy appropriate to the callback method; protect cookie-authenticated initiation against CSRF. The provider redirect does not carry the application's bearer header. Database state associated with a user is not, by itself, browser binding.

Before exchanging a code or linking credentials, validate state, expiry, browser continuity and the initiating principal. Atomically consume the validated transaction so competing callbacks cannot both exchange it. Bound recovery after failure; start a fresh transaction when necessary instead of repeatedly redeeming a code. Keep callback query strings, codes and credentials out of chat and telemetry.

When using Google, consult its [web-server OAuth guidance](https://developers.google.com/identity/protocols/oauth2/web-server) for the selected flow. Request offline access when the feature requires a durable refresh token, and test the applicable consent configuration and token-expiry rules.

## 3. Validate and publish durable credentials

Establish the provider account using its documented trusted identification mechanism. Fully validate any OIDC token used for this purpose. Check the actual granted scopes against the operation; request added permissions deliberately when the feature changes.

If a later response omits a refresh token, preserve the existing token only when the trusted account and client bindings still match an active connection. Account/client changes require valid new durable authority. Publish new secret material through a conditional index update against the expected revision and status. Keep payloads in the protected store and only references/metadata in the index.

Complete this step when account switching and omitted-token responses cannot relabel another connection's credential or overwrite a newer connection.

## 4. Coordinate refresh and failure

Coordinate concurrent refreshes per connection. After obtaining replacement material and storing a new version, activate it only if the expected connection revision, status and account/client bindings remain current. Recheck validity after nonrotating refresh too. Reconcile unused versions and provider-side changes when activation loses a race; storage and provider operations do not share the index's database transaction.

An expected-version/connected-status compare-and-swap is useful partial protection. It does not automatically cover reconnect, same-user refresh serialisation or replica coordination. Advance the revision for account, client, grant and status changes. Apply a rejected grant to the revision that failed, rather than disconnecting a newer connection.

Distinguish recognised invalid grants from outages, malformed responses and quota failures. Preserve durable authorisation during transient failure and return a safe unavailable outcome. Classify provider error reasons before retrying; keep eligible attempts and underlying transports within the operation's total budget.

Cache short-lived access tokens with conservative expiry and keys covering principal, provider, account/client, scope and revision. Keep refresh tokens in the protected credential store. For replicas, use shared authoritative state and test invalidation or an explicit maximum revocation delay.

## 5. Disconnect locally before remote cleanup

Atomically mark the connection unavailable and advance its revision first, blocking new calls. Then revoke provider authority where supported, retire owned credential versions and invalidate caches across replicas. Record remote revocation and retirement failures for bounded reconciliation without reconnecting the user. Distinguish local access removal from confirmed provider revocation. Define what happens to requests already in flight; disabling a secret cannot erase plaintext already in use.

## Completion and tests

Use [validation.md](validation.md) to record executed evidence. Exercise wrong/expired/replayed state, a copied consent URL in another browser, a changed initiating principal, missing scopes, same-account reconnect without a refresh token, account/client switching, simultaneous refreshes, disconnect during rotating and nonrotating refresh, stale failure after reconnect, provider revocation timeout, repeated disconnect and another warm replica.

Assert that rejected callbacks make no exchange/linking call, stale refresh cannot publish or authorise a subsequent tool operation, temporary failure preserves the connection, and disconnect leaves the chosen local and remote outcomes explicit. Mark unexecuted real-provider/replica cases as unverified. Complete a production implementation only when the applicable invariants and tests pass; complete a review with concrete findings and evidence boundaries.
