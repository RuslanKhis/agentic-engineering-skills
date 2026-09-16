# Updated skills — laptop verification, 16 September 2026

Reviewed the replacement skills, restored missing distribution files, installed
the repaired checkout locally, and exercised its offline checks.
**All 12 packages validated; 476 unique tests passed with zero failures or skips.**
The separate coding-agent trials below are recorded independently.

## Source review and repairs

The starting checkout was `22cd37d`. Review covered all eleven replacement
specialists: their entrypoints, implementation references, helpers, assets and
tests. Historical verification records were read as provenance, not counted as
new executions. The deeper instructions remain independently usable without the
book, companion source, or another skill collection.

| Issue found | Change and evidence |
| --- | --- |
| Replacing `skills/` removed the advertised entrypoint and one metadata file | Restored the router's four files (`SKILL.md`, licence, OpenAI metadata and composition reference) and `safe-api-tool-calls/agents/openai.yaml` from `a789894`. |
| A final-response flag could still admit private event content | Updated `public_text.py` to reject partial, user/non-model and tool-bearing events independently of ADK's final flag; added regressions. This projection is not general-purpose secret detection. |
| Deeply nested TOML crashed the guardrails inspector | Reproduced the traceback, caught parser recursion exhaustion, and added a real-CLI regression requiring structured incomplete inspection. |
| Optional database tests could fail before reporting missing prerequisites | Added explicit SQLAlchemy, aiosqlite and greenlet checks, with a compatible `sqlalchemy[asyncio]` setup note for the observed macOS arm64 environment. |

The safe-API fixtures deliberately contain defects for a repair exercise. Their
separate acceptance suite requires a selected, reviewed generated candidate.
The fresh Claude trial below also led to explicit guidance and regressions for
safe stack-location logging and preserving contract-valid amount spellings.

## Installation on this laptop

Used **Skills CLI 1.5.24** with **Node 24.15.0**, installing from the local checkout
plus the repairs above. Existing skill copies and relevant lock records were
backed up before replacement. This did not publish the changes to GitHub.

Equivalent command from this repository with a compatible Node runtime:

```bash
npx skills@1.5.24 add . --skill '*' -a claude-code codex -g -y
```

| Location | Verified installation |
| --- | --- |
| `~/.agents/skills` | All 12 packages, 229 files, matching source; Codex's canonical installation. |
| `~/.claude/skills` | All 12 packages available through symlinks to the canonical installation. |
| `~/Documents/adk-claude-starter/.claude/skills` | All 12 project-local copies refreshed, 229 matching files; previous copies backed up. |

Start a fresh session after installation: `$adk-engineer` in Codex or
`/adk-engineer` in Claude Code. Specialists use the corresponding prefix.

## Reproduce the offline checks

Executed on **CPython 3.12.9**, **macOS 26.6.2 arm64**, in a temporary environment.
This installs the principal recorded test dependencies; it is not a complete
transitive lock or a required dependency set for applications using these skills.

```bash
CHECK_ENV="$(mktemp -d)/venv"
python3.12 -m venv "$CHECK_ENV"
"$CHECK_ENV/bin/python" -m pip install \
  'PyYAML==6.0.3' 'markdown-it-py==4.2.0' 'pytest==9.1.1' \
  'google-adk[db]==2.8.0' 'google-genai==2.19.0' \
  'google-cloud-aiplatform==1.153.1' 'google-cloud-dlp==3.38.0' \
  'sqlalchemy[asyncio]==2.0.54' 'aiosqlite==0.22.1' 'greenlet==3.5.6' \
  'httpx==0.28.1' 'pydantic==2.13.5' 'google-auth==2.58.0' \
  'opentelemetry-sdk==1.42.1'
```

From the repository root, run the ordinary gate and its three supplemental suites:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  "$CHECK_ENV/bin/python" -B -I scripts/check_repo.py
"$CHECK_ENV/bin/python" -B -I -m unittest discover \
  -s skills/adk-workflow-design/tests -p test_runtime_contracts.py -v
