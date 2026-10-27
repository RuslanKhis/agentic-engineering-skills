"""G03: own revenue only (C1) and read-only warehouse (C2), against a Toolbox double.

The double stands in for the Toolbox server and client at their documented contract: bound
parameters are hidden from the model's schema and added by the client; readOnly sources accept
SELECT only. It is offline evidence; the same cases still need running against a real server.
"""
import base64
import json
import re
import unittest
from pathlib import Path

from portal.identity import IdentityError, claims_from_iap_header, customer_id_for
from portal.tenant import check_tool_call

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
AUD = "/projects/1/global/backendServices/2"
DIRECTORY = {"buyer@pennine-hardware.example": "C-10482", "accounts@tamar-building.example": "C-10517"}
ROWS = {"C-10482": [("2026-09-01", "100.00")], "C-10517": [("2026-09-01", "999.00")]}


class ToolboxDouble:
    """Client + server for one tool; records every statement that reaches the 'warehouse'."""

    def __init__(self, bound):
        self.bound, self.executed = dict(bound), []

    def schema_for_model(self):
        return [p for p in ("tenant_id", "start_month", "end_month", "table") if p not in self.bound]

    def call(self, args):
        if set(args) & set(self.bound):
            raise ValueError("bound parameter supplied by the model")
        merged = {**args, **self.bound}
        self.executed.append(merged)
        return ROWS.get(merged["tenant_id"], [])

    @staticmethod
    def run_statement(sql, executed):
        """readOnly source: dry-run classifies the statement; anything but SELECT is refused."""
        if not re.match(r"\s*(SELECT|WITH)\b", sql, re.I) or re.search(r"\b(DELETE|DROP|SET|COMMIT)\b|;\s*\S", sql, re.I):
            raise PermissionError("statement type not allowed on a read-only source")
        executed.append(sql)


def fake_verifier(claims):
    def verify(token, audience):
        if token != "valid":
            raise ValueError("bad signature")
        return claims
    return verify


def unsigned_jwt(claims):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b"=").decode()
    return f"{enc({'alg': 'none'})}.{enc(claims)}."


GOOD = {"iss": "https://cloud.google.com/iap", "aud": AUD, "email": "buyer@pennine-hardware.example"}


class IdentityTests(unittest.TestCase):
    def test_forged_unsigned_assertion_is_rejected(self):
        forged = unsigned_jwt({**GOOD, "email": "accounts@tamar-building.example"})
        with self.assertRaises(IdentityError):
            claims_from_iap_header({"x-goog-iap-jwt-assertion": forged}, AUD,
                                   verifier=fake_verifier(GOOD))  # verifier rejects: token != "valid"

    def test_missing_header_and_missing_audience_fail_closed(self):
        with self.assertRaises(IdentityError):
            claims_from_iap_header({}, AUD, verifier=fake_verifier(GOOD))
        with self.assertRaises(IdentityError):
            claims_from_iap_header({"x-goog-iap-jwt-assertion": "valid"}, "", verifier=fake_verifier(GOOD))

    def test_wrong_issuer_or_audience_is_rejected(self):
        for bad in ({**GOOD, "iss": "https://evil.example"}, {**GOOD, "aud": "other"}):
            with self.assertRaises(IdentityError):
                claims_from_iap_header({"x-goog-iap-jwt-assertion": "valid"}, AUD, verifier=fake_verifier(bad))

    def test_verified_claims_map_to_customer(self):
        claims = claims_from_iap_header({"x-goog-iap-jwt-assertion": "valid"}, AUD, verifier=fake_verifier(GOOD))
        self.assertEqual(customer_id_for(claims, DIRECTORY), "C-10482")


class TenantTests(unittest.TestCase):  # A1, A2
    def setUp(self):
        self.tb = ToolboxDouble({"tenant_id": "C-10482"})

    def test_model_never_sees_tenant_id(self):  # A1
        self.assertNotIn("tenant_id", self.tb.schema_for_model())

    def test_own_revenue_only(self):  # A1
        rows = self.tb.call({"table": "invoices_summary", "start_month": "2026-09-01", "end_month": "2026-09-01"})
        self.assertEqual(rows, ROWS["C-10482"])
        self.assertEqual({e["tenant_id"] for e in self.tb.executed}, {"C-10482"})

    def test_other_account_named_in_message_cannot_reach_the_tool(self):  # A2
        args = {"tenant_id": "C-10517", "table": "invoices_summary", "start_month": "a", "end_month": "b"}
        self.assertIsNotNone(check_tool_call("customer-revenue", args))  # agent callback refuses
        with self.assertRaises(ValueError):
            self.tb.call(args)  # and the client refuses independently
        self.assertEqual(self.tb.executed, [])

    def test_free_form_sql_tool_is_not_callable(self):
        self.assertIsNotNone(check_tool_call("execute-sql", {"sql": "SELECT 1"}))
        self.assertIsNone(check_tool_call("customer-revenue", {"table": "credit_summary"}))


class ReadOnlyTests(unittest.TestCase):  # A3
    BYPASSES = [
        "WITH d AS (DELETE FROM users RETURNING *) SELECT * FROM d;",
        "SELECT purge_inactive_records();",  # UDF write: needs the real server's dry-run (see report)
        "COMMIT; SET default_transaction_read_only = off; DROP TABLE orders;",
        "DROP TABLE sales.invoices_summary",
    ]

    def test_non_select_refused_with_nothing_executed(self):
        for sql in self.BYPASSES[:1] + self.BYPASSES[2:]:
            executed = []
            with self.assertRaises(PermissionError, msg=sql):
                ToolboxDouble.run_statement(sql, executed)
            self.assertEqual(executed, [])


@unittest.skipIf(yaml is None, "PyYAML not installed")
class ToolsYamlTests(unittest.TestCase):
    def setUp(self):
        self.cfg = yaml.safe_load((ROOT / "tools.yaml").read_text())

    def test_source_is_read_only_and_scoped(self):
        src = self.cfg["sources"]["fernhill-bq"]
        self.assertIs(src["readOnly"], True)
        self.assertNotEqual(src.get("writeMode"), "allowed")
        self.assertEqual(src["allowedDatasets"], ["sales"])

    def test_no_free_form_tool_anywhere(self):
        kinds = {t["kind"] for t in self.cfg["tools"].values()}
        self.assertNotIn("bigquery-execute-sql", kinds)
        self.assertEqual(self.cfg["toolsets"]["customer-portal"], ["customer-revenue"])

    def test_table_template_parameter_is_an_allowlist(self):
        tp = self.cfg["tools"]["customer-revenue"]["templateParameters"][0]
        self.assertEqual(sorted(tp["allowedValues"]), ["credit_summary", "invoices_summary"])


if __name__ == "__main__":
    unittest.main()
