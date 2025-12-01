# src/agents/planner.py
from __future__ import annotations
from typing import Any, Dict

from .base import Agent


class PlannerAgent(Agent):
    """
    First agent: given description + requirements, produce a high level plan.
    For now this is a stub that just structures the input.
    """

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        description: str = state.get("description", "")
        requirements: list[str] = state.get("requirements", [])

        # TODO: call self.context.llm here to turn this into a real plan.
        high_level_plan = {
            "modules": [
                "domain models (Expense, Category, TimeRange)",
                "data storage (in-memory / DB)",
                "comparison engine",
                "charting API",
            ],
            "notes": "Stub plan for Expense Comparator based on description + requirements.",
        }

        state["plan"] = high_level_plan
        return state
