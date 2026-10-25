# Field feedback and privacy

*What a field note holds, where it stays, and what never leaves your machine.*

When a skill's instruction does not match what happens in your project (an API
that changed, a step that fails, a specialist chosen wrongly, a default you
always override), `adk-engineer` can record a short, generalised **field
note**. At the end of the session it may ask once whether you want to share
it. Sharing means opening a GitHub issue form in your browser with the note
already filled in; you read it, tick the privacy box and press Submit, or
close the tab. Nothing is sent by the coding agent or by the helper script.

## Where notes live

`${AGENTIC_ENGINEERING_HOME:-~/.agentic-engineering}/field-notes/notes.jsonl`
on your machine. When a sandbox blocks writing there, the note goes to
`.agentic-field-notes/` in the project, which ignores itself in git, and the
agent tells you so. Delete either file whenever you like.

## Switches

| Setting | Effect |
| --- | --- |
| `AES_FIELD_NOTES=off` | Nothing is recorded |
| `AES_FIELD_NOTES=quiet` | Notes are recorded; the agent does not ask to share |
| `AES_FIELD_NOTES_REDACT=Name,Other` | Extra terms replaced with `<redacted>` |
| Answer "keep it local" or "not now" | The note stays on your machine and is not offered again |

## What is never sent

No data leaves your machine unless you press Submit on GitHub yourself, and
then only the form's text, which you have read. The note format has no field
for, and the helper's redaction removes or replaces:

- source code beyond a short reproduction (code blocks over 15 lines are dropped);
- file contents, logs, transcripts, prompts, model outputs or session data;
- client, employer, product or person names (write synthetic names; the project
  folder's name and your OS user name are replaced automatically, and the agent
  passes any client name it knows);
- home and temporary paths (`/Users/...`, `/home/...`, `C:\Users\...`, `/tmp/...`), except
  the part after `skills/` or `site-packages/`;
- email addresses and service-account emails;
- URLs other than public documentation (Google, ADK, PyPI, GitHub docs and this
  repository), and any URL with a query string;
- IP addresses, GCP project IDs and bucket names;
- credentials: private keys, AWS and Google API keys, OAuth and JSON Web
  Tokens, GitHub and Slack tokens, `password=`/`token=` values and other long
  random strings;
- HTML comments and invisible or direction-changing Unicode characters.

The issue URL itself passes through your browser to GitHub when you open it,
so it carries only the redacted text you saw in the preview. No telemetry,
analytics or identifier is collected; there is no background upload and no
pull request is ever opened for you.

Redaction is pattern-based and can miss things. Read the preview; the form's
required privacy checkbox is there for that reason.

## How maintainers handle reports

Reports are read as data, in a session without write tools or access to
private repositories, because issue text is untrusted input to the
maintainer's own coding agent. A report changes a skill only after it is
reproduced in a clean fixture; the accepted case is then added to the
evaluation cases with the issue number as its source. See
[CONTRIBUTING](../CONTRIBUTING.md#triage-field-reports).
