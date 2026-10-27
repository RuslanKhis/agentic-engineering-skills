import unittest

from review_app.grouping import group_for_pack


def rec(rid, label, text, page=14, kind="clause", **kw):
    return {"record_id": rid, "document": "DMP", "version": "v3", "page": page, "kind": kind,
            "label": label, "text": text, **kw}


class GroupingTests(unittest.TestCase):
    def test_clauses_become_units(self):
        records = {"r1": rec("r1", "4.1", "4.1 Respect the street."), "r2": rec("r2", "4.2", "4.2 Rear extensions.")}
        units = group_for_pack(records, ["r1", "r2"])
        self.assertEqual([u["key"] for u in units], ["DMP:4.1", "DMP:4.2"])

    def test_continuation_joins_its_clause(self):
        records = {"r1": rec("r1", "(b)", "(b) height up to 3 m, except where", continued_by="r2"),
                   "r2": rec("r2", "(b)", "the site is in a Conservation Area.", page=15, continues="r1")}
        units = group_for_pack(records, ["r1", "r2"])
        self.assertEqual(len(units), 1)
        self.assertIn("Conservation Area", units[0]["text"])

    def test_footnotes_are_not_units(self):
        records = {"r1": rec("r1", "4.1", "4.1 See note.7"), "r2": rec("r2", "7", "7 A note.", kind="footnote")}
        self.assertEqual(len(group_for_pack(records, ["r1", "r2"])), 1)


if __name__ == "__main__":
    unittest.main()
