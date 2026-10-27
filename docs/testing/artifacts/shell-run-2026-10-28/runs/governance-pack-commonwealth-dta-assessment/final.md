I've drafted the pack, and the checker passes on all nine documents with no errors or warnings. Nothing is sent or signed. Every sign-off is `pending`, and the plan marks G05 "drafted, not sent".

## Where the files are
Everything is in `docs/governance/claims-triage/`:
- `regulatory-memo.md`
- `privacy-impact-input-pack.md`, for the privacy officer's PIA. James Whitlam is the reviewer.
- `impact-assessment.md`, which includes the DTA inputs
- `system-card.md`, which carries the APP 1.8 disclosure facts
- `security-questionnaire.md`, for Anita Desai
- Four draft-answer documents (`government-form-answers-*.md`): the DTA impact assessment tool, the transparency statement inputs, the use case register row and the agentic addendum. These are not the official forms. The CCO's officers complete and approve them in the official tool.

I also edited `docs/plans/claims-triage.md`. I added W3 (DTA assessment approval before deployment), W4 (a conditional AI Review Committee referral) and W5 (APP privacy policy entries). I also added a G05 evidence block.

## Regimes in scope
- **Australia only:** the CCO is a non-corporate Commonwealth entity and the claimants are Australian residents.
- **United States, EU, UK, New Zealand, Singapore and Canada are out:** there is no client, data subject or processing link to any of them. Claimants' residence is not recorded, so this is an assumption for counsel to confirm.
- **No transfer annex or Article 30 records:** neither applies to an Australia-only pack.

## Main obligations (all `counsel_required: yes`)
- **APP 1.7 to 1.9:** the automated-decision entries in the privacy policy apply from 10 December 2026. That is two days after the pilot decision on 2026-12-08.
- **Privacy impact assessment:** required if this is a high privacy risk project under the Agencies Privacy Code (W2). It is counsel's call.
- **DTA AI impact assessment:** due to begin by 15 December 2026 and to be finished before deployment (W3). I proposed an inherent rating of high and a residual rating of high as `assumption:` only. The agency sets the ratings.
- **Sensitive information and Gemini:** APP 3.3 and APP 11 for health, mental-health and family violence information, and APP 8 for the Gemini endpoint.

## Counsel questions that block the pilot decision
- Is triage "substantially and directly related" to a decision that significantly affects claimants (APP 1.7)?
- Is officer review "extensive human oversight", given automation bias is a named harm and no pilot override figure exists?
- Does the CCO's legislation authorise automated triage?
- Is the Gemini endpoint a use or a disclosure (APP 8)?
- Does the contract carry s 95B terms, and who notifies a data breach?
- APP 6 for re-using past decisions as the evaluation set.

## Gaps and the goal each needs
- **Gemini model page not read** (no network allowed): retirement date, processing region, training use and abuse-monitoring retention are all unknown. Goal for `adk-model-and-output-contracts`.
- **No sensitive-data screening evidence** on prompts or logs. Goal for `protect-adk-sensitive-data`.
- **Retention is undecided** for the decisions table and the evaluation set, and there is no access or correction path. Goal for the design owner.
- **No pilot measures:** override rate against the 11% baseline, review depth, group-level fairness and under-prioritising errors. M2 is 79%. Goal for `adk-agent-evaluation`.
- **No incident procedure, kill switch, monitoring, call caps or encryption facts.** Goal for `adk-release-engineering`.
- **No officer training, claimant notice, contest route or consultation** on the record.
- **Official DTA pages not re-read:** I used the crosswalk's versions, checked 2026-10-26.

## Questions I could not ask, and what I assumed
- **Who the agency's officers are:** the assessing officer, approving officer, use-case owner and the CCO's enabling Act. I left these as `agency:` items.
- **Where claimants live:** I assumed none are outside Australia.
- **Consultancy home:** I assumed Australia, per D4.

## Waits to schedule
- **W5 (privacy policy entries):** needed before 10 December 2026, so it is the tightest.
- **W3, W4 and W2:** needed before the pilot deploys. W1 (IRAP) is booked for 2026-11-16.
- **No pilot-approval goal yet:** the plan has no pilot-approval goal, so W1 to W5 aren't attached to anything. Add them to that goal's Depends on when it exists.

## Next step
```text
/adk-presenter Prepare the pilot-decision presentation for the CCO executive board (2026-12-08) from docs/plans/claims-triage.md; cite docs/governance/claims-triage/system-card.md for limits and oversight, and show the open counsel questions and W1 to W5 as risks.
```