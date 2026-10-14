# Requirements to contracts: before/after measurement · 15 October 2026

The designer already asked for observable invariants, but the word "contract"
meant four things (system promises, provider replay behaviour, model-facing
surfaces, the plan format), requirements and invariants had no IDs, and goals
cited decisions rather than the promises their tests prove. This change makes
the contract the visible, traceable unit between a requirement and its
evidence, and measured the effect against the previous skills.

## What changed

- `adk-system-designer` defines a **contract** as a precise, observable promise
  derived from a requirement, and keeps the word for that meaning: provider
  behaviour is a *provider guarantee*, what the model reads is its *interface*,
  the browser shape is a *protocol*.
- The chain is now requirement → contract → design choice → reason → tradeoff
  → verification → evidence.
- Each critical contract has six fields: invariant, scope, authority,
  enforcement (with the recheck at the effect), failure outcome and evidence.
  Requirements, contracts and decisions are numbered `R`, `C` and `D`.
- Vague requirements are decomposed until each contract has one enforcement
  point; [design decisions](../../skills/adk-system-designer/references/design-decisions.md#decompose-a-requirement-into-contracts)
  has a worked advertiser example. A tightened contract is revised in place
  with its dependants listed.
- The design template's "Guarantees and acceptance" table became "Requirements
  and contracts"; the decision table cites the contracts each decision enforces.
- Plan goals and tickets carry `contracts: [...]`, acceptance cases name the
  contract they prove, and `adk-engineer` records evidence per contract with
  its tier.
- [Delivery profiles](../../skills/adk-system-designer/references/delivery-profiles.md)
  size the contract set: three to five one-line contracts in the compact form.
- `scripts/check_schedule.py --design` reports any contract no goal cites and
  not marked `gap:` or `deferred:`, goals citing unknown contracts, and ticket
  contract lists that differ from the plan (two new offline tests).

## Method

Same method as the [delivery-constraints record](delivery-constraints-2026-10-09.md):
fresh headless Claude Code sessions (`claude -p`, Claude Code 2.1.299, Opus
5.5, `--setting-sources project`) with all twenty skills copied into the
project's `.claude/skills/`, before (commit `57de159`) and after (working
tree). [Runner](artifacts/contracts-2026-10-15/run.sh),
[prompts](artifacts/contracts-2026-10-15/prompts.tsv) and the headless session
rules were identical across conditions.

| ID | Scenario | What it probes |
| --- | --- | --- |
| K1 | Advertiser asset search and campaign buying, one engineer, three-week pilot; a second turn adds territory, flight dates and modification rights | Decomposition, six fields, recheck at the effect, contract revision, goal-to-contract tracing |
| K2 | Afternoon demo of a read-only travel-policy bot, user unavailable | Contracts stay few and small in the compact form |

The assertions were written into [`evals/scenarios.json`](../../evals/scenarios.json)
(`system-design-contracts-*`) before any run. Outputs were packaged as A and
B with the condition randomised; session reports and dot-folders were removed
because they could reveal the condition. A separate blind grader per scenario
scored each assertion 0–2 and five 1–5 dimensions; the
[mapping](artifacts/contracts-2026-10-15/blind_mapping.json) was revealed
after grading. [Outputs](artifacts/contracts-2026-10-15/outputs/).

## Results

The grader preferred the after condition in both scenarios.

| Scenario | Assertions before → after | Dimensions before → after (of 25) |
| --- | --- | --- |
| K1 advertiser pilot | 11/16 → 15/16 | 17 → 22 |
| K2 read-only demo | 4/8 → 7/8 | 18 → 20 |
| **Total** | **15/24 → 22/24** | **35 → 42** |

Points the graders cited:

- **K1 decomposition:** after split "buy campaigns" into quote (C3), payload-
  bound confirmation (C4), at most one order (C5) and status from receipts
  (C6). Before had no status-from-records guarantee and bound the payload only
  in its data table.
- **K1 tracing:** after's contract table had every field with R links and
  tiered evidence; every phase 1 acceptance item cites a contract and the
  schedule helper reported all twelve cited. Before's acceptance items cited
  no invariant, and six phase 1 goals proved no named guarantee.
- **K1 terminology:** before used "guarantee", "invariant" and "contract" for
  system promises, and "contract" again for the model surface and the booking
  API. After used "contract" consistently.
- **K1 revision:** both kept the rights promise's identity and listed
  dependants. After kept the schedule at 19 working days by deferring
  modification requests; before absorbed the change and grew to 29.
- **K2:** after stated five one-line contracts, each with its enforcement
  point, and every goal cited them; before had no contract layer. Neither
  added confirmation, idempotency or recovery machinery.

Effort: before 85 turns, about 35 minutes and $16.00 over three sessions;
after 70 turns, about 33 minutes and $13.59.

## Defects remaining

| Defect | Seen in | Suggested correction |
| --- | --- | --- |
| Length: K1 after was 14,461 words (design 6,645, plan 7,816) against 12,910 before; the design grew by a third. Both K2 outputs were about 1,850 words against the 1,200-word compact form | K1 after, both K2 | Contract tables replace prose and the decision table's rationale rather than add to it; check the reading budget against the profile before handing over |
| Enforcement overclaimed: K2 after's spend contract said "bounded" while enforced by a budget alert, which only observes | K2 after | Enforcement must be able to stop or refuse the violation; an alert or log is evidence, not enforcement |
| One check mapped to several failure cells: K2 after sent unavailable, rejected and rate-limited model failures to a "key unset" test | K2 after | A grid cell's cited acceptance item must exercise that failure |

## What this establishes and what it does not

Two scenarios, one run per condition, one grader each, using assertions
written by the author of the change. It shows the designer now produces a
numbered, traceable contract layer and uses the term consistently, without
adding machinery to a read-only design. It does not establish that the
router records per-contract evidence when it carries out a goal (no
implementation run), activation behaviour (descriptions unchanged, not
rerun) or effects on other profiles.
