# Codex CLI smoke test: safe API tool calls

Tested on 15 September 2026 against repository commit `7dc536afbcfa21a94df5f1a62071eee719a7f344`.

## Scope

Installed **only** `safe-api-tool-calls` into a temporary project, invoked it by name in a fresh Codex CLI session, and asked it to repair a small Python refund tool. The project supplied a deterministic in-memory provider and an existing, deliberately broken tool. No book files were supplied to the coding session.

The provider simulates a refund being committed before its reply is lost. Its contract binds an idempotency key to the submitted amount and permits replay without another refund. A trusted upstream caller supplies the operation ID and explicit approval. The tool must validate inputs, preserve operation identity across retries and later invocations, stop after a bounded number of attempts, and report an unresolved outcome honestly.

This tests an ordinary Python function and mock client. It does **not** exercise an ADK tool wrapper, ADK confirmation, real payment service, database, deployment, network deadline, or durable recovery after a process restart.

## Environment and invocation

| Component | Version / setting |
| --- | --- |
| Codex CLI | `0.153.4` |
| Skills CLI | `1.5.24`, existing cached package |
| Node.js | `24.15.0` |
| Python | `3.11.4`, existing interpreter |
| pytest | `8.4.2` |
| Codex model | Existing configured default; no model override |
| Child command sandbox | `workspace-write` |

The existing interpreter also contained `google-adk==2.8.0` and `google-genai==2.19.0`; this fixture did not import or exercise either package. No dependencies were installed or changed.

Commands below use placeholders for machine-specific executable and directory paths:

```sh
XDG_STATE_HOME="$RUN_DIR/state" "$NODE" "$CACHED_SKILLS_CLI" add "$REPOSITORY" \
  --skill safe-api-tool-calls -a codex -y

"$CODEX" exec --ephemeral --json --sandbox workspace-write \
  --skip-git-repo-check -C "$RUN_DIR/project" \
  -o "$RUN_DIR/final.txt" - < "$RUN_DIR/prompt.txt" \
  > "$RUN_DIR/transcript.jsonl" 2> "$RUN_DIR/stderr.txt"
```

The installer ran from the temporary project and copied the standalone package to `.agents/skills/safe-api-tool-calls`. The transcript records Codex reading its `SKILL.md` and compatibility, writes, deadlines, validation and inspection references, then running its inspection helper. The `adk-engineer` router was not installed in this project.

The first CLI launch was blocked by the outer filesystem sandbox when initializing Codex's existing local state. A scoped, approved retry allowed the CLI to initialize and connect using the existing account. Its generated shell commands retained `workspace-write`; no sandbox or approval bypass flags were used. The model connection was live, while all refund behavior was simulated locally.

Exact prompt:

```text
$safe-api-tool-calls Fix this tool so a lost refund reply cannot cause a duplicate, retries are bounded, and unapproved requests never reach provider; implement and test locally. Read README.md for the public interface and provider contract. Use the installed standalone skill in this project. Follow the fixture scope and preserve provider.py. Run local tests with the existing interpreter specified in README.md. Do not access external services, deploy or install dependencies.
```

## Results

**Passed in one generation session; no corrective follow-up was needed.** Codex changed `refund_tool.py`, generated `test_refund_tool.py`, and ran its **55 tests successfully**. The provider and installed skill files remained unchanged, verified by SHA-256.

Acceptance tests were written before generation and kept outside the coding project's directory. The intentionally broken implementation failed **14 of 16** cases. After the CLI finished, the same acceptance suite passed **16 of 16** cases:

| Independent acceptance check | Result |
| --- | --- |
| Unapproved or invalid approval values make zero provider calls | Passed, 4 cases |
| Invalid money values make zero provider calls | Passed, 5 cases |
| Lost-reply retry and later invocation share one operation and one refund effect | Passed |
| Transient failure respects the configured attempt limit | Passed |
| Permanent rejection is not retried | Passed |
| Repeated lost replies return `unknown`, with one refund effect | Passed |
| A later rejection does not erase a lost reply's uncertainty within the same invocation | Passed |
| A changed amount for the same operation cannot create a second refund | Passed |
| Separate operations remain distinct | Passed |

The preserved source and both test suites were then run from the archived artifact directory: **71 passed in 0.08s**. These are parametrized test cases, with overlap between the generated and independent suites; they are not 71 different production integrations.

Review the [generated refund tool](artifacts/api/refund_tool.py), [generated tests](artifacts/api/test_refund_tool.py), [independent acceptance tests](artifacts/api/test_acceptance.py), and [fixture with reproduction instructions](artifacts/api/README.md). These files are test evidence, not a production payment integration.

## Evidence and limits

The [archived artifact directory](artifacts/api/) preserves the initial broken tool, exact prompt, mock provider, generated source and tests, independent acceptance tests and sanitized fixture contract. The temporary run also retains hashes, test outputs and the raw JSONL transcript. Machine-specific paths and account/session details are omitted from the archived artifacts and this public report.

Installed `SKILL.md` SHA-256: `893f014bf0d20b89205f446de774c3496be2efd53a31b227cf62cf1a0d47b4f5`.

This single smoke test can establish that direct skill invocation produced working code for the supplied contract. It cannot establish that the skill improves results compared with an unskilled baseline, works for every provider, or supplies production authorization, provider durability or real ADK integration.
