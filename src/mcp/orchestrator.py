from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .agents.base import Agent, AgentResult
from .tools.llm import LLMTool


@dataclass
class OrchestratorStepLog:
    agent_name: str
    input_data: Any
    output_data: Any
    metadata: Dict[str, Any]


@dataclass
class OrchestratorResult:
    final_output: Any
    steps: List[OrchestratorStepLog]


class Orchestrator:
    """
    Orchestrates the sequence of agents to fulfill a target request.
    """

    def __init__(self, agents: List[Agent], tools: Dict[str, Any]) -> None:
        self.agents = agents
        self.tools = tools

    def run(self, target_description: str) -> OrchestratorResult:
        """
        Run the full pipeline on a target description (e.g., 'Build an expense comparator app').
        """
        context: Dict[str, Any] = {
            "tools": self.tools,
            "target_description": target_description,
        }

        current_input: Any = target_description
        logs: List[OrchestratorStepLog] = []

        for agent in self.agents:
            result: AgentResult = agent.run(current_input, context=context)
            logs.append(
                OrchestratorStepLog(
                    agent_name=agent.name,
                    input_data=current_input,
                    output_data=result.content,
                    metadata=result.metadata,
                )
            )
            current_input = result.content  # next agent receives previous content

        return OrchestratorResult(final_output=current_input, steps=logs)
