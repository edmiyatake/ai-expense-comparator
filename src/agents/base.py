# src/agents/base.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from mcp.tools.base import ToolRegistry


class OrchestratorIO(Protocol):
    """
    Minimal protocol for anything that wants to report logs / messages
    back to the orchestrator or caller.

    For now, the orchestrator itself does not implement this protocol,
    but you can extend it later.
    """

    def log(self, message: str) -> None:
        ...


class Agent(ABC):
    """
    Base class for all agents participating in the multi-agent system.
    """

    def __init__(self, name: str, description: str) -> None:
        self._name = name
        self._description = description

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @abstractmethod
    def run(
        self,
        user_request: str,
        tools: ToolRegistry,
        io: OrchestratorIO | None = None,
    ) -> str:
        """
        Execute a single agent pass.

        For the initial dummy planner, this can simply generate a textual plan.
        In a more advanced design, this might return a full "agent action" object.
        """
        raise NotImplementedError
