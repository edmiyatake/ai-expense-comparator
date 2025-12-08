# src/agents/dummy_planner.py

from __future__ import annotations

from textwrap import dedent

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry


class DummyPlannerAgent(Agent):
    """
    Extremely simple planner used as a placeholder.

    Given a user request (the high-level description of the software),
    it emits a coarse system plan that the orchestrator can later refine.
    """

    def __init__(self) -> None:
        super().__init__(
            name="dummy_planner",
            description="Produces a simple step-by-step implementation plan.",
        )

    def run(
        self,
        user_request: str,
        tools: ToolRegistry,
        io: OrchestratorIO | None = None,
    ) -> str:
        if io:
            io.log(f"[{self.name}] Received user request for planning.")

        # Very naive “planning” that just restates the request and a template plan.
        plan = dedent(
            f"""
            High-level plan for the requested application:

            1. Clarify requirements from the natural-language description.
            2. Derive domain model: entities, relationships, and constraints for expenses.
            3. Define core services and APIs for creating, listing, and comparing expenses.
            4. Decide on storage schema (e.g., relational DB for expenses, NoSQL for logs).
            5. Generate a backend scaffolding with routes, handlers, and validation.
            6. Generate a minimal frontend or CLI flow for inputting expenses and comparisons.
            7. Integrate evaluation and regression tests for the generated application.
            8. Iterate on the design based on tool feedback and user adjustments.

            Original user request:
            {user_request.strip()}
            """
        ).strip()

        if io:
            io.log(f"[{self.name}] Produced plan with {len(plan.splitlines())} lines.")

        return plan
