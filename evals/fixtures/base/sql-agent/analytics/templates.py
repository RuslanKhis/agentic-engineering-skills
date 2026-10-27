"""Reviewed SQL templates. Values are bound as BigQuery query parameters, never formatted in."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Template:
    name: str
    sql: str
    params: dict  # name -> BigQuery type
    reviewed_by: str
    reviewed_on: str


TEMPLATES = {
    "top_customers_by_revenue": Template(
        name="top_customers_by_revenue",
        sql=(
            "SELECT c.account_name, SUM(l.net_amount_gbp) AS net_revenue_gbp\n"
            "FROM `fernhill-analytics.sales.invoices` i\n"
            "JOIN `fernhill-analytics.sales.invoice_lines` l USING (invoice_id)\n"
            "JOIN `fernhill-analytics.sales.customers` c USING (customer_id)\n"
            "WHERE i.status = 'posted' AND i.invoice_date BETWEEN @start_date AND @end_date\n"
            "GROUP BY c.account_name\n"
            "ORDER BY net_revenue_gbp DESC, c.account_name\n"
            "LIMIT @limit"
        ),
        params={"start_date": "DATE", "end_date": "DATE", "limit": "INT64"},
        reviewed_by="M. Okafor (finance)",
        reviewed_on="2026-09-18",
    ),
    "monthly_revenue_for_region": Template(
        name="monthly_revenue_for_region",
        sql=(
            "SELECT DATE_TRUNC(i.invoice_date, MONTH) AS month, SUM(l.net_amount_gbp) AS net_revenue_gbp\n"
            "FROM `fernhill-analytics.sales.invoices` i\n"
            "JOIN `fernhill-analytics.sales.invoice_lines` l USING (invoice_id)\n"
            "JOIN `fernhill-analytics.sales.customers` c USING (customer_id)\n"
            "WHERE i.status = 'posted' AND c.region = @region\n"
            "  AND i.invoice_date BETWEEN @start_date AND @end_date\n"
            "GROUP BY month ORDER BY month"
        ),
        params={"region": "STRING", "start_date": "DATE", "end_date": "DATE"},
        reviewed_by="M. Okafor (finance)",
        reviewed_on="2026-09-18",
    ),
}

REGIONS = ("North", "Midlands", "South", "Scotland", "Wales")


def validate_params(template: Template, values: dict) -> list[str]:
    errors = []
    for name in template.params:
        if name not in values:
            errors.append(f"missing {name}")
    extra = set(values) - set(template.params)
    if extra:
        errors.append(f"unexpected {', '.join(sorted(extra))}")
    if "region" in values and values["region"] not in REGIONS:
        errors.append("unknown region")
    if "limit" in values and not (1 <= int(values["limit"]) <= 50):
        errors.append("limit out of range")
    return errors
