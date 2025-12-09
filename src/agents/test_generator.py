# src/agents/test_generator.py

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

    The final test skeletons are written to generated/docs/tests.md via the File
    tool when available.

    In addition, this agent generates a minimal but executable pytest test module
    under generated/tests/test_app.py, so that the system produces real runnable
    tests corresponding to the generated app/app.py module.
    """

    def __init__(self) -> None:
        super().__init__(
            name="test_generator",
            description="Generates test plans, skeletons, and pytest modules for the Expense Comparator.",
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
        Build the LLM prompt for generating test skeletons (Markdown).
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

    def _build_test_module_prompt(
        self,
        user_request: str,
        planner_plan: Optional[str],
        requirements_text: Optional[str],
        code_skeleton: Optional[str],
    ) -> str:
        """
        Build the LLM prompt for generating a real pytest test module
        targeting the generated app/app.py.
        """
        header = (
            "You are a senior Python test engineer.\n\n"
            "Generate a SINGLE pytest test module for the Expense Comparator CLI\n"
            "application implemented in the module app.app.\n\n"
            "Assume app/app.py defines at least:\n"
            "- dataclass Expense\n"
            "- function totals_by_category(expenses: List[Expense]) -> Dict[str, float]\n"
            "- function compare_periods(period_a: List[Expense], period_b: List[Expense]) "
            "  -> Dict[str, Dict[str, float]]\n\n"
            "Requirements for the test module:\n"
            "- The file will be saved as tests/test_app.py inside a generated/ directory.\n"
            "- Use pytest-style tests (plain functions starting with 'test_').\n"
            "- At the top, ensure imports work when running tests from the project root by:\n"
            "  * adjusting sys.path as needed so 'from app.app import Expense, totals_by_category, compare_periods' works.\n"
            "- Include at least 3 tests, for example:\n"
            "  * test_totals_by_category_simple_case\n"
            "  * test_compare_periods_detects_increase\n"
            "  * test_compare_periods_handles_missing_categories\n"
            "- Use real assertions, not TODOs, so the tests are executable.\n"
            "- Use small, in-memory Expense lists; do NOT read files.\n\n"
            "Return ONLY valid Python code. Do not include Markdown, backticks, or explanations.\n"
        )

        parts: list[str] = [header, "\nContext for the application and tests:\n"]

        parts.append("User Description:\n")
        parts.append(user_request.strip())
        parts.append("\n")

        if planner_plan:
            parts.append("High-level Implementation Plan:\n")
            parts.append(planner_plan.strip())
            parts.append("\n")

        if requirements_text:
            parts.append("Structured Requirements:\n")
            parts.append(requirements_text.strip())
            parts.append("\n")

        if code_skeleton:
            parts.append("Code Skeleton (summary):\n")
            parts.append(code_skeleton.strip()[:2000])  # avoid overly long prompts
            parts.append("\n")

        return "\n".join(parts)

    # --------------------------------------------------------------------- #
    # Deterministic fallback test artifacts
    # --------------------------------------------------------------------- #

    def _fallback_markdown_skeletons(self) -> str:
        """
        Deterministic Markdown test skeletons if the LLM is not available.
        """
        return dedent(
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

    def _fallback_test_module(self) -> str:
        """
        Deterministic minimal pytest module if the LLM is not available.
        This targets the generated app/app.py module and provides real,
        runnable tests.
        """
        return dedent(
            """
            import sys
            from pathlib import Path

            # Ensure the 'generated' directory parent is on sys.path so that
            # 'import app.app' works when tests are run from the project root.
            CURRENT_FILE = Path(__file__).resolve()
            GENERATED_ROOT = CURRENT_FILE.parents[2]  # .../generated/
            PROJECT_ROOT = GENERATED_ROOT.parent
            if str(PROJECT_ROOT) not in sys.path:
                sys.path.insert(0, str(PROJECT_ROOT))

            import pytest  # type: ignore

            from app.app import Expense, totals_by_category, compare_periods


            def test_totals_by_category_simple_case():
                expenses = [
                    Expense(date="2025-01-01", description="Groceries", amount=50.0, category="Groceries"),
                    Expense(date="2025-01-02", description="Groceries", amount=30.0, category="Groceries"),
                    Expense(date="2025-01-03", description="Rent", amount=1000.0, category="Rent"),
                ]

                totals = totals_by_category(expenses)

                assert totals["Groceries"] == pytest.approx(80.0)
                assert totals["Rent"] == pytest.approx(1000.0)
                # No other categories should be present
                assert set(totals.keys()) == {"Groceries", "Rent"}


            def test_compare_periods_detects_increase():
                period_a = [
                    Expense(date="2025-01-01", description="Groceries", amount=50.0, category="Groceries"),
                ]
                period_b = [
                    Expense(date="2025-02-01", description="Groceries", amount=80.0, category="Groceries"),
                ]

                comparison = compare_periods(period_a, period_b)
                groceries = comparison["Groceries"]

                assert groceries["period_a"] == pytest.approx(50.0)
                assert groceries["period_b"] == pytest.approx(80.0)
                assert groceries["delta"] == pytest.approx(30.0)


            def test_compare_periods_handles_missing_categories():
                period_a = [
                    Expense(date="2025-01-01", description="Groceries", amount=50.0, category="Groceries"),
                ]
                period_b = [
                    Expense(date="2025-02-01", description="Rent", amount=1000.0, category="Rent"),
                ]

                comparison = compare_periods(period_a, period_b)

                # Groceries only in period A
                groceries = comparison["Groceries"]
                assert groceries["period_a"] == pytest.approx(50.0)
                assert groceries["period_b"] == pytest.approx(0.0)
                assert groceries["delta"] == pytest.approx(-50.0)

                # Rent only in period B
                rent = comparison["Rent"]
                assert rent["period_a"] == pytest.approx(0.0)
                assert rent["period_b"] == pytest.approx(1000.0)
                assert rent["delta"] == pytest.approx(1000.0)
            """
        ).strip()

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

        # --- Preferred path: use LLM tool for Markdown skeletons --- #
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
                        f"[{self.name}] LLM tool failed during test Markdown generation, "
                        f"falling back to deterministic skeletons: {result.error}"
                    )

        # --- Fallback: deterministic test skeletons if no LLM or LLM failed --- #
        if test_skeletons is None:
            if io:
                io.log(f"[{self.name}] Using fallback deterministic test skeletons.")
            test_skeletons = self._fallback_markdown_skeletons()

        # --- Persist Markdown test skeletons via File tool, if available --- #
        if "file" in tools_dict:
            if io:
                io.log(f"[{self.name}] Writing test skeletons via file tool.")
            file_result = tools.invoke(
                "file",
                {
                    "operation": "write",
                    # Relative to FileTool's sandbox root (generated/)
                    "path": "docs/tests.md",
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
                io.log(f"[{self.name}] File tool not registered; skipping test Markdown write.")

        # ------------------------------------------------------------------ #
        # New: generate executable pytest module under generated/tests/
        # ------------------------------------------------------------------ #
        if io:
            io.log(f"[{self.name}] Starting pytest module generation.")

        test_module_code: str | None = None

        # Preferred: use LLM to generate tests/test_app.py
        if "llm_chat" in tools_dict:
            prompt = self._build_test_module_prompt(
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
                        "You generate clean, runnable pytest modules. "
                        "Return only valid Python code, no Markdown, no commentary."
                    ),
                },
            )
            if result.success and isinstance(result.output, str):
                test_module_code = result.output.strip()
                if io:
                    io.log(f"[{self.name}] Successfully generated pytest module via LLM.")
            else:
                if io:
                    io.log(
                        f"[{self.name}] LLM tool failed during pytest module generation, "
                        f"falling back to deterministic module: {getattr(result, 'error', None)}"
                    )

        # Fallback deterministic pytest module if LLM not available or failed
        if test_module_code is None:
            if io:
                io.log(f"[{self.name}] Using fallback deterministic pytest module.")
            test_module_code = self._fallback_test_module()

        # Write tests/test_app.py and tests/__init__.py through File tool
        if "file" in tools_dict:
            if io:
                io.log(f"[{self.name}] Writing tests/test_app.py via file tool.")
            test_result = tools.invoke(
                "file",
                {
                    "operation": "write",
                    "path": "tests/test_app.py",
                    "content": test_module_code,
                },
            )
            if not test_result.success and io:
                io.log(
                    f"[{self.name}] Failed to write tests/test_app.py via file tool: "
                    f"{test_result.error}"
                )

            if io:
                io.log(f"[{self.name}] Writing tests/__init__.py via file tool.")
            init_result = tools.invoke(
                "file",
                {
                    "operation": "write",
                    "path": "tests/__init__.py",
                    "content": "# Generated tests package for Expense Comparator\n",
                },
            )
            if not init_result.success and io:
                io.log(
                    f"[{self.name}] Failed to write tests/__init__.py via file tool: "
                    f"{init_result.error}"
                )
        else:
            if io:
                io.log(
                    f"[{self.name}] File tool not registered; "
                    f"cannot persist pytest module to generated/."
                )

        # Return the Markdown skeletons as the primary textual artifact
        return test_skeletons
