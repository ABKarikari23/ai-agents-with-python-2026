import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("part1_main", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Part1ConceptsTest(unittest.TestCase):
    def test_chatbot_answer_looks_like_a_response(self):
        chatbot = MODULE.Chatbot()
        response = chatbot.respond("What is an AI agent?")
        self.assertIn("AI agent", response)

    def test_agent_generates_goal_driven_report(self):
        agent = MODULE.SimpleAgent()
        result = agent.run("Research the impact of AI on education in Ghana")

        self.assertIn("impact of ai on education in ghana", result["goal"].lower())
        self.assertGreaterEqual(len(result["plan"]), 3)
        self.assertIn("education", result["summary"].lower())


if __name__ == "__main__":
    unittest.main()
