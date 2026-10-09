I've written the design, the plan with all phases, 13 phase-1 tickets and `REPORT.md`; nothing was implemented or committed. Everything is a draft: you weren't available, so all 18 of my assumptions and every decision that depends on them still need your confirmation.

**Files:**
- `docs/architecture/home-claim-intake.md` — the design, with the assumptions table (A1–A18) at the top
- `docs/plans/home-claim-intake.md` — the plan, covering phase 1, phase 2 and a "later" list
- `docs/tickets/home-claim-intake/G01…G13-*.md` — one ticket per phase-1 goal
- `REPORT.md` — the six sections you asked for

**Profile:** I planned it as a production service, because it serves external customers, handles personal data and writes into ClaimCenter.

**Main design choices:**
- **The model can't create claims.** One ADK agent can only edit the customer's own claim draft.
- **Code builds the summary.** The summary the customer sees comes from the draft, not from model text.
- **Submit runs a separate worker.** Pressing Submit hands the frozen draft to a worker with its own credentials. It records each step so one confirmed submission creates at most one ClaimCenter claim. If the outcome is unclear, it looks the claim up by our reference number or passes it to claims operations.
- **Model:** `gemini-3.8-flash` on an EU Vertex endpoint. The two other current Flash versions retire on Vertex before GA.
- **Hosting:** everything stays in the EU, on two Cloud Run services.

**Cut line:**
- **Phase 1 (G01–G13, to 2026-11-20):** a team member files a claim with photos on staging and gets a claim number from the Guidewire sandbox, with no real customer data. It needs 267–418 of the 690 hours available after a 25% reserve. It finishes in 16.8–26.0 of 30 working days, bounded by the chain G01 → G06 → G12.
- **Phase 2 (G14–G25):** production hardening, a closed pilot with real customers, then GA on 2027-03-09. It needs 332–540 of 1,540 hours. The worst case leaves only about 6 working days of slack, almost all spent waiting on the Guidewire production client and the pilot go decision. Phase 2 goals have no tickets yet; you asked for phase 1 only.

**Checks:**
- **Schedule check:** the designer's script failed both phases on the first run. The security review G13 waited on G06, and GA waited on the pilot quality-iteration goal G22. I fixed the dependencies rather than dropping any minimum safety control, and both phases now pass.
- **Tickets:** they match the plan.
- **Other checks:** the designer's own tests pass (8/8) and the document links resolve.
- **Not run:** nothing that needs `google.adk`, the network, Guidewire or Vertex. There is no application code to test.

**Still open:**
- **Guidewire:** how ClaimCenter prevents duplicate claims, and its endpoints for creating claims and attaching photos. G01 will establish this; I couldn't look it up here.
- **EU availability** of the chosen model and of the data-protection services (G02).
- **Baseline:** current figures for claim call-backs and time to a claim number, from claims operations.
- **Legal:** EU AI Act classification and the wording that tells customers they're talking to an AI.
- **Retention:** how long to keep the submission record and the transcripts.

Next prompt:
```text
/adk-engineer Carry out G01 from docs/plans/home-claim-intake.md.
```