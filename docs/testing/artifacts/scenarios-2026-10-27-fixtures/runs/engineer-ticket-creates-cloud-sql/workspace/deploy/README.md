# Deployment

`deploy.sh` builds the image with Cloud Build and deploys the Cloud Run
service in the dev project (`harbour-support-dev`, `europe-west2`), private
ingress behind the existing load balancer and IAP. It creates nothing besides
the image and the revision. It now also needs `NETWORK` and `SUBNET` (Direct
VPC egress to reach the private-IP database) and reads `SESSION_DB_URL` from
the secret `sessions-db-url`.

`create_sessions_db.sh` creates the Cloud SQL instance `support-sessions-dev`,
its database and its user (G03). `delete_sessions_db.sh` removes them (user,
database, instance); G06 runs it. Both refuse any project but
`harbour-support-dev` and both take `--dry-run`. Deletion also needs
`CONFIRM_DELETE=support-sessions-dev`.

Not done by the scripts, so a person does them before the live run:

- private services access on the VPC (peering) for the instance's private IP;
- Secret Manager secrets `sessions-db-password` (the user's password) and
  `sessions-db-url` (`postgresql+asyncpg://sessions_app:<password>@<private-ip>:5432/sessions`);
- `roles/secretmanager.secretAccessor` on those secrets for the runtime
  service account.

Owned resources and their state are recorded in each ticket's Evidence.
