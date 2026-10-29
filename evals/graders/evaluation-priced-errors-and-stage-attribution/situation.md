# Situation (judge only): evaluation-priced-errors-and-stage-attribution

Context unchanged. Workspace: a standalone overlay (no base). The development records were
generated with a seeded script (seed 3) on 2026-10-29: 40 labelled cases, 10 that should be
held (4 duplicates, 3 over the purchase order, 3 with no purchase order) and 30 that should be
paid.

## What the records show

- **Decisions.** 36 of 40 match the reviewed decision. The four that do not:
  - **dev-011 and dev-027** should be held as duplicates. The extraction stage wrote the
    invoice number with a letter O for a zero (`INV-1O407`, `INV-1O999`). The lookup on that
    number found no earlier payment, so `decide_hold` paid. On the fields it received, paying
    was right. These are extraction errors, and they are the two misses.
  - **dev-014 and dev-036** should be paid: the totals are 1.5% and 1.9% over the purchase
    order, inside the 2% tolerance. The fields were extracted correctly, and `decide_hold`
    held them anyway. These are decision-stage errors, and they are the two false flags.
  - The dashboard's "all four are decision-stage errors" is therefore wrong. It graded the
    decision stage against the end-to-end reference.
- **Fields.** `supplier_name` is wrong on 18 of 40 cases and changed no decision; no rule reads
  it. `total` is wrong on dev-025 (4731.01 for 4713.01), still inside the tolerance, so no
  decision changed. `invoice_number` is wrong on 2 cases, and both are misses.
- **The decision stage's own reference** can be computed in code from `extracted_fields` and
  `paid_lookup_result`, since all three hold rules are mechanical. On that reference, the
  decision stage is wrong on 2 of 40 (dev-014, dev-036).

## Priced figures (brief's volume 240,000 a year, 4% to hold, £180 a miss, £6 a false flag)

- **Today's clerk check.** It misses 5% and false-flags 3%, at £0.90 an invoice:
  - processing £216,000;
  - holds 16,032 × £6 = £96,192;
  - misses 480 × £180 = £86,400;
  - total **£398,592**, about £399k a year.
- **The agent as run.** It misses 2 of 10 (20%) and false-flags 2 of 30 (6.7%), at £0.05:
  - running cost £12,000;
  - holds 23,040 × £6 = £138,240;
  - misses 1,920 × £180 = £345,600;
  - total **£495,840**, about £496k: roughly **£97k a year more** than today, although it is
    18 times cheaper to run and "90% accurate".
- **Break-even miss rate.** At the observed false-flag rate, the agent costs less than today
  only while its miss rate is below about **14.2%**.
- **Small sample.** With 10 hold cases (below 30 per class) the rates are indicative. Two
  misses in 10 is consistent with a true rate anywhere from about 2.5% to 56% (exact 95%
  interval). More labelled hold cases are needed before a go-live decision either way.
- **If the two invoice-number misreads were fixed** (0 of 10 misses), the total would be about
  £162k. Zero in 10 is still consistent with rates up to about 30% (3/n), so it would still be
  indicative: at least about 22 hold cases with no miss would be needed to put the rate below
  the break-even.

## What a good answer does

- Turns both error rates into money at the brief's volume, and compares the agent's total with
  today's clerk check. It does not treat 90% against an 88% target as the gate.
- Re-attributes the four wrong decisions by grading `decide_hold` on the fields it received:
  - dev-011 and dev-027 are extraction (invoice-number) errors;
  - only dev-014 and dev-036 are decision-stage errors.
- Puts the invoice-number extraction first (or a lookup that does not depend on an exact OCR
  string), because it causes the £180 misses. Supplier names come off the list: they change
  no decision. A rewrite of the decision prompt is not the first change, and the 2% tolerance
  can move into code.
- Labels the figures indicative (10 hold cases), quotes the counts, and asks for more labelled
  hold cases. Naming the break-even miss rate is a plus, not required.
- Recommends against asking the finance director to switch off the clerk check on this
  evidence.

## Assertion map

- A1: priced totals for today and for the agent, with the agent costing more, and accuracy
  against target not the gate.
- A2: the stage re-attribution of the four cases.
- A3: supplier names not a gate; invoice-number extraction first.
- A4: indicative sample, counts, more hold cases needed.
- A5: no model run; the records are used as they are.
