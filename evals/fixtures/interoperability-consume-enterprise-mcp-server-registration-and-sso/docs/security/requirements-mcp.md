# Security requirements for the Loyalty Cloud connection (Ahmed, security)

- No dynamic client registration against vendor authorization servers.
- No per-user consent screens: our staff sign in with Northwind SSO (Entra ID tenant
  `northwind.example`), which offers enterprise-managed authorization for SaaS apps.
- Tokens never reach the model or the browser.
