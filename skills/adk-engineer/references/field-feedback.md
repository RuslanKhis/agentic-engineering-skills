# Field feedback

Read this when a skill's instruction did not match what happened in this
session, and again at the end of the session if a note was recorded. A field
note is a short, generalised record that the toolkit's maintainers can act on.
It is not a lesson about this project; keep project-specific lessons in the
project's own documents.

Nothing is sent by you or by the helper. The user may share a note by opening
a prefilled GitHub issue form and pressing Submit themselves; that click is
their consent. Never run `gh issue create`, post to an API, or open a pull
request unless the user explicitly asks in their own words.

## When to record

Record one note per divergence, after the fix or workaround is known, when:

- a documented API call, flag or import fails on the installed version
  (`wrong-api`);
- a documented step fails or cannot be followed as written (`failed-step`);
- the situation is real and common but the skill has no guidance for it
  (`missing-case`);
- the routing table sent the work to the wrong specialist and you redirected
  it (`misrouted`);
- the user overrides a skill default (`overridden-default`); offer to share it
  only when the helper reports the same quote recorded before at least once;
- a bundled helper script crashes or reports wrongly (`helper-error`).

Do not record the user's own mistakes, a project's unusual setup, a flaky
network, a preference stated once, or anything you could not tie to a line in
a skill package.

## Entry schema

The helper accepts only these keys and rejects any other:

| Key | Content |
| --- | --- |
| `skill` | The skill directory name, for example `adk-memory-architecture` |
| `skill_version` | Pass `--skill-md <installed SKILL.md>`; the helper reads `metadata.version` or uses a SHA-256 prefix |
| `host` | `claude-code`, `codex`, `antigravity`, `gemini-cli` or `other` |
| `model` | The model name you run as, if known |
| `kind` | One of the six kinds above, or `other` |
| `said` | File and line inside the skill package and a short quote: `references/memory-bank.md:88 "..."` |
| `happened` | Observed behaviour, the error's last line, installed `google-adk`, `google-genai` and Python versions |
| `repro` | The smallest steps or code that show it, with synthetic names (`acme-demo`, `example.com`) |
| `proposed` | What the skill should say instead, in prose; never a diff |
| `evidence` | `observed-once`, `reproduced-fresh` (a new session saw it too) or `reproduced-fixture` (a clean fixture and a check) |

## Privacy rules

Write the note as if a stranger will read it. Before calling the helper,
generalise: replace client, employer, product, person and project names with
synthetic ones; describe data by shape (`a table of claims`) not content; quote
only the error line, not logs; never include credentials, tokens, `.env`
values, transcripts or code over 15 lines. The helper then redacts on record
and again on preview: home and temporary paths, the project folder's name, the OS user name,
emails, service accounts, non-documentation URLs, IP addresses, GCP project
and bucket IDs, common secret formats and long random strings; it drops long
code blocks, HTML comments and invisible Unicode. Pass any client or product
name you know with `--redact <name>`. Redaction is a safety net, not
permission to paste raw material.

## Commands

`$SKILL_DIR` is this skill's directory. Run from the project root so its
folder name is redacted.

```bash
python3 $SKILL_DIR/scripts/field_notes.py add --skill <name> --skill-md <path to its SKILL.md> \
  --host <host> --model <model> --kind <kind> --said '<file:line "quote">' \
  --happened '<what happened>' --repro '<synthetic steps>' --proposed '<prose>' \
  --evidence observed-once [--redact <client name>]
python3 $SKILL_DIR/scripts/field_notes.py preview          # pending notes, exact text, redaction counts
python3 $SKILL_DIR/scripts/field_notes.py url --id <fn-id>  # prints the prefilled link; marks it offered
python3 $SKILL_DIR/scripts/field_notes.py mark --id <fn-id> --state declined   # or local-only
```

The log is `${AGENTIC_ENGINEERING_HOME:-~/.agentic-engineering}/field-notes/notes.jsonl`,
next to any private practice notes in the same home but kept apart from them.
When a sandbox blocks writing there, the helper saves to
`.agentic-field-notes/` in the project with its own `.gitignore` and prints a
notice; tell the user where the note went.

`AES_FIELD_NOTES=off` records nothing. `AES_FIELD_NOTES=quiet` records but you
do not offer sharing; mention once that notes exist. `AES_FIELD_NOTES_REDACT`
holds extra comma-separated terms to redact.

## Offer sharing once, at the end

Offer at most once per session, after the requested work is finished, and
only if this session recorded at least one note that is still pending. Do not interrupt the task to ask. Run `preview`, show
the user the exact text it prints, and ask one question with three answers:

1. Share: run `url --id <id>` for each note, give the user the link and offer
   to open it in their browser. They review the form, tick the privacy box and
   press Submit. When the helper says the URL is too long, it writes a Markdown
   report and prints the blank form link instead; tell the user to paste each
   section.
2. Keep it local: `mark --state local-only`. Nothing else happens.
3. Not now: `mark --state declined`; do not ask about these notes again.

When the session recorded no note, say nothing about field feedback, not
even that there is nothing to share. If the user declines or does not
answer, drop the subject. Never count an
earlier session's yes as consent for a new note.
