# Operations handover: claims-intake

Status: **draft**, not yet accepted by Kestrel (acceptance: <Kestrel role> on <date>)
From: Brightlane (agency) · To: Kestrel IT operations
Release in production: `claims-intake` 1.2.0 (`pyproject.toml`); build tag not recorded in the repo (see Q3)
Hypercare: <start> to <end> (not stated anywhere in the repo; see Q1). Tier 3 moves from Brightlane on the takeover date, 2026-11-17 (`README.md`), unless a support contract says otherwise.
Built from: no design, plan or rollout pack exists in this repository. Everything below is taken from `README.md`, `claims_agent/`, `deploy/deploy.sh`, `monitoring/` and `docs/operations/access.md`.

Evidence labels: every item is `offline` (read from files in the repo, nothing run against the project) unless stated. Nothing here was checked against the live project `kestrel-claims-prod`. Items marked `unverified: from the repo` need someone with project access to confirm.

## 0. Blockers before 2026-11-17

1. **The pinned model may already be retired.** `claims_agent/agent.py:8` pins `gemini-2.5-flash`. The adk-agent-evaluation compatibility note (read 2026-10-22) states that this model **retired on Vertex AI on 2026-10-20**. The service uses Vertex (`GOOGLE_GENAI_USE_VERTEXAI=true`, `deploy/deploy.sh:8`). I could not check the provider's lifecycle page (no network) and the `adk-model-and-output-contracts` lifecycle table is not installed. `refresh before relying`. Someone with access must, today, (a) read the Vertex model lifecycle page, (b) send a real request to the service and see whether it answers. If retired, the service is failing now and the 5xx alert below goes to Brightlane, not Kestrel. Choosing the replacement model is a Tier 3 change that needs an evaluation re-run first; none exists in the repo (section 1).
2. **Every alert goes to a Brightlane mailing list.** Both policies use channel `8812`, `oncall@brightlane-agency.example` (`monitoring/notification-channels.json`). After 2026-11-17 nobody at Kestrel is told. Add a Kestrel channel to both policies and verify with a test notification before the takeover date.
3. **No alert for stopped telemetry, and no quality alert.** See section 4.
4. **Brightlane holds Owner on the project** (two named users) and the repository admin role, and rotates the secret (`docs/operations/access.md`). Section 6 lists the transfer.

## 1. What the agent must never do, and how that is checked

Only one behavioural rule is written down, in the instruction (`claims_agent/agent.py:10-11`). No design document names contracts, so the rest of this table is **proposed, for Kestrel to accept or change** (see Q2).

| Contract | Invariant | Enforcement | Evidence and how to re-run it |
| --- | --- | --- | --- |
| C1 | Never promise a payout | Prompt text only. No tool, callback or gate enforces it. | **None.** No evaluation exists. `tests/test_policy.py` covers `check_cover` only (`python -m unittest discover -s tests -t .`; two tests, not run this session). |
| C2 (proposed) | Cover statements come from `check_cover`, not from the model's memory | Prompt text only | None |
| C3 (proposed) | No personal data of policy holders in logs or traces | Not configured. Content capture gates are unset, so the ADK 2.12.0 defaults apply (`unverified`). | None. Policy belongs to protect-adk-sensitive-data. |

Note: `check_cover` reads a hard-coded dictionary with one synthetic policy (`claims_agent/policy.py:4`). The secret `policy-api-token` is injected as `POLICY_API_TOKEN` but nothing in `claims_agent/` reads it. Either a policy API call is not yet wired (so the deployed agent cannot check real cover), or the code in production differs from this repository. Confirm which (Q4).

## 2. System map

