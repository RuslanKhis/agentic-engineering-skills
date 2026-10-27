I wrote the portability assessment at `docs/portability/claims.md`, but I couldn't run the checker. The Bash tool is disabled in this session, so A3 is unverified.

**Done**
- **Classification (A1):** I classified every component, citing D1–D6 and the relevant R and C items.
- **Comparison (A2):** I compared AWS, Azure and LangGraph against the current build.
- **Dimensions and strategy:** the doc covers the five dimensions, boundaries, risks, a phased outline and relative effort with no invented figures. The recommendation is to keep GCP and ADK, hold the exit plan, and run no second provider now.
- **Code inspected:** `claims/agent.py` and `claims/tools.py` show Firestore called inside the tool bodies, and no session or memory service wired in yet.
- **Identity risk I found:** the verified `sub` keys both claim ownership (C1) and the Memory Bank scope (C2). A move to a different identity provider breaks R1 and R2 unless `sub` is preserved or remapped.
- **Ticket evidence:** I filled in the G07 ticket's Evidence section and left its status at `ready`.

**Left undone**
- **Checker (A3):** run `python3 .claude/skills/adk-portability-planning/scripts/check_portability.py docs/portability/claims.md --design docs/architecture/claims.md --plan docs/plans/claims.md`. I checked the document against the script's rules by hand, which is not a pass.
- **Design hash:** `design before` and `design after` aren't recorded, since `git hash-object` also needs a shell. The design file was only read.
- **Sources:** there was no web access, so sources carry the skill references' 2026-10-26 read date. Several claims stay marked `unverified`, such as ADK on Bedrock or Azure through `LiteLlm` and Gemini's absence from Azure.
- **Not checked:** the G01 tests weren't in the workspace, so I couldn't see how they fake Firestore.
- **Tick-offs and hours:** I haven't ticked A3 or entered human hours.

**Questions I couldn't ask, and what I assumed**
These are all in the doc's Open questions section.

| Question | Assumed |
| --- | --- |
| Is there a date or trigger for leaving GCP? | None, so this is an exit plan, not multicloud. |
| Would a move keep calling Gemini across clouds? | Not assumed; both shapes are shown. |
| Must in-flight session history carry over? | No. |
| May Memory Bank memories be discarded and rebuilt? | Yes, with consent and erasure records carried across. |
| How many claims, photos and policy versions are there? | Modest volumes. |
| Can `sub` be preserved or mapped? | Unknown, so identity effort is "unknown; needs a spike". |
| Which frameworks to compare? | LangGraph only, since the scope gate names only that one. |

I made no optional recommendations. A frozen evaluation set would be useful, but its specialist skill (`adk-agent-evaluation`) isn't installed here, so I raised it as an open question for the designer.

After the checker passes and the hash matches, the owner can set the ticket to `verified_local`. Then Martin Cole reads it. The next ready goals are G03–G06.

```text
/adk-engineer Carry out G03 from docs/plans/claims.md. Read
docs/architecture/claims.md, use the goal's primary and supporting skills,
verify its acceptance cases locally and record evidence in its ticket.
```