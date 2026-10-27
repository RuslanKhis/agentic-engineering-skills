# Situation: interoperability-consume-enterprise-mcp-server-registration-and-sso

Overlay on support-assistant: pyproject pins mcp>=2.1,<3; vendor note with AS metadata supporting
CIMD, DCR endpoint, iss parameter and JWT bearer grant, server revision 2026-07-28 (A1, A2, A3);
recorded tools/list with a name containing spaces and a name longer than 64 characters, a
`pattern`/`minimum`/`additionalProperties` that ADK's conversion may drop, and a server-minted
`adjustment_handle` (A4); security requirements (no DCR, no consent screens); ticket T-48 for
recording the mcp major version and revision. No network or credentials. Context unchanged.