| Item | Value | Source |
| --- | --- | --- |
| Host | Cloud Run service `claims-intake`, europe-west2 | `README.md`, `deploy/deploy.sh` |
| Project | `kestrel-claims-prod` | same |
| Ingress / auth | `--no-allow-unauthenticated`, ingress `internal-and-cloud-load-balancing` | `deploy/deploy.sh:5` |
| Runtime identity | `claims-intake@kestrel-claims-prod.iam.gserviceaccount.com` (no key files referenced) | `deploy/deploy.sh:6` |
| Secret | `policy-api-token`, mounted as env `POLICY_API_TOKEN`, version `latest` | `deploy/deploy.sh:7` |
| Model | `gemini-2.5-flash` via Vertex AI, **alias without a version suffix** | `agent.py:8`, `deploy.sh:8` |
| Judge model | none (no evaluation) | n/a |
| Framework | `google-adk==2.12.0`, Python >= 3.11 | `pyproject.toml` |
| Tools | `check_cover` (local function) | `agent.py:13` |
| Session store | No `SESSION_SERVICE_URI` in `deploy.sh`, so ADK's default applies. If that is in-memory, sessions vanish on instance restart and scale-down, and "alert to session" debugging fails. `unverified: from the repo` | `deploy.sh` |
| Telemetry | No `OTEL_*`, `ADK_*` or `--otel_to_cloud` setting in the repo, and no Dockerfile or entrypoint shown (`--source .` builds it). Whether traces, ADK metrics or content capture are on is `unverified`. | `deploy.sh` |
| BigQuery analytics, log sinks, dashboards | None in the repo; none known | n/a |
| Containers / Dockerfile / start command | Not in the repo | n/a |

## 3. Support tiers and RACI

| Tier | Who | Handles | Hours |
| --- | --- | --- | --- |
| 1 | Kestrel service desk | User reports, known issues, triage | <Q5> |
| 2 | Kestrel IT operations | Alerts, runbook actions, access, quota, cost alerts | <Q5> |
| 3 | Brightlane until 2026-11-17 (or until the contract ends, Q1), then Kestrel's ADK engineers (not yet named) | Code, prompt, tool, model changes; root cause | <Q5> |

Severity table (proposed, to accept):

- Sev1: an outside action or payout promise to a claimant, personal data exposure, full outage.
- Sev2: quality drop past a threshold, partial outage, a wrong output that reached a customer.
- Sev3: one wrong draft caught by the handler, single reports.

Response targets per tier: **to be set by Kestrel** (Q5). None are invented here.

R = responsible, A = accountable (exactly one), C, I. **Proposed assignments, all unconfirmed.** Names of people are blank because the repo names none on the Kestrel side. "Product owner" and "DPO" roles need Kestrel to name them.

| Activity | Service desk | Kestrel IT | Brightlane | Kestrel product owner | Kestrel DPO |
| --- | --- | --- | --- | --- | --- |
| Sev1 incident response | I | **A**, R | R (until takeover) | I | C |
| Release and rollback | I | **A**, R | R (until takeover), C after | C | |
| Model migration before retirement | | C | R | **A** | |
| Evaluation-set refresh | | C | R | **A** | |
| Monthly cost review | | R | | **A** | |
| Quarterly access review | | R | | | **A** |
| Feedback triage | R | C | | **A** | |
| Postmortem and action tracking | I | **A**, R | R | C | C |
| Breach notification decision | | I | I (tells the controller without undue delay) | C | **A** (controller decides) |

Check: each row has exactly one A. The cost review accountability (product owner) and the access review (DPO) are guesses to confirm (Q6).

## 4. Alerts

Both policies are in `monitoring/`. Whether they are deployed and enabled is `unverified: from the repo`; the files show what was designed, not what runs.

| Alert policy | Condition | Severity | Channel | Owning tier | Runbook entry |
| --- | --- | --- | --- | --- | --- |
| claims-intake 5xx rate > 2% for 10 min | `run.googleapis.com/request_count`, `response_code_class="5xx"`, threshold 0.02, 600 s | proposed Sev2 | `8812`, Brightlane on-call (**must move**) | 2 | R1 |
| claims-intake p95 latency > 12 s for 15 min | `run.googleapis.com/request_latencies`, p95 per 60 s, threshold 12000 ms, 900 s | proposed Sev3 | `8812` (**must move**) | 2 | R2 |
| Telemetry stopped arriving | **does not exist** | | | 2 | R3 |
| Quality drop (feedback or Online Monitor) | **does not exist** | | | 2 then 3 | R4 |

Defects in the files (not changed, because the alert definitions are deployed assets and changing them is a Tier 3 decision):

