# Decision memo: campaign shopping assistant, proof of concept review

One page, sent before the meeting as the pre-read and after it as the record.
Everything here is in the deck's evidence; nothing new appears in a memo.

**Decision requested:** choose between stopping, extending the pilot with the two missing safeguards at a larger share of sessions, and building for production now; we recommend extending the pilot.
**Deadline for the decision:** to be confirmed (not in the record). The refund evidence for the run is complete on 18 November; the extension waits on this decision.
**Owner:** Larkspur Digital, for Clare Hollis (decider).

## What we found

Three of the four success criteria agreed on 26 August are met. Checkout completion was 4.2% on 312 assistant sessions against a 3.6% threshold (M1); catalogue answers matched on 96.5% of 200 test questions against 95%, measured on build v0.3.2, not the live v0.4.0 (M3); spend was £386 against £1,500 (M5). Refunds were not met on the point estimate: 1 of 13 assistant orders, 7.7%, against 6.4%, with 30 days not yet elapsed for most orders (M4). The lift is within chance: sessions without the assistant on the same campaign completed at 3.4% (M2), and 13 checkouts give a plausible range of roughly 2.5% to 7.0% (our estimate). Two acceptance cases were not run: the delivery-service outage fallback (G02/A3) and hiding the assistant at £60 a day (G03/A3). Not measured: value in pounds, production running cost.

## Options

| Option | What it means | Cost (hours, money) | Risk | Recommendation |
| --- | --- | --- | --- | --- |
| A. Extend the pilot | Larger share of campaign sessions; deliver G02/A3 and G03/A3; re-run accuracy on v0.4.0; re-measure refunds | Hours not estimated; we estimate about £284 per three weeks at the same 10% share, rising with the share | Refunds may stay above 6.4% | Recommended: it is the only option that settles the open criterion |
| B. Build for production now | Every campaign page; account area undecided (D5) | Not yet estimated | Refunds unproven; safeguards untested; account area conflicts with D3 | Not recommended |
| C. Stop | Keep code and test set | £0 further | Forfeits an encouraging, unproven result | |

## If approved

- **Scope:** same campaign landing pages; storefront flag for the spend stop (storefront team), outage test double and G02/A3 (Larkspur Digital), accuracy re-run on v0.4.0. Share of sessions: to be chosen by the decider.
- **Success criteria for the next review:** proposed, not yet agreed: S1 to S4 as agreed on 26 August, with refunds measured over 30 days on a sample the decider judges large enough, and checkout completion compared with the same-campaign control (M2).
- **Kill criteria:** proposed, not yet agreed: refund rate on assistant orders above 6.4% on the larger sample.
- **Next review:** to be set; first checkpoint 18 November (refund window of the run closes).

## Decision record (filled after the meeting)

| Decision | Owner | Date | Conditions |
| --- | --- | --- | --- |

Open questions raised, with who answers each and by when.
Open decisions carried: D6 (agency edits to campaign briefs), owner Clare Hollis.
