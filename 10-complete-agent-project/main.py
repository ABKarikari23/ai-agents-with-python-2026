"""Run the provider-neutral Part 10 knowledge assistant demo."""

from __future__ import annotations

import argparse
import logging

from app.agent import run_agent
from app.model_adapter import DemoModelAdapter
from app.memory import initialize_memory

logger = logging.getLogger("ai_agent")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    parser = argparse.ArgumentParser(description="Run the Part 10 AI agent demo.")
    parser.add_argument(
        "request",
        nargs="?",
        default="What should I check if my application is unavailable even though the server is online?",
        help="Question for the IT knowledge assistant",
    )
    args = parser.parse_args()

    initialize_memory()
    response = run_agent(
        model=DemoModelAdapter(),
        user_id="demo-user",
        request=args.request,
    )
    print(response)


if __name__ == "__main__":
    main()
