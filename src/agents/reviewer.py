# src/agents/reviewer.py

from __future__ import annotations

from textwrap import dedent
from typing import Optional

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry


class ReviewerAgent(Agent):
    """
    Agent that reviews the generated requirements, code skeleton, and test
    skeletons for the Expense Comparator application.

    It focuses on:
      - Strengths and good coverage
      - Gaps and missing pieces
      - Inconsistencies between requirements, code, and tests
      - Risks and complexity hotspots
      - Recommended next steps for a human team
    """

    def __init__(self) -> None:
        super().__init__(
            name="reviewer",
            description="Reviews generated artifacts and suggests improvements.",
        )

    def _build_prompt(
        self,
        user_request: str,
        planner_plan: Optional[str],
        requirements_text: Optional[str],
        code_skeleton: Optional[str],
        test_skeleton: Optional[str],
    ) -> str:
        header = (
            "You are a senior software architect and code reviewer.\n\n"
            "The target application is an Expense Comparator. It should:\n"
            "- Load expenses (e.g., CSV exports from banks)\n"
            "- Normalize and categorize transactions\n"
            "- Compare expenses across time periods and custom date ranges\n"
            "- Provide trends and summaries (text and optional charts)\n\n"
            "You are given:\n"
            "- The user's description\n"
            "- A high-level implementation plan\n"
            "- Structured requirements\n"
            "- A code skeleton (project structure, modules, classes, functions)\n"
            "- A test skeleton (test files, scenarios, sample tests)\n\n"
            "Review these artifacts and provide feedback.\n\n"
            "Return your answer in plain Markdown with exactly these sections:\n"
            "1. Strengths (what is well-covered)\n"
            "2. Gaps and Missing Coverage\n"
            "3. Inconsistencies or Misalignments\n"
            "4. Risks and Complexity Hotspots\n"
            "5. Recommended Next Steps\n"
        )

        parts = [header, "\nUser Description:\n", user_request.strip(), "\n"]

        if planner_plan:
            parts.extend(
                [
                    "High-level Implementation Plan:\n",
                    planner_plan.strip(),
                    "\n",
                ]
            )

        if requirements_text:
            parts.extend(
                [
                    "Structured Requirements:\n",
                    requirements_text.strip(),
                    "\n",
                ]
            )

        if code_skeleton:
            parts.extend(
                [
                    "Code Skeleton:\n",
                    code_skeleton.strip(),
                    "\n",
                ]
            )

        if test_skeleton:
            parts.extend(
                [
                    "Test Skeleton:\n",
                    test_skeleton.strip(),
                    "\n",
                ]
            )

        return "\n".join(parts)

    def run(
        self,
        user_request: str,
        tools: ToolRegistry,
        io: OrchestratorIO | None = None,
        planner_plan: Optional[str] = None,
        requirements_text: Optional[str] = None,
        code_skeleton: Optional[str] = None,
        test_skeleton: Optional[str] = None,
    ) -> str:
        if io:
            io.log(f"[{self.name}] Starting review of generated artifacts.")

        tools_dict = tools.list_tools()
        if "llm_chat" in tools_dict:
            if io:
                io.log(f"[{self.name}] Using llm_chat tool for review.")

            prompt = self._build_prompt(
                user_request=user_request,
                planner_plan=planner_plan,
                requirements_text=requirements_text,
                code_skeleton=code_skeleton,
                test_skeleton=test_skeleton,
            )

            result = tools.invoke(
                "llm_chat",
                {
                    "prompt": prompt,
                    "system_prompt": (
                        "You are a concise, constructive reviewer. "
                        "Follow the requested sections exactly. "
                        "Be specific but avoid long essays."
                    ),
                },
            )

            if result.success and isinstance(result.output, str):
                if io:
                    io.log(f"[{self.name}] Successfully produced review via LLM.")
                return result.output.strip()

            if io:
                io.log(
                    f"[{self.name}] LLM tool failed during review, "
                    f"falling back to deterministic review: {result.error}"
                )

        # Fallback deterministic review if no LLM is available or it fails.
        if io:
            io.log(f"[{self.name}] Using fallback deterministic review.")

        fallback = dedent(
            """
            # Strengths (what is well-covered)

            - Clear separation of concerns in the code skeleton:
              - CSV I/O, normalization, categorization, time window handling,
                aggregation, comparison, and visualization are modeled as distinct modules.
            - Domain models (Transaction, ExpenseCategory, TimeWindow, ComparisonResult)
              align well with the Expense Comparator requirements.
            - Test skeletons cover all major modules:
              - CSV loading, normalization, categorization, time windows,
                aggregation, and comparison.
            - Example pytest-style tests demonstrate realistic usage patterns
              (e.g., tmp_path for CSVs, simple aggregation/comparison flows).

            # Gaps and Missing Coverage

            - Visualization module is not explicitly covered by tests
              (e.g., ensuring tables/graphs reflect ComparisonResult data correctly).
            - Configuration behavior (config.settings) is not tested,
              especially category rules, bank-specific mappings, and date formats.
            - Edge cases around multiple currencies, very large datasets,
              or missing/duplicate transactions are only mentioned but not fully explored.
            - No explicit tests for error-handling paths in normalization
              (e.g., invalid dates, non-numeric amounts beyond CSV I/O).

            # Inconsistencies or Misalignments

            - Requirements mention helping users understand spending patterns
              and “financial well-being,” but there is no explicit module for
              “insights” or “recommendations” beyond raw comparisons.
            - TimeWindow and comparison logic is well represented, but
              non-functional requirements (performance, robustness) are not reflected
              in the tests beyond a brief note on large CSVs.
            - The CLI entrypoint (app.main) is described as orchestrating the pipeline,
              but there are no tests specifically validating CLI wiring or argument parsing.

            # Risks and Complexity Hotspots

            - Normalization and categorization rules can become complex as more banks
              and categories are added; this may require more sophisticated configuration
              or rule engines over time.
            - Time window and aggregation logic can be error-prone around boundary dates,
              time zones, and daylight savings adjustments (if applicable).
            - Visualization may introduce external dependencies (plotting libraries)
              that can complicate testing and deployment environments.
            - Performance and memory usage could become an issue with very large
              CSV files or many time windows if aggregation/comparison are not optimized.

            # Recommended Next Steps

            - Add tests for:
              - config.settings behavior, especially category rules and bank-specific schemas.
              - visualization, even if using simple text-based output assertions.
              - CLI-level integration (smoke tests that run a small end-to-end scenario).
            - Consider introducing an “insights” or “recommendations” module that:
              - Highlights biggest spending increases,
              - Flags categories that consistently overshoot a baseline,
              - Suggests categories to investigate.
            - Define concrete performance expectations (e.g., number of transactions)
              and add at least one stress-style test for aggregation/comparison.
            - Refine error-handling paths so that bad data is surfaced clearly to users,
              and add corresponding negative tests.
            """
        ).strip()

        return fallback
