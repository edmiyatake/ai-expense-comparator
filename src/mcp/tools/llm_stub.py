# src/mcp/tools/llm_stub.py
from __future__ import annotations
from typing import Any
from .base import LLMTool


class StubLLM(LLMTool):
    """
    Temporary fake LLM that just echoes what you send.
    Useful so you can develop the orchestrator without real API keys.
    """

    async def generate(self, *, messages: list[dict[str, str]], **kwargs: Any) -> str:
        last = messages[-1]["content"] if messages else ""
        return f"[StubLLM response to]: {last[:200]}"