"$CHECK_ENV/bin/python" -B -I -m unittest discover \
  -s skills/adk-operational-guardrails/tests -p adk_boundary.py -v
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  "$CHECK_ENV/bin/python" -B -I -m pytest \
  skills/adk-sql-agent-engineering/assets/test_adk_contract.py -q -p no:cacheprovider
```

The executed harness used a child environment without ambient provider keys,
disabled dotenv discovery, and pointed ADC/cloud configuration at absent test
paths. Relevant SDK fixtures blocked network access; the guardrails supplemental
run additionally blocked sockets/DNS before imports. In-memory OpenTelemetry
export must remain enabled for the tests that assert span contents. No Google
provider request, cloud deployment or credential mutation was performed.

| Executed gate | Passed | Skipped |
| --- | ---: | ---: |
| Repository validator/runner regressions | 35 | 0 |
| Eleven specialist helper suites, including optional SDK checks within those suites | 419 | 0 |
| Additional workflow runtime contracts | 8 | 0 |
| Additional guardrails Runner contracts | 4 | 0 |
| Additional SQL workflow/SDK serialisation contracts | 10 | 0 |
| **Unique total** | **476** | **0** |

All twelve packages reported zero structural errors or warnings; authored eval
cases passed schema/coverage checks, not actual activation evaluation.
`git diff --check` passed. Expected SDK warnings and injected failure logs remained.

The initial full gate stopped at the optimisation suite: missing greenlet caused
three database errors, and an overly broad harness telemetry-disable flag caused
eight local-span failures/errors. The dependency and harness were corrected;
the final full gate passed in 39.88 seconds. Both attempts are retained with
[structured results and versions](artifacts/updated-skills/evidence/repository-check-summary.json)
and [full final output](artifacts/updated-skills/evidence/repository-check.txt).
Failed attempts and earlier repeated suites are not added to the 476 total.

## Coding-agent trials

- **Claude Code 2.1.266 — safe API adapter:** the fresh `/safe-api-tool-calls`
  invocation discovered all twelve installed commands. Initial generation passed
  21 authored tests and five acceptance tests. Independent review then reproduced
  traceback source-literal leakage and unnecessarily restricted amount spelling.
  Two new acceptance regressions failed against that version. One resumed repair
  corrected both. Final independent execution passed **24 authored + 7 acceptance
  tests** on the exact **Python 3.11.4 / HTTPX 0.28.1** fixture pins. Agent-side
  checks used Python 3.12.9. [Prompts, final code, earlier defects and rerun guide](artifacts/updated-skills/api/README.md).
- **Codex CLI 0.153.4 — router and finite streaming:** `$adk-engineer` loaded the
  installed frontend, workflow and optimisation guidance. Codex adapted the
  finite-answer asset into the public adapter, preserving its API, unrelated
  settings and MIT notice. Independent execution passed **30 authored + 10
  acceptance tests** on **Python 3.11.4**. Tests cover provisional output,
  aggregate replacement, identity, late errors, thought/tool exclusion,
  cancellation and cleanup. [Task, generated code and rerun guide](artifacts/updated-skills/finite/README.md).

The final examples therefore pass **71 tests**, separately from the 476 repository
checks. The original 15 acceptance methods were outside the task projects;
two further API methods were added after review. The API's original five also
ship inside the installed skill, so this is not a concealed benchmark. No run
without skills was used to measure whether skills caused the improvement.

[Discovery evidence](artifacts/updated-skills/evidence/discovery.json) records the
actual skill reads. Claude used its existing configured model with session-only
medium effort; Codex inherited `gpt-6-astra` with ultra effort. Both retained their
normal permission controls. [File hashes](artifacts/updated-skills/evidence/source-hashes.json)
identify the installed source, including the final post-review guidance.

These trials exercise particular installed commands and generated code, not
comprehensive activation, comparative model quality or every skill's live/cloud
behavior. Coding-agent model calls are distinct from the offline ADK checks.
