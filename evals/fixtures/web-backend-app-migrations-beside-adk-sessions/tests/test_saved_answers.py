import unittest

try:
    import sqlalchemy  # noqa: F401
except ImportError:  # the suite still runs where only the standard library is installed
    raise unittest.SkipTest("sqlalchemy is not installed")

from app import saved_answers
from app.db import make_engine


class SavedAnswersTests(unittest.TestCase):
    def setUp(self):
        self.engine = make_engine("sqlite:///:memory:")

    def test_save_then_get(self):
        answer_id = saved_answers.save(self.engine, "cust-ana", "Return window?", "30 days.")
        self.assertEqual(saved_answers.get(self.engine, answer_id)["answer"], "30 days.")

    def test_list_only_own(self):
        saved_answers.save(self.engine, "cust-ana", "q1", "a1")
        saved_answers.save(self.engine, "cust-ben", "q2", "a2")
        self.assertEqual([r["question"] for r in saved_answers.list_for(self.engine, "cust-ana")], ["q1"])


if __name__ == "__main__":
    unittest.main()
