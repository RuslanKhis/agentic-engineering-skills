# Stage promotion and roll back as one unit

Read this when a tested release candidate must reach production traffic gradually and a bad release must leave quickly. First deployment, identity and packaging belong to deploy-adk-on-google-cloud; monitoring during the canary belongs to adk-agent-observability. This reference owns the traffic plan, the sample design and the rollback bundle.

## The rollback bundle

A rollback restores the release unit, not one component:

| Component | Where it is read from | Rollback action |
| --- | --- | --- |
| Image digest (Cloud Run, GKE) or Agent Runtime revision ID | Platform revision | Shift traffic to the previous revision |
| Prompt version and hash | Git commit in the image, or registry label | Same commit in the image, or move the label back; verify the hash in the startup log |
| Model ID and judge ID | Code or configuration in the image, eval config in git | Same commit; if the model is read from an environment variable or secret, restore that version too |
| Tool schema hash | Captured by the scripted-model test | Same commit; confirm the hash after rollback |
| Secret versions | Secret Manager version numbers bound to the revision | Rebind the previous version numbers, never `latest` |
| Eval-set hash and expectations | Git | Informational; the gate that approved the previous release is recorded in its changelog row |

A platform rollback that keeps a new prompt label, a rotated secret or a schema-incompatible data migration is a new, untested state. deploy-adk-on-google-cloud's production reference covers data migrations and in-flight tool operations; rehearse the chosen rollback in a non-production target before relying on it.

## Cloud Run: tagged revision, stepped traffic, rollback