- The 5xx alert is named a "rate" and "2%" but its filter selects only the 5xx **count** series, with no ratio, no denominator and no aggregation. The threshold 0.02 on a count means it fires on essentially any sustained 5xx, and it would not behave as a 2% error ratio. Replace it with a ratio condition (5xx requests over all requests) or rename it to match what it does. Neither has been tested.
- The latency alert has no `groupByFields`, so Cloud Monitoring aggregates in the default way; confirm it is evaluated per service, not per revision, as intended.
- Neither policy has documentation text, a severity label, or a "no data" setting, so a service that stops receiving traffic (or whose requests all fail before reaching Cloud Run metrics) raises nothing.
- The channel is email only. A mailbox is not paging.

## 5. Runbook entries

None has been rehearsed. Each needs Kestrel Tier 2 to rehearse it once before hypercare exit. For debugging steps follow the adk-agent-observability debugging runbook (alert, trace, session, reproduction), keeping the trace, invocation and session IDs at every hop.

### R1 5xx alert

- Symptom: 5xx alert email.
- First check: Cloud Run logs for `claims-intake`; send one test request. First suspect, given section 0: the model call failing because the pinned model is retired or quota is exhausted. Second: the secret or service account.
- Safe actions for Tier 2: roll back to the previous Cloud Run revision (`gcloud run services update-traffic`, Tier 2 has this once it holds the Run Admin role).
- Escalate when: rollback does not clear it in <Q5 target>, or the logs show model errors (needs a Tier 3 model change).
- Approval needed for: changing the model, changing the secret, opening ingress.
- Rehearsed by Tier 2 on: not yet.

### R2 Latency alert

- Symptom: p95 above 12 s for 15 minutes.
- First check: compare with request volume and with model latency in the trace. Check for cold starts and for provider-side slowness.
- Safe actions: roll back; raise minimum instances only after Kestrel finance approves the cost.
- Escalate when: still above threshold after rollback.
- Rehearsed: not yet.

### R3 Telemetry stopped (to create)

- Symptom: no spans or ADK metrics for N minutes while the 5xx and request-count metrics show traffic.
- First check: whether telemetry is configured at all (section 2 shows no setting in the repo), then exporter errors in the logs, then API enablement and writer roles.
- Safe actions: none by Tier 2 beyond reporting; enabling APIs, roles or content capture needs approval and cost estimate.
- Rehearsed: not yet. The test ("fired once in a test") cannot pass until the alert exists.

### R4 Quality complaint (to create)

- Symptom: a handler reports a wrong draft or a payout promise through the route below.
- First check: get the session ID, then the trace, then reproduce (debugging runbook).
- Safe actions: none; escalate to Tier 3 and, for a payout promise, to the Sev1 route.
- **Feedback route:** none exists in the repo. A route must be named before go-live (Q7).
- Rehearsed: not yet.

### Secret rotation

- `policy-api-token`: Brightlane rotates today. After transfer, the Kestrel owner creates a new version, deploys, and checks the service uses it. Because `deploy.sh:7` uses `:latest`, a new version takes effect on the next deployment or revision, not instantly. Names only here, never values.
- Rehearsed: not yet.

## 6. Transfer of access

Starting point is `docs/operations/access.md` (offline). Dates and verification are blank on purpose: none has happened.

| Item | From | To | Date | Verified by new owner | Old access removed and verified |
| --- | --- | --- | --- | --- | --- |
| Project Owner role on `kestrel-claims-prod` | Brightlane (tom@, ines@) | Kestrel IT group (not named) with least-privilege roles | before 2026-11-17 | not done | not done |
| Runtime service account `claims-intake@...` (no key; confirm none was created) | Brightlane-administered | Kestrel IT | | | |
| Secret `policy-api-token` and rotation | Brightlane | Kestrel owner (not named); runtime SA stays accessor | | not done | not done |
| GitHub repository admin | Brightlane | Kestrel | | not done | not done |
| CI secrets | not listed | unknown whether any exist | | | |
| Alert channel 8812 | Brightlane on-call | Kestrel channel added; 8812 detached from both policies | | not done | not done |
| Billing account | Kestrel finance | already Kestrel | n/a | confirm budget alerts exist (`unverified`) | n/a |
| OAuth client, domain, certificate | none in the repo | confirm none exist | | | |

