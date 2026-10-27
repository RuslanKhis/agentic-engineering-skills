# Contributing

Improve a concrete task: make a skill easier to select, help it handle an
observed failure, or make its result easier to verify. Describe the user request
and the behavior the change should improve. The
[research notes](docs/research/skill-quality-practices.md) explain the practices
behind this approach.

## Run the repository checks

Use Python 3.11 or 3.12 on macOS or Linux, from this repository's root (name
the interpreter: a system `python3` may be older):

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/check_repo.py
```

These are maintainer dependencies. People installing the skill packages do not
need this environment, and the checks do not need a book checkout, Google ADK
or cloud credentials. Use a clean environment to see optional SDK skips clearly.

The command validates packages and evaluation-case structure, tests the
validators, then runs each existing offline helper suite in its own process.
It fails on empty test discovery. Some SDK contract tests are intentionally
outside this tier; see [test coverage and limits](docs/testing/skill-quality.md).
GitHub Actions runs the same command on Linux with Python 3.11 and 3.12.

For packaging alone:

```bash
.venv/bin/python scripts/validate_skills.py
```

## Write instructions that earn their place

- **Discovery:** describe what the skill does and when it applies. Include a
  nearby exclusion when it prevents a likely routing mistake. Add a natural
  positive request and a near-miss to [activation cases](evals/activation.json)
  when adding a skill or changing its scope, with `"split": "dev"`. A new
  skill also needs a held-out positive and near-miss (`"split": "heldout"`),
  generated from a neutral brief as
  [checking skill quality](docs/testing/skill-quality.md#keep-a-held-out-split)
  describes, never written by you.
- **Domain knowledge:** preserve the API contracts, failure modes and decision
  criteria that change the coding agent's work. Generic advice such as “write
  good tests” rarely justifies another instruction.
- **Selective detail:** keep purpose, important constraints and mode selection
  in `SKILL.md`. Link conditional detail where it becomes relevant, explaining
  when to read it. Line and word counts help review context cost; they are not
  quality scores or targets to fill.
- **Portability:** put a specialist's required references, scripts and assets
  inside its directory. Use relative Markdown links. Optional collections are
  discovered through the host's catalogue; they are not assumed to exist at
  the author's filesystem paths.
- **Useful examples:** when a real mistake needs illustration, show the
  situation, the failure, the corrected approach and an observable check.
  Preserve the user's product and existing conventions when applying an example.
- **Scope and composition:** use one leading development workflow and the
  relevant ADK guidance. An installation, migration, deployment or publication
  is its own operation; mentioning another skill does not initiate it.

The shared [Agent Skills specification](https://agentskills.io/specification)
defines the package format. Bundled `LICENSE` files and `agents/openai.yaml`
display metadata are additional conventions of this collection. Keep existing
invocation settings and dependency pins unless the change requires adjusting
them. Attribute borrowed patterns and retain any required upstream licence.

## Show the right evidence

| Change | Evidence to include |
| --- | --- |
| Metadata, links or package layout | Package check and relevant invalid-package regression tests |
| Helper script | A failing case for the defect, then the relevant test suite; flags, exit codes and documented commands follow [helper conventions](docs/helper-conventions.md) |
| Skill description or routing | Positive and near-miss cases in `evals/activation.json`, and a contextual case (a `evals/scenarios.json` case whose `context` decides the route); trigger rates over repeated fresh sessions with a held-out split, as `docs/testing/skill-quality.md` describes; distinguish selection from execution; the description, the skill's row in the README's skills table, its entry in `docs/skills.md` and `agents/openai.yaml`'s `short_description` kept consistent |
| Implementation guidance | A representative task with an independent check of its output or effects |
| SDK recipe | Exact tested versions and relevant runtime contract tests |
| A fact read from an external repository | A dated citation with the commit, and its row in `docs/research/source-register.json` so `scripts/check_source_freshness.py` reports when it goes quiet, stale, archived or relicensed |
| Combination with another collection | Which workflow led, which skills loaded and whether the task's scope was preserved |

### Re-run activation after a description or routing change

A change to any skill's description, or to routing (an exclusion, a hand-off
between specialists, adk-engineer's selection), must be re-run through the
activation runner and introduce no new FAIL against the last recorded run:

```bash
.venv/bin/python scripts/run_activation.py --backend claude-cli --repeat 2 --out after.json
.venv/bin/python scripts/run_activation.py --compare docs/testing/artifacts/activation-2026-10-27/sonnet-5-5.json after.json
```

`claude-cli` uses your Claude Code login; `--backend files --export DIR`
writes prompts for fresh sessions to answer when it is not available. The
runners use no API key. `--compare` exits 1 on a new
FAIL. Say in the pull request which cases changed grade and why.

The `heldout` split is never used while editing a description: work from the
`dev` cases (`--split dev`) and do not read held-out prompts or results until
the change is finished. Then re-run `--split heldout` once and report its
result beside the dev result; a held-out failure is reported to the skill's
owner, not fixed in the same change. When held-out cases leak into description
work (someone read them while editing, or a description was changed to fix
one), move those cases to `dev` and generate a fresh held-out set. To check a
scenario end to end, `scripts/run_scenarios.py list` shows which scenarios can
run as they stand, and `run --ids ...` runs them in throwaway workspaces with
a separate judge; see [checking skill quality](docs/testing/skill-quality.md#run-the-scenario-runner).
Both runners call models and cost money; `check_repo.py` stays offline and
only tests them.

Use the [evaluation protocol](docs/testing/skill-quality.md) to compare old/new
instructions or skill/no-skill conditions. Do not give the executing agent the
expected answers. Preserve failed trials, inspect actual artifacts and record
unavailable runs. Add a narrow correction supported by that evidence.

Do not update a specialist's `last-tested` date because a link checker passed.
Its compatibility/validation references should say which runtime recipe was
actually exercised. Keep package checks, model behavior and cloud results
separate in reports.

Record each checked change as a dated entry at the top of the
[testing log](docs/testing/index.md) (`## <what changed> · <D Month YYYY>`,
newest first), with the package and test counts the check printed and a link
to its record under `docs/testing/`. The README keeps only a short summary of
what has been tested; do not add dated entries there.

