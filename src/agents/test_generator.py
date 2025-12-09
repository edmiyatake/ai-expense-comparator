# src/agents/test_generator.py

from __future__ import annotations

from textwrap import dedent
from typing import Optional

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry, ToolContext  # <-- added ToolContext import


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
            ...
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
            ...
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

            # NEW: context for this LLM call
            ctx_skeleton = ToolContext(
                run_id="test-generator-skeletons",
                caller=self.name,  # "test_generator"
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
                context=ctx_skeleton,  # <-- pass context
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

            # NEW: separate context for this LLM call
            ctx_module = ToolContext(
                run_id="test-generator-pytest-module",
                caller=self.name,
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
                context=ctx_module,  # <-- pass context
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
