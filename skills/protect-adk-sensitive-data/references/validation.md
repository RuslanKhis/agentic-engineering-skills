# Validate the changed boundary

Select tests that cover the actual change. Preserve the target's runner and
test framework. Mock external providers and the model for ordinary tests; do
not confuse local protection doubles with a fully offline application.

## Regression matrix

| Boundary changed | Minimum meaningful checks |
| --- | --- |
| SDP | Denied finding short-circuits; empty/truncated and malformed results withhold; partial transformation failure withholds; safe transformed value alone reaches downstream sinks; timeout/cancellation and length bounds |
| Armor mapping | Allow, complete permitted transform, mixed blocking match, unknown/no verdict, missing required filter, partial/skipped execution, API failure and output block-only |
| Gateway | Auth precedes paid calls; oversized/escaped body and slow reads bounded; no raw canary in model request, session or logs; foreign/incompatible-policy sessions rejected |
| Tool arguments | Unknown tool/extra authority fields block; strict validation before and after protection; actual ADK saves protected call arguments; next plugin still runs; side effect sees only safe data |
| Tool results | Projection drops private fields; validate before paid screening and after replacement; structural fields reject free text; wrong requested/returned reference, oversized note/nested collection and invalid enum/date reject |
| Authorisation | Principal cannot access another user's resource/contact or combine an owned resource with a foreign destination |
| Release | Safe final answer passes; blocked/error event plus final text withholds; thoughts/tool payloads absent; sensitive text split across chunks never leaks a prefix; JSON and SSE agree; iterator closes |
| Lifecycle | Repeated requests reuse intended clients; shutdown closes each owned resource despite another close failure; unused lazy client not opened at shutdown |
| Cloud scripts, if generated | Help/dry-run no mutation; repeated setup no duplicate; same-name foreign resource refused; partial failure preserves ownership; repeated cleanup ignores foreign resources and verifies owned absence |

Use synthetic canaries with explicit sink assertions. A test that merely checks
the response says “blocked” can miss leaked history, logs or completed writes.
Run real pinned ADK callbacks through its runner with a scripted model when the
change depends on callback timing. For tool side effects, use an injected sink
whose call count and arguments are asserted. Denied/incomplete cases must leave
that count zero. Keep a log-capture assertion and forbid network calls in the
offline harness. Do not install a service emulator merely to satisfy a narrow
controller test.

## Bundled resource checks

Using the selected existing Python interpreter and resolved skill path:

```sh
python /path/to/skill/scripts/inspect_project.py --help
python /path/to/skill/scripts/inspect_project.py /path/to/package --dry-run
python /path/to/skill/scripts/inspect_project.py /path/to/package
python -m unittest discover -s /path/to/skill/tests -v
```

The inspector is read-only in both modes. An exit-zero inventory is not a
compatibility pass; review any unresolved metadata. The asset is a library, not
a command-line script, so `--help`/`--dry-run` do not apply to it. Its tests use
only the standard library and fake provider functions. The module requires
Python 3.11+ for its timeout API; only Python 3.11.4 was exercised here.

For a skill edit, run the available Agent Skills structural validator, parse the
frontmatter/UI YAML, check local links and unfinished markers, and run syntax /
format checks supported by the existing toolchain. Copy the complete skill to a
temporary workspace without the companion repository and repeat these checks.
No manuscript, original source path or machine-local import may be required.

## Forward-test the skill's instructions

Use fresh fixtures and record actual actions/diffs, not just a hypothetical
answer. Give an independent agent only the skill, fixture and realistic request.
Do not supply an expected answer. Review its work against the request afterwards.

Exercise greenfield input protection; a customised project with partial
protection; missing credentials/prerequisites; a cloud change requiring a
concrete approval plan; a near-miss such as Cloud Armor WAF configuration; and
repeat invocation on the already changed project. Check preservation of package
pins and domain contracts, safe refusal of unapproved cloud changes, no
credential invention, no activation for unrelated work, and no duplicate edits.
Only claim coding-agent environments in which this behavioural test was run.

## Evidence labels and completion

- **Fresh offline:** commands and result counts from this task, with doubles and
  limitations named. Syntax checks are not integration tests.
- **Fresh live:** new approved calls with exact backend/versions/target, bounded
  call/time/cost envelope and cleanup evidence. Omit this label if none ran.
- **Historical live:** dated companion evidence, scoped to its actual workflow.
  It does not validate today's target, new asset or a modified provider adapter.
- **Production guidance:** requirements/adaptations not yet established by the
  target's tests, including identity, durability, residency and detector accuracy.

Report skipped/inapplicable checks and why. An implementation is ready for its
stated scope only when the changed invariants have evidence and pending cloud
or production work is explicit. See [compatibility.md](compatibility.md) for
provenance and [skill-validation.md](skill-validation.md) for this package's
recorded creation checks.
