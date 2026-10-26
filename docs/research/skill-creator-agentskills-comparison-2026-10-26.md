# skill-creator and the Agent Skills reference compared with this toolkit — 26 October 2026

## Scope and snapshot

A review of [agentskills/agentskills](https://github.com/agentskills/agentskills)
at commit `69ef37e` (2026-08-09; the specification and the `skills-ref`
reference library) and of `skills/skill-creator` in
[anthropics/skills](https://github.com/anthropics/skills) at commit
`dbd4588` (2026-10-09), cloned on 26 October 2026 and read. Both were first
reviewed on 15 September 2026 ([skill quality practices](skill-quality-practices.md));
this note pins them. The published `skills-ref` 0.1.1 was installed in a
throwaway environment and run on a copy of this repository's `skills/`,
never inside the repository.

**Licence.** `skills-ref` and `skill-creator` are Apache-2.0; the
specification text is CC BY 4.0 (paraphrased with attribution).
anthropics/skills has no root licence and sets one per skill: `docx`,
`pdf`, `pptx` and `xlsx` are proprietary, `doc-coauthoring` has none, and
its third-party notices include GPL-3.0 FFmpeg. Nothing from that
repository is copied.

**Maintenance.** agentskills quiet; anthropics/skills active
(skill-creator last changed 2026-04-20).

**Conclusion.** All 25 skills pass the reference validator. Its parser is
stricter than ours in three ways (a `---` inside frontmatter, inline YAML
collections, anchors and aliases), which `validate_skills.py` now mirrors
rather than taking a demonstration library as a CI dependency. The
published wheel's command is `agentskills`, not the `skills-ref` the
specification names. skill-creator's description loop and blind comparator
are worth having as method, not as tools: activation is now measured as a
trigger rate over repeated runs with a held-out split, and the existing
blind A/B practice is written down with one upstream addition, flagging
assertions that pass in both conditions.

## Method

The reference parser (strictyaml, split on `---`) was read and run on the
copy; the differences were shown on synthetic skills in the spike and
confirmed against `validate_skills.py`. The description lengths were
measured. One scenario case covers the maintainer journey; the fresh-agent
trial is in the
[testing record](../testing/skill-creator-agentskills-alignment-2026-10-26.md).

## Drift corrected

None.

## Imported, by specialist

- **Toolkit checks.** `scripts/validate_skills.py` rejects the three forms
  the reference parser rejects, with tests; one existing test that accepted
  inline metadata now uses block form.
- **docs/testing/skill-quality.md.** An optional cross-check with the real
  command; activation as a trigger rate over three runs with a held-out
  split and the 1,024-character limit; blind A/B rules with a mapping file
  written before grading and non-discriminating assertions flagged.

After the trial: `CONTRIBUTING.md` names the interpreter, defines a
contextual case, says what to do when a reproduction needs model sessions
you cannot run, accepts a report without an issue number, and asks for the
README entry and `short_description` to stay consistent with a changed
description; `skill-quality.md` says how to mark train and held-out cases
and what to cut to make room; and `check_repo.py` accepts an activation
case's `split` only as `train` or `held-out`, with a test.

## Routed, not copied

None.

## Vendored assets

None.

## Left out, with reasons

- `skills-ref` as a CI dependency: a demonstration library; its rules are
  mirrored instead.
- skill-creator's automated description loop: Claude Code only, live model
  calls, and it pushes descriptions towards triggering at the expense of
  exclusions.
- Its comparator agent, which writes its rubric after reading both outputs.
- Anything from the proprietary or unlicensed skills in anthropics/skills.

## Limits

The comparator and description loop were read, not run.
