# Skills and context caching

Use this reference when specialised instructions inflate ordinary requests,
irrelevant history reaches a narrow child, or repeated stable input suggests
context caching. First identify the actual root, tools, children, `App` and
Runner or serving loader. Imported definitions alone do not establish wiring.

## Load instructions progressively

If requests need different specialist guidance, give each Skill a descriptive
name and task-selection description. Keep common routing instructions small;
load full instructions for the selected task and additional resources only
when needed. Register the `SkillToolset` on the executing agent and use the
loading protocol supplied by the installed ADK version. Verify discovery,
loading and the returned instruction contents; a configuration print or the
model's claim that it used a Skill is insufficient. The official
[Skills documentation](https://adk.dev/skills/) describes this progression
and the toolset's supplied system instructions.

Treat Skill instructions as guidance. Apply caller authorisation, SQL policy
and execution limits in trusted application code. If the Skill contains
scripts, establish its execution environment, allowed inputs and permissions,
then exercise failures before relying on it. Successful loading of an inline
instruction does not verify script execution or sandboxing.

If a formatter or validator needs only current input, consider
`include_contents="none"`. This excludes previous-turn conversation content;
current input, instructions, tool exchanges and interpolated state still
matter. Seed a synthetic historical marker and a current-input marker, inspect
the outgoing model request, and require historical absence plus current-input
presence. Bound the supplied data and validate the result. A child declared
with `mode="single_turn"` can make multiple model and tool calls; give nested
work explicit call, attempt, input, output and elapsed-time budgets.

## Verify a cache experiment

If a substantial stable prefix is reused, first confirm model/backend support,
permitted retention and freshness requirements. Keep tenant-specific material
out of shared prefixes. Keep ordinary instructions small and consider retrieval
for large reference collections. Context caching retains model input; it does
not replace session storage or cache completed answers.

Configure `ContextCacheConfig` on the `App` and preserve that `App` in the Runner
or serving integration. In ADK 2.8.0, `min_tokens` gates activation using earlier
response token metadata; the provider's minimum also applies.
`cache_intervals` counts invocations, while `ttl_seconds` controls retention.
One user turn can contain several model requests. Treat
`min_tokens=2048`, `ttl_seconds=600`, `cache_intervals=5` as historical experiment
inputs. If adding a creation deadline, `create_http_options` accepts
`types.HttpOptions(timeout=10_000)` in that version; the timeout is milliseconds.
Recheck the installed API and [cache documentation](https://adk.dev/context/caching/)
before changing versions or choosing provider thresholds.

Run the authorised experiment with a synthetic prefix and known expected
content. Record cache creation, expiry, subsequent provider cached-input token
counts, misses, total input/output usage and answer correctness. Require positive
provider cache usage for a reuse claim. Missing metadata means unknown.
Configuration and a quick response prove neither reuse nor a speedup. Measure
warm-instance and cache effects separately; compare successful requests with
the same workload and consumption path.

Reserve attempts before dispatch and preserve cumulative limits across recovery.
Retry appropriate transient failures only within the declared policy; validation
failures require correction. Reject reported errors, fabricated fallback values
and `MAX_TOKENS` as successful completion. A passed component cannot turn a failed
combined answer into a pass. Usage counters are not invoices or monetary caps.

Record owned cache identities at the provider creation boundary, including
uncertain outcomes. A cache may exist even when the following generation fails.
Reconcile pending creation before another attempt. Delete owned caches separately
from sessions and compute, verify absence, and retain unresolved receipts. Report
provider retention separately from active-resource absence.
