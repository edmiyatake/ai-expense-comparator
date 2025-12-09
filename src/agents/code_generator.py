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

    It also generates a minimal but executable Python application module under
    the generated/ directory (e.g., generated/app/app.py), so that the system
    produces real runnable code, not just documentation.

    If the LLM tool (llm_chat) is available, it uses that to generate a richer
    skeleton and app module. Otherwise it falls back to deterministic templates
    aligned with the Expense Comparator specification.
    """

    def __init__(self) -> None:
        super().__init__(
            name="code_generator",
            description="Generates a code skeleton and Python application module for Expense Comparator.",
        )

    # ------------------------------------------------------------------ #
    # Prompt construction helpers
    # ------------------------------------------------------------------ #

    def _build_prompt(
        self,
        user_request: str,
        planner_plan: Optional[str],
        requirements_text: Optional[str],
    ) -> str:
        """
        Build the LLM prompt for generating a code skeleton (Markdown).
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

    def _build_app_module_prompt(
        self,
        user_request: str,
        planner_plan: Optional[str],
        requirements_text: Optional[str],
    ) -> str:
        """
        Build the LLM prompt for generating a real, runnable Python module
        representing a minimal Expense Comparator application.
        """
        header = (
            "You are a senior Python backend engineer.\n\n"
            "Generate a SINGLE Python module for a minimal Expense Comparator CLI application.\n"
            "The module will be saved as app/app.py inside a generated/ directory.\n\n"
            "Requirements for the module:\n"
            "- Use only the Python standard library.\n"
            "- Define a dataclass `Expense` with fields: date (str), description (str), "
            "  amount (float), category (str), account (str | None).\n"
            "- Define functions to:\n"
            "  * group expenses by category\n"
            "  * compute total spending per category for a given list of expenses\n"
            "  * compare two periods of expenses and compute deltas per category\n"
            "- Provide a `main()` function that:\n"
            "  * constructs two small hard-coded example periods of expenses\n"
            "  * runs the comparison\n"
            "  * prints a readable text report to stdout showing per-category totals and deltas\n"
            "- Include a `if __name__ == '__main__':` guard that calls `main()`.\n\n"
            "Return ONLY valid Python code. Do not include Markdown, backticks, or explanations.\n"
        )

        parts = [header, "\nHigh-level context for the application:\n"]

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

        return "\n".join(parts)

    # ------------------------------------------------------------------ #
    # Deterministic fallbacks (no LLM)
    # ------------------------------------------------------------------ #

    def _fallback_skeleton(self) -> str:
        """
        Deterministic Markdown code skeleton if the LLM is not available.
        """
        return dedent(
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

    def _fallback_app_module(self) -> str:
        """
        Deterministic minimal Python app module if the LLM is not available.
        This code is intentionally simple but runnable and aligned with the
        Expense Comparator concept.
        """
        return dedent(
            """
            from __future__ import annotations

            from dataclasses import dataclass
            from collections import defaultdict
            from typing import List, Dict, Optional


            @dataclass
            class Expense:
                \"\"\"Represents a single expense record.\"\"\"
                date: str
                description: str
                amount: float
                category: str
                account: Optional[str] = None


            def group_by_category(expenses: List[Expense]) -> Dict[str, List[Expense]]:
                \"\"\"Group expenses by their category.\"\"\"
                groups: Dict[str, List[Expense]] = defaultdict(list)
                for exp in expenses:
                    groups[exp.category].append(exp)
                return groups


            def totals_by_category(expenses: List[Expense]) -> Dict[str, float]:
                \"\"\"Compute total amount spent per category.\"\"\"
                grouped = group_by_category(expenses)
                return {
                    category: sum(e.amount for e in items)
                    for category, items in grouped.items()
                }


            def compare_periods(
                period_a: List[Expense],
                period_b: List[Expense],
            ) -> Dict[str, Dict[str, float]]:
                \"\"\"
                Compare spending between two periods.

                Returns a mapping:
                    {
                        category: {
                            "period_a": total_a,
                            "period_b": total_b,
                            "delta": total_b - total_a,
                        },
                        ...
                    }
                \"\"\"
                totals_a = totals_by_category(period_a)
                totals_b = totals_by_category(period_b)

                categories = set(totals_a.keys()) | set(totals_b.keys())
                comparison: Dict[str, Dict[str, float]] = {}

                for cat in sorted(categories):
                    a_val = totals_a.get(cat, 0.0)
                    b_val = totals_b.get(cat, 0.0)
                    comparison[cat] = {
                        "period_a": a_val,
                        "period_b": b_val,
                        "delta": b_val - a_val,
                    }

                return comparison


            def format_comparison_report(comparison: Dict[str, Dict[str, float]]) -> str:
                \"\"\"Render a simple text report for CLI output.\"\"\"
                lines: List[str] = []
                lines.append("Expense Comparison Report")
                lines.append("=" * 28)
                lines.append(f"{'Category':20} {'A':>10} {'B':>10} {'Δ (B-A)':>10}")
                lines.append("-" * 54)

                for cat, data in comparison.items():
                    lines.append(
                        f"{cat:20} "
                        f"{data['period_a']:10.2f} "
                        f"{data['period_b']:10.2f} "
                        f"{data['delta']:10.2f}"
                    )

                lines.append("")
                lines.append("Positive deltas indicate increased spending in period B.")
                lines.append("Negative deltas indicate reduced spending in period B.")
                return "\\n".join(lines)


            def main() -> None:
                \"\"\"Run a simple hard-coded comparison demo.\"\"\"
                period_a = [
                    Expense(date="2025-01-01", description="Groceries", amount=120.0, category="Groceries"),
                    Expense(date="2025-01-05", description="Rent", amount=1000.0, category="Rent"),
                    Expense(date="2025-01-10", description="Coffee", amount=25.0, category="Dining Out"),
                ]

                period_b = [
                    Expense(date="2025-02-01", description="Groceries", amount=150.0, category="Groceries"),
                    Expense(date="2025-02-05", description="Rent", amount=1000.0, category="Rent"),
                    Expense(date="2025-02-11", description="Dinner", amount=60.0, category="Dining Out"),
                    Expense(date="2025-02-15", description="Movie", amount=30.0, category="Entertainment"),
                ]

                comparison = compare_periods(period_a, period_b)
                report = format_comparison_report(comparison)
                print(report)


            if __name__ == "__main__":
                main()
            """
        ).strip()

    # ------------------------------------------------------------------ #
    # Main run method
    # ------------------------------------------------------------------ #

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
        skeleton_text: str | None = None

        # --- Preferred path: use LLM tool for skeleton --- #
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
                skeleton_text = result.output.strip()
            else:
                if io:
                    io.log(
                        f"[{self.name}] LLM tool failed during code skeleton generation, "
                        f"falling back to deterministic skeleton: {result.error}"
                    )

        # --- Fallback: deterministic skeleton if no LLM or LLM failed --- #
        if skeleton_text is None:
            if io:
                io.log(f"[{self.name}] Using fallback deterministic code skeleton.")
            skeleton_text = self._fallback_skeleton()

        # --- Persist skeleton to disk via File tool, if available --- #
        if "file" in tools_dict:
            if io:
                io.log(f"[{self.name}] Writing code skeleton to file tool.")
            file_result = tools.invoke(
                "file",
                {
                    "operation": "write",
                    # Path is relative to generated/ root
                    "path": "docs/code_skeleton.md",
                    "content": skeleton_text,
                },
            )
            if not file_result.success and io:
                io.log(
                    f"[{self.name}] Failed to write code skeleton via file tool: "
                    f"{file_result.error}"
                )
        else:
            if io:
                io.log(f"[{self.name}] File tool not registered; skipping skeleton file write.")

        # ------------------------------------------------------------------
        # New: generate executable Python app module under generated/app/
        # ------------------------------------------------------------------
        if io:
            io.log(f"[{self.name}] Starting app module generation.")

        app_module_code: str | None = None

        # Preferred: use LLM to generate app/app.py
        if "llm_chat" in tools_dict:
            prompt = self._build_app_module_prompt(
                user_request=user_request,
                planner_plan=planner_plan,
                requirements_text=requirements_text,
            )
            result = tools.invoke(
                "llm_chat",
                {
                    "prompt": prompt,
                    "system_prompt": (
                        "You generate clean, runnable Python modules. "
                        "Return only valid Python code, no Markdown, no commentary."
                    ),
                },
            )
            if result.success and isinstance(result.output, str):
                app_module_code = result.output.strip()
                if io:
                    io.log(f"[{self.name}] Successfully generated app module via LLM.")
            else:
                if io:
                    io.log(
                        f"[{self.name}] LLM tool failed during app module generation, "
                        f"falling back to deterministic module: {getattr(result, 'error', None)}"
                    )

        # Fallback deterministic module if LLM not available or failed
        if app_module_code is None:
            if io:
                io.log(f"[{self.name}] Using fallback deterministic app module.")
            app_module_code = self._fallback_app_module()

        # Write app/app.py and app/__init__.py through File tool
        if "file" in tools_dict:
            if io:
                io.log(f"[{self.name}] Writing app/app.py via file tool.")
            app_result = tools.invoke(
                "file",
                {
                    "operation": "write",
                    "path": "app/app.py",
                    "content": app_module_code,
                },
            )
            if not app_result.success and io:
                io.log(
                    f"[{self.name}] Failed to write app/app.py via file tool: "
                    f"{app_result.error}"
                )

            # Minimal __init__.py to make app a package
            if io:
                io.log(f"[{self.name}] Writing app/__init__.py via file tool.")
            init_result = tools.invoke(
                "file",
                {
                    "operation": "write",
                    "path": "app/__init__.py",
                    "content": "# Generated Expense Comparator application package\n",
                },
            )
            if not init_result.success and io:
                io.log(
                    f"[{self.name}] Failed to write app/__init__.py via file tool: "
                    f"{init_result.error}"
                )
        else:
            if io:
                io.log(
                    f"[{self.name}] File tool not registered; "
                    f"cannot persist app module to generated/."
                )

        # Return the skeleton text as the primary textual artifact
        return skeleton_text
