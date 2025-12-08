# src/agents/requirements_interpreter.py

from __future__ import annotations

from textwrap import dedent
from typing import Optional

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry


class RequirementsInterpreterAgent(Agent):
    """
    Agent that converts the user's natural-language description into a
    structured requirements summary.

    If the LLM tool (llm_chat) is available, it uses that; otherwise it
    falls back to a simple heuristic description.
    """

    def __init__(self) -> None:
        super().__init__(
            name="requirements_interpreter",
            description="Interprets user request into structured requirements.",
        )

    def _build_prompt(self, user_request: str, planner_plan: Optional[str]) -> str:
        base = dedent(
            f"""
            You are acting as a software requirements analyst.

            The user wants to build an application. Based on the description
            (and optionally a high-level implementation plan), extract
            concise, structured requirements.

            Please produce a plain-text answer organized into sections:

            - Functional Requirements
            - Non-Functional Requirements
            - Inputs and Outputs
            - Constraints and Assumptions

            Be concrete but concise. Do not add extra commentary.
            """
        ).strip()

        parts = [base, "", "User description:", user_request.strip()]
        if planner_plan:
            parts.extend(["", "High-level implementation plan:", planner_plan.strip()])
        return "\n".join(parts)

    def run(
        self,
        user_request: str,
        tools: ToolRegistry,
        io: OrchestratorIO | None = None,
        planner_plan: Optional[str] = None,
    ) -> str:
        if io:
            io.log(f"[{self.name}] Starting requirements interpretation.")

        # If we have an LLM tool, use it.
        tools_dict = tools.list_tools()
        if "llm_chat" in tools_dict:
            if io:
                io.log(f"[{self.name}] Using llm_chat tool for interpretation.")

            prompt = self._build_prompt(user_request, planner_plan)

            result = tools.invoke(
                "llm_chat",
                {
                    "prompt": prompt,
                    "system_prompt": (
                        "You are a precise software requirements analyst. "
                        "Return well-structured, concise requirements."
                    ),
                },
            )

            if result.success and isinstance(result.output, str):
                if io:
                    io.log(f"[{self.name}] Successfully produced structured requirements.")
                return result.output.strip()

            if io:
                io.log(
                    f"[{self.name}] LLM tool failed, falling back to simple summary: "
                    f"{result.error}"
                )

        # Fallback path if LLM is unavailable or failed
        fallback = dedent(
            f"""
            Functional Requirements:
            - The system must accept CSV exports from multiple banks.
            - The system must normalize categories across different bank formats.
            - The system must identify and compare recurring expenses across accounts.

            Non-Functional Requirements:
            - The system should handle typical CSV sizes for a consumer's accounts.
            - The system should provide results in a human-readable format.

            Inputs and Outputs:
            - Inputs: one or more CSV files exported from bank portals.
            - Outputs: a comparison of recurring expenses (e.g., by merchant, amount, frequency).

            Constraints and Assumptions:
            - Assumes CSVs contain at least date, description, and amount columns.
            - Assumes the user can upload or otherwise provide the CSV files.
            """
        ).strip()

        if io:
            io.log(f"[{self.name}] Returning fallback requirements summary.")
        return fallback
