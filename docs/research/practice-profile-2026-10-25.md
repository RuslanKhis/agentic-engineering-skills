# A practice profile kept outside the project — 25 October 2026

## Question

An AI engineer who runs several ADK projects, for an employer and for
clients, retypes the same context into every new project: the business and
its KPIs, who decides and how, the delivery defaults, the stack conventions,
the security floor, the presentation style, and the lessons earlier projects
taught. Where can that context live so the flow skills (`adk-discovery`,
`adk-system-designer`, `adk-presenter`, `adk-engineer`) read it without
copy-pasted prompts, without one client's facts reaching another client's
project, and without paying for it in every session?

Every page below was read on 25 October 2026 unless a date is given.

## Host-native memory loads everywhere

Each host has a user-level instruction file, and each loads it in every
project. That is the wrong scope for client facts.

- **Claude Code.** `~/.claude/CLAUDE.md` is "Personal preferences for all
  projects" and `~/.claude/rules/` "apply to every project on your machine";
  CLAUDE.md files and auto memory are "loaded at the start of every
  conversation". Auto memory is "per repository, shared across worktrees".
  An `@path` import in a project file that resolves outside the working
  directory raises a one-time approval dialog; imports in user-scope files
  load without one. Imports "don't reduce its context cost" — imported files
  load with the file that imports them.
  [Memory](https://code.claude.com/docs/en/memory).
- **Codex.** The global `AGENTS.md` in the Codex home (`~/.codex` unless
  `CODEX_HOME` is set) lets "every repository inherit your working
  agreements" and is read once per session.
  [AGENTS.md](https://developers.openai.com/codex/guides/agents-md).
  "Local Codex memories are off by default", enabled with
  `[features] memories = true`, stored under `~/.codex/memories/`, with
  `memories.use_memories` controlling injection "into future sessions" and a
  separate "global memory consolidation" model; the page describes
  machine-level scope, not per-project scope.
  [Memories](https://developers.openai.com/codex/memories) (redirects to
  learn.chatgpt.com). The research brief said memories are unavailable in
  the EEA, UK and Switzerland; the current page says nothing about regions,
  and secondary reports of a 16 June 2026 rollout say they are available
  there but off by default. Not relied on: the design does not use Codex
  memories either way.
- **Gemini CLI.** The global `~/.gemini/GEMINI.md` "Provides default
  instructions for all your projects". Its memory guidance routes
  "cross-project personal preferences" to that global file, and "the stored
  facts are automatically included in the hierarchical context system for
  all future sessions". A client fact saved this way reaches every project.
  [GEMINI.md](https://geminicli.com/docs/cli/gemini-md/),
  [memory](https://geminicli.com/docs/tools/memory/).
- **Antigravity.** "Global rules apply across all projects on your
  workstation" (`~/.gemini/AGENTS.md`, `~/.gemini/GEMINI.md`,
  `~/.gemini/config/rules/*.md`, CLI `~/.gemini/antigravity-cli/rules/*.md`).
  Note the overlap with Gemini CLI's `~/.gemini/GEMINI.md`.
  [Rules](https://antigravity.google/docs/rules).

**Consequence.** Client context in any of these files leaks across clients
and costs context in sessions that never use it. The profile lives in its
own directory, is read only at named steps, and is never written through a
host memory tool. At most a one-line pointer (where the root is) belongs in a
host's global file.

## Reaching a directory outside the workspace

- **Claude Code.** File reads need no approval "within the working directory
  and additional directories"; extend with `--add-dir <path>`, `/add-dir`, or
  `additionalDirectories` in settings. Files there "follow the same
  permission rules"; their CLAUDE.md files are not loaded unless
  `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` — good, the profile is not
  auto-loaded. A `Read(~/path/**)` allow rule uses the home anchor; edits
  still follow the permission mode.
  [Permissions](https://code.claude.com/docs/en/permissions).
- **Codex.** `workspace-write` is "the default low-friction mode": the agent
  "can read files, edit within the workspace". Extra write locations go in
  `sandbox_workspace_write.writable_roots` (`array<string>`, "Additional
  writable roots when `sandbox_mode = "workspace-write"`").
  [Sandboxing](https://developers.openai.com/codex/concepts/sandboxing),
  [configuration reference](https://developers.openai.com/codex/config-reference).
  Whether reads outside the workspace prompt is not stated on the page.
- **Gemini CLI.** `/directory add <path1>,<path2>` "Add a directory to the
  workspace"; "Disabled in restrictive sandbox profiles", where
  `--include-directories` at start-up is the alternative.
  [Commands](https://geminicli.com/docs/reference/commands/).
- **Antigravity.** Rules may include `~/` paths, but no documented setting
  for reading an arbitrary directory outside the workspace was found.
  Untested; the skill says so.

## Prior art

- **Cline Memory Bank.** Six files in `memory-bank/`; the custom instructions
  say "I MUST read ALL memory bank files at the start of EVERY task", and
  updates happen on an "update memory bank" command or after significant
  changes. Read-everything costs context every task; without an update step
  the files go stale. [Cline docs](https://docs.cline.bot/prompting/cline-memory-bank).
  Taken: an explicit update step. Rejected: read-all-every-task.
- **Matt Pocock's `setup-matt-pocock-skills`** (`mattpocock/skills` at
  `5beb35b`, MIT, already in the source register). One setup skill writes
  configuration other skills read ("Skills like `to-tickets`, `triage`, and
  `to-spec` read from and write to it"); it asks one section at a time and
  says "Lead each section with the recommended answer so the user can accept
  it in a word"; the files stay editable by hand. Taken: the setup skill, the
  accept-in-a-word interview, consumers that read rather than re-ask. Nothing
  copied.
- **basic-memory** (an MCP knowledge base over Markdown) was considered and
  not read in depth: a server process is too heavy for a few files the agent
  can read directly.
- **Context files cost more than they help unless specific.** Gloaguen et al.,
  "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for
  Coding Agents?" ([arXiv 2602.11988](https://arxiv.org/abs/2602.11988), v1
  12 Feb 2026, v3 29 Sep 2026): context files "do not generally improve task
  success rates" and raise inference cost by over 20%; agents follow explicit
  instructions in them well; overviews do not help; non-standard practices
  are where they pay. Taken: each skill reads only its sections, at one step;
  size caps; lessons filtered by specialist.
- **Memory poisoning.** Rehberger, "Hacking Gemini's Memory with Prompt
  Injection and Delayed Tool Invocation" (embracethered.com, 10 February
  2025): instructions hidden in a summarised document ask the model to save
  false memories when the user next replies "yes", "sure" or "no"; the saved
  memories persist into future sessions. Recommendations: explicit
  confirmation before saving, review memories, confirm sensitive tool calls
  once untrusted data is in context. Taken: a fact is proposed only from what
  the user said or the project recorded, never from an ingested document,
  page or tool result; the user's yes answers a displayed diff, not a
  question; every entry carries source and date; review prunes.

## Design decisions

1. **Name: practice profile**, not memory, so "add memory to my ADK agent"
   keeps routing to `adk-memory-architecture`.
2. **Root** `${AGENTIC_ENGINEERING_HOME:-~/.agentic-engineering}` with
   `README.md`, `engineer.md`, `bindings.md` (repo path → org slug, no
   content), `orgs/<slug>/profile.md` (frontmatter with `review_by`, about
   180 days; sections that map to existing scope-gate and discovery
   questions; cap 150 lines), `orgs/<slug>/lessons.md` (cap 40 active), and
   `orgs/<slug>/projects/<slug>.md` pointer cards. `field-notes/` is reserved
   for adk-engineer's field feedback (generalised, shareable; distinct from
   private lessons).
3. **Readers and steps.** Discovery at its entry and scope gate; the designer
   at its scope gate, as accept-in-a-word defaults labelled with source, the
   org security floor raising and never lowering the skill's floor; the
   presenter for audience and style only, never numbers; the engineer for
   lessons tagged with the chosen specialist and stack conventions. No other
   specialist reads it.
4. **Precedence.** Project record > the user's current message > org profile
   > `engineer.md` > skill defaults; a conflict is named and asked.
5. **Client separation.** The org comes from `bindings.md` keyed on the repo
   path and is confirmed once; an unbound repo means ask, never infer from
   the git remote; one session reads one org directory; no global "active
   org".
6. **Writes.** Only an end-of-skill harvest: a diff, each line with source
   and date, a regex scan for secrets and personal data, written after an
   explicit yes. Past `review_by` an entry is "stale, confirm?" and never a
   default. The profile is data, not instructions.
7. **Packaging.** A `practice-profile` skill (init, bind, remember, review)
   with a stdlib helper, and a short identical
   `references/practice-profile.md` in each of the four flow skills, checked
   byte-identical by `scripts/validate_skills.py`. With no root directory,
   the flow skills behave exactly as before.

## Not verified

Antigravity access to a directory outside the workspace; whether Codex
prompts for reads outside the workspace; Codex memories' current regional
availability (secondary sources only).