Verification: the new owner performs the action once (rotate the secret, deploy a revision, change a policy channel). `gcloud projects get-iam-policy kestrel-claims-prod` shows the grants. Brightlane keeps no standing access after 2026-11-17 unless the support contract says so, with an expiry (Q1). I ran none of this.

## 7. Recurring ownership

| Task | Owner | Cadence or date | Source |
| --- | --- | --- | --- |
| Model retirement: `gemini-2.5-flash` | proposed: Kestrel product owner (A), Brightlane (R) | **already past: retired on Vertex 2026-10-20 per note, read 2026-10-22** | adk-agent-evaluation compatibility note; lifecycle table not installed, `refresh before relying` |
| Judge model | none | none exists. Any future judge must be pinned; ADK's default judge is `gemini-2.5-flash` | same |
| Evaluation-set refresh | to name | monthly proposed | needs production feedback and a session store that survives restarts |
| Cost review | to name | monthly proposed, first after the first full bill | no cost contract in the repo |
| Feedback triage | to name | weekly proposed | no feedback table exists |
| Access review | to name | quarterly | |
| ADK / dependency pin review (`google-adk==2.12.0`, `google-cloud-secret-manager==2.25.0`) | Kestrel ADK engineers | each release or quarterly | `pyproject.toml` |

## 8. Known limits

| Limit | Trigger that brings it forward |
| --- | --- |
| No evaluation set; C1 unenforced beyond the prompt | before any change to model, prompt or tool; now, because of the model blocker |
| Policy data is a one-record dictionary; the secret is unused by the code | before real claims use real cover checks (Q4) |
| Sessions may be in-memory (`unverified`) | the first incident that needs a session after a restart |
| Telemetry configuration unknown; no content-capture decision | before the first incident review |
| No quality alert, no telemetry-stopped alert, no feedback route | before hypercare exit |
| 5xx alert condition is not a ratio | next alert change |
| Model is an unversioned alias | when choosing the replacement, pin a version the provider documents |

## 9. Incident review

Triggers (proposed, to agree): user-visible degradation past a threshold; any rollback; resolution beyond <target>; a monitoring failure; an outside effect or payout promise the contracts forbid; personal data in an answer, log or trace; a sustained quality drop; harmful output reaching a user; cost overrun past the stop.
Template: `docs/operations/claims-intake/postmortem-template.md`. Reviews go in `docs/operations/claims-intake/postmortems/<date>-<slug>.md`.

## 10. Hypercare exit (operations)

- [ ] Every RACI row has exactly one accountable owner (proposed; Kestrel to confirm).
- [ ] Every alert routes to a Kestrel channel; the telemetry-stopped alert fired once in a test. (Fails today.)
- [ ] Every access row verified by the new owner; Brightlane access removed and verified absent. (Fails today.)
- [ ] Every runbook entry rehearsed by Tier 2. (Fails today.)
- [ ] Model-retirement calendar, evaluation refresh and cost review have owners and dates. (Fails today; retirement date already passed per the note.)
- [ ] The rollout pack's hypercare exit test passed. (No rollout pack exists. Blocker.)

## Open questions and the assumptions used

Nobody was available to answer, so each was written down and assumed.

- Q1 Is there a support contract after 2026-11-17, and what are the hypercare dates? Assumed: no contract; Brightlane access ends on 2026-11-17.
- Q2 Which contracts has Kestrel agreed beyond "never promise a payout"? Assumed: C2 and C3 are proposals only.
- Q3 What build tag is deployed? Assumed: the repo's `1.2.0` is deployed (unverified; `--source .` deploys do not tag).
- Q4 Does production call the policy API? Assumed: the repo is what runs, so cover checks use the one-record dictionary.
- Q5 Hours and response targets. Assumed: none set; left blank rather than invented.
- Q6 Who at Kestrel is product owner and DPO? Assumed: roles exist; names to be supplied.
- Q7 Where do handlers report a wrong answer? Assumed: no route; blocker.
