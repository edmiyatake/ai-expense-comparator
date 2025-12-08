# src/agents/test_generator.py

from __future__ import annotations

from textwrap import dedent
from typing import Optional

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry


class TestGeneratorAgent(Agent):
    """
    Agent that proposes executable test cases for the generated code skeleton.

    It focuses on:
      - Module-level test files
      - Key behaviours to cover per module
      - Example pytest-style test functions

    If the LLM tool (llm_chat) is available, it uses that; otherwise it falls
    back to a deterministic template aligned with the Expense Comparator design.
    """

    def __init__(self) -> None:
        super().__init__(
            name="test_generator",
            description="Generates test skeletons for Expense Comparator modules.",
        )

    def _build_prompt(
        self,
        user_request: str,
        planner_plan: Optional[str],
        requirements_text: Optional[str],
        code_skeleton: Optional[str],
    ) -> str:
        header = (
            "You are a senior engineer specializing in testability and quality.\n\n"
            "The target application is an Expense Comparator. It allows users to:\n"
            "- Load expenses (e.g., CSV exports from banks)\n"
            "- Normalize and categorize transactions\n"
            "- Compare expenses across time periods and custom date ranges\n"
            "- View trends via text summaries and optional charts\n\n"
            "Based on the description, plan, requirements, and code skeleton below, "
            "propose an automated test suite.\n\n"
            "Return your answer in plain Markdown with these sections:\n"
            "1. Test Files and Scope (which test_*.py files exist and what they focus on)\n"
            "2. Key Test Scenarios per Module\n"
            "3. Example pytest-Style Test Functions (code blocks with minimal bodies)\n"
            "4. Edge Cases and Negative Tests\n\n"
            "Tests should target the modules in the skeleton (csv_io, normalization, "
            "categorization, time_windows, aggregation, comparison, visualization, etc.).\n"
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
                    "Proposed Code Skeleton:\n",
                    code_skeleton.strip(),
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
    ) -> str:
        if io:
            io.log(f"[{self.name}] Starting test generation.")

        tools_dict = tools.list_tools()
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
                        "You are a precise test engineer. "
                        "Return only the requested Markdown sections with pytest-style examples. "
                        "Keep the examples short and focused."
                    ),
                },
            )

            if result.success and isinstance(result.output, str):
                if io:
                    io.log(
                        f"[{self.name}] Successfully generated test skeletons via LLM."
                    )
                return result.output.strip()

            if io:
                io.log(
                    f"[{self.name}] LLM tool failed during test generation, "
                    f"falling back to deterministic test skeletons: {result.error}"
                )

        # Fallback: deterministic test plan if no LLM is available or it fails.
        if io:
            io.log(f"[{self.name}] Using fallback deterministic test skeletons.")

        fallback = dedent(
            """
            # Test Files and Scope

            tests/
              test_csv_io.py          # Loading and validating CSV inputs
              test_normalization.py   # Normalizing raw rows into Transaction objects
              test_categorization.py  # Mapping transactions to ExpenseCategory
              test_time_windows.py    # Building and validating TimeWindow objects
              test_aggregation.py     # Aggregating expenses by category and time window
              test_comparison.py      # Comparing aggregates across time windows

            # Key Test Scenarios per Module

            - test_csv_io.py
              - Successfully load a valid CSV file and return the expected number of transactions.
              - Raise an error when required columns (date, description, amount) are missing.
              - Handle invalid numeric values (non-numeric amount) gracefully.

            - test_normalization.py
              - Convert raw bank-specific rows into normalized Transaction instances.
              - Normalize positive/negative amounts consistently for debits/credits.
              - Normalize date formats (e.g., '2025-01-01', '01/01/2025') into a standard date type.

            - test_categorization.py
              - Apply simple category rules (e.g., 'Starbucks' → COFFEE / DINING).
              - Ensure unknown merchants fall back to an 'UNCATEGORIZED' category.
              - Allow configuration-based overrides from config.settings.

            - test_time_windows.py
              - Build TimeWindow objects for specific start/end dates.
              - Reject invalid ranges where start_date >= end_date.
              - Build common windows such as current month vs previous month.

            - test_aggregation.py
              - Aggregate expenses by category within a single TimeWindow.
              - Aggregate across multiple TimeWindows and return per-window totals.
              - Handle empty transaction lists without crashing.

            - test_comparison.py
              - Compare two TimeWindows and compute per-category deltas.
              - Identify categories with increased vs decreased spending.
              - Summarize total change in spending across all categories.

            # Example pytest-Style Test Functions

            ```python
            # tests/test_csv_io.py
            import pytest

            from expense_comparator.csv_io import load_csv_files

            def test_load_valid_csv(tmp_path):
                csv_content = "date,description,amount\\n2025-01-01,Coffee,-4.50\\n"
                csv_file = tmp_path / "transactions.csv"
                csv_file.write_text(csv_content)

                transactions = load_csv_files([str(csv_file)])

                assert len(transactions) == 1
                assert transactions[0].description == "Coffee"
                assert transactions[0].amount == -4.50


            def test_load_csv_missing_required_columns(tmp_path):
                csv_content = "date,amount\\n2025-01-01,-4.50\\n"
                csv_file = tmp_path / "bad.csv"
                csv_file.write_text(csv_content)

                with pytest.raises(ValueError):
                    load_csv_files([str(csv_file)])
            ```

            ```python
            # tests/test_aggregation.py
            from datetime import date

            from expense_comparator.aggregation import aggregate_expenses
            from expense_comparator.models import Transaction, TimeWindow

            def test_aggregate_single_window_single_category():
                txns = [
                    Transaction(
                        date=date(2025, 1, 1),
                        description="Coffee",
                        amount=-4.50,
                        account_id="acc-1",
                        raw_category="COFFEE",
                        normalized_category="DINING",
                    )
                ]
                window = TimeWindow(
                    start_date=date(2025, 1, 1),
                    end_date=date(2025, 2, 1),
                    label="Jan 2025",
                )

                result = aggregate_expenses(txns, [window])

                assert "DINING" in result[window.label]
                assert result[window.label]["DINING"].total == -4.50
            ```

            ```python
            # tests/test_comparison.py
            from expense_comparator.comparison import compare_expenses
            from expense_comparator.models import ComparisonResult

            def test_compare_two_windows_simple_delta():
                aggregated = {
                    "Jan 2025": {"DINING": 100.0},
                    "Feb 2025": {"DINING": 150.0},
                }

                results = compare_expenses(aggregated)

                assert isinstance(results, list)
                assert any(
                    r.window_a == "Jan 2025"
                    and r.window_b == "Feb 2025"
                    and r.per_category_deltas.get("DINING") == 50.0
                    for r in results
                )
            ```

            # Edge Cases and Negative Tests

            - Empty CSV files or files with only headers.
            - Transactions outside of all configured TimeWindows.
            - Multiple currencies (if supported) or inconsistent currency codes.
            - Extremely large CSV files (stress tests on aggregation/comparison).
            - Date parsing failures and invalid date ranges.
            - Categories that appear in one window but not another.
            """
        ).strip()

        return fallback
