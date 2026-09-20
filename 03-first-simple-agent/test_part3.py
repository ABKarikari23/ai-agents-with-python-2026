import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("part3_main", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Part3SimpleAgentTest(unittest.TestCase):
    def test_calculator_tool_handles_valid_expression(self):
        result = MODULE.calculate("25 * 400")
        self.assertEqual(result, "10000")

    def test_agent_uses_tool_for_calculation(self):
        agent = MODULE.SimpleAgent()
        result = agent.run("What is 15% of 40000?")

        self.assertEqual(result["tool_used"], "calculator")
        self.assertIn("6000", result["final_response"])
        self.assertIn("15%", result["final_response"])


if __name__ == "__main__":
    unittest.main()
