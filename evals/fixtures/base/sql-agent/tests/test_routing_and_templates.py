import unittest

from analytics.metadata import collect, expand_derived
from analytics.router import route
from analytics.templates import TEMPLATES, validate_params


class RouterTests(unittest.TestCase):
    def test_top_customers_uses_template(self):
        r = route("Who were our top 10 customers by revenue last quarter?")
        self.assertEqual((r.path, r.template), ("template", "top_customers_by_revenue"))

    def test_revenue_question_goes_to_generated_route(self):
        self.assertEqual(route("How much revenue came from invoices in GBP last week?").path, "generated")

    def test_unrelated_question_clarifies(self):
        self.assertEqual(route("What is the weather in Leeds?").path, "clarify")


class TemplateTests(unittest.TestCase):
    def test_unknown_region_is_rejected(self):
        t = TEMPLATES["monthly_revenue_for_region"]
        self.assertIn("unknown region", validate_params(t, {"region": "Mars", "start_date": "2026-01-01",
                                                            "end_date": "2026-03-31"}))

    def test_limit_bounds(self):
        t = TEMPLATES["top_customers_by_revenue"]
        self.assertIn("limit out of range", validate_params(t, {"start_date": "a", "end_date": "b", "limit": 500}))


class MetadataTests(unittest.TestCase):
    def test_collect_keeps_only_exposed_columns(self):
        rows = [{"table_name": "customers", "column_name": "account_name", "data_type": "STRING"},
                {"table_name": "customers", "column_name": "credit_limit_gbp", "data_type": "NUMERIC"}]
        ctx = collect("revenue", lambda sql, params: rows)
        self.assertEqual([c["name"] for c in ctx["tables"]["customers"]["columns"]], ["account_name"])

    def test_expand_derived(self):
        sql = expand_derived("SELECT * FROM `monthly_net_revenue` WHERE month = '2026-09-01'",
                             {"monthly_net_revenue": "SELECT 1 AS month"})
        self.assertIn("(SELECT 1 AS month)", sql)


if __name__ == "__main__":
    unittest.main()
