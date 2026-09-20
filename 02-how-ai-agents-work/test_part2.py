import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("part2_main", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Part2AgentLoopTest(unittest.TestCase):
    def test_model_decision_and_tool_call(self):
        agent = MODULE.SimpleAgent()
        result = agent.run("Research the benefits of solar energy for small businesses in Ghana")

        self.assertEqual(result["goal"], "Research the benefits of solar energy for small businesses in Ghana")
        self.assertIn("tool", result["decision"].lower())
        self.assertIn("solar", result["observation"].lower())
        self.assertIn("summary", result["final_response"].lower())

    def test_memory_tracks_user_context(self):
        memory = MODULE.Memory()
        memory.add("preferred_language", "Python")
        memory.add("budget", "GHS 5000")

        self.assertEqual(memory.get("preferred_language"), "Python")
        self.assertEqual(memory.get("budget"), "GHS 5000")


if __name__ == "__main__":
    unittest.main()
