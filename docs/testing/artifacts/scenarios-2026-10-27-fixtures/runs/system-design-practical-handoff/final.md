The design and plan are written, but nothing has been built. Neither the schedule checker nor the independent plan review has been run, so the plan is unreviewed.

## First thing to build locally

**G01**, a streamed chat run with honest failure. It is a FastAPI route through the real ADK Runner, with a scripted model that can fail midway. It also has an in-memory stand-in for the preference store and a test user that fails closed.

I put it first because the stream and failure behaviour is where the unknowns are. One is what ADK stores after a run fails midway. Another is how the React client decides a reply is finished. It needs no cloud credentials, no database and no model key. Saving and deleting the language (G02) is ordinary CRUD, so it follows.

## What I did

I wrote two files:
- `docs/architecture/support-assistant.md` is the design. It has 9 contracts, 10 decisions, a table of 15 assumed answers (nobody could be asked), failure grids, the web security rule table and 8 open decisions.
- `docs/plans/support-assistant.md` is the plan. It has goals G01–G07 for phase 1 (local), coarse goals G08–G13 for phase 2 (live model, Cloud Run, real OIDC, governance), a Later list and a copyable run prompt.

I treated this as an MVP/pilot, with phase 1 local only. The design keeps your constraints and keeps group preferences out of this release. It adds three choices of my own: the agent gets no tools, so it cannot change a preference; the language lives in an application table rather than ADK session state; and the pilot runs on a single Cloud Run instance.

## What I left undone

- **Schedule helper not run.** No shell was available. Phase 1 is about 24.5–43.5 hours by hand, against about 54 usable hours if one part-time developer works 20 days. The run command is in the plan.
- **No independent plan review**, and no tickets.
- **Unconfirmed assumptions:**
  - OIDC details, the existing React app and the existing PostgreSQL instance.
  - The allowance values, model spend cap and language list.
  - The model ID: the lifecycle table that should supply it isn't installed here, so G08 picks it.
  - How ADK handles a mid-stream failure.
  - Whether Cloud Run buffers the stream.
- **Missing skills.** Several skills the plan names are not installed here (for example `adk-fastapi-backend`, `adk-presenter` and `deploy-adk-on-google-cloud`). The plan lists them as setup prerequisites. Matt Pocock's skills are not installed either, and the plan only says how it could feed them.

## Next prompt

```text
/adk-engineer Carry out G01 from docs/plans/support-assistant.md.
Read docs/architecture/support-assistant.md and preserve its accepted decisions.
Use adk-frontend-integration with adk-agent-evaluation.
Work locally only: no cloud, no deployment, no real model calls. Verify A1 to A12
and record actual evidence and remaining blockers in the plan.
```

Request the OIDC details (W1) and model access (W3) now, so they run in parallel with G01.