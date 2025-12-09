# src/agents/planner.py
from __future__ import annotations

from typing import Any, Optional

from .base import Agent
from mcp.tools.base import ToolRegistry, ToolContext, ToolResult


class PlannerAgent(Agent):
    """
    Planner agent.

    Given a user request describing the AI Expense Comparator,
    produce a high-level implementation plan. By default, this uses
    the LLM tool; if the LLM is unavailable, it falls back to a
    simple hard-coded outline.
    """

    def __init__(self, llm_tool_name: str = "llm_chat") -> None:
        self._llm_tool_name = llm_tool_name

    def run(
        self,
        user_request: str,
        tools: ToolRegistry,
        io: Optional[Any] = None,
    ) -> str:
        """
        Synchronous interface to match Orchestrator.run() expectations.

        - user_request: raw natural language description / requirements
        - tools: ToolRegistry with "llm" registered
        - io: orchestrator (used for logging, if provided)
        """
        logger = getattr(io, "log", None)

        def log(msg: str) -> None:
            if callable(logger):
                logger(f"[PlannerAgent] {msg}")

        # If the LLM tool is not registered, return the stub plan.
        tool_names = tools.list_tools().keys()
        if self._llm_tool_name not in tool_names:
            log(f"LLM tool '{self._llm_tool_name}' not found; using stub plan.")
            return self._stub_plan(user_request)

        # Build a system prompt specialized for the planner role.
        system_prompt = (
            "You are the Planner Agent for an AI-driven code generation system "
            "called the AI Expense Comparator. Based on the user request, "
            "produce a clear, high-level implementation plan.\n\n"
            "Requirements for your answer:\n"
            "- Do NOT write any code.\n"
            "- Organize the plan into sections such as: Domain Model, "
            "Persistence / Storage, MCP Tools, Agents & Orchestrator, "
            "API / CLI surface, and Testing.\n"
            "- Use numbered lists or bullet points.\n"
            "- Focus on concrete components and responsibilities so other agents "
            "can implement them later."
        )

        ctx = ToolContext(run_id="planner-initial", caller="planner")

        result: ToolResult = tools.invoke(
            self._llm_tool_name,
            {
                "prompt": user_request,
                "system_prompt": system_prompt,
            },
            context=ctx,
        )

        if not result.success:
            log(f"LLM call failed ({result.error}); falling back to stub plan.")
            return self._stub_plan(user_request)

        plan_text = str(result.output).strip()
        log("LLM plan generation succeeded.")
        return plan_text

    # ------------------------------------------------------------------ #
    # Fallback stub
    # ------------------------------------------------------------------ #

    def _stub_plan(self, user_request: str) -> str:
        """
        Simple hard-coded outline used if the LLM tool is unavailable.
        Returns text because the orchestrator expects a string.
        """
        return (
            "# High-Level Plan (Stub)\n\n"
            "Based on the description of the AI Expense Comparator, we will implement:\n\n"
            "1. **Domain Models**\n"
            "   - Expense (id, date, description, amount, category, account)\n"
            "   - Category (id, name, type, color)\n"
            "   - TimeRange (start_date, end_date)\n\n"
            "2. **Data Storage Layer**\n"
            "   - In-memory repository for demo\n"
            "   - Optional persistence adapter for a real DB later\n\n"
            "3. **Comparison Engine**\n"
            "   - Compute spending by category and time range\n"
            "   - Support custom date ranges and multiple comparison periods\n\n"
            "4. **Visualization Interface**\n"
            "   - Produce chart-friendly data structures (e.g., JSON for bar/line charts)\n\n"
            "5. **Agents & MCP Tools**\n"
            "   - Requirements Interpreter Agent\n"
            "   - Code Generator Agent\n"
            "   - Test Generator Agent\n"
            "   - Reviewer Agent\n"
            "   - LLM, File, and Usage Tracker tools\n\n"
            "6. **CLI / API Surface**\n"
            "   - Simple CLI or HTTP endpoint to trigger the pipeline\n\n"
            "7. **Testing**\n"
            "   - Unit tests for comparison logic and basic agent flows.\n"
        )
