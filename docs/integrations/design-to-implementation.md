# Continue from system design to implementation

`adk-system-designer` produces a design and a plan that another coding-agent
session can use. The design explains decisions. The plan maps them to ADK and
application components, GCP responsibilities, useful goals, relevant skills and
observable acceptance checks.

For the complete sequence of copyable prompts, follow the README's
[design → tickets → implementation walkthrough](../../README.md#from-design-to-working-tickets).
This guide explains which document owns what, how a ticket carries the ADK
guidance, and how to resume the work.

## Ask for the handoff

In Claude Code:

```text
/adk-system-designer Design a support assistant using our existing React,
OIDC login and PostgreSQL with Google ADK on GCP. We need an explicitly saved
language preference and streamed replies. Write the architecture and a plan
with goal IDs, dependencies, concrete integration points, skills and acceptance
checks. Identify the first goal we can implement locally. No deployment yet.
```

In Codex, use `$adk-system-designer`. In Google clients, ask to use the skill
by name. The default document locations are `docs/architecture/<topic>.md` and
`docs/plans/<topic>.md`; existing project conventions take precedence.

A goal might be **“A signed-in user saves, uses and forgets a language preference
across conversations.”** Its implementation route includes an owner-scoped profile
API/store, loading the preference at the agent invocation boundary and the UI
action. `adk-memory-architecture` leads; auth or frontend guidance applies where
those boundaries change. Checks cover a later session, restart, another user's
access and forgetting. Exact file paths and SDK calls come from the target project
or remain labelled proposals pending compatibility checks.

The [plan template](../../skills/adk-system-designer/assets/implementation-plan-template.md)
shows the goal fields and resumption information. A design-ready goal does not
grant new cloud or tracker permissions. Tests remain planned until run.

## Continue directly

Use the goal ID and actual document paths from the generated plan:

```text
/adk-engineer Continue G01 from docs/plans/support-assistant.md.
Read docs/architecture/support-assistant.md and preserve accepted decisions.
Use the primary skill named in G01. Implement the local slice and its acceptance
checks, then update the plan with what changed, actual results and remaining
blockers. Keep cloud work outside this step.
```

Use `$adk-engineer` in Codex. This route works with this toolkit alone.

## Continue with Matt Pocock's workflows

Read the installed workflow instructions and project setup first. These are
suggested continuations using ordinary Markdown, not an automatic importer.
Pass the actual architecture and plan paths explicitly, including when starting
a fresh conversation. Run each stage as a separate chat request and review its
output before continuing. The README shows [installation, local tracker setup
and every handoff command](../../README.md#from-design-to-working-tickets).

| State of the work | Next workflow | What to carry forward |
| --- | --- | --- |
| Large effort with significant unresolved decisions | `wayfinder` | Destination, accepted decisions, precise questions, unknowns, blockers and relevant skills |
| Agreed design requiring several implementation sessions | `to-spec` → `to-tickets` → `implement` | Design, goal outcomes, dependencies, testing decisions and acceptance cases |
| Small, settled implementation goal | `implement`, or the relevant ADK specialist with `tdd` when requested | The selected goal and its agreed public test boundaries |

Wayfinder normally resolves **decision questions**. Its map can point to the
architecture and name relevant ADK skills in its Notes. Ready build goals remain
the implementation handoff; large settled maps feed the specification workflow.
[Wayfinder](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md),
[workflow router](https://github.com/mattpocock/skills/blob/main/skills/engineering/ask-matt/SKILL.md).

For example, after installing and configuring Matt's collection:

```text
/wayfinder Use docs/architecture/support-assistant.md and
docs/plans/support-assistant.md as inputs for the remaining design decisions.
Use support-assistant-design as the effort name in our local Markdown tracker.
Preserve accepted decisions, link their canonical documents and carry the
relevant ADK skills into the map. Keep ready build goals for the later handoff.
```

The first invocation charts the map. To resume it in a later session, use the
actual returned map path, for example:

```text
/wayfinder Continue .scratch/support-assistant-design/map.md.
```

For a settled design, supply those same documents to `to-spec`, then use the
project's configured ticket workflow. Include the resolved map if one was used.
Resolve decisions that block the selected goals before creating ready build
tickets; unrelated future questions can remain open. Adapt the material to its format:
`to-spec` describes module/interface decisions, while concrete file/API inspection
notes can remain linked in the handoff. `to-tickets` produces buildable slices
with dependencies. [Specification instructions](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md),
[ticket instructions](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md).

### Where the documents and tickets live

For the README's **local Markdown tracker** example:

| Artifact | Example location | Its responsibility |
| --- | --- | --- |
| Architecture | `docs/architecture/support-assistant.md` | Requirements, accepted choices, reasons and tradeoffs |
| Goal plan | `docs/plans/support-assistant.md` | Implementation routes, dependencies and handoff; link to the adopted tracker for current work status |
| Optional decision map | `.scratch/support-assistant-design/map.md` | Index of open and resolved design questions |
| Optional decision tickets | `.scratch/support-assistant-design/issues/` | One question and its resolution per ticket |
| Specification | `.scratch/support-assistant/spec.md` | Agreed feature behaviour, module/interface contracts and testing decisions |
| Build tickets | `.scratch/support-assistant/issues/` | Small deliverable outcomes, blockers, skills, acceptance and execution evidence |

Use separate effort names for the decision map and implementation spec: both
workflows create an `issues/` directory with numbered files. The names above are
examples; use the paths your agent actually creates. With GitHub or another
configured tracker, pass the returned issue links instead.
[Local tracker conventions](https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md).

Once adopted, that spec/tracker owns execution status; update the original plan
to point to it. Keep architectural decisions in the architecture document and
link them from the spec and tickets. If a decision changes, update the affected
requirements and checks together.

### What to carry into a ticket

A goal can become several tickets. Preserve the outcome and dependency meaning
instead of requiring a one-to-one conversion. During `to-tickets`, ask the agent
to consult the relevant ADK specialists and include their names in the ticket,
so a fresh implementation session can load them too.

For example, a saved-language ticket should carry:

```markdown
## Save, use and forget a preferred language

Linked context: the saved-language goal and ownership decisions in the design.
Primary skill: adk-memory-architecture.
Supporting skills: adk-tool-auth-and-secrets for identity;
adk-frontend-integration for the preferences UI and API.
Blocked by: the actual prerequisite tickets, or none after repository inspection.

- [ ] A signed-in user saves a language and sees it used in a later conversation.
- [ ] The saved value survives a backend restart against the local database.
- [ ] Another user cannot read or change that preference.
- [ ] Forgetting removes it from subsequent invocation inputs.
- [ ] A delayed stale save cannot restore a forgotten preference.

Evidence: record actual commands and results; all checks are initially pending.
```

The implementation approach must also identify the UI → authenticated API →
store → invocation path. A controlled model can verify that this path passes
the setting correctly; live language quality needs its own evaluation. Use
project-specific checks and keep detailed code inspection notes linked from the
plan. The spec and ticket should remain readable as behaviour and contracts.

### Resume implementation with the right specialist

Use one leading workflow and name the supporting ADK skills. For example, after
the streaming ticket is ready, paste its actual path into this request:

```text
/implement Implement .scratch/support-assistant/issues/03-stream-replies.md.
Read its linked specification and architecture, and verify its blockers are done.
Use adk-frontend-integration for the browser and streaming contract,
adk-tool-auth-and-secrets for session ownership, and adk-agent-evaluation
for the relevant failure checks. Work on this ticket and run its local checks.
Review the ticket's full changes, including staged and unstaged edits, against
its spec and the state before this ticket. Resolve actionable review findings.
Record evidence and remaining gaps in the ticket; mark it complete only when
the acceptance checks pass. Leave changes uncommitted for review.
Keep deployment in its own ticket.
```

The filename above is illustrative. In Codex, use `$implement`; in Google
clients, ask to use the skill by name. Matt's `implement` drives development,
testing and review and normally **commits to the current branch**; the example
explicitly overrides that last step and includes uncommitted changes in review.
Review and commit the accepted changes before starting the next ticket.
Recording ticket completion and resolving review findings are explicit requests
here, so the next session has a reliable record of what is ready.
[Implementation instructions](https://github.com/mattpocock/skills/blob/main/skills/engineering/implement/SKILL.md).

If a ticket needs clarification, ask its specialist to review the proposed
approach and checks before implementation. If it reveals a consequential new
requirement, return to `adk-system-designer` with the ticket and design paths;
update the decision and affected tickets, then resume `implement` with the same
ticket. See the README's [planning and implementation examples](../../README.md#from-design-to-working-tickets).

After individual tickets pass, run the combined application journey with
`adk-agent-evaluation`. Keep local, live-model and hosted results explicit;
writing a plan or checking a ticket box does not establish unrun evidence.

Upstream behavior was checked on 25 September 2026. Installed versions and
project configuration determine the actual workflow. Missing optional skills
leave direct continuation available.
