# src/agents/code_generator.py

from __future__ import annotations

from textwrap import dedent
from typing import Optional

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry


class CodeGeneratorAgent(Agent):
    """
    Agent that turns plans + requirements into a concrete code skeleton for the
    Expense Comparator application.

    It proposes:
      - Project structure (folders/files)
      - Key modules and responsibilities
      - Core classes and functions

    If the LLM tool (llm_chat) is available, it uses that to generate a richer
    skeleton. Otherwise it falls back to a deterministic template aligned with
    the Expense Comparator specification.
    """

    def __init__(self) -> None:
        super().__init__(
            name="code_generator",
            description="Generates a code skeleton and module layout for Expense Comparator.",
        )

    def _build_prompt(
        self,
        user_request: str,
        planner_plan: Optional[str],
        requirements_text: Optional[str],
    ) -> str:
        """
        Build the LLM prompt for generating a code skeleton.
        """
        header = (
            "You are a senior backend engineer.\n\n"
            "The target application is an Expense Comparator in the finance domain.\n"
            "It should allow users to:\n"
            "- Input or upload expenses (e.g., CSV exports from banks).\n"
            "- Categorize expenses (groceries, transportation, entertainment, etc.).\n"
            "- Compare expenses across different time periods and custom date ranges.\n"
            "- View trends and summaries via charts/graphs and text summaries.\n"
            "- Identify areas where users can improve their financial well-being.\n\n"
            "Given the inputs below, propose a concrete Python code skeleton.\n\n"
            "Return your answer in plain Markdown with exactly these sections:\n"
            "1. Project Structure (tree layout rooted at src/)\n"
            "2. Modules and Responsibilities (1–3 sentences each)\n"
            "3. Core Classes and Functions (short signatures + 1–2 line docstrings)\n"
            "4. TODOs and Open Questions\n\n"
            "Do NOT write full implementations; only structural code skeletons and descriptions.\n"
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

        return "\n".join(parts)

    def run(
        self,
        user_request: str,
        tools: ToolRegistry,
        io: OrchestratorIO | None = None,
        planner_plan: Optional[str] = None,
        requirements_text: Optional[str] = None,
    ) -> str:
        if io:
            io.log(f"[{self.name}] Starting code skeleton generation.")

        tools_dict = tools.list_tools()
        if "llm_chat" in tools_dict:
            if io:
                io.log(f"[{self.name}] Using llm_chat tool to generate code skeleton.")

            prompt = self._build_prompt(
                user_request=user_request,
                planner_plan=planner_plan,
                requirements_text=requirements_text,
            )

            result = tools.invoke(
                "llm_chat",
                {
                    "prompt": prompt,
                    "system_prompt": (
                        "You are a precise, practical software engineer. "
                        "Return only the requested Markdown sections. "
                        "Do not add marketing language or extra commentary."
                    ),
                },
            )

            if result.success and isinstance(result.output, str):
                if io:
                    io.log(f"[{self.name}] Successfully generated code skeleton via LLM.")
                return result.output.strip()

            if io:
                io.log(
                    f"[{self.name}] LLM tool failed during code generation, "
                    f"falling back to deterministic skeleton: {result.error}"
                )

        # Fallback: deterministic skeleton if no LLM is available or it fails.
        if io:
            io.log(f"[{self.name}] Using fallback deterministic code skeleton.")

        fallback = dedent(
            """
            # Project Structure

            src/
              app/
                main.py                      # CLI entrypoint orchestrating Planner, Requirements, CodeGen
              expense_comparator/
                __init__.py
                models.py                    # Domain models: Transaction, ExpenseCategory, TimeWindow, ComparisonResult
                csv_io.py                    # Load and validate CSV files from different banks
                normalization.py             # Normalize bank-specific schemas into a common internal format
                categorization.py            # Categorize transactions into normalized categories
                time_windows.py              # Build and validate date ranges / time windows
                aggregation.py               # Aggregate expenses by category and time window
                comparison.py                # Compare aggregated expenses across time periods
                visualization.py             # Produce charts/graphs or text-based reports
              config/
                __init__.py
                settings.py                  # Global settings (paths, date formats, default categories)
              tests/
                test_csv_io.py
                test_normalization.py
                test_categorization.py
                test_time_windows.py
                test_aggregation.py
                test_comparison.py

            # Modules and Responsibilities

            - app.main
              - Parse CLI arguments (CSV file paths, date ranges, output options).
              - Coordinate the end-to-end pipeline:
                load → normalize → categorize → aggregate → compare → visualize.

            - expense_comparator.models
              - Define core dataclasses:
                - Transaction
                - ExpenseCategory
                - TimeWindow
                - ComparisonResult
              - Provide helper methods for common conversions (e.g., from dict / CSV row).

            - expense_comparator.csv_io
              - Functions to load CSV files from disk.
              - Handle bank-specific quirks (column names, date formats, decimal separators).
              - Validate required columns such as date, description, amount.

            - expense_comparator.normalization
              - Convert raw CSV rows from different banks into normalized Transaction objects.
              - Apply basic cleaning for descriptions, signs (debit/credit), and currencies.

            - expense_comparator.categorization
              - Assign each Transaction to an ExpenseCategory using rules or mappings.
              - Allow configuration of category rules in config.settings.

            - expense_comparator.time_windows
              - Build TimeWindow objects for user-specified or default ranges.
              - Helpers for:
                - current month vs previous month
                - custom start/end dates
                - rolling windows (e.g., last 90 days)

            - expense_comparator.aggregation
              - Aggregate Transactions by category and time window.
              - Compute totals, averages, and basic statistics needed for comparison.

            - expense_comparator.comparison
              - Compare aggregated expenses across time windows.
              - Identify increases/decreases by category and overall spending trends.
              - Produce ComparisonResult objects summarizing differences.

            - expense_comparator.visualization
              - Render ComparisonResult objects as:
                - text-based tables for CLI
                - optional charts/graphs (e.g., bar charts, line charts) if a plotting library is available.
              - Focus on clearly showing where spending has increased or decreased.

            - config.settings
              - Central place for:
                - default categories
                - bank-specific CSV configurations
                - date format strings
                - any feature flags.

            # Core Classes and Functions

            - class Transaction:
              - Represents a single financial transaction.
              - Fields: date, description, amount, account_id, raw_category, normalized_category.

            - class ExpenseCategory:
              - Represents a normalized category (e.g., GROCERIES, RENT, ENTERTAINMENT).
              - Fields: name, description, optional parent_category.

            - class TimeWindow:
              - Represents a closed-open date interval [start, end).
              - Fields: start_date, end_date, label (e.g., "Jan 2025", "Last 90 days").

            - class ComparisonResult:
              - Represents the result of comparing expenses across two or more TimeWindows.
              - Fields: window_a, window_b, per_category_deltas, total_delta, notes.

            - function load_csv_files(paths: list[str]) -> list[Transaction]
              - Read and parse CSV files into Transaction objects.

            - function normalize_transactions(raw_rows: list[dict]) -> list[Transaction]
              - Convert raw bank rows into normalized Transaction instances.

            - function categorize_transactions(transactions: list[Transaction]) -> list[Transaction]
              - Apply category rules and return transactions with normalized_category set.

            - function build_time_windows(config: dict, user_args: dict) -> list[TimeWindow]
              - Construct TimeWindow objects based on CLI flags or defaults.

            - function aggregate_expenses(transactions: list[Transaction], windows: list[TimeWindow]) -> dict
              - Aggregate expenses by category and time window.

            - function compare_expenses(aggregated: dict) -> list[ComparisonResult]
              - Compare aggregates between windows to find increases/decreases per category.

            - function render_report(results: list[ComparisonResult]) -> str
              - Produce a human-readable summary of spending patterns and trends.

            # TODOs and Open Questions

            - Decide whether to support only CSV uploads or also manual input / API integration.
            - Specify exact CSV schemas per bank (column names, locales, currencies).
            - Clarify expected charting library (text-only, matplotlib, or another option).
            - Determine performance requirements (max number of transactions and files per run).
            - Decide how configuration (categories, rules, date ranges) will be persisted.
            """
        ).strip()

        return fallback
