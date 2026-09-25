I’m using the **adk-system-designer** skill to work through the architecture with you before we code.

The core journey is: someone asks about a customer case, the agent retrieves the records they’re allowed to see, answers from those records, and helps create an escalation. Google ADK and GCP are fixed; the services depend on who uses it and where those records live.

Three decisions will shape the first design:

1. **Who will use the agent?** Customers viewing their own cases, internal support staff, or both? This determines how the backend enforces access to case records.
2. **Where are cases and escalations managed today?** For example, an existing support platform, a database, or a process you haven’t built yet. If you already have a system of record, we should design around it.
3. **What should “create an escalation” mean?** Prepare a draft for a person, submit after that person confirms, or submit automatically under defined rules? This determines the approval and recovery requirements.

Plain-language answers are enough; you don’t need to choose cloud services yet.
