# Codex CLI smoke test: persistent language preferences

**Result:** a real `$adk-engineer` invocation selected the memory specialist,
implemented the feature, and passed **54 generated tests plus 18 independent
acceptance tests**. The preserved final snapshot passes all **72 tests** together.

This was a local code-generation check on **15 September 2026**, using an
isolated temporary project. Codex contacted its configured service to generate
code. The generated application tests used SQLite and installed ADK types;
they did not invoke a Google model or deploy cloud resources.

## What was installed and invoked

All twelve skills were installed from the local repository using the cached
**skills CLI 1.5.24**, with the arguments below. Paths are represented by
variables to avoid publishing workstation-specific locations:

```bash
# Run from the isolated fixture directory.
XDG_STATE_HOME="$TEST_ROOT/state" "$NODE" "$SKILLS_CLI" \
  add "$REPO" --skill '*' -a codex -y
```

The installer copied the packages into the fixture's `.agents/skills/`.
The installed router and memory instruction files matched the repository bytes.
Their SHA-256 hashes were:

| Installed instruction | SHA-256 |
| --- | --- |
| `adk-engineer/SKILL.md` | `5d690853e7f3f4b8b789c26ca51f9fade617677fd095d338aaa56378e03d7020` |
| `adk-memory-architecture/SKILL.md` | `37f694261f90c765b2a28f2542322aa27ceaf1da082df40c9bb568fb3f48bf8e` |

The [exact prompt](artifacts/memory/prompt.txt) was supplied through stdin,
preserving the literal `$adk-engineer` mention:

```text
$adk-engineer Add a preferred-language setting to this ADK assistant so it survives new conversations and process restarts. Keep two users isolated and let each user forget their setting. Keep SQLite and the existing interfaces in README.md. Implement the feature and run offline tests using the documented interpreter. Stay within this fixture; do not edit installed skills, deploy anything, call Google models, access credentials, or change the preinstalled environment. Tell me what you changed and actually tested.
```

```bash
"$CODEX" exec --ephemeral --json --sandbox workspace-write \
  --skip-git-repo-check -C "$TEST_ROOT/project" \
  -o "$TEST_ROOT/final.txt" - \
  < "$TEST_ROOT/prompt.txt" \
  > "$TEST_ROOT/transcript.jsonl" 2> "$TEST_ROOT/stderr.log"
```

This uses Codex's documented [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
and [explicit skill invocation](https://learn.chatgpt.com/docs/build-skills).
No model, authentication, home directory or user configuration override was used.
The first launch stopped before generation because the outer desktop sandbox
blocked CLI app-server initialization. An approved retry let the CLI initialize
and contact its configured service; its generated commands retained the
`workspace-write` sandbox. That run completed with exit code **0** in about
seven minutes, without a corrective follow-up prompt.

## Evidence that routing worked

The JSONL transcript recorded:

1. An opening message applying `adk-engineer` and `adk-memory-architecture`.
2. A successful command reading `.agents/skills/adk-memory-architecture/SKILL.md`.
3. A successful command reading `.agents/skills/adk-engineer/SKILL.md`.
4. Inspection of the fixture, dependency versions and installed ADK instruction
   APIs, followed by source changes and executed tests.

The prompt did not name the memory specialist. Codex chose a deterministic
profile for an exact user-controlled language setting, consistent with the
specialist's guidance. It retained SQLite and the existing interfaces.

## Review the input and generated code

The compact [artifact snapshot](artifacts/memory/) contains:

- [Original fixture contract](artifacts/memory/original/README.md),
  [storage stubs](artifacts/memory/original/profile_store.py) and
  [initial agent](artifacts/memory/original/agent.py).
- [Generated SQLite store](artifacts/memory/generated/profile_store.py) and
  [ADK agent factory](artifacts/memory/generated/agent.py).
- [Generated storage tests](artifacts/memory/generated/tests/test_profile_store.py),
  [ADK tests](artifacts/memory/generated/tests/test_agent.py) and
  [offline test guards](artifacts/memory/generated/tests/conftest.py).
- Independently authored [acceptance tests](artifacts/memory/acceptance/test_acceptance.py)
  and [ADK boundary checks](artifacts/memory/acceptance/test_adk_boundary.py).
- The [pinned manifest](artifacts/memory/generated/pyproject.toml) and exact prompt.

Generated Python files were preserved byte-for-byte. Only the interpreter path
in the fixture README files was replaced with `$PYTHON`. Installed skill copies,
raw transcripts, caches, databases and virtual environments are excluded from
the public snapshot.

The generated instruction callable reads the latest setting each time ADK
resolves the instructions:

```python
def instruction(context: ReadonlyContext) -> str:
    # Identity comes only from the server-owned scope, never session state.
    language = store.get_preferred_language(scope)
    text = "Answer clearly and helpfully."
    if language is not None:
        text += f" Answer in {language}."
    return text
```

## What passed

The independent tests were kept outside the CLI's project. They tested the
documented public interfaces, without directing Codex to a specialist or
showing it the acceptance test implementation. All **18 failed** against the
original incomplete fixture and all **18 passed** against generated code.

| Check | Observed result |
| --- | --- |
| Skills installation | All 12 packages installed locally |
| Router and memory instructions | Both installed files read successfully |
| Generated regression suite | 54 passed; CLI ran it again after its final edits |
| Independent acceptance | 18 passed |
| Preserved snapshot: both suites together | 72 passed in 1.38 seconds |
| Google model inference and cloud deployment | Not run |

Coverage includes preference replacement; explicit consent; invalid language
and identity rejection without mutation; exact user and application isolation;
SQL parameterization; independent Python processes; new ADK conversations;
changes and forgetting on existing agent instances; and propagated storage
failures. ADK checks use actual `LlmAgent`, `ReadonlyContext` and
`canonical_instruction`. The generated suite blocks network connections,
Google credential discovery/loading and Google Gen AI client construction.

The test environment was **Python 3.11.4**, **google-adk 2.8.0**,
**google-genai 2.19.0**, and **pytest 8.4.2**. The CLI was **0.153.4**;
its existing configuration selected **gpt-6-astra** with **ultra** reasoning.
Pytest reported one upstream ADK `BaseAgentConfig` deprecation warning.

To run the preserved final snapshot, set `PYTHON` to an interpreter containing
the pinned dependencies, then run from the repository root:

```bash
cd docs/testing/artifacts/memory/generated
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
  "$PYTHON" -B -m pytest tests ../acceptance -q -p no:cacheprovider
```

## Limits

This proves that this installed entry skill routed a concrete memory request
and generated functioning local code for the stated fixture. It does not test
every specialist, Claude Code invocation, probabilistic answer quality, a live
Google model, production authentication, managed memory services or deployment.
The fixture supplies trusted identity through an application-owned factory;
it does not implement an authentication server. The retained generated code is
testing evidence, not a production application template.
