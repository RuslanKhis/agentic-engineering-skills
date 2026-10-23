# MITRE ATLAS and CoSAI Risk Map alignment — 23 October 2026

*What changed, what was checked, and what a fresh agent did with it.*

## Change

See the [comparison note](../research/atlas-cosai-comparison-2026-10-23.md).
In the repository: the identifier paragraph in the security skill's
threat-model reference (eleven ATLAS 2026.09 agent techniques, ten Risk Map
risks and six controls, cited by id, with the caution that the map's
technique mappings are still `@5.0.1`) and a companion line in the checklist
asset. After the trial: the companion line extended to LLM02 by cross-tenant
retrieval, LLM05 and LLM07, with the rule to write "no listed ATLAS id"
rather than stretch one; the security inspector now counts `corpus`,
`knowledge` and `kb` as private-data tokens (with a test), and the validation
reference says how `predicate` filters and retrieval tools are reported;
mode (f) skips the code-execution section when the inventory shows no
executor; a tool-call budget in `before_tool_callback` for projects served by
`adk web` without Runner code; the rule to replace remote toolsets before a
Runner test; and the taint sample's comment on extracting values rather than
whole chunks. **One scenario case** (`security-review-with-atlas-and-cosai-ids`).

## Automated checks

`scripts/validate_skills.py` after the edits: **22 packages**, 0 errors,
0 warnings; `git diff --check` clean; `check_repo.py` 700 tests after the
inspector change, no failures.

## Fresh-agent trial

One trial, in a subagent with a fresh context, the 22 packages readable as
installed skills, no Google skill installed, no credentials, no network, no
ADK installed, on a synthetic project, without the expected answers.

### Security: a review reported in ATLAS and CoSAI vocabulary

The project: an ADK 2.12 knowledge agent searching a corpus shared across
tenants, sending mail, with an unfiltered vendor MCP server and no turn
limit.

What the agent did: a review with eight findings, each carrying the ATLAS
technique, the Risk Map risk and the OWASP id beside it, the enforcement
point, the observable check, the evidence label and the owning skill;
SDK-free tools and policy modules (tenant-scoped search failing closed, a
mail allow-list re-checked in the body, a gate with tool-call budgets, an
egress allow-list and taint refusal, a result labeller extracting addresses
and URLs); the toolset filtered, prefixed and held for confirmation with an
empty allow-list until an authorised listing; 21 offline tests run, 2 Runner
tests reported as not run; the inspector before and after.

Ease rating: **4 of 5**. The vocabulary rule was already in the threat-model
reference; the ids had to be assembled from prose.

Frictions and what was done the same day:

| Friction | Fix |
| --- | --- |
| The inspector reported a shared-corpus search as not private, so the trifecta looked absent | Retrieval-corpus tokens added with a test; the limit stated in validation |
| A constant-built `tool_filter` shows as `predicate` | Stated |
| ATLAS ids were prose; LLM05, LLM07 and cross-tenant disclosure had no companion | Companion line extended; "no listed ATLAS id" rule |
| No bound recipe for a project without Runner code | The `before_tool_callback` budget with `temp:` and session counters |
| A real `McpToolset` reaches the network in a Runner test | Replace remote toolsets before the test |
| The taint sample would miss an address inside a long chunk | Comment: store extracted values, not chunks |
| Mode (f) meant 90 KB of reading for a small agent | Skip rule for the code-execution section |
| The `find_spec` skip trap | Already fixed in the evaluation skill the same day |

## What this does not establish

The Runner tests and the authorised MCP listing did not run; the ids were
taken from the skill's reference rather than re-fetched.
