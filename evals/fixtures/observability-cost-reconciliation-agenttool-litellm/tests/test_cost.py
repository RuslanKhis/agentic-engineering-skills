import json
from pathlib import Path
import unittest

from research.cost import load_prices, session_cost, session_usage

HERE = Path(__file__).resolve().parent.parent


class CostTests(unittest.TestCase):
    def test_usage_per_model(self):
        session = json.loads((HERE / "sessions/sess-2026-10-21-0412.json").read_text())
        usage = session_usage(session)
        self.assertEqual(usage["o-reasoner-2"]["input"], 9370)

    def test_cost_is_positive(self):
        session = json.loads((HERE / "sessions/sess-2026-10-21-0412.json").read_text())
        self.assertGreater(session_cost(session, load_prices(HERE / "prices.json")), 0)


if __name__ == "__main__":
    unittest.main()
