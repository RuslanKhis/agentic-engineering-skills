I've written the plan into the Notes section of `docs/tickets/T-48.md`. It is design only. I wrote no code, tests or manifest, and I made no network calls and ran no tests. The IdP and vendor behaviour comes from the vendor note and the MCP specs, not from anything I ran against a server.

**Registration (no dynamic client registration)**
- Use a Client ID Metadata Document. We host a JSON document at an HTTPS URL on our own domain, and that URL is our `client_id`.
- The document lists a `redirect_uris` entry we never use, because the field is required.
- It authenticates with `private_key_jwt`, so no client secret exists.
- Client state is keyed by the vendor's issuer. We never call their `registration_endpoint`, even though they advertise it.
- Before any live test the vendor must confirm four things in writing:
  - Their authorization server accepts our metadata document.
  - It accepts the JWT bearer grant from a client registered this way.
  - It trusts our IdP's identity assertions.
  - They have set the scopes per grant.
- If any of those is a no, ask for a pre-registered client ID. Do not fall back to dynamic registration.

**Credential binding (no consent screens)**
- Per call, we exchange the user's Northwind ID token at the IdP for an identity assertion aimed at the vendor's authorization server and MCP server. We then present that assertion to the vendor as a JWT bearer grant.
- No vendor refresh token is stored. Tokens never reach the model or the browser.
- The access token goes in through `McpToolset(header_provider=...)`, and the provider reads the verified principal from `app/auth.py`. A provider that raises fails closed.
- Read tools use a `loyalty.read` token. Adjustment tools use a separate toolset requesting `loyalty.adjust`, and only staff can get it.
- ADK 2.12.0 speaks revision 2026-07-28 only with `ADK_ENABLE_MCP_MODERN_PROTOCOL=1`, which is experimental. I recommend enabling it and proving it against a fake server first.

**What the tool contract must survive**
- Two of the four tools can't be exposed as named. `list points history` has spaces, and the confirm tool's name is about 90 characters. I recommend wrapping all four tools as our own functions with clean names, with the client code in `app/clients/` and no ADK imports there.
- `member_id` must not be a model argument. We validate `^LC[0-9]{8}$` ourselves and fill it from the verified principal.
- `delta` is capped and `reason` is bounded.
- `start_points_adjustment` is staff-only. We store each handle against the principal who started it. Confirm refuses a handle issued to someone else, an unknown one, or one already used, so duplicates converge on one effect.
- Confirmation is a strict-boolean `require_confirmation` answered by the signed-in staff user. A timeout on confirm is reported as an unknown outcome, not retried.
- The tool list I reviewed is the vendor's staging file, so we need to re-inventory production and commit that manifest.

**Questions I couldn't ask, and what I assumed**
1. `app/auth.py` verifies the Google IAP assertion, not an Entra ID token, and the token exchange needs the Entra one. I assumed IAP is federated to Northwind SSO and the original ID token can be read server-side. If it can't, the design is blocked.
2. Customers aren't in the Northwind tenant, so enterprise-managed authorization can't cover customer balance and history reads. I assumed a vendor-supported service grant, or a staff token with `member_id` resolved server-side. Owner: Jonas with Ahmed.
3. I took security's word that the IdP issues these identity assertions today. The IdP admin should check.
4. The mapping from customer principal to `member_id` doesn't exist in `app/store.py` yet.

**Left undone:** the code in `app/tools/` and `app/clients/`, the fake-server tests (the ticket lists them), the production tool inventory, hosting the metadata document (needs Ahmed's sign-off), and every vendor and IdP action.