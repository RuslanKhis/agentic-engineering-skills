I wrote the rollout pack, but I could not run its check script because Bash is disabled in this session. The pack is not ready until `check_rollout.py` passes. Please run this from the project root:

`python3 .claude/skills/adk-presenter/scripts/check_rollout.py --pack docs/rollout/claims/rollout-pack.md --design docs/architecture/claims.md`

I wrote it against the check's rules: every will, won't and hands-over line cites a contract (C1–C7), and all three audiences have a message. I have not run it, so fix whatever it flags.

The pack is at `docs/rollout/claims/rollout-pack.md`. It has the assumptions and gaps table, the will/won't table, the user guide, a quick-reference card, a training plan, and messages for the sponsor, middle managers and frontline users. It also has the AI disclosure text, adoption metrics, the feedback channel and the hypercare exit test.

**Open questions, and what I assumed**
- **Go-live date:** "two weeks" from today is 11 November, but the plan says 10 November. I used the plan's date. Helen Okafor settles it.
- **Release build:** the plan names no go-live build. I assumed v1.2.0, the build behind M2 and M3. M1 was measured on v1.0.3.
- **Training slots:** the brief allows 45-minute sessions on Tuesday and Thursday afternoons, so I used those. The managers' session is tomorrow (29 October), which may be too short notice.
- **Hypercare exit thresholds:** these are not agreed with Helen Okafor, so the test is marked `Status: proposed`. Only the 9% re-routing limit comes from the record. The 80%, 15% and 70% figures are my proposals.
- **Feedback scale:** I assumed a -1/1 thumbs scale for the "report a problem" control. The design only says it writes a feedback record.

**Left undone, with who settles it**
- **Operations handover:** there is no document yet (G13 is in progress), so the support tiers are assumed defaults. The Fenwick IT lead and Tom Reid settle this.
- **Go-live decision:** it is not recorded in the plan. Helen Okafor settles it.
- **Dublin evidence:** M2 and M3 cover Leeds only, and Dublin is marked "not yet measured". Larkspur Digital and the claims MI analyst settle this.
- **Retention period:** it is not in the record, so the "Your data" section does not state one. Tom Reid and the Fenwick data protection lead settle it.
- **Disclosure:** the status is `applies`, because Dublin handlers are EU users. Who counts as provider, and whether Article 50(2) machine-readable marking covers edited drafts, are marked `verify` for counsel.
- **Team-only figures:** whether adoption figures are shown per team and not per person is unrecorded. The manager message asks Helen Okafor to confirm.
- **Support contacts:** names and numbers are not in the record, so the card uses roles.
- **Not produced:** the split-out guide and card for distribution, and the guide's sign-in link. Larkspur Digital needs to supply that link.

Before sending, read the guide aloud to one frontline handler.

**Next goal:** G13, the operations handover to Fenwick IT, which would close the support-tier gap. Agreeing the hypercare exit thresholds with Helen Okafor before 10 November is the other gap that blocks the hypercare end date.