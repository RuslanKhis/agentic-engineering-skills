# Working with other skill collections

Read this when another collection supplies the project's lifecycle or the user
asks to combine skills. Keep one development workflow for the task and use the
selected ADK specialist for the application decisions. Additional collections
are optional; their presence does not expand the user's request.

## Establish the project and scope

Read the relevant project instructions and existing design before choosing a
workflow. An `agents-cli-manifest.yaml` identifies an Agents CLI project; inspect
its declared agent directory, framework, version and deployment target alongside
the actual code. Read `.agents-cli-spec.md` when present and relevant. A manifest
is evidence of project conventions, not permission to execute platform commands.

| Situation | How to proceed |
| --- | --- |
| User chose the Agents CLI lifecycle for a new project | Use the installed `google-agents-cli-workflow` for the requested lifecycle phases and this toolkit's specialist for the feature. Reuse the agreed design. |
| Focused change in an existing Agents CLI project | Select the primary ADK specialist. Preserve the manifest, generated server/transport, dependency pins, model and infrastructure ownership. Consult the relevant installed Google skill for the specific interface or command needed. |
| Existing ADK application without Agents CLI | Work in its current layout and environment. Adopting a scaffold is a separate requested change; a downloaded recipe can be studied without converting the application. |
| User chose Matt Pocock's `tdd`, `diagnosing-bugs` or another process skill | Follow that installed process and use the ADK specialist's domain guidance. Keep the existing task and design instead of starting another interview or ticketing workflow. |

State the division of work briefly. For example: “I’ll use the memory specialist
for storage and user isolation, and the existing Agents CLI conventions for
integration.” Load only the optional skills relevant to that division.

## Select optional guidance

- `google-agents-cli-adk-code`: installed ADK interfaces and reference recipes.
- `google-agents-cli-scaffold`: a requested project creation or scaffold change.
- `google-agents-cli-eval`: Agents CLI dataset, trace, metric and result formats.
- `google-agents-cli-deploy`: the adopted delivery mechanism and generated infrastructure.
- `google-agents-cli-observability`: telemetry setup and export destinations.
- `google-agents-cli-publish`: requested Gemini Enterprise registration.

Discover these through the coding agent's available-skills catalogue. Read the
selected skill's instructions before relying on it. If an optional collection
is absent, report that limitation and continue work supported by this toolkit;
offer installation only when its capability is needed. This differs from a
missing primary specialist, which the entry skill handles explicitly.

Google's code skill points to its full workflow, including scaffolding and live
evaluation. Honour the user's actual task when combining those instructions.
For a local feature request, complete the local change and report any separate
platform prerequisite. A skill's command example is not authorisation to install
tools, change cloud resources or run paid evaluations.

## Check the combined result

Keep deterministic application checks and real-model evaluations distinct.
Scripted-model Runner tests can verify identity, consent and stored effects;
live evaluations measure model-dependent choices. Agents CLI JSON results and
native ADK evaluation artifacts have different contracts, so verify the producer
and schema before choosing a checker.

Use the existing deployment path and account for each telemetry destination when
those concerns are in scope. Preserve ownership and configuration that the
feature does not need to change. Finish with the actual checks, any workflow
conflict that remains, and the precise prerequisite for unverified work.
