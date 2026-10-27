# Cost question from finance, 2026-10-22

For session sess-2026-10-21-0412 (the only research turn run on 21 October)
the dashboard shows USD 0.2650 and the gateway invoice totals USD 0.4498.
At the same time the dashboard's output tokens for o-reasoner-2 (30,780) are
higher than the invoice's completion tokens (22,475), and the gateway says its
completion counts already include reasoning tokens. The invoice also bills
o-mini-2, which never appears in the dashboard, and counts 7 o-reasoner-2
requests where the session shows 3 model responses. The per-request gateway
log for the day is in `billing/`.
