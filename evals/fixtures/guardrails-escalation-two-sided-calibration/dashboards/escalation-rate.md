# Dashboard: expense triage escalation rate (production)

Owner: finance operations. Source: Cloud SQL `claims` table, refreshed hourly.

Metric: `count(lane = 'finance_review') / count(lane is not null)` per day.

| Week | Claims triaged | Escalated | Rate |
| --- | --- | --- | --- |
| 2026-09-29 | 1,412 | 790 | 56 % |
| 2026-10-06 | 1,388 | 819 | 59 % |
| 2026-10-13 | 1,450 | 885 | 61 % |
| 2026-10-20 | 1,397 | 852 | 61 % |

Finance review team note (2026-10-22): reviewers now bulk-approve the queue each
afternoon because most escalations are routine. Product target: escalation rate under 10 %.
