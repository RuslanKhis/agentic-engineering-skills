# engineer-ends-with-checkpoint-after-contract-delta: what the fixture holds

Original context: "A five-ticket proof of concept (save and forget a language
preference, streamed replies, a journey check, a review presentation). Implementing G01
shows that forgetting must also clear a cached copy in session state, which the design's
C2 does not say, and that forget should be a soft delete kept 30 days. The person says
the work took about six hours against an estimate of 2-3. ADK is not installed."
(Rewritten in the person's voice; facts unchanged.)

Workspace = support-assistant + support-plan bases, no overlay. G01 is `ready`, estimate
total 2-3, contracts C1, C2, SB01; design C2 reads "after forget, the next session does
not use the language" with Evidence `planned: forget test, local`. The design's
Components section says the saved value is copied into session state as
`user:language` — a user-scoped key, so it outlives the session and must be cleared on
forget (the narrowing the person reports).

Expected (A1-A3): `contract_deltas: [C2: forget also clears the user:language copy in
session state]` in G01's front matter; a `Rulings:` entry for the 30-day soft delete
with why and cost if wrong; design's C2 invariant text not edited; `actual: 6 h`;
design Evidence cells updated only for contracts evidenced (C1, C2 if their tests were
written and counted as evidence at the tier achieved); plan_status.py run or reported as
not run (no shell); final prompt is `/adk-system-designer Checkpoint docs/plans/support.md`
naming the C2 delta and the ruling (6 h vs 2-3 h also pushes phase hours, 14 h capacity),
not the G02 prompt. google-adk is not installed: SDK-dependent tests reported as not run.
