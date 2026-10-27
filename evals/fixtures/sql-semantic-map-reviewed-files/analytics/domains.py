"""Semantic domains for the generated-query route.

Each domain lists the tables the author may see, the columns exposed to it, the joins it may use
and any derived tables (defined by SQL that the metadata collector expands into the candidate).
"""

PROJECT = "fernhill-analytics"
DATASET = "sales"

DOMAINS = {
    "revenue": {
        "description": "Invoiced revenue by customer, product line and month.",
        "tables": {
            "invoices": {
                "key": ["invoice_id"],
                "columns": ["invoice_id", "customer_id", "invoice_date", "currency", "status"],
            },
            "invoice_lines": {
                "key": ["invoice_id", "line_no"],
                "columns": ["invoice_id", "line_no", "sku", "quantity", "net_amount_gbp"],
            },
            "customers": {
                "key": ["customer_id"],
                "columns": ["customer_id", "account_name", "region", "account_manager"],
            },
        },
        "relationships": [
            {"from": "invoice_lines.invoice_id", "to": "invoices.invoice_id", "cardinality": "many_to_one"},
            {"from": "invoices.customer_id", "to": "customers.customer_id"},
        ],
        "derived": {
            "monthly_net_revenue": (
                "SELECT i.customer_id, DATE_TRUNC(i.invoice_date, MONTH) AS month, "
                "SUM(l.net_amount_gbp) AS net_revenue_gbp "
                "FROM `fernhill-analytics.sales.invoices` i "
                "JOIN `fernhill-analytics.sales.invoice_lines` l USING (invoice_id) "
                "WHERE i.status = 'posted' GROUP BY 1, 2"
            ),
        },
    },
    "products": {
        "description": "Product catalogue and product lines.",
        "tables": {
            "products": {
                "key": ["sku"],
                "columns": ["sku", "product_line", "description", "list_price_gbp", "discontinued"],
            },
        },
        "relationships": [],
        "derived": {},
    },
    "returns": {
        "description": "Credit notes against invoices.",
        "tables": {
            "credit_notes": {
                "key": ["credit_note_id"],
                "columns": ["credit_note_id", "invoice_id", "issued_on", "amount_gbp", "reason_code"],
            },
            "invoices": {
                "key": ["invoice_id"],
                "columns": ["invoice_id", "customer_id", "invoice_date"],
            },
        },
        "relationships": [
            {"from": "credit_notes.invoice_id", "to": "invoices.invoice_id", "cardinality": "many_to_one"},
        ],
        "derived": {},
    },
}
