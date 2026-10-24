# CaMeL alignment — 24 October 2026

Source note: [comparison](../research/camel-comparison-2026-10-24.md).

## Changed journey

`adk-agent-security`, injection-resistant structure: the capability gate
and plan-then-execute.

## Fresh-agent trial

Run on 25 October 2026. A fresh agent with only the skill packages built,
offline, CaMeL-style protection for a synthetic ADK 2.12 mail agent
(`search_mail`, `read_email`, `send_email`, `delete_file` and a newly added
`archive_thread`) that a reviewer said an injected email could steer. It
installed google-adk 2.12.0 and pytest from PyPI; no CaMeL code and no
remote model were used.

Result: a planner that sees only the user's turn and has no tools; an
application step that keeps a planned action only when its target appears
in the user's message and freezes the plan once per invocation; a
deny-by-default gate plugin with one-use plan steps, provenance and readers
tags, a hold for mailbox text sent outside its readers, and query-bound
references for many-target archives; confirmation on `delete_file`; and
identity from `tool_context.user_id`. It declined CaMeL's interpreter and a
quarantined reader in front of `read_email` (it would change what users
see), and said how close the result gets: actions and targets are fixed
before any email is read; data-flow tags follow strings and a paraphrase
passes; the executor can still skip or misreport a step.

`pytest`: **21 passed, 0 failed** (17 scripted-model Runner tests with the
network blocked, 4 policy tests), including a control in which the same
attacks without the gate send mail to the attacker and archive the thread.
Two deliberate breaks (no one-use reservation, re-freezing on resume) failed
4 and 2 tests. The security inventory's `write_tool_without_gate` went from
2 to 0; `trifecta_present` stayed at 1.

Ease: 3 of 5.

## Frictions and fixes (same day)

1. On 2.12.0 an agent's `before_agent_callback` runs again when a
   confirmation resumes the invocation, with the same invocation id and the
   confirmation as `user_content`; re-freezing refused the confirmed delete.
   Fixed: freeze once per invocation id, stated as observed in this trial.
2. `SequentialAgent` is deprecated on 2.12.0 in favour of `Workflow`
   (checked in the installed source). Fixed: the pattern table says so and
   routes the choice to `adk-workflow-design`.
3. The security inspector did not treat `archive_thread` as a write tool.
   Fixed, with a test. Plugins showing as dynamic is unchanged; when runner
   plugins are present the helper already asks the reviewer to confirm one
   gates the tool.
4. `trifecta_present` remains after the fix and the skill did not say
   whether that is acceptable. Fixed: the frozen plan is a mitigation the
   owner accepts, not a removed leg (`SKILL.md` and the gate rules).
5. Whether the planner's draft counts as model-written policy. Fixed: it is
   model output; bind each step's target to the user's words before
   freezing.
6. A held confirmation ends the invocation. Fixed: stated, with the pointer
   to the confirmation wire shape.
7. No recipe for many-target steps. Fixed: bind to the user's query and
   accept only ids it returned.
8. The sample's substring taint match blocks legitimate arguments when a
   tainted value is short. Fixed: a minimum length, exact match below it.
9. The confirmation wire protocol is in another skill. Fixed by the pointer
   in 6.

## Limits

No live model ran; CaMeL's own results were not reproduced.
