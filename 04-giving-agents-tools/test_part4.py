import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("part4_main", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Part4ToolingTest(unittest.TestCase):
    def test_get_weather_tool_returns_data(self):
        result = MODULE.get_weather("Accra")
        self.assertIn("Accra", result["city"]) 
        self.assertIn("temperature", result)

    def test_tool_aware_agent_chooses_weather_tool(self):
        agent = MODULE.ToolAwareAgent()
        result = agent.run("What is the weather in Accra?")

        self.assertEqual(result["tool_used"], "get_weather")
        self.assertIn("Accra", result["final_response"])
        self.assertIn("temperature", result["final_response"].lower())


if __name__ == "__main__":
    unittest.main()
