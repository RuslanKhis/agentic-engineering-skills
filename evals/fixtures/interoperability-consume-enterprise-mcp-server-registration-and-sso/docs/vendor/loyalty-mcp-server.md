# Vendor note: Loyalty Cloud MCP server (from their onboarding pack, 2026-10-20)

- Endpoint: `https://mcp.loyaltycloud.example/v2/mcp` (Streamable HTTP).
- Protocol revision: 2026-07-28.
- Authorization server: `https://auth.loyaltycloud.example` (metadata at
  `/.well-known/oauth-authorization-server`). It advertises
  `client_id_metadata_document_supported: true`, a `registration_endpoint`
  for dynamic client registration, `authorization_response_iss_parameter_supported: true`,
  and the JWT bearer grant `urn:ietf:params:oauth:grant-type:jwt-bearer`.
- Scopes: `loyalty.read`, `loyalty.adjust`.
- Tools (from their staging `tools/list`, recorded below): balances, history,
  points adjustments. `start_points_adjustment` returns an `adjustment_handle`
  you pass to `confirm_points_adjustment`.
