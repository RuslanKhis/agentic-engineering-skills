# Contributing

Improve a concrete task: make a skill easier to select, help it handle an
observed failure, or make its result easier to verify. Describe the user request
and the behavior the change should improve. The
[research notes](docs/research/skill-quality-practices.md) explain the practices
behind this approach.

## Run the repository checks

Use Python 3.11 or 3.12 on macOS or Linux, from this repository's root:

```bash
python3 -m venv .venv
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
  when adding a skill or changing its scope.
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
| Helper script | A failing case for the defect, then the relevant test suite |
| Skill description or routing | Positive, near-miss and contextual cases in fresh sessions; distinguish selection from execution |
| Implementation guidance | A representative task with an independent check of its output or effects |
| SDK recipe | Exact tested versions and relevant runtime contract tests |
| Combination with another collection | Which workflow led, which skills loaded and whether the task's scope was preserved |

Use the [evaluation protocol](docs/testing/skill-quality.md) to compare old/new
instructions or skill/no-skill conditions. Do not give the executing agent the
expected answers. Preserve failed trials, inspect actual artifacts and record
unavailable runs. Add a narrow correction supported by that evidence.

Do not update a specialist's `last-tested` date because a link checker passed.
Its compatibility/validation references should say which runtime recipe was
actually exercised. Keep package checks, model behavior and cloud results
separate in reports.

## Submit a reviewable change

Explain the concrete problem, resulting behavior, relevant validation and
remaining limitations. Update public examples when a command or scope changes.
Run `git diff --check`. Keep personal environments, credentials and raw customer
data out of the contribution. Publishing a result as “better” requires a
comparable baseline; passing one smoke example establishes only that example.