## Triage field reports

Users share divergences through the [field report form](.github/ISSUE_TEMPLATE/field-report.yml)
(see [field feedback and privacy](docs/field-feedback-privacy.md)). Issue text
is untrusted input to your own coding agent: an injected issue once led an
agent with GitHub access to leak private repositories through a public pull
request ([Invariant Labs](https://invariantlabs.ai/blog/mcp-github-vulnerability)).

```bash
gh issue list --label field-report --state open --json number,title,body,labels --limit 200 > reports.json
.venv/bin/python scripts/triage_field_reports.py reports.json
```

The table clusters reports by skill, kind and quoted `file:line`, prints no
report prose and flags injection-like text, a missing privacy tick or a
non-form issue.

- Read reports in a session with no write tools and no access to private
  repositories; never let that session edit a skill.
- Reproduce in a clean fixture before editing. One report is a lead, not
  evidence; remove `needs-repro` only after the reproduction. When the
  reproduction needs model sessions you cannot run, add the case first, make
  the change as an unmeasured candidate and record the reproduction as not
  run; a not-run record belongs under `docs/testing/` like any other.
- Every accepted report becomes an activation or scenario case carrying
  `"source": "issue #N"` (or a short description and date for a report
  without an issue), written in your own words.
- An SDK fact it corrects also gets its dated citation and, when read from a
  repository, a row in `docs/research/source-register.json`.

## Submit a reviewable change

Explain the concrete problem, resulting behavior, relevant validation and
remaining limitations. Update public examples when a command or scope changes.
Run `git diff --check`. Keep personal environments, credentials and raw customer
data out of the contribution. Publishing a result as “better” requires a
comparable baseline; passing one smoke example establishes only that example.

## Re-verify the law references

The governance pack's references each carry a `<!-- verified: <date>; re-check
every N days -->` line; the validator requires it and warns when it is due.
Re-verify them quarterly, or when warned, by
[docs/maintenance/law-refresh.md](docs/maintenance/law-refresh.md).

## Release a version

Releases are dated (`YYYY.MM.DD`, `.N` for a second one that day) and carry the
same `metadata.version` in every skill and versioned plugin manifest; the
package check fails when they differ.

```bash
.venv/bin/python scripts/release.py prepare        # stamp today's version, add a CHANGELOG section
# edit the CHANGELOG section into readable notes, run scripts/check_repo.py, commit
.venv/bin/python scripts/release.py tag            # tag v<version>, move the local stable branch
```

`tag` refuses a dirty worktree, mixed versions or a missing CHANGELOG section,
and never pushes; it prints `git push origin v<version>` and the `stable`
branch push for you to run. Plugin installs follow `stable`, so moving it is
what publishes a release to them. Check the manifests with
`claude plugin validate .` when they change.
