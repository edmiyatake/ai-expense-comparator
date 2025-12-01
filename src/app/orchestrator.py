# src/app/orchestrator.py
from __future__ import annotations
from typing import Any, Dict, List

from src.agents.base import AgentContext
from src.agents.planner import PlannerAgent
from src.mcp.tools.llm_stub import StubLLM
from src.mcp.tools.file_stub import LocalFileTool
from src.mcp.tools.usage_tracker import InMemoryUsageTracker


class Orchestrator:
    """
    Coordinates the multi-agent pipeline for one generation request.
    """

    def __init__(self) -> None:
        # In a fancier version these would be injected / configured.
        self.usage_tracker = InMemoryUsageTracker()
        self.llm = StubLLM()
        self.file_tool = LocalFileTool()
        self.context = AgentContext(
            llm=self.llm,
            file_tool=self.file_tool,
            usage_tracker=self.usage_tracker,
        )

        # Initialize agents in the order they should run
        self.agents = [
            PlannerAgent("planner", self.context),
            # TODO: add RequirementsInterpreterAgent, CodeGeneratorAgent, etc.
        ]

    async def run(
        self,
        *,
        description: str,
        requirements: List[str],
    ) -> Dict[str, Any]:
        """
        Execute the end-to-end pipeline and return final state.
        """
        state: Dict[str, Any] = {
            "description": description,
            "requirements": requirements,
        }

        for agent in self.agents:
            state = await agent.run(state)

        # For now, pretend we generated some files:
        state.setdefault("code_paths", ["generated/app.py"])
        state.setdefault("test_paths", ["generated/test_app.py"])
        return state

    def get_usage_stats(self) -> Dict[str, Any]:
        return self.usage_tracker.get_stats()
