# src/mcp/tools/base.py

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ToolContext:
    """
    Context object passed to tools at invocation time.

    This is intentionally simple for now, but it gives you a place to add
    shared state later (e.g. logger, config, run id, etc.).
    """
    run_id: Optional[str] = None


@dataclass
class ToolCall:
    """
    A structured representation of a tool invocation request.
    """
    name: str
    arguments: Dict[str, Any]


@dataclass
class ToolResult:
    """
    A structured representation of a tool invocation result.
    """
    name: str
    success: bool
    output: Any
    error: Optional[str] = None


class Tool(ABC):
    """
    Base class for all MCP-style tools.
    """

    def __init__(self, name: str, description: str, parameters_schema: Dict[str, Any]):
        self._name = name
        self._description = description
        self._parameters_schema = parameters_schema

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def parameters_schema(self) -> Dict[str, Any]:
        """
        JSON-Schema-like description of the expected arguments.
        This is useful when you want an LLM to choose and populate tools.
        """
        return self._parameters_schema

    @abstractmethod
    def invoke(
        self,
        arguments: Dict[str, Any],
        context: Optional[ToolContext] = None,
    ) -> ToolResult:
        """
        Execute the tool with the given arguments and return a ToolResult.
        """
        raise NotImplementedError


class ToolRegistry:
    """
    Simple in-memory registry for tools, keyed by name.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool with name '{tool.name}' is already registered")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        try:
            return self._tools[name]
        except KeyError:
            raise KeyError(f"Tool '{name}' is not registered")

    def list_tools(self) -> Dict[str, Tool]:
        return dict(self._tools)

    def invoke(
        self,
        name: str,
        arguments: Dict[str, Any],
        context: Optional[ToolContext] = None,
    ) -> ToolResult:
        tool = self.get(name)
        return tool.invoke(arguments, context=context)
