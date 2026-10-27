import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from analytics import semantic
from analytics.domains import DOMAINS

try:
    import sqlglot  # noqa: F401
    HAVE_SQLGLOT = True
except ImportError:
    HAVE_SQLGLOT = False


class MapCase(unittest.TestCase):
    """Each test mutates a private copy of the real semantic tree."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.root = self.tmp / "semantic"
        shutil.copytree(semantic.ROOT, self.root)

    def edit(self, rel: str, fn):
        path = self.root / rel
        doc = yaml.safe_load(path.read_text())
        fn(doc)
        path.write_text(yaml.safe_dump(doc))

    def problems(self, **kw):
        return semantic.problems(self.root, require_review=False, check_sql=HAVE_SQLGLOT, **kw)


class RealFilesTests(MapCase):
    def test_real_files_pass_structure(self):
        self.assertEqual(self.problems(), [])

    def test_unreviewed_files_fail_the_review_gate(self):
        self.assertTrue(any("reviewed_by" in e for e in semantic.problems(self.root, check_sql=False)))

    def test_relationship_cardinalities_survive_the_migration(self):
        rels = {(r["from"], r["to"]): r["cardinality"] for r in DOMAINS["revenue"]["relationships"]}
        self.assertEqual(rels[("invoices.customer_id", "customers.customer_id")], "many_to_one")
        self.assertEqual(rels[("invoice_lines.invoice_id", "invoices.invoice_id")], "many_to_one")

    def test_derived_sql_is_carried_over(self):
        self.assertIn("SUM(l.net_amount_gbp)", DOMAINS["revenue"]["derived"]["monthly_net_revenue"])


class BrokenTreeTests(MapCase):
    def rel(self, name, fn):
        def apply(doc):
            fn(next(r for r in doc["relationships"] if r["name"] == name))
        self.edit("relationships.yml", apply)

    def assert_fails(self, text):
        self.assertTrue(any(text in e for e in self.problems()), self.problems())

    def test_missing_join_type(self):
        self.rel("invoices_to_customers", lambda r: r.pop("join_type"))
        self.assert_fails("join_type")

    def test_missing_condition(self):
        self.rel("invoices_to_customers", lambda r: r.pop("condition"))
        self.assert_fails("condition")

    def test_condition_on_unknown_column(self):
        self.rel("invoices_to_customers",
                 lambda r: r.update(condition="invoices.customer_ref = customers.customer_id"))
        self.assert_fails("not a column")

    def test_unknown_model(self):
        self.rel("invoices_to_customers", lambda r: r.update(models=["invoices", "nowhere"]))
        self.assert_fails("known models")

    def test_one_side_not_joined_on_primary_key(self):
        self.rel("invoices_to_customers",
                 lambda r: r.update(condition="invoices.customer_id = customers.region"))
        self.assert_fails("primary key")

    def test_many_to_many_is_refused(self):
        self.rel("invoices_to_customers", lambda r: r.update(join_type="MANY_TO_MANY"))
        self.assert_fails("fan-out")

    def test_table_without_primary_key(self):
        self.edit("models/customers.yml", lambda d: d.pop("primary_key"))
        self.assert_fails("no primary_key")

    def test_domain_exposes_unknown_column(self):
        self.edit("domains/products.yml", lambda d: d["tables"]["products"].append("cost_gbp"))
        self.assert_fails("unknown or no columns")

    def test_domain_uses_unknown_table(self):
        self.edit("domains/products.yml", lambda d: d["tables"].update(ghosts=["id"]))
        self.assert_fails("unknown table")

    @unittest.skipUnless(HAVE_SQLGLOT, "sqlglot not installed")
    def test_derived_write_is_rejected(self):
        self.edit("domains/revenue.yml",
                  lambda d: d["derived"].update(bad="DELETE FROM `fernhill-analytics.sales.invoices` WHERE TRUE"))
        self.assert_fails("rejected by the SQL policy")

    @unittest.skipUnless(HAVE_SQLGLOT, "sqlglot not installed")
    def test_derived_multi_statement_is_rejected(self):
        self.edit("domains/revenue.yml", lambda d: d["derived"].update(bad="SELECT 1; SELECT 2"))
        self.assert_fails("rejected by the SQL policy")

    @unittest.skipUnless(HAVE_SQLGLOT, "sqlglot not installed")
    def test_derived_unparseable_is_reported(self):
        self.edit("domains/revenue.yml", lambda d: d["derived"].update(bad="SELECT FROM WHERE ((("))
        self.assert_fails("cannot be checked")

    @unittest.skipUnless(HAVE_SQLGLOT, "sqlglot not installed")
    def test_derived_outside_the_domain_is_rejected(self):
        self.edit("domains/revenue.yml",
                  lambda d: d["derived"].update(bad="SELECT * FROM `fernhill-analytics.sales.credit_notes`"))
        self.assert_fails("not in the domain")


@unittest.skipUnless(HAVE_SQLGLOT, "sqlglot not installed")
class ExamplesTests(MapCase):
    def test_pending_masks_literals_and_is_not_duplicated(self):
        from analytics.examples import record_pending
        pending = self.tmp / "pending"
        sql = "SELECT region FROM `fernhill-analytics.sales.customers` WHERE account_name = 'Acme Ltd'"
        path = record_pending("revenue", sql, pending)
        self.assertNotIn("Acme", path.read_text())
        self.assertEqual(set(json.loads(path.read_text())), {"domain", "sql"})
        self.assertIsNone(record_pending("revenue", sql.replace("Acme Ltd", "Other plc"), pending))

    def test_only_reviewed_policy_clean_examples_reach_the_author(self):
        from analytics.examples import promoted
        (self.root / "examples").mkdir()
        good = {"question": "q", "sql": "SELECT region FROM `fernhill-analytics.sales.customers`",
                "reviewed_by": "A. Reviewer", "reviewed_on": "2026-10-27"}
        docs = [good,
                {**good, "reviewed_by": None},
                {**good, "sql": "DELETE FROM `fernhill-analytics.sales.customers` WHERE TRUE"},
                {**good, "sql": "SELECT * FROM `fernhill-analytics.sales.credit_notes`"}]
        (self.root / "examples" / "revenue.yml").write_text(yaml.safe_dump({"examples": docs}))
        out = promoted("revenue", set(DOMAINS["revenue"]["tables"]), self.root)
        self.assertEqual(len(out), 1)

    def test_no_example_file_means_no_examples(self):
        from analytics.examples import promoted
        self.assertEqual(promoted("products", {"products"}, self.root), [])


@unittest.skipUnless(HAVE_SQLGLOT, "sqlglot not installed")
class GeneratedRouteTests(unittest.TestCase):
    def test_unexpanded_derived_name_is_rejected_without_execution_or_queueing(self):
        from analytics.generated import answer
        rows = [{"table_name": t, "column_name": c, "data_type": "STRING"}
                for t, s in DOMAINS["revenue"]["tables"].items() for c in s["columns"]]
        queued = []
        # `monthly_net_revenue` followed by a newline is not matched by expand_derived's " name " rule.
        result = answer("q", "revenue", lambda s, p: rows,
                        lambda ctx, q: "SELECT * FROM monthly_net_revenue\nLIMIT 5",
                        bq_client=None, on_success=lambda d, s: queued.append(s))
        self.assertEqual(result["status"], "rejected")
        self.assertEqual(queued, [])


if __name__ == "__main__":
    unittest.main()
