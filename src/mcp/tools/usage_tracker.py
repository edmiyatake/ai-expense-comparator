# src/mcp/tools/usage_tracker.py

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LLMUsageSummary:
    """Aggregated usage information for the LLM."""
    call_count: int
    total_tokens: int


class UsageTracker:
    """
    Tracks LLM usage across a single run of the application.

    It records:
      - number of API calls
      - total tokens used (prompt + completion)
    """

    def __init__(self) -> None:
        self._call_count: int = 0
        self._total_tokens: int = 0

    def record_call(self, total_tokens: int | None) -> None:
        """
        Record a single LLM API call.

        total_tokens may be None if the API did not return usage stats
        (in that case we only increment the call count).
        """
        self._call_count += 1
        if total_tokens is not None:
            self._total_tokens += total_tokens

    @property
    def call_count(self) -> int:
        return self._call_count

    @property
    def total_tokens(self) -> int:
        return self._total_tokens

    def summary(self) -> LLMUsageSummary:
        return LLMUsageSummary(
            call_count=self._call_count,
            total_tokens=self._total_tokens,
        )
