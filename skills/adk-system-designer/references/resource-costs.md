# Resource cost ledger: what charges while idle, and how to prove it is gone

Read before naming a GCP resource. A resource bills per use (requests,
tokens, bytes) or while provisioned (hourly or monthly until deleted). Before
creating a while-provisioned resource, the goal records the idle cost at the
chosen configuration with the pricing date, the cleanup command and the
verification. A deletion returning success starts verification; it does not
end it. Billing reports lag, and dependants and retention (backups,
soft-deleted objects, a database tier) keep charging after the parent is gone.
Use the cleanup path for resources you own, never a project-wide reset. Rows
were checked against the linked pages on 21 October 2026.


| Resource | Billing basis | Charges while idle? | What people forget | Cleanup (your own resources only) | Verify absent |
| --- | --- | --- | --- | --- | --- |
| Cloud Run service ([pricing](https://cloud.google.com/run/pricing)) | Request-based: vCPU-s, GiB-s, requests; instance-based: instance lifetime | Yes with min instances (idle rate) or instance-based billing | Min instances; the Artifact Registry image | `gcloud run services delete` | `gcloud run services list` empty |
| Agent Runtime ([pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing), [delete](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/reference/rest/v1/projects.locations.reasoningEngines/delete), [scaling](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/optimize-and-scale)) | vCPU-h and GiB-h; Sessions and Memory Bank: GiB-month plus operations | "Idle time ... between turns is not billed"; `min_instances` defaults to 1; scale to zero: confirm on the pricing page | Sessions and memories; delete needs `force` | `DELETE .../reasoningEngines/ID?force=true` or SDK `delete(force=True)` | List reasoning engines: none |
| Vector Search ([pricing](https://cloud.google.com/vertex-ai/pricing), [undeploy](https://docs.cloud.google.com/vertex-ai/docs/vector-search/deploy-index-public)) | Per node-hour per VM hosting a deployed index; build and update per GiB | Yes, every hour deployed; an undeployed index: confirm on the pricing page | The deployed index after the demo (the classic trap); the bucket the build read from | `gcloud ai index-endpoints undeploy-index`, then `delete`; `gcloud ai indexes delete` | Both `list` commands empty, 20 minutes later |
| RAG Engine ([modes](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/deployment-modes), [pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)) | Spanner mode: RagManagedDb tier, Basic (default, fixed) or Scaled (autoscaling); Serverless mode: confirm on the pricing page | Yes in Spanner mode, at the tier | Deleting corpora leaves the tier provisioned | `UpdateRagEngineConfig` tier `Unprovisioned` (data unrecoverable); Serverless: `DeleteRagCorpus` each | `GetRagEngineConfig` shows `Unprovisioned`; `ListRagCorpora` empty |
| Cloud SQL ([pricing](https://cloud.google.com/sql/pricing), [stop](https://docs.cloud.google.com/sql/docs/postgres/start-stop-restart-instance), [delete](https://docs.cloud.google.com/sql/docs/postgres/delete-instance), [backups](https://docs.cloud.google.com/sql/docs/postgres/backup-recovery/backups)) | Per second running; storage, IP, backups | Yes; stopped still bills storage and IP | On-demand and final backups outlive the instance; PITR logs after deletion: confirm on the pricing page | `gcloud sql instances delete`, then `gcloud sql backups delete` | `instances list` and `backups list` empty |
| AlloyDB ([pricing](https://cloud.google.com/alloydb/pricing), [delete](https://docs.cloud.google.com/alloydb/docs/cluster-delete), [backups](https://docs.cloud.google.com/alloydb/docs/backup/overview), [stop](https://docs.cloud.google.com/alloydb/docs/instance-restart)) | Hourly per vCPU and GiB per node; storage; backups until outside retention | Yes; stopped still bills storage and IP | A backup "exists independently from its original cluster" | `gcloud alloydb clusters delete --force`, then `gcloud alloydb backups delete` | `clusters list` and `backups list` empty |
| Memorystore ([pricing](https://cloud.google.com/memorystore/docs/redis/pricing)) | Provisioned GiB-hour; per node with replicas | Yes, "whether you use the instance or not" | The instance | `gcloud redis instances delete` | `gcloud redis instances list` empty |
| BigQuery ([pricing](https://cloud.google.com/bigquery/pricing), [materialized views](https://docs.cloud.google.com/bigquery/docs/materialized-views-intro)) | On-demand per TiB scanned; editions per slot-hour, commitments 50-slot minimum; storage per GiB-month; BI Engine per GiB-hour | Storage, commitments and BI Engine reservations while they exist; refresh bills with no queries | Reservations; the refresh schedule | `bq rm -r -d DATASET`; `bq rm --reservation`, `--capacity_commitment`, the BI Engine reservation | `bq ls`, `--reservation`, `--capacity_commitment` empty |
| Cloud Storage ([pricing](https://cloud.google.com/storage/pricing), [soft delete](https://docs.cloud.google.com/storage/docs/soft-delete), [buckets](https://docs.cloud.google.com/storage/docs/deleting-buckets)) | Per GB-month by class, for live, noncurrent and soft-deleted objects alike | Yes while objects, versions or soft-deleted copies exist | Soft delete (7-day default) bills after `rm`; the bucket is a separate delete | Retention 0 on a disposable bucket; `gcloud storage rm --recursive`; `gcloud storage buckets delete` | `gcloud storage buckets list` empty |
| GKE ([pricing](https://cloud.google.com/kubernetes-engine/pricing)) | Flat fee per cluster-hour; Standard: nodes until deleted; Autopilot: per Pod request | Yes: fee plus nodes, or any scheduled Pod | Load balancers and disks from Services and PVCs | Delete owned namespaces, then `gcloud container clusters delete` | `clusters list`, `forwarding-rules list`, `disks list` clean |
| External Application Load Balancer ([pricing](https://cloud.google.com/vpc/network-pricing)) | Per forwarding rule per hour plus GiB processed | Yes, hourly | An unattached static IP bills higher | `gcloud compute forwarding-rules delete`, then proxy, map, backend, address | `forwarding-rules list` and `addresses list` empty |
| Cloud NAT ([pricing](https://cloud.google.com/nat/pricing)) | Per gateway-hour by VM count, per GiB, per external IP-hour | Yes | The Cloud Router and NAT addresses | `gcloud compute routers nats delete`; release addresses | `gcloud compute routers nats list` empty |
| Provisioned Throughput ([pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing), [purchase](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/provisioned-throughput/purchase-provisioned-throughput)) | Per GSU per term (1 week to 1 year); per-model minimum GSUs | Yes: fees "apply regardless of actual usage"; not cancelable mid-term | Auto-renewal on monthly and longer terms | Turn renewal off; let the term expire | Order expired; no successor |
| Online Monitors ([pricing](https://cloud.google.com/vertex-ai/pricing), [monitors](https://docs.cloud.google.com/gemini-enterprise-agent-platform/optimize/evaluation/evaluate-online)) | Judge (autorater) tokens per sampled instance, at the sampling percentage up to max samples per run | Yes while traffic flows | A monitor left enabled on a demo | Disable or delete the monitor | Monitor absent; judge-model SKU flat |
| Model Armor ([pricing](https://cloud.google.com/security-command-center/pricing)) | Per token screened above a monthly no-cost allocation; SDP inside it free | No | Floor settings screen every covered call; their own cost: confirm on the pricing page | `gcloud model-armor templates delete`; clear floor settings | `gcloud model-armor templates list` empty |
| Sensitive Data Protection ([pricing](https://cloud.google.com/sensitive-data-protection/pricing)) | Per GiB inspected or transformed; discovery subscription per second while deployed | No for content methods; yes for a discovery subscription | Job triggers; the subscription | Delete job triggers; cancel the subscription | Trigger list empty; no subscription |
| Secret Manager ([pricing](https://cloud.google.com/secret-manager/pricing)) | Per active (enabled or disabled) version per location per month; accesses per 10,000 | Yes per active version | Disabled versions still count | `gcloud secrets delete` | `gcloud secrets list` empty |
| Logging and Monitoring ([pricing](https://cloud.google.com/stackdriver/pricing)) | Logs per GiB above the allotment; retention per GiB-month beyond 30 days; metrics per MiB; traces per span | Only retention beyond 30 days or a source still writing | Custom retention on `_Default`; a log in two buckets bills twice | `gcloud logging buckets update --retention-days=30`; delete user buckets and sinks | `gcloud logging buckets list` shows defaults |
| Artifact Registry ([pricing](https://cloud.google.com/artifact-registry/pricing)) | Per GiB-month above a free 0.5 GiB | Yes, every pushed digest | Each `gcloud run deploy --source` push | `gcloud artifacts repositories delete` | `gcloud artifacts repositories list` empty |
| Cloud Build ([pricing](https://cloud.google.com/build/pricing)) | Per build-minute by machine type above the free minutes; queueing free | No | The staging bucket and images it leaves | `gcloud builds triggers delete`; the bucket and repository above | `gcloud builds triggers list` empty |

Notes:

- **RAG Engine.** The tier is project-level and bills until set to
  `Unprovisioned`, which also deletes the data.
- **Vector Search.** Backend cleanup after undeploy takes 10 to 20 minutes.
- **Cloud SQL and AlloyDB backups.** After an instance is deleted, list its
  remaining backups with `gcloud sql backups list --instance=-` (the form for
  deleted instances; confirm on the backups page). Automated Cloud SQL backups roll off daily
  after deletion; on-demand, final and AlloyDB backups bill until deleted or
  expired.
- **GCS soft delete.** Deleted objects "continue to accrue storage charges
  until their retention period expires".

## Write it into the goal

A goal that creates a while-provisioned resource carries a **Resources
created** block, one row per resource: exact name; configuration (tier, nodes,
instances); idle cost per day with pricing date and URL; cleanup command;
verification command; and the owner of its lifetime, a named teardown goal or
a production cost contract (see [GCP decisions](gcp-decisions.md#cost-and-
capacity-assumptions)). A resource without an owner is not created. When the
price cannot be looked up during design (a one-pass draft, no network), write
the billing unit from this table and a placeholder for the figure, and make
reading the pricing page and filling it in the creating goal's first
acceptance item; the placeholder is never presented as a retrieved price.


## Verify the bill, not the command

First the resource list, dependants included. Then the billing report once
caught up: cost details are "typically ... available within a day, but can
sometimes take more than 24 hours" ([view
history](https://docs.cloud.google.com/billing/docs/how-to/view-history)); a
BigQuery export "might take a few hours" to start, five days with a backfill
([export](https://docs.cloud.google.com/billing/docs/how-to/export-data-
bigquery-setup)). Teardown is done when the SKU shows no charge the day after.
For the operation, consult the installed Google skill `cloud-run-basics`,
`cloud-sql-basics`, `alloydb-basics`, `bigquery-basics`, `google-cloud-
storage-basics`, `gke-basics`, `agent-platform-rag-engine-management` or
`gcloud` (from google/skills); if it is not installed, adk-engineer explains
how to get it.


Sources: figures are list prices in USD at the fetch date (21 October 2026) and change.
