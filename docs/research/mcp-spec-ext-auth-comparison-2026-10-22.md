# MCP specification revisions and ext-auth compared with this toolkit — 22 October 2026

## Scope and snapshot

A review of the Model Context Protocol specification at
[modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol)
commit `80041ab` (2026-10-20), sparse-cloned on 22 October 2026 into its own
directory (the `docs/specification/` tree and `seps/`) and read, and of
[modelcontextprotocol/ext-auth](https://github.com/modelcontextprotocol/ext-auth)
at commit `fb374c7` (2026-06-18; MIT). The specification repository is in a
licence transition from MIT to Apache-2.0 (its LICENSE says so; documentation
other than specifications is CC-BY-4.0), which is why every fact is
paraphrased with a link and nothing is copied. Files read:
`2025-11-25/changelog.mdx` and `server/tools.mdx`; `2026-07-28/changelog.mdx`,
`server/tools.mdx` and `basic/authorization/client-registration.mdx`;
ext-auth's `specification/stable/enterprise-managed-authorization.mdx` and
`specification/draft/oauth-client-credentials.mdx`. The 2026-07-28 wire
behaviour was already observed in the conformance spike on an ADK 2.12.0
server.

**Conclusion.** The memo's list is right and short: the two revisions add
rules that change what three specialists recommend. The tool-interface skill
gains the tool-name bounds, the validation-error rule and the schema-dialect
gap between a server's 2020-12 schema and ADK's Gemini-subset conversion; the
interoperability skill gains the design consequences of a stateless protocol
(server-minted state handles are model-visible data; deterministic listing is
a cache contract) and the consumer's registration, discovery and
issuer-binding rules; the tool-auth skill records issuer-keyed registrations,
`iss` validation and Enterprise-Managed Authorization in its credential
index. The client-credentials profile is a draft and is labelled so.

## Method

Changelogs were read before prose, the normative pages for the facts the
changelogs name, and ext-auth's stable and draft documents separately. Each
fact is placed at the decision it changes with the commit and date; the
toolkit's rules (annotations never decide policy, allow-list by name, private
by default) stand. One scenario case covers the consumer journey; a
fresh-agent trial on it is recorded in the
[testing record](../testing/mcp-spec-ext-auth-alignment-2026-10-22.md).

## Drift corrected

- The memo attributed CIMD to 2026-07-28; CIMD arrived as a recommended
  mechanism in 2025-11-25 (SEP-991) and 2026-07-28 deprecated Dynamic Client
  Registration in its favour (PR #2858). The skills say both.
- The memo's "deterministic listing" is a SHOULD on the server, not a MUST;
  recorded as such.
- Beyond the memo: results carry `resultType`, list results carry `ttlMs`
  and `cacheScope`, error codes were renumbered into a reserved range
  (`-32020` to `-32099`), and Roots, Sampling, Logging and HTTP+SSE are
  deprecated under the feature lifecycle; only the design-changing items went
  into the skills, the rest is left to the SDK.

## Imported, by specialist

- **adk-tool-interface-design.** SEP-986 name rules; SEP-1303 validation
  errors as tool execution errors; the 2020-12 dialect and ADK's subset.
- **adk-agent-interoperability.** The 2026-07-28 shape and its two design
  consequences in the exposure reference; discovery, registration priority,
  issuer binding and the two ext-auth profiles in the consumption reference.
- **adk-tool-auth-and-secrets.** Issuer-keyed registrations, `iss`
  validation and Enterprise-Managed Authorization in the lifecycle reference,
  with provenance in its evidence file.

## Routed, not copied

Nothing to route; the specification is cited.

## Vendored assets

None; the licence transition rules out copying text.

## Left out, with reasons

- Tasks extension, `subscriptions/listen`, OpenTelemetry `_meta` keys,
  `x-mcp-header`, icons, URL-mode elicitation: SDK and host concerns.
- The SEP files themselves: the changelogs cite them and the pages carry the
  normative text.
- Security best practices page: already covered by the toolkit's own rules
  and the conformance spike's `dns-rebinding-protection` and header checks.

## Limits

Read, not run beyond the conformance spike; ext-auth's enterprise profile
references an IETF draft (identity-assertion authorization grant, -04) that
may change.
