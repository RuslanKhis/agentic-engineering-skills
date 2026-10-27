I wrote the design into the Notes section of `docs/tickets/T-48.md`. It is a design only: I changed no code, pins or tests. Nothing was run against Loyalty Cloud or Entra, because there was no network or credentials. The vendor facts come from their onboarding note and the staging `tools/list`, and the specification facts come from the MCP authorization docs. None of it is verified against a live system.

**Register**
- Use a Client ID Metadata Document. The vendor's server advertises both that and dynamic client registration (DCR), and the spec's order is pre-registered id, then metadata document, then DCR as a fallback.
- The client has no DCR code path. A test fails if the fake authorization server's `registration_endpoint` gets a request.
- Host one JSON document at an HTTPS URL, and that URL is our `client_id`. It carries `private_key_jwt` client authentication, the JWT-bearer grant type and a `jwks_uri` for public keys. It also needs one `redirect_uris` entry, even though the flow is headless and never uses it.
- The service is behind IAP, so the document and the public keys need an unauthenticated path.
- Ask the vendor to allow-list our client id and enable the JWT-bearer grant for `loyalty.read` and `loyalty.adjust`.

**Bind credentials**
- Staff path: exchange the staff member's Entra ID token for an identity-assertion grant (ID-JAG) with `audience` set to the vendor's issuer and `resource` set to the MCP server. Present that grant at the vendor's token endpoint as a JWT bearer grant. No consent screen is involved.
- The token reaches MCP only through `header_provider`. It is cached in memory only, with one exchange in flight per principal. No refresh token is stored, and a failed mint fails the call closed.
- The adjuster role gets `loyalty.adjust`, and everyone else gets `loyalty.read` only.
- Credentials are keyed by issuer and client id.

**Tool contract**
- `list points history` has spaces in its name, and the confirm tool's name is 90 characters. Neither is a valid model function name, and ADK cannot rename MCP tools.
- Every tool takes `member_id` from the model. That breaks the rule that the user ID comes from the verified principal.
- I recommend four app-owned tools instead. They call the vendor through a client in `app/clients/`, with no `member_id` parameter, the member resolved server-side and a local `^LC[0-9]{8}$` check.
- Adjustments are recorded server-side, and a confirm must match the handle's owner. Approval should be a durable review record, with an operation key so a duplicate approval gives one effect.
- Results are cut down to the expected fields. Failures return actionable errors, and writes are never retried automatically.
- Commit the tool manifest and diff it against the live list. The schema constraints are partly dropped by ADK, so the tool must validate them itself.

**Questions I couldn't ask, and what I assumed**
- **IAP and Entra:** an IAP assertion is not an Entra ID token, so it can't be the exchange input. I assumed a server-side Entra sign-in that holds the staff token against the `Principal`.
- **Customers:** they have no Entra identity, so the enterprise grant can't cover balance reads for signed-in customers. I assumed the staff path ships first, and customer reads wait on the vendor confirming a client-credentials profile.
- **Not in the store:** the store has no loyalty member id and no staff role.
- **Other open items:**
  - the public host for the metadata document
  - which Entra groups mean adjuster and approver
  - the adjustment cap
  - whether Entra supports ID-JAG exchange
  - whether the vendor's confirm is idempotent
  - whether the vendor accepts the legacy handshake with `ADK_ENABLE_MCP_MODERN_PROTOCOL` off. The flag is experimental on ADK 2.12.0, so test it against staging.
- **`mcp` pin:** `pyproject.toml` has `mcp>=2.1,<3`, which is a range rather than a pin. I left it alone.

**Left undone:** no tool inventory run, because it needs the live server and approval; the metadata document, signing key, and Entra and vendor configuration; and no fakes or tests yet.