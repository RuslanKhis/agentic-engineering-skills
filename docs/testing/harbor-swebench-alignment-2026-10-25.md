# Harbor and SWE-bench alignment — 25 October 2026

Source note: [comparison](../research/harbor-swebench-comparison-2026-10-25.md).

## Changed journeys

`adk-agent-evaluation`, turning an incident into a regression; and
`adk-system-designer`'s ticket template, which gains `pass_to_pass` and
base-commit evidence.

## Fresh-agent trial

A fresh agent with only the skill packages built a git repository for an
ADK 2.12 refund agent: a base commit that refunds twice when the user
confirms twice, and a "fix" that stops the double refund but also deletes
the ownership check. It then added the regression, said when the case
passes, and wrote the follow-up ticket on the designer's template. It
installed google-adk 2.12.0 and pytest; the network was blocked by a
guard it proved raises.

Results per commit (one double-refund regression, two neighbour tests, a
do-nothing control):

| Commit | `fail_to_pass` | `pass_to_pass` | Control | Verdict |
| --- | --- | --- | --- | --- |
| base | failed (2 refunds) | 2 passed | passed | defect reproduced |
| merged fix | passed | foreign-order denial **failed** | passed | not resolved |
| a reference fix (owner check restored) | passed | 2 passed | passed | resolved; test sound |

The agent rejected the merged fix as a cross-customer refund, kept CI red
rather than marking the test expected-to-fail, and wrote a ticket to
restore the denial.

Ease: 3 of 5.

## Frictions and fixes (same day)

1. `pass_to_pass` meant tests in one skill and earlier acceptance items in
   the other. Fixed: one meaning, with test ids when there are no earlier
   tickets.
2. "Base commit" did not fit an incident whose fix had already landed.
   Fixed: the commit that had the defect.
3. A merged candidate that fails `pass_to_pass`. Fixed: a reference fix
   proves the test, the candidate is not resolved, the case stays red.
4. The ticket template assumes a design and plan. Not changed: the
   template belongs to a design-driven plan; an incident follow-up outside
   one fills those fields with none.
5. The evaluation skill never pointed to the ticket template. Fixed.
6. No owner named for a removed ownership check. Not changed: the security
   skill's "Identity never comes from the model" already owns in-tool
   authorisation.
7. No routing row for incidents. Fixed.
8. No network-guard recipe. Fixed.
9. and 10. No way to build a tool context for replay; identity on 2.12.
   Fixed: `ToolContext` is `Context` on 2.12.0 (checked in source) and
   replay goes through the Runner with a scripted model.
11. Expected-to-fail versus red CI. Fixed: leave it red.

## Limits

No live run, CI service or model was used.
