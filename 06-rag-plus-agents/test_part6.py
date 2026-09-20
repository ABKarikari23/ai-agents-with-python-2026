import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).with_name("main.py")
SPEC = importlib.util.spec_from_file_location("part6_main", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Part6RAGTest(unittest.TestCase):
    def test_retrieval_returns_relevant_document(self):
        knowledge_base = {
            "vpn.txt": "Employees accessing the corporate VPN must use multi-factor authentication.",
            "network.txt": "Network connectivity problems should be checked for IP configuration and DNS.",
            "security.txt": "Employees must never share passwords or API keys.",
        }

        retriever = MODULE.RAGRetriever(knowledge_base)
        results = retriever.search("How do I reset my VPN password?")

        self.assertTrue(results)
        self.assertIn("vpn", results[0]["source"].lower())

    def test_agent_uses_rag_for_answer(self):
        knowledge_base = {
            "vpn.txt": "Employees accessing the corporate VPN must use multi-factor authentication.",
            "network.txt": "Network connectivity problems should be checked for IP configuration and DNS.",
            "security.txt": "Employees must never share passwords or API keys.",
        }

        agent = MODULE.RAGAgent(knowledge_base)
        response = agent.answer("How do I reset my VPN password?")

        self.assertIn("vpn", response.lower())
        self.assertIn("multi-factor authentication", response.lower())


if __name__ == "__main__":
    unittest.main()
