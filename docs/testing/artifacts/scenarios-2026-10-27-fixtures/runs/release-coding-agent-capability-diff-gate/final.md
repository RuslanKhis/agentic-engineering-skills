**No, `agents-shipgate diff --application` is not enough on its own.** I've added a gate built on the security skill's capability inspector instead. Nothing was run, because Bash was disabled in this session.

**Why shipgate alone fails.** The skill's notes on shipgate 1.2.0, from an offline trial on ADK 2.12 fixtures, say these things:
- It exits 0 whatever it finds, including added tools and partial comparisons. It only exits 2 when a ref can't be read. So it can't block anything.
- It reported no change when `require_confirmation` or the `before_tool_callback` was removed, or when the `McpToolset` filter was widened. Those are the exact controls in your agent.
- Any `McpToolset` made the comparison partial.
- It does add something useful: it digests each tool body, so a new outbound POST inside an existing tool shows up. I'd keep it as an advisory step, pinned to a version, after you've reviewed it. I did not wire it in.

**What I added**
- `.github/workflows/capability-gate.yml` runs the inspector on the merge-base tree and on the PR head with `--compare`.
  - Both runs use the inspector from the base branch tip, so the PR can't rewrite its own judge.
  - The workflow uses `pull_request_target` for the same reason. The head code is only parsed, never run.
  - A capability change needs the `capability-approved` label. The label must have been applied by someone with maintain or admin rights, which a coding agent's token won't have.
  - A new push removes the label, so an approval doesn't carry over to later commits.
- `ci/capability_gate.py` maps the inspector's exit status to a verdict:
  - Exit 1 (capability changed) needs approval.
  - Exit 3 (partial scan) needs approval only if a changed file is in `unread_paths`. Your new `Workflow` is always unread, so blocking every PR on that would fail them all. A change to `app/reporting.py` does block.
  - Anything else is NOT RUN and fails the job, never a pass.
- `tests/test_capability_gate.py` covers the verdict mapping.
- `.github/CODEOWNERS` puts the agent, callbacks, tools, clients, auth, settings, prompts and workflows under an owner. The inspector sees declarations, not what a tool body does, so a change inside `refund_order` or `send_email` would go through without the label.

**Assumptions** (nobody was there to answer)
- `.claude/skills/adk-agent-security/` is committed to your repo. The inspector path in the workflow points there. The skill suggests `.agents/skills/`, but the inspector skips both directories.
- A `capability-approved` label from a maintainer or admin counts as human approval.
- This workspace isn't a git repository, so the base/head flow couldn't be tried here even with Bash.

**Left undone or needs you**
- Run `python -m unittest discover -s tests -t .`, and run the inspector once on the repo. I haven't seen its real output, including whether the `Workflow` shows up as expected.
- Replace `@your-org/agent-owners` in `CODEOWNERS` with the real team.
- Enable "Require review from Code Owners" in branch protection.
- Make `capability-gate` a required status check.
- Create the `capability-approved` label.
- The PR that adds this gate will have no gate run on it, because its base has no workflow. Merge it by hand, then confirm the next PR is gated.
- Prompt text, `max_refund_cents` and model IDs are not capability changes to the inspector. Only CODEOWNERS review covers them.