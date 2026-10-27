I have not fixed the refusal. I can't reproduce it here, and the code you described should not cause it.

**Which protocol version you're on**
- The packages are AG-UI 1.0: `ag-ui-protocol` 1.0.0, `@ag-ui/client` 1.0.2 and CopilotKit 1.79.0.
- The approval contract in use is the older tool-message one, not the 1.0 interrupt/resume one. `useHumanInTheLoop` answers `adk_request_confirmation` with a `role: "tool"` message. `app/agui.py` leaves `emit_interrupt_outcome` at its default of `False`.
- The 1.0 contract would end the run with an interrupt outcome and need an answer through `resume` (`useInterrupt`). You aren't using it.

**Why I couldn't fix it**
- With the flag off, the backend shouldn't report interrupts, so `@ag-ui/client` 1.0 shouldn't block your next message. Something doesn't match, and I couldn't tell what.
- Two things could explain it. The installed `ag-ui-adk` may differ from the 0.9.0 pin, or the backend may actually be emitting an interrupt outcome.
- The SDKs aren't installed here and there's no network, so I couldn't check either.
- To find out, record one paused refund run and look at its `RUN_FINISHED` event. An `outcome` of type `interrupt` means the backend is on the other contract. Also run `pip show ag-ui-adk` in the deployed environment.

**What I changed**
- `app/agui.py`: the tool-message contract is now explicit, with `EMIT_INTERRUPT_OUTCOME = False` passed to `ADKAgent`. This doesn't change behaviour. The risk it removes is a later default change or edit breaking the frontend without anyone noticing.
- `tests/test_agui_contract.py`: asserts the flag is `False`. It skips when the SDK isn't installed. I didn't run it.
- `docs/tickets/support/G06.md`: added the declared contract and the open question above.

I didn't touch the web app, since `useHumanInTheLoop` is correct for this contract. A2 and A3 remain unticked and unverified.

**Undone**
- Wire-level tests: flag off, a tool message resumes the run; flag on, a tool message returns `INTERRUPT_RESUME_REQUIRED`. I couldn't write these without the SDK.
- Checking that the refund runs once on Approve and not on Decline.

**Unrelated security issue**
- `user_id_extractor` in `app/agui.py` reads `userId` from the client's `forwarded_props`. That breaks the `AGENTS.md` rule that the user ID comes from the verified principal.
- I left it alone because it's a separate change, but fix it before the pilot.

**Assumption:** I assumed the tool-message contract is the one you want, since you described the frontend that way.