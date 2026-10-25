# Community field feedback — 25 October 2026

## Question

How can a coding agent using these skills record where real use diverged from
what a skill says, and let the user share it with the maintainers, without
sending anything the user has not read or exposing client data?

## Sources read on 25 October 2026

- **Claude Code `SendFeedback`** ([tools reference](https://code.claude.com/docs/en/tools-reference#sendfeedback-tool-behavior)).
  Drafts are saved under `~/.claude/feedback/drafts/` and "nothing reaches
  Anthropic until you send it". Drafted when a tool keeps failing, Claude
  cannot help, a mistake is noticed or the user asks. At most three cards a
  session by default; `feedbackDrafts: quiet` shows only a count; `off` or
  `CLAUDE_CODE_SEND_FEEDBACK=0` stops drafting. After a dismissed card it asks
  whether to turn drafting off and stops asking after two declines. Drafts
  expire after 30 days; the queue holds ten. Not offered in non-interactive
  runs or under zero data retention.
- **Next.js telemetry** ([nextjs.org/telemetry](https://nextjs.org/telemetry)).
  Does not collect "environment variables, file paths, contents of files,
  logs, or serialized JavaScript errors". `NEXT_TELEMETRY_DISABLED=1` opts
  out; `NEXT_TELEMETRY_DEBUG=1` prints the payload to stderr and sends nothing.
- **Homebrew analytics** ([docs.brew.sh/Analytics](https://docs.brew.sh/Analytics)).
  "Homebrew displays a notice before analytics are enabled so a user can opt
  out before sending an event"; `HOMEBREW_NO_ANALYTICS=1` or `brew analytics
  off`. No user identifier, IP address, build logs or configuration values.
- **GitHub issue forms** ([syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms),
  [form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema)).
  Forms live in `.github/ISSUE_TEMPLATE/`; `name`, `description` and `body`
  are required; `labels` is optional. An element `id` "can only use
  alpha-numeric characters, `-`, and `_`" and "is the canonical identifier
  for the field in URL query parameter prefills". `validations.required`
  "prevents form submission until element is completed. Only for public
  repositories." Checkbox options can each be `required`.
- **Prefilled issue URLs** ([creating an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue)).
  Query parameters `title`, `body`, `labels`, `milestone`, `assignees`,
  `projects` and `template`; "you can also use URL query parameters to fill
  custom text fields that you have defined in issue form templates". Each
  parameter needs the permission of the equivalent action (so `labels` from an
  outside user may be ignored or refused); a URL over the server limit returns
  `414 URI Too Long`. No number is documented.
- **`gh issue create`** ([manual](https://cli.github.com/manual/gh_issue_create)).
  `--body-file` reads the body from a file; `--web` opens the browser to
  create the issue.
- **Invariant Labs, GitHub MCP exploit** ([post, 26 May 2025](https://invariantlabs.ai/blog/mcp-github-vulnerability)).
  A malicious issue in a public repository hijacked an agent that was asked
  to review issues; it read private repositories and leaked them through a
  pull request in the public one. "Always Allow" removed the human check. The
  authors' mitigations: one repository per session and least privilege, plus
  monitoring. Issue text is untrusted input to the maintainer's own agent.

## Measured

An anonymous probe of `issues/new?template=field-report.yml&body=<n × "a">`
on 25 October 2026 (GET only, nothing created; redirects not followed):
302 to sign-in up to about 6,600 characters, server errors from about 7,100,
and `414` from about 8,240. The limit for a signed-in user was not measured.
The helper caps the prefilled URL at 6,000 encoded characters and otherwise
writes a Markdown report and prints the blank form link.

## Unverified

- Whether dropdown fields prefill from a query parameter (the docs say text
  fields; the helper passes the option label by `id` anyway, and the user
  selects it otherwise).
- Whether `labels` declared in the form apply to issues from users without
  triage permission, and what happens when the labels do not exist yet. The
  maintainer must create `field-report` and `needs-repro`.
- The exact URL limit for signed-in users.

## Decisions

- **Issues, not pull requests.** One user's evidence is a lead to reproduce,
  not a change; pull requests need forks and authentication; and untrusted
  text would flow into skill files.
- **Never auto-send.** The helper has no network code. The agent runs
  `gh issue create` only when the user explicitly asks; the user's own Submit
  click on the prefilled form is the consent.
- **Notice before send, like Homebrew; print not send, like Next.js debug.**
  `preview` prints the exact redacted text and counts before any link exists.
- **Fewer prompts than SendFeedback.** One offer per session, at the end, and
  only when the session recorded a note; `quiet` and `off` switches; declined
  notes are never offered again. No expiry is enforced; the user may delete
  the log.
- **Allowlisted schema.** Ten keys mirror the form; unknown keys are rejected,
  so a transcript or file cannot be smuggled in by a careless call.
- **Shared home, separate file.** `~/.agentic-engineering/field-notes/` sits
  beside the planned private practice profile but holds only the shareable,
  generalised subset; a sandbox fallback writes a self-ignoring
  `.agentic-field-notes/` in the project.
- **Maintainer triage prints no prose.** The triage table shows only values
  checked against fixed vocabularies and strict `file:line` matches, and
  flags injection-like text; reading happens without write tools.
