# src/agents/requirements_interpreter.py

from __future__ import annotations

from textwrap import dedent
from typing import Optional

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry


class RequirementsInterpreterAgent(Agent):
    """
    Agent that turns a natural-language description + planner plan into
    a structured requirements document for the Expense Comparator.

    It focuses on:
      - Functional requirements
      - Non-functional requirements
      - Data & integration requirements
      - Visualization/reporting requirements
      - Out-of-scope items & assumptions

    If the LLM tool (llm_chat) is available, it uses that to generate a
    richer requirements document. Otherwise it falls back to a deterministic
    template aligned with the Expense Comparator specification.

    The final requirements are also written to generated/artifacts/requirements.md
    via the File tool when available.
    """

    def __init__(self) -> None:
        super().__init__(
            name="requirements_interpreter",
            description="Interprets the user description into structured requirements.",
        )

    # --------------------------------------------------------------------- #
    # Prompt construction
    # --------------------------------------------------------------------- #

    def _build_prompt(
        self,
        user_request: str,
        planner_plan: Optional[str],
    ) -> str:
        """
        Build the LLM prompt for interpreting requirements.
        """
        header = (
            "You are a senior product-minded backend engineer.\n\n"
            "The target application is an Expense Comparator in the finance domain.\n"
            "It should allow users to:\n"
            "- Manually enter expenses and optionally upload CSV exports from banks.\n"
            "- Categorize expenses into categories such as groceries, transportation, entertainment, etc.\n"
            "- Compare expenses across different time periods and custom date ranges.\n"
            "- View trends and summaries via charts/graphs and text summaries.\n"
            "- Identify areas where users can improve their financial well-being.\n\n"
            "Given the inputs below, extract a clear, structured set of requirements.\n\n"
            "Return your answer in Markdown with exactly these sections:\n"
            "1. Functional Requirements\n"
            "2. Non-Functional Requirements\n"
            "3. Data & Integration Requirements\n"
            "4. Visualization & Reporting Requirements\n"
            "5. Out-of-Scope and Assumptions\n\n"
            "Within each section, use a numbered list of short, testable statements.\n"
            "Avoid marketing language; be specific and implementation-agnostic.\n"
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
    ) -> str:
        if io:
            io.log(f"[{self.name}] Starting requirements interpretation.")

        tools_dict = tools.list_tools()
        requirements_text: str | None = None

        # --- Preferred path: use LLM tool if available ---
        if "llm_chat" in tools_dict:
            if io:
                io.log(f"[{self.name}] Using llm_chat tool to interpret requirements.")

            prompt = self._build_prompt(
                user_request=user_request,
                planner_plan=planner_plan,
            )

            result = tools.invoke(
                "llm_chat",
                {
                    "prompt": prompt,
                    "system_prompt": (
                        "You are precise and requirements-driven. "
                        "Return only the requested Markdown sections, "
                        "with numbered, testable requirement statements."
                    ),
                },
            )

            if result.success and isinstance(result.output, str):
                if io:
                    io.log(
                        f"[{self.name}] Successfully generated structured requirements via LLM."
                    )
                requirements_text = result.output.strip()
            else:
                if io:
                    io.log(
                        f"[{self.name}] LLM tool failed during requirements interpretation, "
                        f"falling back to deterministic requirements: {result.error}"
                    )

        # --- Fallback: deterministic requirements if no LLM or LLM failed ---
        if requirements_text is None:
            if io:
                io.log(f"[{self.name}] Using fallback deterministic requirements document.")

            requirements_text = dedent(
                """
                # Functional Requirements

                1. The system SHALL allow users to manually enter individual expenses, including date, description, amount, category, and account.
                2. The system SHALL allow users to upload one or more CSV files containing expenses exported from banks or financial institutions.
                3. The system SHALL parse uploaded CSV files and map columns into the internal expense model (date, description, amount, category, account).
                4. The system SHALL allow users to define and edit expense categories (e.g., groceries, transportation, entertainment).
                5. The system SHALL support assigning each expense to exactly one primary category.
                6. The system SHALL allow users to select one or more time periods (e.g., specific months, custom date ranges) for comparison.
                7. The system SHALL compute total spending per category for each selected time period.
                8. The system SHALL compute differences in spending per category between time periods (absolute and percentage change where applicable).
                9. The system SHALL provide a summary of overall spending trends across time periods (e.g., total increase/decrease, top increasing categories).
                10. The system SHALL provide textual summaries describing key insights (e.g., “Spending on groceries increased by 20% compared to last month.”).
                11. The system SHALL provide a way to export or copy comparison results (e.g., as text or CSV) for external use.

                # Non-Functional Requirements

                1. The system SHOULD produce comparison results for typical datasets (up to tens of thousands of expenses) within a few seconds on a standard laptop.
                2. The system SHOULD produce deterministic results for the same input data and configuration.
                3. The system SHALL validate input data and report errors (e.g., invalid dates, missing amounts) in a clear, actionable way.
                4. The system SHOULD be structured so that storage (in-memory vs database) can be swapped via a well-defined interface.
                5. The system SHOULD be testable via automated unit tests for core comparison and aggregation logic.

                # Data & Integration Requirements

                1. The expense model SHALL, at minimum, support: id, date, description, amount, category, and account.
                2. The system SHALL treat amounts as decimal-safe numeric types (not floating-point) to avoid rounding errors.
                3. The system SHOULD support configurable CSV mappings, so different banks with different column names can be handled without code changes.
                4. The system SHOULD separate raw imported categories from normalized categories used for comparison.
                5. The system SHOULD allow default categories and mapping rules to be defined in configuration.

                # Visualization & Reporting Requirements

                1. The system SHALL produce chart-ready data structures (e.g., JSON suitable for bar/line charts) representing spending per category over time.
                2. The system SHOULD support at least one comparison-friendly visualization format (e.g., bar chart comparing category spend for two periods).
                3. The system SHALL provide textual summaries alongside any chart-friendly outputs so users can understand trends without viewing charts.
                4. The system SHOULD highlight top increasing and decreasing categories in the summary (e.g., top 3 increases, top 3 decreases).

                # Out-of-Scope and Assumptions

                1. Real-time bank API integrations (e.g., direct connections to financial institutions) are OUT OF SCOPE for the initial version; the system assumes CSV uploads or manual input.
                2. Multi-currency conversion and foreign exchange rate handling are OUT OF SCOPE; the system assumes a single currency per dataset.
                3. User authentication, multi-user account management, and persistence of user profiles are OUT OF SCOPE for the initial CLI/desktop-focused implementation.
                4. The system assumes that the user has already cleaned obviously corrupted CSV files (e.g., non-tabular content) before upload.
                5. Advanced budgeting features (e.g., goals, alerts, or recommendations) are OUT OF SCOPE for the initial version; the focus is on comparison and insight into existing spending patterns.
                """
            ).strip()

        # --- Persist requirements to disk via File tool, if available ---
        if "file" in tools_dict:
            if io:
                io.log(f"[{self.name}] Writing requirements document via file tool.")
            file_result = tools.invoke(
                "file",
                {
                    "operation": "write",
                    # Relative to FileTool's sandbox root (generated/)
                    "path": "artifacts/requirements.md",
                    "content": requirements_text,
                },
            )
            if not file_result.success and io:
                io.log(
                    f"[{self.name}] Failed to write requirements via file tool: "
                    f"{file_result.error}"
                )
        else:
            if io:
                io.log(f"[{self.name}] File tool not registered; skipping requirements write.")

        return requirements_text
