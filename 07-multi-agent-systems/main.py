"""
Multi-Agent Systems — How Specialized Agents Coordinate
Part of: AI Agents with Python 2026

This example demonstrates the orchestration pattern from the Part 7 article:
- specialized agents with clear roles
- a shared task state
- sequential coordination
- review and validation before completion
"""

from __future__ import annotations

from orchestrator import Orchestrator


def main():
    print("Part 7: Multi-Agent Systems — How Specialized Agents Coordinate")

    task = "Explain how AI agents use Python tools safely and effectively."
    orchestrator = Orchestrator()
    result = orchestrator.run(task)

    print("\nTask:", task)
    print("Status:", result.status)
    print("\nResearch summary:")
    print(result.research["summary"] if result.research else "No research output")
    print("\nDraft preview:")
    print((result.draft or "No draft available")[:300])
    print("\nReview:")
    if result.review:
        print(result.review.get("message", "No review message"))
        if result.review.get("issues"):
            print("Issues:", result.review["issues"])
    else:
        print("No review performed")

    if result.errors:
        print("\nErrors:", result.errors)


if __name__ == "__main__":
    main()
