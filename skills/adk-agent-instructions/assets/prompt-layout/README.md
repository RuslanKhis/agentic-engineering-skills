# Prompt layout template

Copy `prompts/` into the target project and rename `example_agent` to the
agent's name. The linter in this skill discovers `prompts/<agent>/instruction.md`
and the sibling `description.txt`; `examples/*.json` are exemplars as data and
`CHANGELOG.md` carries the prompt version (its first heading). The loader and
contract test are described in `references/prompt-as-code.md`.
