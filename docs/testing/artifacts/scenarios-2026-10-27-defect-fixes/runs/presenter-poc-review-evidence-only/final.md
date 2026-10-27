I wrote the leadership deck (13 slides plus two appendix slides), a one-page decision memo and a pre-wiring file. I could not run the deck checker because Bash is disabled in this session, so the deck is unchecked.

Files are in `docs/presentations/campaign-assistant/`:
- `production-approval-business.md`
- `decision-memo-production-approval.md`
- `pre-wiring-production-approval.md`

**What the deck says.** The proof of concept met three of the four criteria agreed on 26 August, and I recommend extending the pilot rather than building for production.

| Criterion | Threshold | Measured | Result |
| --- | --- | --- | --- |
| Checkout completion (S1) | at least 3.6% | 4.2% on 312 sessions | met |
| Refund rate (S2) | not above 6.4% | 1 of 13 orders, 7.7% | not met |
| Catalogue answers (S3) | at least 95% | 96.5% on 200 questions | met |
| Spend (S4) | within £1,500 | £386 | met |

- **Refunds:** 7.7% is my own arithmetic from the 1-of-13 record. The sample is too small to say either way, and the 30 days hasn't passed for most orders; the last orders reach it on 18 November.
- **Checkout lift:** sessions without the assistant on the same campaign completed at 3.4%, so the lift over the fair comparison is 0.8 points. 13 checkouts give a plausible range of roughly 2.5% to 7.0%, which is my estimate. The deck says the lift is encouraging but not yet distinguishable from chance.
- **Accuracy test:** it ran on build v0.3.2, but the live campaign ran v0.4.0.
- **Not run:** two acceptance cases, the delivery-API outage fallback and hiding the assistant at £60 a day.
- **Spend:** the run cost about £0.91 per assistant session, which is also my estimate.
- **No demo:** none is recorded, so the deck says so and shows the measured results instead.

**Questions I couldn't ask, and what I assumed:**
- **Decision date:** it isn't in the record, so the deck says "to be confirmed".
- **Spend-stop flag owner:** the storefront team isn't named, so I proposed Raj Patel as the chaser. This needs confirming.
- **Control group:** the plan doesn't say how the 27,600-session control was built. The deck says the record doesn't say, and doesn't claim the comparison is clean.
- **Design and plan disagree:** the design lists the £60 spend stop as evidenced, but the plan records it as not run. I treated the plan as right and left both documents untouched.

**Not measured, so not on any slide as a figure:**
- The value of the lift in pounds.
- Production running cost per month.
- The cost of the extension, beyond "about £284 per three weeks at the same share".

**Left undone:**
- The deck check hasn't been run. The slide and notes word budgets and the spoken-time estimate are unverified, so please run `check_deck.py` before using the deck.
- Nobody has been briefed and no rehearsal has happened. The pre-wiring table says "pending".
- No slides are rendered, only the outline.
- The plan's change records and G05 evidence aren't updated.
- The memo's success and kill criteria for the extension are marked "proposed, not yet agreed".

**Next step:** after the meeting, record the decision in the memo and the plan. If you want a technical version, run `/adk-presenter` for that audience.