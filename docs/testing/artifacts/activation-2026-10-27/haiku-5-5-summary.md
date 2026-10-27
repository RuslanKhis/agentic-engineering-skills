Activation run: backend claude-cli, model claude-haiku-5-5, 114 cases x 1 repeat(s)
catalogue 0d93b63db2ea4b1a  corpus f51ed02934672ec3

| Run | PASS | PARTIAL | FAIL | ERROR |
| --- | --- | --- | --- | --- |
| repeat 1 | 111 | 1 | 2 | 0 |
| all | 111 | 1 | 2 | 0 |

Cases not passing in every repeat:
- engineer-positive [adk-engineer, positive] FAIL: primary adk-memory-architecture; supporting adk-frontend-integration,adk-agent-instructions. Remembering a customer's preferred language across sessions is agent memory work, while showing responses in the web app touches the frontend contract and the instructions may need to use the stored language.
- practice-profile-host-memory-near-miss [practice-profile, near-miss] FAIL: primary practice-profile; supporting -. Recording a standing preference across projects is a practice-profile remember action, although the request names the coding agent's host memory file, which the skill explicitly excludes.
- tool-interface-toolset-positive [adk-tool-interface-design, positive] PARTIAL: primary adk-agent-interoperability; supporting adk-tool-interface-design. Consuming an MCP server with tool filtering and name prefixes is interoperability work, and tool selection, naming, and result shaping to limit context are tool interface design.
