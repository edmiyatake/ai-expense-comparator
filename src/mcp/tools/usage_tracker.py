# src/mcp/tools/usage_tracker.py
from __future__ import annotations
from typing import Any, Dict
from .base import UsageTrackerTool


class InMemoryUsageTracker(UsageTrackerTool):
    def __init__(self) -> None:
        self.total_calls = 0
        self.total_tokens_prompt = 0
        self.total_tokens_completion = 0
        self.per_agent: Dict[str, Dict[str, int]] = {}

    def record_call(
        self,
        *,
        agent_name: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> None:
        self.total_calls += 1
        self.total_tokens_prompt += prompt_tokens
        self.total_tokens_completion += completion_tokens

        agent_stats = self.per_agent.setdefault(
            agent_name,
            {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0},
        )
        agent_stats["calls"] += 1
        agent_stats["prompt_tokens"] += prompt_tokens
        agent_stats["completion_tokens"] += completion_tokens

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_calls": self.total_calls,
            "total_tokens_prompt": self.total_tokens_prompt,
            "total_tokens_completion": self.total_tokens_completion,
            "per_agent": self.per_agent,
        }
