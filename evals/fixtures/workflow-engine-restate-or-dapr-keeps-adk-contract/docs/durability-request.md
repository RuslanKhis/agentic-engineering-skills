# Refund approvals must survive restarts

Raised by Sam Okoye (operations), 2026-10-22.

- A manager approves each refund from the back office. Approvals can take days (weekends,
  leave); the customer should not have to start again.
- Pods in the `support` namespace are rescheduled several times a week. On 2026-10-14 a pod was
  replaced while a refund waited for approval; the approval later failed with "session not
  found on this worker" and the customer was asked to start over.
- Operations would rather not run a Temporal cluster. Restate was trialled by the payments team
  this summer; Dapr 1.15 already runs on our GKE cluster (statestore on Cloud SQL for
  PostgreSQL, see deploy/gke/components/).
- Harbour Outfitters has about 4,000 staff.
- The token budget (app/budget.py) and the 8-call limit (RUN_CONFIG) stay, and approval stays
  with a manager.
