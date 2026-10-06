# Compatibility and evidence boundaries

Read this before citing version-dependent behaviour. This skill was written
against the google-adk **2.8.0** source tree (tag v2.8.0) and the adk-python
main CHANGELOG and source as of **2026-10-06** (2.11.0 released 2026-10-01).
Nothing here was executed against a live model; every behaviour below is a
reading of source or documentation, and the target's installed version decides
which column applies.

## Verified in 2.8.0 source

| Behaviour | Where |
| --- | --- |
| `instruction: str | InstructionProvider`; callable bypasses state injection | `agents/llm_agent.py`, `canonical_instruction` |
| Template pattern `{+[^{}]*}+`; `{var}`, `{var?}`, `{artifact.name}`, `{prefix:name}` with `app:`/`user:`/`temp:`; invalid names left unchanged; missing key raises `KeyError('Context variable not found: ...')` | `utils/instructions_utils.py` |
| `{{var}}` injects state like `{var}` (same pattern) | same |
| No backslash or `${}` escape | same (pattern has no look-behind) |
| Jinja2 path with `use_jinja2=True`, `StrictUndefined`, optional dependency | same; CHANGELOG 2.7.0 |
| `static_instruction` sent literally; when set, `instruction` is appended to `contents` as `role='user'` with no label | `flows/llm_flows/instructions.py` |
| `global_instruction` deprecated with `DeprecationWarning`; root only | `agents/llm_agent.py`, `canonical_global_instruction` |
| `GlobalInstructionPlugin` prepends to `config.system_instruction` in `before_model_callback`; import path `google.adk.plugins.global_instruction_plugin` | `plugins/global_instruction_plugin.py` |
| Transfer text rendered with "Agent name: / Agent description:" per target; skipped for `task` and `single_turn`; `single_turn`/`task` children are not transfer targets | `flows/llm_flows/agent_transfer.py` |
| `mode` literal `'chat' | 'task' | 'single_turn'`; `task` adds `FinishTaskTool` and skips `output_key` on text; sub-agents wrapped as `_TaskAgentTool` / `_SingleTurnAgentTool` by mode; task tool description suffix about parallel calls | `agents/llm_agent.py`, `tools/agent_tool.py` |
| `include_contents` `'default'` or `'none'` (current turn only) | `flows/llm_flows/contents.py` |
| `validate_generate_content_config` rejects `tools`, `system_instruction`, `response_schema` | `agents/llm_agent.py` |
| `FunctionTool` description is the cleaned docstring; parameter descriptions not derived ("Do not support parameter description for now") | `tools/function_tool.py`, `tools/_automatic_function_calling_util.py` |
| Relayed agent output fenced between quoted-content markers with a data-not-instructions preamble | `flows/llm_flows/_fencing.py` |
| `output_key` skipped when `event.author != self.name` | `agents/llm_agent.py` |
| `BaseAgent.description` docstring: one line preferred, used for delegation | `agents/base_agent.py` |
| `AgentTool` docstring discourages direct use in favour of `mode='single_turn'` | `tools/agent_tool.py` |

## Changed after 2.8.0 (CHANGELOG and main source, read 2026-10-06)

| Version | Change relevant to instructions |
| --- | --- |
| 2.9.0 (2026-09-10) | dynamic instruction labelled with a preamble so the model does not read it as a user turn; `transfer_reason` argument on `transfer_to_agent`; transfers restricted to declared targets; agent name added to the missing-variable error |
| 2.10.0 (2026-09-24) | templating leaves `${var}` and `\{var}` as written (pattern gains `(?<![\$\{\\])`); server-supplied tool descriptions fenced; non-string `system_instruction` serialised for OpenAI |
| 2.11.0 (2026-10-01) | Jinja2 instructions rendered in a sandbox with a read-only state mapping |

## Documentation read (adk-docs snapshot, 2026-10-06)

`agents/llm-agents.md` (instruction ingredients, tips, description guidance),
`sessions/state.md` (templating, f-string note, `InstructionProvider` for
literal braces; no escape syntax documented), `tutorials/agent-team.md`
(delegation best practice, "Docstrings are Crucial"), `workflows/patterns.md`
(coordinator and `output_key` bus), `safety/index.md` (vague instructions as
a risk source; instructions alone insufficient), `optimize/index.md`
(`GEPARootAgentPromptOptimizer`, root agent only, experimental).

## Not verified

- Any live model behaviour, including every vendor prompting claim; these are
  cited as vendor guidance or practitioner reports and must be re-measured on
  the target's evaluation set.
- The `adk web` Trace request tab and the `gcp.vertex.agent.llm_request`
  span contents; cited from documentation and a coordinator's research
  summary, not exercised.
- Issue-tracker pitfalls (#628, #5706, #3527, #4606, #6062, #6216, #6652,
  #3739, #3163, #3330, #2686, #3758, #6450, #6816): read as reported
  behaviour on the versions named in each thread.
- Behaviour of versions before 2.7.0 or after 2.11.0.
- Cache hit rates with `static_instruction`; the mechanics are read from
  source, the measurement belongs to optimise-adk-on-google-cloud.

## Working with a different pin

Read the installed `instructions_utils.py` and `instructions.py` before
relying on either column. On 2.10.0 and later, backslash escapes are an
acceptable fourth option for literal braces; on 2.8.0 and 2.9.x they are not.
When the pin is unknown, write `{var?}` or a provider, which behave the same
across all versions above. Do not change the pin to make an instruction
render; identify the incompatible behaviour and request a version decision.
