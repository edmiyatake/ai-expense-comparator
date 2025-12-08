# src/mcp/orchestrator.py

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from agents.base import Agent
from mcp.tools.base import ToolRegistry, ToolContext, ToolResult


logger = logging.getLogger(__name__)


@dataclass
class OrchestratorConfig:
    """
    Configuration for the Orchestrator.
    """
    use_llm_refinement: bool = True
    llm_tool_name: str = "llm_chat"
    system_prompt: str = (
        "You are a senior software architect helping to refine plans for an "
        "AI-driven code generation system called the AI Expense Comparator. "
        "Rewrite the given plan into a concise, actionable outline."
    )


class Orchestrator:
    """
    Main entry point for coordinating agents and tools in the MCP-style system.
    """

    def __init__(
        self,
        planner: Agent,
        tools: ToolRegistry,
        config: Optional[OrchestratorConfig] = None,
    ) -> None:
        self._planner = planner
        self._tools = tools
        self._config = config or OrchestratorConfig()

    def log(self, message: str) -> None:
        """
        Simple logging hook so agents can optionally report progress.
        """
        logger.info(message)

    def run(self, user_request: str) -> str:
        """
        Orchestrate a single end-to-end run:

        1. Ask the planner agent for a high-level plan.
        2. Optionally refine that plan through the LLM tool.
        3. Return the final text back to the caller.
        """
        self.log("[Orchestrator] Starting run.")
        self.log(f"[Orchestrator] User request: {user_request!r}")

        # Step 1: Planner
        plan = self._planner.run(user_request=user_request, tools=self._tools, io=self)
        self.log("[Orchestrator] Planner produced initial plan.")

        # Step 2: Optional LLM refinement
        if not self._config.use_llm_refinement:
            self.log("[Orchestrator] LLM refinement disabled; returning raw plan.")
            return plan

        if self._config.llm_tool_name not in self._tools.list_tools():
            self.log(
                "[Orchestrator] LLM tool not registered; returning raw planner output."
            )
            return plan

        ctx = ToolContext(run_id="initial-run")

        tool_result: ToolResult = self._tools.invoke(
            self._config.llm_tool_name,
            {
                "prompt": plan,
                "system_prompt": self._config.system_prompt,
            },
            context=ctx,
        )

        if not tool_result.success:
            self.log(
                f"[Orchestrator] LLM refinement failed: {tool_result.error}. "
                "Falling back to planner output."
            )
            return plan

        refined = str(tool_result.output).strip()
        self.log("[Orchestrator] LLM refinement succeeded.")
        return refined
