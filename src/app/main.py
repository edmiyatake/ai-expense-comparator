# src/app/main.py

from __future__ import annotations

import argparse
import logging
import os
import sys

from agents.dummy_planner import DummyPlannerAgent
from mcp.orchestrator import Orchestrator, OrchestratorConfig
from mcp.tools.base import ToolRegistry
from mcp.tools.llm import LLMTool


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def build_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    # Register the LLM tool if an API key seems to be available.
    if os.getenv("OPENAI_API_KEY"):
        registry.register(LLMTool())
    else:
        # It is not an error to run without the LLM; the orchestrator will
        # simply fall back to the raw planner output.
        logging.getLogger(__name__).warning(
            "OPENAI_API_KEY not set. LLMTool will not be registered; "
            "results will not be refined by an LLM."
        )

    return registry


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AI Expense Comparator – MCP Orchestrator CLI",
    )
    parser.add_argument(
        "request",
        nargs="?",
        help="Natural-language description of the software to generate.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    configure_logging()
    args = parse_args(argv)

    if args.request:
        user_request = args.request
    else:
        # Interactive prompt fallback
        print(
            "Enter a natural-language description of the application you want "
            "the AI Expense Comparator to design:"
        )
        user_request = input("> ").strip()

    tools = build_tool_registry()
    planner = DummyPlannerAgent()

    config = OrchestratorConfig()
    orchestrator = Orchestrator(planner=planner, tools=tools, config=config)

    result = orchestrator.run(user_request)
    print("\n=== Orchestrator Output ===\n")
    print(result)
    print("\n===========================\n")


if __name__ == "__main__":
    main(sys.argv[1:])
