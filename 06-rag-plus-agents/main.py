"""
RAG + AI Agents — Connecting Agents to Your Own Knowledge Sources
Part of: AI Agents with Python 2026

This example demonstrates the RAG concept described in the article:
- a small knowledge base
- relevance-based document retrieval
- a simple agent that answers using retrieved context instead of guessing
"""

from __future__ import annotations


class RAGRetriever:
    """Simple keyword-based retriever for a small knowledge base."""

    def __init__(self, knowledge_base: dict):
        self.knowledge_base = knowledge_base

    def search(self, query: str, limit: int = 3):
        query_words = set(query.lower().split())
        scored = []

        for source, text in self.knowledge_base.items():
            source_lower = source.lower()
            text_lower = text.lower()
            score = 0

            for word in query_words:
                if word in source_lower:
                    score += 3
                if word in text_lower:
                    score += 1

            if score > 0:
                scored.append({"source": source, "text": text, "score": score})

        return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]


class RAGAgent:
    """Agent that answers using retrieved knowledge instead of general assumptions."""

    def __init__(self, knowledge_base: dict):
        self.retriever = RAGRetriever(knowledge_base)

    def answer(self, question: str) -> str:
        matches = self.retriever.search(question)

        if not matches:
            return (
                "I couldn't find relevant information in the knowledge base for this question. "
                "Please check the available documents or ask a different question."
            )

        context = "\n\n".join(
            f"Source: {match['source']}\n{match['text']}" for match in matches
        )

        return (
            f"Using the retrieved knowledge, here is the answer: {context} "
            f"This clearly indicates that the relevant knowledge strongly supports the answer."
        )


def main():
    print("Part 6: RAG + AI Agents — Connecting Agents to Your Own Knowledge Sources")

    knowledge_base = {
        "vpn.txt": "Employees accessing the corporate VPN must use multi-factor authentication.",
        "network.txt": "Network connectivity problems should be checked for IP configuration and DNS.",
        "security.txt": "Employees must never share passwords or API keys.",
    }

    retriever = RAGRetriever(knowledge_base)
    agent = RAGAgent(knowledge_base)

    question = "How do I reset my VPN password?"
    results = retriever.search(question)

    print("\nRelevant retrieved documents:")
    for item in results:
        print(f"- {item['source']} (score: {item['score']})")

    print("\nAgent answer:")
    print(agent.answer(question))


if __name__ == "__main__":
    main()
