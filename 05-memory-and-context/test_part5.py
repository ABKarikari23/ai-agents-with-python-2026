import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("part5_main", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Part5MemoryTest(unittest.TestCase):
    def test_memory_stores_and_retrieves_user_pref(self):
        memory = MODULE.Memory()
        memory.add("name", "Abraham")
        memory.add("preferred_language", "Python")

        self.assertEqual(memory.get("name"), "Abraham")
        self.assertEqual(memory.get("preferred_language"), "Python")

    def test_agent_uses_memory_in_context(self):
        agent = MODULE.AgentWithMemory()
        agent.memory.add("name", "Abraham")
        agent.memory.add("preferred_language", "Python")

        result = agent.respond("Recommend a project for me")

        self.assertIn("Abraham", result)
        self.assertIn("Python", result)
        self.assertIn("project", result.lower())


if __name__ == "__main__":
    unittest.main()
