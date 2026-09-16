# Reproduce the implementation-depth evaluation

These fixtures are deliberately incomplete **evaluation inputs**, not starter
implementations. Use them to test an agent applying this skill. They require
no book, account, credentials or external service. The adapter case uses an
already installed HTTPX 0.28.1; the approval case uses Python 3.11's standard
library. Preserve the target's interpreter and pins.

1. Copy the skill and the selected `fixtures/adapter`, `fixtures/approval` or
   `fixtures/operations` directory into separate clean temporary directories.
   Preserve the original fixture. Give a fresh agent the installed skill path,
   the copied fixture and **only that fixture's `request.txt`** as the request.
   Permit the agent to read the skill's entry point/references/scripts and its
   own fixture; withhold this file, acceptance tests, other fixtures and previous
   evaluation reports. Use an existing interpreter and forbid network calls,
   credential inspection and external mutations.
2. Let the agent implement and validate the two code cases inside its copy.
   The operations case produces a recovery plan from supplied facts; it must
   not act on a real account. Save its actual response separately.
3. After completion, inspect the generated code before executing it. Select
   the trusted output through `SAFE_API_EVAL_PROJECT`, then run the independent
   acceptance tests from outside the fixture. `SKILL_DIR` is the installed
   skill path and `PYTHON` an existing compatible interpreter:

   ```bash
   SAFE_API_EVAL_PROJECT="$ADAPTER_OUTPUT" "$PYTHON" -B -m unittest discover \
     -s "$SKILL_DIR/tests/acceptance" -p test_adapter.py -v
   SAFE_API_EVAL_PROJECT="$APPROVAL_OUTPUT" "$PYTHON" -B -m unittest discover \
     -s "$SKILL_DIR/tests/acceptance" -p test_approval.py -v
   ```

   Set the two output paths to the completed temporary copies. These tests
   intentionally import that code; they are not a sandbox for untrusted code.
   They block accidental socket connections during test execution and use
   HTTPX `MockTransport` or local async doubles. An unset output path is an
   error rather than a silent skipped evaluation.
   Run each test command under the evaluation host's finite process timeout
   (30 seconds is ample for these local fixtures); a faulty generated loop must
   not leave the evaluator waiting indefinitely.
4. Review the operational response against these distinctions: effective child
   configuration versus IDE selection; CLI versus application ADC identity and
   quota; billing metadata denial versus billing disabled; enabled API versus
   successful model generation; old pending operation ownership versus a new
   project; occupied port ownership; local session/backup cleanup; stale index
   entries versus direct inventories; API-disabled versus empty; retained
   soft-deleted storage versus a zero-cost claim. It should propose ordered,
   reviewable steps and preserve unknowns, without executing cloud operations.
5. Record agent-produced tests separately from these independent assertions.
   Include failures and untested behaviour. To test repeat use, hash the
   completed fixture, issue the same request again, rerun relevant checks and
   inspect changes; a repeat should reuse an adequate existing implementation.

The shipped incomplete inputs are negative controls: the independent tests
must fail against them and pass only after a suitable repair. The assertions
check public outcomes and side effects, not a particular generated algorithm
or exact prose. The operational rubric is reviewed as meaning, not a keyword
test. This evaluation does not reproduce a live ADK confirmation dialog,
provider deduplication, concurrency, managed deployment or billing behaviour.

The earlier six-case creation evaluation remains in
[forward-evaluation.md](forward-evaluation.md). These retained fixtures add
repeatable coverage for the later response-validation, stale-approval and
operational-recovery guidance; they do not retrospectively reconstruct the
earlier disposable fixtures.
