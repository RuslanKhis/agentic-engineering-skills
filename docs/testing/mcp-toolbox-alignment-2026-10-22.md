# mcp-toolbox alignment — 22 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/mcp-toolbox-comparison-2026-10-22.md).
In the repository:

- **Facts** from googleapis/mcp-toolbox v1.14.0 (commit `3581e0a`) went into
  five specialists at the decision each serves, cited to the documentation
  file and labelled vendor documentation: a Toolbox branch checklist in the
  SQL skill (engine-level read-only lock and why `COMMIT;` chaining and pool
  poisoning do not apply, the BigQuery flags and the `allowedDatasets`
  analysis, the prebuilt tool's own production note, basic over template
  parameters, secure parameters for tenant ids, the three bypass fixtures)
  with the `DataAgentToolset` facts beside it; the client's protocol default
  and pin, the credential strategies and the main-branch signature in the
  interoperability skill; the `readOnlyHint` enforcement note in the
  security skill; the version-conditional tool-output screening of the ADK
  Model Armor plugin (2.12.0) and the gateway and floor-setting paths in the
  sensitive-data skill, with the finding that the Toolbox page's ADK sample
  does not screen tool results; secure parameters and the IAP assertion
  facts in the auth skill.
- **No routing line**: Toolbox is a server and a library, not a skill.
- **One scenario case** (`sql-toolbox-read-only-and-secure-tenant`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean. The full `scripts/check_repo.py` counts
are in the README entry for this date. No helper script, test or
`last-tested` date changed.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK or Toolbox SDK, on a synthetic project, without the expected answers.
It was interrupted by a usage limit before it had read the ticket and was
resumed; the resumed run completed normally.

### SQL agent: tenant-scoped answers through Toolbox

Fixture: an ADK analytics agent using `ToolboxToolset` against a
`tools.yaml` with a free-form `bigquery-execute-sql` tool, a `bigquery-sql`
template whose table name was a template parameter, a `tenant_id` ordinary
parameter the instruction told the model to read from the user's message, a
server that decoded an IAP assertion without verifying it, and ticket G03
with contracts for the verified tenant, the source-level read-only lock and
fail-closed writes.

Observed: the agent led with adk-sql-agent-engineering, found the Toolbox
checklist by grepping, and mapped the three contracts onto it: `readOnly:
true` with `allowedDatasets` on the source, the free-form tool removed with
the vendor's production note as the justification, the template-parameter
table name replaced by a reviewed fully qualified constant, `tenant_id` as a
`secure: true` parameter bound in code from a verified IAP assertion through
a per-request context variable and stripped from the model-facing
declaration, a credential strategy policy that forbids the no-auth strategy
off loopback, and a Toolbox double at the documented contract that answered
the three bypass fixtures fail-closed with zero jobs. It implemented the
assertion verification the fixture had left as a TODO, kept the ADK imports
out of the identity boundary, filled the Evidence section with the
contract lines, the A4 justification, the planned live steps, the controls
left out and the human effort owed, and set `verified_local`. Offline: 27
tests on Python 3.13 with the standard library runner (10 skipped for a
missing library or the SDK) and 25 on Python 3.9 with pytest (2 skipped);
the SDK wiring test and every live Toolbox and BigQuery step were reported
as not run. Ease: **4 of 5**; the checklist mapped the contracts almost one
to one, and the point lost was the verification path without the SDK.

Fixed the same day: the SQL skill's "read next" table has a direct row for
the Toolbox and managed-data-agent executor; the checklist says the offline
double stands in for the server at its documented contract, which
adk-engineer's rule against imitating the SDK permits; adk-engineer says
what to do when the only interpreter that meets the pin lacks the test
runner; the interoperability selection row says which `ToolboxToolset`
signature to write against when no SDK is installed; and the auth skill's
identity reference carries the IAP assertion facts (header, keys, issuer,
audience shapes, skew, `sub` and `email`) read on Google's page that day,
with the rule that a tenant is not an IAP claim. Noted, not changed: the
`tools.yaml` key spellings are quoted from the vendor's documentation and
nothing bundled checks them offline.

## Limits

One trial on one synthetic project; no Toolbox server, database or SDK, so
the DSN lock, the dry-run rejection, the secure-parameter wire format and the
SDK signatures were read, not exercised. The trial's own double is offline
evidence of the documented contract and nothing more.
