# Codex CLI code-generation checks

Tested on 15 September 2026 against skills from commit
`7dc536afbcfa21a94df5f1a62071eee719a7f344`.

## Result

Three fresh Codex CLI sessions read the installed skills, generated Python code
and tests, and completed successfully. Their implementations passed **125
generated tests and 37 independent acceptance tests: 162 tests in total**.
The saved snapshots also passed when rerun from this repository.

| Invocation | Generated behaviour | Generated tests | Independent tests | Evidence |
| --- | --- | ---: | ---: | --- |
| `$adk-engineer` | SQLite language preferences, consent, user/application isolation, forgetting and ADK instruction integration | 54 | 18 | [Memory report](codex-memory-smoke.md) · [Generated store](artifacts/memory/generated/profile_store.py) |
| `$safe-api-tool-calls` | Approval checks, bounded retries and stable refund identity with an injected provider | 55 | 16 | [API report](codex-api-smoke.md) · [Generated tool](artifacts/api/refund_tool.py) |
| `$adk-workflow-design` | Concurrent document lookups, combined results, cancellation and failure handling through a real local ADK Runner | 16 | 3 | [Workflow details below](#workflow-case) · [Generated agent](artifacts/workflow/workflow.py) |

These are representative implementation checks. They do not exercise every
specialist or every example prompt in the README.

## What was installed and exercised

The memory and workflow projects installed all twelve skills from this checkout
with the Skills CLI. The API project installed only `safe-api-tool-calls`, testing
standalone use. Each installation belonged to its temporary project; no global
skill installation was added.

The workflow installation contained all **166 source files**, byte-identical
to the packages in this repository. Installation and generation did not modify
the skill instructions. The memory transcript records reads of both
`adk-engineer/SKILL.md` and `adk-memory-architecture/SKILL.md`. The direct
invocations read their installed specialist and relevant references.

Each coding session received a small existing project, a concrete request and
an executable interface contract. Separate acceptance tests were held outside
the project that Codex was asked to edit. The original incomplete fixtures
failed 18 memory checks, 14 of 16 API checks, and all 3 workflow checks.
Passing results therefore required observable implementation changes.

No corrective follow-up or manual repair of the generated implementations was
needed. This is evidence of successful use, rather than a comparison with a
control run without skills; it does not measure how much the skills improved
the model's performance.

## Environment and boundaries

| Component | Recorded version or setting |
| --- | --- |
| Codex CLI | `0.153.4` |
| Codex model | Existing configured default; no model override |
| Skills CLI | `1.5.24`, already cached |
| Node.js | `24.15.0` |
| Python | `3.11.4` |
| Google ADK | `2.8.0` |
| Google GenAI | `2.19.0` |
| pytest / pytest-asyncio | `8.4.2` / `1.4.0` |
| Generated shell commands | `workspace-write` sandbox |

The existing Python environment supplied the dependencies; no packages or pins
were changed. The CLI used its existing account to contact the Codex model
service. The generated applications used synthetic inputs and local test
doubles. No Google model request, real payment call or cloud deployment ran.

The memory and workflow suites exercised actual ADK APIs. The API case tested
an ordinary Python tool function and mock provider; it did not exercise ADK's
tool wrapper or confirmation mechanism. The workflow runs reported ADK's
`BaseAgentConfig` deprecation warning without test failures.

The outer process required normal OS access to initialize Codex's existing
local state after the enclosing sandbox blocked startup. The successful retries
retained the CLI's `workspace-write` command sandbox. No sandbox-bypass flags
were used. Raw transcripts remain in the temporary run directories; public
snapshots omit account details, caches and machine-specific paths.

## Workflow case

The supplied `build_workflow(policy_lookup, glossary_lookup) -> BaseAgent`
function initially raised `NotImplementedError`. The two injected asynchronous
lookups accept document text and return strings. The requested behaviour was
to run them concurrently, publish both exact outputs in session state and the
final response, and avoid publishing a successful review when either fails.

The main request was:

```text
$adk-workflow-design Implement the document review workflow in this project.
It should look up policy and terminology independently at the same time,
then combine their answers. Use the existing ADK interface described in
README.md, and run local tests that prove the steps overlap and failures
cannot appear as success.
```

The [complete prompt](artifacts/workflow/prompt.txt) also limited work to the
temporary project, the installed interpreter and local injected lookups.
The [snapshot README](artifacts/workflow/README.md) preserves the input contract
and instructions for rerunning the code checks.

The observed invocation, with local paths replaced by placeholders, was:

```bash
"$CODEX" exec --ephemeral --json --sandbox workspace-write \
  --skip-git-repo-check -c 'approval_policy="never"' \
  -C "$PROJECT" -o "$RUN_DIR/logs/final.txt" - \
  < "$RUN_DIR/prompt.txt"
```

It completed with exit **0** in **436 seconds**. The transcript records reads
of `SKILL.md` and the specialist's compatibility, orchestration, runtime and
validation references, plus inspection of the installed SDK's actual APIs.
See the official [non-interactive CLI documentation](https://learn.chatgpt.com/docs/non-interactive-mode)
for the command interface.

The generated implementation uses a custom `BaseAgent` and Python asynchronous
tasks for the deterministic lookups. It commits both successful results through
an ADK event, cancels and drains unfinished sibling work on failure, and
invalidates stale results before another review in the same session.

| Workflow check | Outcome |
| --- | --- |
| Original stub against independent checks | 3 failed |
| CLI's generated Runner tests | 16 passed; 1 ADK deprecation warning |
| Independent Runner checks | 3 passed; 1 ADK deprecation warning |
| Saved snapshot, both suites together | 19 passed; 1 warning, in 1.05 seconds |

The independent concurrency check uses barriers: neither lookup may finish
until the other has started. It also checks exact stored results and final
text, failure without successful output, and isolation between users' sessions.
The generated tests additionally cover both completion orders, cancellation,
invalid return values and failed repeat invocations. They block socket access,
Google authentication and GenAI client construction.

## Inspect or rerun the generated code

Each snapshot contains generated source and tests, the original incomplete
implementation, the prompt, independent tests and a short run guide:

- [Memory snapshot](artifacts/memory/README.md)
- [Refund-tool snapshot](artifacts/api/README.md)
- [Workflow snapshot](artifacts/workflow/README.md)

Rerunning these snapshots checks the saved implementations. Testing skill
behaviour again requires a fresh project with the original fixture, installed
skills and the recorded prompt. The results do not establish production
durability, real provider integration, deployment readiness, or compatibility
with every coding agent or SDK version.
