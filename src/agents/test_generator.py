from __future__ import annotations

from textwrap import dedent
from typing import Optional

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry


class TestGeneratorAgent(Agent):
    """
    Agent that turns the code skeleton + requirements into a set of test skeletons
    for the Expense Comparator application.

    It focuses on:
      - Unit tests for core comparison logic and aggregations
      - Tests for CSV parsing / normalization / categorization
      - Edge cases and validation behavior

    If the LLM tool (llm_chat) is available, it uses that to generate richer
    test skeletons. Otherwise it falls back to a deterministic template aligned
    with the Expense Comparator specification.

    The final test skeletons are also written to
    generated/artifacts/test_skeletons.md via the File tool when available.
    """

    def __init__(self) -> None:
        super().__init__(
            name="test_generator",
            description="Generates test skeletons for the Expense Comparator.",
        )

    # --------------------------------------------------------------------- #
    # Prompt construction
    # --------------------------------------------------------------------- #

    def _build_prompt(
        self,
        user_request: str,
        planner_plan: Optional[str],
        requirements_text: Optional[str],
        code_skeleton: Optional[str],
    ) -> str:
        """
        Build the LLM prompt for generating test skeletons.
        """
        header = (
            "You are a senior software engineer focused on testing.\n\n"
            "The target application is an Expense Comparator in the finance domain.\n"
            "It allows users to enter or upload expenses, categorize them, and\n"
            "compare spending across time periods using charts and summaries.\n\n"
            "Given the inputs below (requirements and code skeleton), propose a\n"
            "concrete Python test plan and test skeletons.\n\n"
            "Return your answer in Markdown with exactly these sections:\n"
            "1. Test Strategy Overview\n"
            "2. Unit Test Skeletons (by module)\n"
            "3. Edge Cases and Negative Tests\n"
            "4. Test Data Suggestions\n\n"
            "In the 'Unit Test Skeletons' section, write pytest-style test function\n"
            "skeletons (names and docstrings, with TODOs instead of real asserts).\n"
            "Do NOT write full implementations or full fixtures; only skeletons.\n"
        )

        parts: list[str] = [header, "\nUser Description:\n", user_request.strip(), "\n"]

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

        return "\n".join(parts)

    # --------------------------------------------------------------------- #
    # Main run
    # --------------------------------------------------------------------- #

    def run(
        self,
        user_request: str,
        tools: ToolRegistry,
        io: OrchestratorIO | None = None,
        planner_plan: Optional[str] = None,
        requirements_text: Optional[str] = None,
        code_skeleton: Optional[str] = None,
    ) -> str:
        if io:
            io.log(f"[{self.name}] Starting test skeleton generation.")

        tools_dict = tools.list_tools()
        test_skeletons: str | None = None

        # --- Preferred path: use LLM tool if available ---
        if "llm_chat" in tools_dict:
            if io:
                io.log(f"[{self.name}] Using llm_chat tool to generate test skeletons.")

            prompt = self._build_prompt(
                user_request=user_request,
                planner_plan=planner_plan,
                requirements_text=requirements_text,
                code_skeleton=code_skeleton,
            )

            result = tools.invoke(
                "llm_chat",
                {
                    "prompt": prompt,
                    "system_prompt": (
                        "You are a precise, pragmatic test engineer. "
                        "Return only the requested Markdown sections with pytest-style "
                        "test skeletons (function names, brief docstrings, and TODOs)."
                    ),
                },
            )

            if result.success and isinstance(result.output, str):
                if io:
                    io.log(
                        f"[{self.name}] Successfully generated test skeletons via LLM."
                    )
                test_skeletons = result.output.strip()
            else:
                if io:
                    io.log(
                        f"[{self.name}] LLM tool failed during test generation, "
                        f"falling back to deterministic skeletons: {result.error}"
                    )

        # --- Fallback: deterministic test skeletons if no LLM or LLM failed ---
        if test_skeletons is None:
            if io:
                io.log(f"[{self.name}] Using fallback deterministic test skeletons.")

            test_skeletons = dedent(
                """
                # Test Strategy Overview

                The primary focus of testing is to ensure that:
                - CSV imports and normalization behave correctly for valid and invalid inputs.
                - Transactions are categorized as expected based on configuration rules.
                - Aggregation and comparison logic produce correct totals and deltas.
                - Visualization/report generation functions consume ComparisonResult objects
                  and produce stable, deterministic outputs for the same inputs.

                We will use pytest-based unit tests for core modules and functions.

                # Unit Test Skeletons (by module)

                ## tests/test_csv_io.py

                ```python
                import pytest

                from expense_comparator.csv_io import load_csv_files

                def test_load_csv_files_valid_input():
                    \"\"\"Loading a well-formed CSV should return a list of Transaction-like objects.\"\"\"
                    # TODO: Arrange a sample CSV file or in-memory representation.
                    # TODO: Call load_csv_files and assert length and basic fields.
                    pass

                def test_load_csv_files_missing_required_columns():
                    \"\"\"Missing required columns should result in a clear validation error.\"\"\"
                    # TODO: Prepare a CSV missing the 'amount' column.
                    # TODO: Assert that an appropriate exception or error is raised.
                    pass
                ```

                ## tests/test_normalization.py

                ```python
                import pytest

                from expense_comparator.normalization import normalize_transactions

                def test_normalize_transactions_sign_and_date_handling():
                    \"\"\"Normalization should correctly handle debit/credit signs and date formats.\"\"\"
                    # TODO: Provide raw rows with different sign conventions and date formats.
                    # TODO: Assert that normalized Transaction objects have correct amounts and dates.
                    pass
                ```

                ## tests/test_categorization.py

                ```python
                import pytest

                from expense_comparator.categorization import categorize_transactions

                def test_categorize_transactions_basic_rules():
                    \"\"\"Transactions should be categorized according to configured rules.\"\"\"
                    # TODO: Provide transactions and a simple category rule set.
                    # TODO: Assert that each transaction has the expected normalized_category.
                    pass
                ```

                ## tests/test_aggregation.py

                ```python
                import pytest

                from expense_comparator.aggregation import aggregate_expenses

                def test_aggregate_expenses_by_category_and_window():
                    \"\"\"Aggregate totals per category and time window should match expected sums.\"\"\"
                    # TODO: Build a small set of transactions across categories and time windows.
                    # TODO: Assert that aggregation results match manually computed totals.
                    pass
                ```

                ## tests/test_comparison.py

                ```python
                import pytest

                from expense_comparator.comparison import compare_expenses

                def test_compare_expenses_detects_increases_and_decreases():
                    \"\"\"ComparisonResult should correctly indicate increases/decreases per category.\"\"\"
                    # TODO: Construct aggregated data for two windows with known differences.
                    # TODO: Assert that per_category_deltas and total_delta match expectations.
                    pass
                ```

                # Edge Cases and Negative Tests

                1. CSV rows with invalid dates (e.g., malformed strings) should be rejected with clear errors.
                2. CSV rows with non-numeric amounts should be rejected or skipped with explicit logging.
                3. Empty datasets (no transactions) should not crash; comparisons should yield zero totals.
                4. Single-window comparisons should gracefully indicate that there is nothing to compare.
                5. Overlapping time windows should be tested to ensure they are handled or explicitly disallowed.

                # Test Data Suggestions

                1. Small synthetic CSVs (5–20 rows) for focused unit tests of parsing and normalization.
                2. A moderate-sized dataset (hundreds of rows) to validate performance and stability.
                3. Cases with multiple accounts and overlapping categories to test aggregation correctness.
                4. Scenarios with significant changes in spending patterns to validate comparison logic.
                """
            ).strip()

        # --- Persist test skeletons via File tool, if available ---
        if "file" in tools_dict:
            if io:
                io.log(f"[{self.name}] Writing test skeletons via file tool.")
            file_result = tools.invoke(
                "file",
                {
                    "operation": "write",
                    # Relative to FileTool's sandbox root (generated/)
                    "path": "artifacts/test_skeletons.md",
                    "content": test_skeletons,
                },
            )
            if not file_result.success and io:
                io.log(
                    f"[{self.name}] Failed to write test skeletons via file tool: "
                    f"{file_result.error}"
                )
        else:
            if io:
                io.log(f"[{self.name}] File tool not registered; skipping test write.")

        return test_skeletons
