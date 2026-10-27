# Helper conventions

Every script under `skills/*/scripts/` that has a command line follows these
rules, so that a command copied from one skill means the same thing in another.
`tests/test_helper_conventions.py` checks them on every `scripts/check_repo.py`
run; `tests/helper_conventions_allowlist.json` holds the few justified
exceptions, each with its reason.

## Target directory: `--project DIR`

- The directory a helper works on is always `--project DIR`. Keep it required
  for inspectors; give it a default of `.` only where the helper already worked
  on the current directory (`check_tickets.py`, `field_notes.py`, `profile.py`).
- Never take the target directory as a positional argument. Positional
  arguments are kept for the documents a checker reads (drafts, an assessment,
  a trace), and each one is listed in the allowlist.
- A Google Cloud project ID is `--gcp-project ID`. `--project` never means a
  GCP project.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean: the check passed, or the inspection completed. Findings a helper only reports (signals, review prompts) do not change it. |
| 1 | Findings or a failed check: a gate the caller asked for did not pass (`--fail-on`, `--require-baseline`, `--expect-adk`, `--compare`), or a checker found errors. |
| 2 | Usage error: bad arguments (argparse's own code), or a named input or project directory that is missing, unreadable or malformed. |
| 3 | Incomplete: the helper could not inspect everything (a limit was reached, a file could not be read or parsed, a source was unreachable), so a clean result is not proven. |

When both 1 and 3 apply, a helper returns 1 if the failure stands whatever the
unread part holds, and 3 if the unread part could change the answer; where
that is not obvious, its `--help` says which wins. Codes above 3 are not used, except `profile.py`'s
documented binding states.

## Output

- The result goes to stdout, as JSON unless the helper has a documented text
  or CSV mode (`--json`, `--format`).
- Diagnostics, warnings and deprecation notes go to stderr, and never echo
  secret values or file contents.

## `--dry-run`

`--dry-run` exists only where it changes what the helper does: it skips a
write (`events_to_eval_set.py`, `apply_brand.py`), reads less
(`inspect_project.py` in memory, SQL, workflow and protect), or stops before a
verdict (`check_eval_results.py`, `check_results.py`). A helper that only reads
keeps an old `--dry-run` as a hidden no-op that says so on stderr.

## Old spellings

A flag that is renamed keeps working as a hidden, deprecated alias: it does the
same thing and prints one line to stderr, such as
`inspect_project.py: --root is deprecated; use --project`. The one exception is
a spelling whose meaning changed: `deploy-adk-on-google-cloud`'s
`--project` used to take a GCP project ID, so a `--project` value that is not
an existing directory, or `--root DIR` combined with `--project`, exits 2 and
says to pass the ID with `--gcp-project`.

## Documenting a helper

Show a helper command as

```bash
python "$SKILL_DIR/scripts/<name>.py" --project . [options]
```

with `$SKILL_DIR` resolved to the directory holding that skill's `SKILL.md`
(`python3` is fine where the skill allows Python 3.9). Use only current flags.
A dated record of past runs (`validation-results.md`, `skill-validation.md`,
`verification-record.md`) keeps the commands that were run at the time.
