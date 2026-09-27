import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("part7_main", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Part7MultiAgentSystemTest(unittest.TestCase):
    def test_orchestrator_runs_complete_workflow(self):
        orchestrator = __import__("orchestrator", fromlist=["Orchestrator"]).Orchestrator()
        result = orchestrator.run("Explain how AI agents use Python tools safely and effectively.")

        self.assertEqual(result.status, "completed")
        self.assertIsNotNone(result.research)
        self.assertIsNotNone(result.draft)
        self.assertIsNotNone(result.review)
        self.assertTrue(result.review["approved"])

    def test_writer_requires_research(self):
        from state import AgentState
        from agents.writer import WriterAgent

        state = AgentState(task="Write an article")
        writer = WriterAgent()
        result = writer.run(state)

        self.assertTrue(result.errors)
        self.assertEqual(result.status, "failed")

    def test_reviewer_requires_draft(self):
        from state import AgentState
        from agents.reviewer import ReviewerAgent

        state = AgentState(task="Review article")
        reviewer = ReviewerAgent()
        result = reviewer.run(state)

        self.assertTrue(result.errors)
        self.assertEqual(result.status, "failed")


if __name__ == "__main__":
    unittest.main()
