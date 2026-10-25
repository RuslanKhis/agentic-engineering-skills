# Field feedback loop — 25 October 2026

Source note: [field feedback research](../research/field-feedback-2026-10-25.md).
Privacy page: [what is never sent](../field-feedback-privacy.md).

## Changed journeys

`adk-engineer` (records a field note when a specialist instruction fails, is
overridden or misroutes; offers sharing once at the end) and, in two lines,
`adk-system-designer` (records overridden scope-gate defaults). Maintainers
gain `scripts/triage_field_reports.py` and the
`.github/ISSUE_TEMPLATE/field-report.yml` form.

## Automated checks

`field_notes.py`: 18 tests (allowlist rejection, required fields, `off` and
`quiet`, sandbox fallback with its own `.gitignore`, repeat counter, preview
redaction of a raw note, prefilled URL by field `id` with no `labels`
parameter, the over-length fallback, state marking, version derivation, and
redaction of each secret format, identifier, URL class, path, long fence,
HTML comment and invisible character). Repository tests: 7 for triage and
form consistency (form skill list equals `skills/`, helper and triage labels
and choices equal the form's, a helper report parses back through triage,
hostile issue prose never printed and flagged). `check_repo.py` passes: 23
packages, 812 tests, 59 optional SDK checks skipped.

## Fresh-agent trials

Each trial ran a general-purpose subagent in its own directory under
`/private/tmp/claude-501/field-feedback-trials/`, with
`AGENTIC_ENGINEERING_HOME` pointed into it, a copy of the skill packages,
the absolute path of `adk-engineer/SKILL.md` and only a ticket request. The
user was unavailable; questions went in the final message.

**Trial 1** (`northwind-claims-agent`, "Stop the KeyError on
customer_tier", primary `adk-agent-instructions`). Drift was planted in the
copy: `SKILL.md:25` documented `--root` where the linter takes `--project`.
The ticket finished `verified_local`. The agent recorded two notes with
`--skill-md`, `--redact northwind --redact claims`: `failed-step` for the
planted flag (quoting the file:line, the exit-2 message and the script's
own line) and `missing-case` for the linter not following an `INSTRUCTION`
constant imported from `prompts.py` into `agent.py`. It ran `preview`,
showed the text and offered share, keep local or not now once, at the end.
Nothing was sent; no browser opened. Inspected notes: no client name, path
or the GCP project from `AGENTS.md`; reproductions use synthetic names
(`pkg`). Answering "share" was simulated afterwards by running `url` on a
copy of the log: a 2,002-character link with every field prefilled.

**Trial 2** (`fleet-helpdesk-agent`, "Add an instruction rendering test").
Intended as the no-divergence control. The ticket finished
`verified_local`, but the agent hit the same import-layout gap on the
unmodified skills and recorded one `missing-case` note (repro named
`acme_demo`), previewed it and offered once at the end. The note was
legitimate, so **the no-divergence path (no note, no offer) was not
exercised**.

**Trial 3** (`depot-helpdesk-agent`, "Make the depot placeholder safe for
office staff", primary `adk-agent-instructions`; the no-divergence control,
added the same day). The instruction string lives in `agent.py`, so the
linter sees it. The run was interrupted by a usage limit after Evidence was
written and resumed in the same agent with a neutral message. The agent made
`{depot?}` optional, passed the lint and existing tests, wrote the Runner
test as not run (no SDK) and set `in_progress`. It read the field-feedback
reference and recorded nothing: no `aes-home` or `.agentic-field-notes/`
was created, and it made no share offer and sent nothing. **Pass**, with one
defect: its final message still added "Field feedback: none recorded ...
nothing to share". Fixed: the reference now says to say nothing when no
note was recorded. That fix was not re-run.

## Friction log

1. Trial 2 did not test the control condition because the fixture's normal
   layout exposes a real gap. Covered by trial 3.
2. Some trial commands lacked the `AGENTIC_ENGINEERING_HOME` prefix (a trial
   harness instruction, not a skill defect); none of them called the helper.
3. `--redact claims` redacts an ordinary word everywhere. Not changed: over-
   redaction is visible in the preview and safe.
4. `/tmp` and `/private/tmp` paths were not redacted, which would have kept
   the macOS user id in a path under the trial directory. Fixed with a test
   while the trials ran (their copies predate it; their notes held no paths).

## Findings the loop surfaced (not fixed on this branch)

- `adk-agent-instructions`: the linter does not resolve an instruction
  constant imported from a sibling module, and `SKILL.md` step 5 does not
  say to lint it with `--prompt-file`. Reported independently by both
  trials; handed to the main session.
- The `--root` drift was planted and exists only in the trial copy.

## Limits

No issue was created; the form, its labels and field prefill were not tried
on GitHub. Dropdown prefill and the signed-in URL limit are unverified (see
the research note). Model selection of the hook across hosts other than
Claude Code was not tested.
