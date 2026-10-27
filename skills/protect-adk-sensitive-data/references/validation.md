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
Exact canaries miss PII the model invents or reformats; a second,
value-independent check is Microsoft Presidio's analyzer run offline over every
captured sink (model request, session events, logs, tool arguments). It is a
test dependency only, added with the project's agreement, never a production
one. Pin `presidio-analyzer` (2.2.364 on PyPI on 2026-10-24, MIT, Python 3.10 to
3.14); it still installs spaCy (3.8.16 resolved on 2026-10-25) whichever engine
you choose. Construct it with `NoOpNlpEngine`, a
`RecognizerRegistry(supported_languages=["en"])` and
`load_predefined_recognizers(nlp_engine=...)`, or with a pre-installed pinned
spaCy model wheel: the default engine calls `spacy.cli.download` for
`en_core_web_lg` at run time, which fails in a no-egress harness or, worse,
succeeds in one that should have had none. The pattern-only route still reaches
the network: the email recognizer validates matches with `tldextract`, which
fetches the Public Suffix List on first use, so set
`TLDEXTRACT_PUBLIC_SUFFIX_LIST_URLS` to an empty string before importing
Presidio and it uses its bundled snapshot (tldextract 5.4.0). That validation
also rejects reserved domains, so canary emails under `.test`, `.invalid` or
`.internal`, and internal-only domains, are invisible to Presidio; leave them to
the exact-canary check, or use `example.com`. Without a spaCy model there is no
person-name detection, phone numbers without context words score 0.4 (below a
0.5 threshold), and some well-formed but invalid numbers are rejected by design,
so set the threshold deliberately and keep names in the canary list. No
recognizer ships for credentials, so add a `PatternRecognizer` per secret format
you hold. Capture the sinks by wrapping `BaseLlm.generate_content_async`, the
session service's `append_event` (on the class you use: `InMemorySessionService`
calls its parent, so wrapping both records events twice), `BaseTool.run_async`
and a logging handler, and report location, field and entity type, never the
matched value; pytest's "Captured log" section prints log records on failure, so
run with `--show-capture=no` or the report itself leaks. Prove it bites with a
deliberate leak per sink that must fail. It is a test oracle only: a Presidio
hit or miss says nothing about Sensitive Data Protection's accuracy, it does not
replace the SDP orchestration tests (block on a forbidden finding, hold on
empty, truncated or malformed results, timeouts), and Presidio never sits in the
production path (microsoft/presidio commit 4f0e236,
`presidio-analyzer/presidio_analyzer/nlp_engine/spacy_nlp_engine.py`,
`conf/no_op.yaml` and `predefined_recognizers/generic/email_recognizer.py`, read
2026-10-24; tldextract and the scores read in the installed packages and
exercised offline on 2026-10-25).
Run real pinned ADK callbacks through its runner with a scripted model when the
change depends on callback timing. For tool side effects, use an injected sink
whose call count and arguments are asserted. Denied/incomplete cases must leave
that count zero. Keep a log-capture assertion and forbid network calls in the
offline harness. Do not install a service emulator merely to satisfy a narrow
controller test.

## Bundled resource checks

Using the selected existing Python interpreter and resolved skill path:

```sh
python "$SKILL_DIR/scripts/inspect_project.py" --help
python "$SKILL_DIR/scripts/inspect_project.py" --project /path/to/package --dry-run
python "$SKILL_DIR/scripts/inspect_project.py" --project /path/to/package
python -B -m unittest discover -s "$SKILL_DIR/tests" -v
```

The inspector is read-only in both modes; exit 3 means some metadata could not be
read. An exit-zero inventory is not a compatibility pass; review any unresolved metadata. Both assets are libraries,
so `--help`/`--dry-run` do not apply. Inspector/controller tests use the standard
library and fake provider functions. The optional regional adapter's tests use
the target's existing `google-cloud-dlp` package for real message types while
replacing client construction/transport; the SDK-dependent group is skipped
when it is absent. Report those skips as unverified SDK integration, not a pass.
Do not install/change dependencies merely to eliminate a skip. Python 3.11+ is
required; only Python 3.11.4 was exercised here.

When adapting the SDK asset, retain both files in one package and verify the
regional endpoint, full template names, absence of inline overrides, actual SDK
response shapes, queue/RPC/host deadlines, cancellation, client reuse and close.
Mocked provider results prove orchestration only. Its stricter response-presence
checks still need a separately approved benign/PII provider canary before live
activation; see [sdp.md](sdp.md).

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
For the deeper implementation references, add focused trials of real regional
SDK adoption, native-plugin bounds and error logging, and operational diagnosis
with tenant-specific policy. Use actual installed SDK types/plugin execution
where those contracts matter, while replacing all provider transports.

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
dated creation and subsequent recheck results.
