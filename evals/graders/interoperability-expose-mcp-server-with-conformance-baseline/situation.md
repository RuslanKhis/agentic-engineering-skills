# Situation: interoperability-expose-mcp-server-with-conformance-baseline

Standalone project: one LlmAgent (`research/agent.py`) with two tools, pyproject pins mcp>=2,<3
and google-adk 2.12.0, a scripted model (`tests/scripted_model.py`, needs the SDK; its Runner test
is skipped without it), CI with Node 22 and no credentials. No MCP server code yet (A1: to_mcp_server
over streamable HTTP, commit the tool manifest from the inventory helper, description a capability
statement without the instruction; A2: pinned conformance command with --requirements and an
expected-failures baseline with reasons, scripted model; A3: baseline entry that starts passing
exits 1, PR tier; A4: do not widen with fixture tools/resources/prompts, approval gate not
satisfiable by an MCP host). The agent has no shell, so nothing can be run.
Context unchanged.

Changed on 28 October 2026 (Phase 11): A1 now carries its own no-shell escape in the assertion text, because judges graded the run step literally despite the note above. In a run without a shell, credit naming the inventory helper command that produces the manifest and reporting the manifest as not generated; a claim that the step ran, with no output to show for it, is still a FAIL.
