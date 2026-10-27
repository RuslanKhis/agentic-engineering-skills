I wrote the portability assessment for the CTO and set G07 to `verified_local`. The skill's check script passes against the design and plan with no warnings, and the design file hash is unchanged. Martin Cole hasn't read it yet.

**Where things are**
- **Assessment:** `docs/portability/claims.md`, status draft.
- **Ticket:** `docs/tickets/claims/G07.md` now has its Evidence filled in, including the design hash before and after.

**What the assessment concludes**
- **Recommendation:** keep GCP and ADK as built, hold an exit plan, and add no second provider and no new abstraction layer. Nothing in the design records a move date or trigger.
- **Components:** all 13 are classified: 1 shared logic, 3 replaceable adapter, 2 provider-specific by choice and 7 expensive dependency. The expensive ones are Memory Bank, sessions, Vertex AI Search, Firestore, Gemini, Identity Platform and the ADK agent wiring.
- **Comparison:** AWS, Azure and LangGraph are compared against the current build.
- **LangGraph:** it would rewrite orchestration, callbacks, sessions and tests. It doesn't remove any of the Google data or model dependencies.
- **Effort:** sizes are relative only. A whole move is large. Identity and the spend cap are marked "unknown; needs a spike".

**Assumptions I proceeded on** (each is also an open question in the document)
- The CTO's concern is exit cost, not a planned move, so this is an exit plan and not multicloud.
- Open sessions can be dropped at a move.
- The ADK 2.12.0 versus 2.13.0 difference doesn't change any classification.
- The items the design doesn't record (observability, IAM layout, secrets, CI) aren't a dominant cost.

**Not done**
- **No web access:** every source row carries the skill reference's 2026-10-26 read date, and I re-read nothing at its source. Several claims stay `unverified`, including Gemini's absence from the live Azure catalogue and ADK reaching Bedrock or Azure through `LiteLlm`.
- **Not code-checked:** `google-adk` isn't installed here. Only `claims/agent.py` and `claims/tools.py` were inspected, and the rest of the baseline is marked design-only.
- **Gap found, no ticket:** the plan has no frozen evaluation set, which a model swap would need. The evaluation specialist isn't installed here, so I recorded it as an open question and made no recommendation block.
- **Human hours:** the `actual:` line in the ticket is left for the owner to fill in.
- **Acceptance:** the owner sets `done` after Martin Cole's read.

**Next prompt**
```text
/adk-engineer Carry out G03 from docs/plans/claims.md. Read
docs/architecture/claims.md, use the goal's primary and supporting skills,
verify its acceptance cases locally and record evidence in its ticket.
```