From the Cloud Run rollouts, rollbacks and traffic migration page (https://docs.cloud.google.com/run/docs/rollouts-rollbacks-traffic-migration, fetched 2026-10-07, vendor):

```bash
# 1. Deploy the candidate with no traffic and a tag; it gets its own URL at 0%
gcloud run deploy SERVICE --image IMAGE@sha256:DIGEST --no-traffic --tag canary --region REGION
# 2. Test the tagged URL (https://canary---SERVICE-HASH.REGION.run.app) with the bounded live tier
# 3. Step traffic
gcloud run services update-traffic SERVICE --to-tags canary=5 --region REGION
gcloud run services update-traffic SERVICE --to-tags canary=25 --region REGION
gcloud run services update-traffic SERVICE --to-latest --region REGION
# Rollback at any step
gcloud run services update-traffic SERVICE --to-revisions PREVIOUS_REVISION=100 --region REGION
```

The page states that in-flight requests complete on the revision that received them during a traffic migration, so a rollback does not cut sessions mid-turn, and that `--to-revisions` can name any retained revision. `adk deploy cloud_run` (2.8.0) exposes `--project`, `--region`, `--service_name`, `--app_name`, `--port`, `--adk_version` and related options and no traffic or tag options (verified in `cli/cli_tools_click.py`), so a tagged canary uses `gcloud run deploy` on the image `adk deploy` built, or a Dockerfile path; the adk-docs Cloud Run page documents both routes. Deploy by digest, not by tag, so the rollback target is the artefact that was tested.

Google's `agents-cli` deploy skill (v1.8.0, fetched 2026-10-07, vendor) gives the same `update-traffic` rollback for Cloud Run and a three-stage pipeline (PR CI, staging CD with load test, production CD behind a GitHub environment approval; `infra cicd --cicd-runner github_actions|google_cloud_build`). Reuse that pipeline shape; add the eval gate tiers and the manifest to it.

When the steps should advance without hand-run commands, Cloud Deploy's canary strategy for Cloud Run (https://docs.cloud.google.com/deploy, canary page dated 2026-10-05, vendor) sets `automaticTrafficControl: true`, `canaryDeployment.percentages` such as `[25, 50, 75]`, and `verify`, `predeploy` and `postdeploy` tasks, advancing with `gcloud deploy rollouts advance`. Put the tier-2 eval in the `verify` task so a phase cannot advance without evidence.

## Agent Runtime: revisions and manual traffic split (Pre-GA)

From the Agent Runtime revisions and traffic page (https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/manage-revisions-and-traffic, page updated 2026-10-07, vendor; **Pre-GA, `v1beta1` API**):

- Creating an agent or updating its versioned fields (the package, deployment and source-code specs and the agent framework, per the page) creates an immutable revision; updating unversioned fields changes all revisions at once. Know which of your fields are versioned before relying on a revision as a rollback target. `adk deploy agent_engine --agent_engine_id` updates an existing resource (2.8.0 option verified), so under this model each such update that touches a versioned field is a new revision.
- `traffic_config` is either `trafficSplitAlwaysLatest` (default: 100% to the newest revision, so every update is an immediate full rollout) or `trafficSplitManual` with targets of revision name and percent that sum to 100 and may only name Active revisions; naming an archived revision returns `FAILED_PRECONDITION`.
- Archived revisions are permanently retired and cannot be restored. Limits are 950 revisions per agent and 6,000 per project per region, not adjustable; the platform removes older revisions automatically (a keep-n-latest garbage-collection strategy, default 100 per the page) and only Active revisions at 0% traffic are eligible; creation fails when no revision is eligible for removal. Pin the rollback target's retention before promotion, and keep the previous revision at a non-zero share or inside the keep window until the canary completes.
- Changing an Agent Gateway binding archives every existing revision; treat a binding change as a release with no rollback target.
- A single revision can be queried directly (`runtimeRevisions/REVISION_ID:query`), bypassing the split; this is the official path for shadow and canary tests before the revision receives traffic.
- The page recommends tracking the revision number as metadata in logs; put it in the startup log beside the prompt hash and model ID.

Set a manual split before the first production update, otherwise "always latest" promotes every update to 100%. A manual split keeps both revisions warm, so size `min_instances` and `max_instances` for two revisions during the canary (Google staff on the developer forum, 2026-07-06, community; the same thread says `agents-cli` does not expose traffic splitting yet). The `agents-cli` deploy skill (v1.8.0, fetched 2026-10-07) still says "Agent Runtime doesn't support revision-based rollback"; the Google page dated 2026-10-07 documents revisions and traffic splitting as a Preview feature. Treat the skill text as stale and the feature as Pre-GA: rehearse it in a non-production project, keep "fix and redeploy" as the fallback, and expect the API to change.

## GKE

Use the deployment's rollout history and `kubectl rollout undo` for the image; the prompt, model, schema and secret components follow the same bundle rules. deploy-adk-on-google-cloud covers the GKE specifics.

## Shadow and A/B sample design

- **Shadow**: send a copy of sampled production requests to the candidate revision's tagged URL or revision query endpoint with tool writes disabled or pointed at a sandbox; compare trajectories and final responses offline. Shadow traffic must never execute a real write twice; safe-api-tool-calls' idempotency contract applies.
- **Canary A/B**: with traffic at 5% then 25%, compare the candidate against the stable revision on the same metrics the nightly judge reports, plus error rate, p95 latency and cost per request. Decide the minimum sample and the duration before the first step (hours at low traffic may be too few requests to see a 2% regression). Record the stop rule.
- **What the sample cannot show**: holdout quality, rare-case regressions and judge-calibrated quality; those come from the gate and the nightly run. Online comparison confirms the offline result; it does not replace it.

Hand sampling, metric collection and alert thresholds to adk-agent-observability; this reference decides what is compared and when traffic moves.

## Approval points

Deploying with `--no-traffic`, creating a revision and querying it directly are low-risk and still name the project and resource. Every traffic change, archive, secret rebind and production deploy is presented with the exact command, revision names, percentages and the rollback command, and waits for approval. Reuse an approval that already covers the exact step.

## Completion

The rollback bundle for the current production release is written down with version numbers and hashes; the candidate was tested at 0% traffic; traffic moved in recorded steps with a stop rule; the rollback command was rehearsed on a non-production target; Pre-GA surfaces are labelled as such in the release record.
