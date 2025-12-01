# src/mcp/tools/base.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict


class LLMTool(ABC):
    """
    Abstract interface for any LLM backend (OpenAI, Gemini, local, etc.).
    Agents will call this instead of talking to an LLM directly.
    """

    @abstractmethod
    async def generate(self, *, messages: list[dict[str, str]], **kwargs: Any) -> str:
        ...


class FileTool(ABC):
    """
    Abstract interface for reading/writing files.
    """

    @abstractmethod
    def write_file(self, path: str, content: str) -> None:
        ...

    @abstractmethod
    def read_file(self, path: str) -> str:
        ...


class UsageTrackerTool(ABC):
    """
    Tracks #calls and token counts for LLM usage.
    """

    @abstractmethod
    def record_call(
        self,
        *,
        agent_name: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> None:
        ...

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        ...
