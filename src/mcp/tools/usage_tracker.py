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
    """
    Aggregated usage information for the LLM, including per-agent breakdown.
    """
    call_count: int
    total_tokens: int
    per_agent: Dict[str, AgentUsageSummary]


class UsageTracker:
    """
    Tracks LLM usage across a single run of the application.

    It records:
      - total number of API calls
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
        Record a single LLM API call.

        total_tokens may be None if the API did not return usage stats
        (in that case we only increment the call count).

        agent is the logical caller (e.g. 'planner', 'requirements_interpreter').
        """
        self._call_count += 1

        if total_tokens is not None:
            self._total_tokens += total_tokens

            if agent is not None:
                # Initialize per-agent summary if needed
                if agent not in self._per_agent:
                    self._per_agent[agent] = AgentUsageSummary(
                        call_count=0,
                        total_tokens=0,
                    )
                # Update that agent's stats
                agent_summary = self._per_agent[agent]
                agent_summary.call_count += 1
                agent_summary.total_tokens += total_tokens

    @property
    def call_count(self) -> int:
        return self._call_count

    @property
    def total_tokens(self) -> int:
        return self._total_tokens

    @property
    def per_agent(self) -> Dict[str, AgentUsageSummary]:
        return self._per_agent

    def summary(self) -> LLMUsageSummary:
        return LLMUsageSummary(
            call_count=self._call_count,
            total_tokens=self._total_tokens,
            per_agent=dict(self._per_agent),
        )
