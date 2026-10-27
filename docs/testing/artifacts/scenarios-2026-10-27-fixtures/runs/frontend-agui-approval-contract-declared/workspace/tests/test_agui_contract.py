import importlib.util
import unittest

HAS_SDK = importlib.util.find_spec("google.adk") is not None and importlib.util.find_spec("ag_ui_adk") is not None


@unittest.skipUnless(HAS_SDK, "needs google-adk and ag-ui-adk")
class ApprovalContractTests(unittest.TestCase):
    def test_tool_message_contract_is_declared(self):
        from app import agui
        self.assertIs(agui.EMIT_INTERRUPT_OUTCOME, False)


if __name__ == "__main__":
    unittest.main()
