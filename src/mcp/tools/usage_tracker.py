# src/mcp/tools/usage_tracker.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class AgentUsageSummary:
    """Aggregated usage information for a single agent."""
    call_count: int
    total_tokens: int


@dataclass
class LLMUsageSummary:
    """Aggregated LLM usage information, including per-agent breakdown."""
    call_count: int
    total_tokens: int
    per_agent: Dict[str, AgentUsageSummary]


class UsageTracker:
    """
    Tracks LLM usage across a single run of the application.

    Records:
      - total API calls
      - total tokens used (prompt + completion)
      - per-agent call count and token usage
    """

    def __init__(self) -> None:
        self._call_count: int = 0
        self._total_tokens: int = 0
        self._per_agent: Dict[str, AgentUsageSummary] = {}

    def record_call(
        self,
        total_tokens: int | None,
        agent: str | None = None,
    ) -> None:
        """
        Record an LLM API call.

        total_tokens may be None if the API response lacks usage info.
        agent is the logical caller (e.g., 'planner', 'code_generator').
        """
        self._call_count += 1

        # Update global token counter
        if total_tokens is not None:
            self._total_tokens += total_tokens

        # Update per-agent stats
        if agent is not None:
            if agent not in self._per_agent:
                self._per_agent[agent] = AgentUsageSummary(
                    call_count=0,
                    total_tokens=0,
                )

            agent_summary = self._per_agent[agent]
            agent_summary.call_count += 1

            if total_tokens is not None:
                agent_summary.total_tokens += total_tokens

    @property
    def call_count(self) -> int:
        return self._call_count

    @property
    def total_tokens(self) -> int:
        return self._total_tokens

    @property
    def per_agent(self) -> Dict[str, AgentUsageSummary]:
        # Return a shallow copy to prevent outside mutation
        return dict(self._per_agent)

    def summary(self) -> LLMUsageSummary:
        """Return aggregated usage info for reporting."""
        return LLMUsageSummary(
            call_count=self._call_count,
            total_tokens=self._total_tokens,
            per_agent=self.per_agent,  # already a safe copy
        )
