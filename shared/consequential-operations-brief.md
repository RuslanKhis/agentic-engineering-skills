<!--
The short form of consequential-operations for a SKILL.md permissions step. It
links references/operating-rules.md, so it belongs only in a package's SKILL.md;
the skill's own operations and limits follow it there.
carriers: adk-agent-evaluation, adk-agent-instructions, adk-agent-interoperability, adk-agent-observability, adk-agent-security, adk-fastapi-backend, adk-frontend-integration, adk-memory-architecture, adk-model-and-output-contracts, adk-operational-guardrails, adk-release-engineering, adk-sql-agent-engineering, adk-tool-auth-and-secrets, adk-tool-interface-design, adk-workflow-design, deploy-adk-on-google-cloud, optimise-adk-on-google-cloud, protect-adk-sensitive-data, safe-api-tool-calls
-->

Inspection is read-only, and code generation authorises no deployment, paid
call or live test. Before any consequential operation (an API, billing or
quota change, a billable resource, a secret, IAM, a data migration, a
deployment, a deletion, or a paid or destructive test), read
[consequential operations](references/operating-rules.md#consequential-operations),
present the exact scope and limits, obtain explicit approval and end the turn
to wait for it. Cleanup is a separate confirmed operation on resources this
workflow created.
