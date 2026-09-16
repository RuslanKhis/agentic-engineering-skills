I’ve turned the practical engineering guidance from my upcoming book into 12 open-source skills for Claude Code, Codex, Google Gemini CLI and Antigravity.

They help your coding agent build and improve applications using Google ADK and Google Cloud.

Install the toolkit, open your project, and describe the change you need:

/adk-engineer Add memory so my agent remembers a user’s preferences across sessions.

/safe-api-tool-calls Make this refund tool handle timeouts without issuing the same refund twice.

/adk-agent-evaluation Add tests that check which tools my agent calls and what actually happens.

In Codex, use $ instead of /. In Gemini CLI, say “Use the adk-engineer skill to…” and describe your request. You can also ask for skills by name in Antigravity.

There’s one entry point, adk-engineer, and eleven specialists covering workflows, API calls, guardrails, deployment, performance, frontend integration, memory, evaluation, sensitive data, authentication and SQL agents.

The collection includes implementation recipes, reusable helpers, failure scenarios and checks your coding agent can run against the code it changes.

We tested installation and code generation through real Claude Code and Codex sessions. The current revision passed 476 repository and SDK checks; two generated examples passed another 71 tests after independent review and repairs.

We also tested Antigravity IDE with Gemini: it used the API-safety skill to repair a local adapter and passed 21 project tests plus nine independent checks. All twelve skills are discoverable in Gemini CLI; code generation through that CLI still needs a separate run.

You can use the skills without reading the book first. They’re free, MIT-licensed, and designed to work in your own projects.

Explore the skills and installation instructions:
https://github.com/RuslanKhis/agentic-engineering-skills

The book explains the engineering decisions behind these practices: Agentic Engineering: Building Production-Grade Multi-Agent Systems with Google ADK on GCP.

#AIEngineering #GoogleADK #GoogleCloud #AgentSkills

Preorder the book on Amazon: [AMAZON PREORDER LINK]
