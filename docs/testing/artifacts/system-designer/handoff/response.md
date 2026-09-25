Created a draft design and practical continuation plan:

- [System design](/private/tmp/adk-designer-practical-handoff-trial/docs/architecture/support-assistant.md)
- [Implementation goals and copyable continuation prompt](/private/tmp/adk-designer-practical-handoff-trial/docs/plans/support-assistant.md)

**Start with G01:** locally save a response language, restart the backend, apply it in a new conversation through a controlled agent adapter, then forget it. This tests the complete preference path without cloud credentials or an ADK version decision.

The design keeps your agreed stack and individual pilot scope. It specifies owner checks, protection against stale saves restoring forgotten preferences, and explicit completed/failed/interrupted stream states. ADK compatibility and hosted verification are separate goals. Future shared preferences and optional Matt Pocock workflows do not block the pilot.

No application code, installations, external calls, issues or cloud changes were made. All verification in the documents is planned, not executed.
