# Incident: a refund paid twice after a worker restart (2026-10-21)

- Customer cust-4471, order HO-30218, refund 6,400 cents (damaged rucksack).
- Fri 17 Oct 16:52: the agent called issue_refund; the invocation paused for confirmation.
- Mon 20 Oct 09:14: manager Dee Harlow approved in the back office. app/approvals.py resumed
  the invocation; the provider accepted refund re_8812 (09:14:07).
- 09:14:08: the worker pod was evicted during a node upgrade before the resumed invocation
  finished writing its events.
- 09:31: the back office showed the approval as still pending; Dee approved again. The resumed
  invocation ran issue_refund again; the provider accepted refund re_8840.
- The customer received 12,800 cents. Finance recovered the second refund on 21 Oct.

Open questions from the review: is ADK's resume enough for waits of several days, or do we need
a durable execution engine? We have Postgres (Cloud SQL) already; there is no Temporal cluster.
