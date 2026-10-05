# R1 trial: scope gate on the planning brief

*6 October 2026 · One fresh general-purpose agent session, Claude Code harness.*

**Maintainer test (feedback round 3, R1).** Give the designer the planning
assignment brief with "3 to 4 hours, judged on holdout predictions, method and
report". The plan it produces must put the core assessment path and a quality
measurement first, name deferred controls, and must not propose officer
revisions, export acknowledgement or a cloud roadmap as early goals.

**Setup.** `brief.md` is the assignment; `prompt.txt` is the exact instruction
the agent received. The agent was pointed at the repository's
`skills/adk-system-designer/SKILL.md` by path, because the copy installed under
the user's home directory predates this round. This is therefore an explicit
file-path invocation of the instructions under test, not a catalogue
activation. No expected answers were supplied. The user was declared
unavailable, so the skill's one-pass-draft branch applied.

**Outputs.** `workspace/docs/architecture/planning-assistant.md` (263 lines)
and `workspace/docs/plans/planning-assistant.md` (304 lines), unedited.

## Assessment against the test

| Criterion | Observed | Result |
| --- | --- | --- |
| Scope gate recorded first | Design opens with purpose, five labelled assumptions, then a "Scope, evaluator and deferred controls" block at line 53 with time, money (a holdout reserve set aside before experiments), evaluator and artifact type | Pass |
| Core assessment path and quality measurement first | Goals in order: G00 15-minute key/model probe, G01 ingestion report, G02 retrieval with gold-set recall, G03 end-to-end draft and baseline on the five development cases, G04 one-change iterations, G05 freeze, holdout run from the reserve, report | Pass |
| Deferred controls named with reasons | Ten rows: officer revision workflow, export acknowledgement, recovery, identity, hosting, LLM judge, memory, hybrid retrieval, data-protection services, parallelism, each with why it waits and what brings it forward | Pass |
| No officer revisions, export acknowledgement or cloud roadmap as early goals | None appear in G00 to G05; hosting is explicitly "nothing is served" | Pass |
| Deliverable produced by the frozen method | G05 refuses a holdout run whose config hash differs from the frozen one; the plan reserves the holdout budget first | Pass (beyond the test) |

## Limitations

- The design and plan total 567 lines for a four-hour assignment. The
  proportionality rule shaped the goals but did not shrink the documents; the
  reader's-budget guidance applies to design documents too and is not yet
  worded that way in the designer.
- One trial, one model, one harness. It shows the revised instructions can
  produce the intended shape, not that they do so reliably or under natural
  activation.
- The agent read the memory skill's ingestion and retrieval helpers while
  designing; a workspace without the sibling skills would need to carry those
  mechanisms in the plan text.
