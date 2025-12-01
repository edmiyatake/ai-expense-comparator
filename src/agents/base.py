# src/agents/base.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict

from src.mcp.tools.base import LLMTool, FileTool, UsageTrackerTool


class AgentContext:
    """
    Things any agent might need: tools, config, shared state, etc.
    For now we only pass tools.
    """

    def __init__(
        self,
        llm: LLMTool,
        file_tool: FileTool,
        usage_tracker: UsageTrackerTool,
    ) -> None:
        self.llm = llm
        self.file_tool = file_tool
        self.usage_tracker = usage_tracker
        # Later: shared memory, run id, etc.


class Agent(ABC):
    """
    Base class for all agents (Planner, Requirements Interpreter, etc.).
    """

    def __init__(self, name: str, context: AgentContext) -> None:
        self.name = name
        self.context = context

    @abstractmethod
    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agents take a 'state' dict and return an updated state.
        The orchestrator will pass the state from one agent to the next.
        """
        ...
