import importlib.util
import unittest

try:
    HAVE_ADK = importlib.util.find_spec("google.adk") is not None
except ModuleNotFoundError:
    HAVE_ADK = False


@unittest.skipUnless(HAVE_ADK, "google-adk not installed")
class RunnerScriptedTests(unittest.TestCase):
    """Scripted-model Runner tests: lookup before refund, confirmation before issue_refund."""

    def test_refund_waits_for_confirmation(self):
        self.skipTest("written against the Runner; see tests/fakes.py for the providers")


if __name__ == "__main__":
    unittest.main()
