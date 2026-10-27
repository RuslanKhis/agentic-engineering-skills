# MCP specification revisions and ext-auth alignment — 22 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/mcp-spec-ext-auth-comparison-2026-10-22.md).
In the repository:

- **Facts** from the specification at commit `80041ab` and ext-auth at
  `fb374c7`, paraphrased with links: tool-name rules, validation errors as
  tool execution errors and the schema-dialect gap in the tool-interface
  skill; the 2026-07-28 shape with its two design consequences in the
  interoperability skill's exposure reference; discovery, registration
  priority, issuer binding and the two ext-auth profiles in its consumption
  reference; issuer-keyed registrations, `iss` validation and
  Enterprise-Managed Authorization in the tool-auth skill's lifecycle
  reference, with provenance in its evidence file.
- **After the trial** (23 October): the 2.12.0 feature flag that selects
  the modern connect path, the `header_provider` failure path, the stable
  profile's wire parameters, the headless-client `redirect_uris` rule, the
  version framing at the top of the consumption reference, and a clean split
  of ownership between the two skills (wire shape in interoperability, token
  lifecycle in tool-auth). The inventory helper's `--diff` now compares by
  tool name when each manifest holds one target, with a test; the
  package's tests were re-run on 23 October (its frontmatter carries no
  `last-tested` field).
- **No routing line.**
- **One scenario case** (`interoperability-consume-enterprise-mcp-server-registration-and-sso`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. The full `scripts/check_repo.py`
counts are in the [testing log](index.md) entry for this date.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK or `mcp` installed, on a synthetic project, without the expected
answers. The trial was interrupted once by a usage limit and resumed from
its saved state.

### Interoperability and tool auth: moving a triage agent to a vendor's remote MCP server

The project: an ADK 2.12 agent calling a vendor REST API with a bearer token
from an environment variable; the vendor retiring that API for a remote MCP
server speaking 2026-07-28, an authorization server that supports client
metadata documents and forbids dynamic registration, an enterprise identity
provider offering managed authorization, and security rules against consent
screens and long-lived vendor tokens.

What the agent did: a metadata-document client registered to the vendor's
issuer with a startup discovery check; the enterprise profile implemented
end to end (token exchange at the identity provider, JWT-bearer at the
vendor's authorization server, a signing key at an exact Secret Manager
version, tokens in memory only, no refresh tokens); a synchronous
`McpToolset` with allow-list, prefix, cache TTL, `header_provider` and a
result validator; a loopback fake of the identity provider, authorization
server and MCP server over which 48 tests ran, 5 SDK-bound tests reported
as not run; the inventory helper run against the fake under both
handshakes; a ticket with four recorded decisions and five open items.

Ease rating: **4 of 5**. The consumption reference answered the three hard
questions in one place; points lost to the material being split across two
skills with cross-references in both directions and to the helper's
URL-keyed manifest.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| `--diff` keyed tools by `target::name`, so a manifest pinned against a fake or staging reported everything added and removed | The helper compares by name when each manifest has one target and reports `keyed_by`; test added; validation reference says so |
| The 2.x connect path was named but not identified | `ADK_ENABLE_MCP_MODERN_PROTOCOL=1` with its default, scope and fallback, from the 2.12.0 registry and session code |
| 2.8.0 statements with no version framing | A sentence at the top of the consumption reference |
| The enterprise profile was one bullet with no URNs; each skill pointed at the other for the concrete flow | Wire parameters in the consumption reference; lifecycle rules (index entry, cache bound, single flight, failure classes, no refresh token, fail closed) in the lifecycle reference, each naming the other as the only home of the other half |
| `redirect_uris` for a headless metadata-document client | One HTTPS URI on the client's host, recorded as unused |
| `header_provider` exception behaviour unknown | Not caught in the 2.12.0 header merge; surfaces as the tool's error; fail closed |
| Committed manifest versus `.adk-evidence/` | One sentence in the validation reference |
| The interpreter rule took two readings; the API Gateway section sat between the parts needed | Left as they are; the rule is complete and the section order is a Phase D question |

## What this does not establish

The vendor's and the identity provider's acceptance of the profile, the
SDK-bound wiring tests and any live exchange did not run.
