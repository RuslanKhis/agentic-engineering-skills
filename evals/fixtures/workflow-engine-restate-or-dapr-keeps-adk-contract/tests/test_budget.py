import unittest

from app import budget


class FakeCallbackContext:
    def __init__(self, state=None):
        self.state = state if state is not None else {}


class FakeUsage:
    def __init__(self, total):
        self.total_token_count = total


class FakeResponse:
    def __init__(self, total):
        self.usage_metadata = FakeUsage(total)


class BudgetCallbackTests(unittest.TestCase):
    """Duck-typed stand-ins for the two attributes the callbacks read; not ADK objects."""

    def test_usage_accumulates_per_invocation(self):
        ctx = FakeCallbackContext()
        budget.after_model(ctx, FakeResponse(1200))
        budget.after_model(ctx, FakeResponse(800))
        self.assertEqual(ctx.state[budget.USED], 2000)

    def test_under_budget_lets_the_call_through(self):
        ctx = FakeCallbackContext({budget.USED: budget.TOKEN_BUDGET - 1})
        self.assertIsNone(budget.before_model(ctx, None))
        self.assertEqual(ctx.state[budget.CALLS], 1)


if __name__ == "__main__":
    unittest.main()
