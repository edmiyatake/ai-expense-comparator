# src/app/main.py

from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import Tuple

from agents.dummy_planner import DummyPlannerAgent
from agents.requirements_interpreter import RequirementsInterpreterAgent
from agents.code_generator import CodeGeneratorAgent
from mcp.orchestrator import Orchestrator, OrchestratorConfig
from mcp.tools.base import ToolRegistry
from mcp.tools.llm import LLMTool
from mcp.tools.usage_tracker import UsageTracker


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def build_tool_registry() -> Tuple[ToolRegistry, UsageTracker]:
    """
    Create the ToolRegistry and attach a UsageTracker to the LLM tool.

    Returns (registry, tracker) so callers can later report usage.
    """
    registry = ToolRegistry()
    usage_tracker = UsageTracker()

    # Register the LLM tool if an API key seems to be available.
    if os.getenv("OPENAI_API_KEY"):
        registry.register(LLMTool(tracker=usage_tracker))
    else:
        logging.getLogger(__name__).warning(
            "OPENAI_API_KEY not set. LLMTool will not be registered; "
            "results will not be refined by an LLM."
        )

    return registry, usage_tracker


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
        print(
            "Enter a natural-language description of the application you want "
            "the AI Expense Comparator to design:"
        )
        user_request = input("> ").strip()

    tools, usage_tracker = build_tool_registry()
    planner = DummyPlannerAgent()
    requirements_agent = RequirementsInterpreterAgent()
    codegen_agent = CodeGeneratorAgent()

    config = OrchestratorConfig()
    orchestrator = Orchestrator(planner, tools, config)

    # 1) Planner + optional LLM refinement via orchestrator
    orchestrator_output = orchestrator.run(user_request)

    # 2) Requirements interpretation
    requirements_output = requirements_agent.run(
        user_request=user_request,
        tools=tools,
        io=None,
        planner_plan=orchestrator_output,
    )

    # 3) Code generation skeleton
    codegen_output = codegen_agent.run(
        user_request=user_request,
        tools=tools,
        io=None,
        planner_plan=orchestrator_output,
        requirements_text=requirements_output,
    )

    print("\n=== Orchestrator Output (Plan / Refined Plan) ===\n")
    print(orchestrator_output)
    print("\n===============================================\n")

    print("=== Requirements Interpreter Output ===\n")
    print(requirements_output)
    print("\n=====================================\n")

    print("=== Code Generator Output (Code Skeleton) ===\n")
    print(codegen_output)
    print("\n===========================================\n")

    # --- LLM usage report (satisfies assignment requirement) ---
    summary = usage_tracker.summary()
    print("=== LLM Usage ===")
    print(f"API calls:     {summary.call_count}")
    print(f"Total tokens:  {summary.total_tokens}")
    print("=================")


if __name__ == "__main__":
    main(sys.argv[1:])
