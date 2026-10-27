# Deployment

`deploy.sh` builds the image with Cloud Build and deploys the Cloud Run
service in the dev project (`harbour-support-dev`, `europe-west2`), private
ingress behind the existing load balancer and IAP. It creates nothing besides
the image and the revision. It now needs `VPC_NETWORK` and `VPC_SUBNET`
(Direct VPC egress to the private-IP session database) and reads the secret
`session-db-url` into `SESSION_DB_URL`.

`create_sessions_db.sh` creates the Cloud SQL instance `support-sessions-dev`
with its database and user (G03). `delete_sessions_db.sh` removes it; it is a
dry run unless `EXECUTE=yes` and `CONFIRM_DELETE=support-sessions-dev` are set,
and G06 runs it. Run both with `bash`.

Steps the scripts do not do, and that need their own approval:

1. Private services access on the VPC must already exist (the create script
   fails otherwise).
2. Create secret `session-db-url` holding
   `postgresql+asyncpg://sessions_app:<password>@<private-ip>/sessions`.
3. Grant the runtime service account `roles/cloudsql.client` on the project (D2).
4. Add `asyncpg` (and `aiosqlite` for the offline tests) to `pyproject.toml`
   with pins chosen where the dependencies can be resolved.

Owned resources and their state are recorded in each ticket's Evidence.
