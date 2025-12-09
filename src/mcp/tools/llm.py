# src/mcp/tools/llm.py

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from openai import OpenAI

from mcp.tools.base import Tool, ToolContext, ToolResult
from mcp.tools.usage_tracker import UsageTracker


class LLMTool(Tool):
    """
    A generic chat-completion LLM tool.

    Expected arguments:
      - prompt: str (required)
      - system_prompt: str (optional)
    """

    def __init__(
        self,
        model: Optional[str] = None,
        tracker: Optional[UsageTracker] = None,
    ) -> None:
        model_name = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

        parameters_schema: Dict[str, Any] = {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "User or agent prompt"},
                "system_prompt": {
                    "type": "string",
                    "description": "Optional system message describing behavior",
                },
            },
            "required": ["prompt"],
        }

        super().__init__(
            name="llm_chat",
            description="LLM chat-completion tool",
            parameters_schema=parameters_schema,
        )

        self._client = OpenAI()
        self._model = model_name
        self._tracker = tracker

    def _extract_total_tokens(self, response: Any) -> Optional[int]:
        """
        Try to extract total_tokens from the OpenAI response object.
        """
        usage = getattr(response, "usage", None)
        if usage is None:
            return None

        # New OpenAI client exposes attributes, not dict keys
        total = getattr(usage, "total_tokens", None)
        if total is None:
            return None

        try:
            return int(total)
        except (TypeError, ValueError):
            return None

    def invoke(
        self,
        arguments: Dict[str, Any],
        context: Optional[ToolContext] = None,
    ) -> ToolResult:
        prompt = arguments.get("prompt")
        system_prompt = arguments.get("system_prompt")

        if not isinstance(prompt, str) or not prompt.strip():
            # No API request -> no usage to record
            return ToolResult(
                name=self.name,
                success=False,
                output=None,
                error="Missing or empty 'prompt' argument",
            )

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Figure out who is calling this tool (which agent)
        caller_agent: Optional[str] = None
        if context is not None:
            # ToolContext should have caller: Optional[str]
            caller_agent = getattr(context, "caller", None)

        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
            )

            content = response.choices[0].message.content

            # Record usage: 1 call, N total tokens (if available), tagged by agent
            if self._tracker is not None:
                total_tokens = self._extract_total_tokens(response)
                self._tracker.record_call(
                    total_tokens=total_tokens,
                    agent=caller_agent,
                )

            return ToolResult(
                name=self.name,
                success=True,
                output=content,
                error=None,
            )

        except Exception as exc:  # noqa: BLE001
            # Even if the API call failed, we still count it as a call;
            # token usage is unknown in that case.
            if self._tracker is not None:
                self._tracker.record_call(
                    total_tokens=None,
                    agent=caller_agent,
                )

            return ToolResult(
                name=self.name,
                success=False,
                output=None,
                error=str(exc),
            )
