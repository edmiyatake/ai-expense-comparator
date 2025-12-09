from __future__ import annotations

from textwrap import dedent
from typing import Optional

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry


class ReviewerAgent(Agent):
    """
    Agent that reviews the plan, requirements, code skeleton, and test skeletons
    for the Expense Comparator and provides an architectural review.

    It focuses on:
      - Coherence between requirements, design, and tests
      - Gaps and risks in the architecture
      - Recommended next steps

    If the LLM tool (llm_chat) is available, it uses that to generate a richer
    architectural review. Otherwise it falls back to a deterministic template.

    The final review is also written to generated/artifacts/review.md
    via the File tool when available.
    """

    def __init__(self) -> None:
        super().__init__(
            name="reviewer",
            description="Reviews the generated artifacts and provides feedback.",
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
        test_skeleton: Optional[str],
    ) -> str:
        """
        Build the LLM prompt for the architectural review.
        """
        header = (
            "You are a principal engineer reviewing an early design for an\n"
            "Expense Comparator application in the finance domain.\n\n"
            "You are given:\n"
            "- The original user description\n"
            "- A high-level implementation plan\n"
            "- Structured requirements\n"
            "- A code skeleton\n"
            "- Test skeletons\n\n"
            "Provide an architectural review that:\n"
            "- Checks alignment between requirements and the proposed design\n"
            "- Identifies major gaps, risks, or missing components\n"
            "- Recommends concrete next steps for implementation\n\n"
            "Return your answer in Markdown with exactly these sections:\n"
            "1. Overall Assessment\n"
            "2. Alignment with Requirements\n"
            "3. Gaps and Risks\n"
            "4. Recommendations and Next Steps\n\n"
            "Use concise, actionable language suitable for a technical design review.\n"
        )

        parts: list[str] = [
            header,
            "\nUser Description:\n",
            user_request.strip(),
            "\n",
        ]

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
                    "Test Skeletons:\n",
                    test_skeleton.strip(),
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
        test_skeleton: Optional[str] = None,
    ) -> str:
        if io:
            io.log(f"[{self.name}] Starting architectural review.")

        tools_dict = tools.list_tools()
        review_text: str | None = None

        # --- Preferred path: use LLM tool if available ---
        if "llm_chat" in tools_dict:
            if io:
                io.log(f"[{self.name}] Using llm_chat tool to generate review.")

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
                        "You are a principal engineer writing a concise design review. "
                        "Be specific, constructive, and pragmatic. "
                        "Return only the requested Markdown sections."
                    ),
                },
            )

            if result.success and isinstance(result.output, str):
                if io:
                    io.log(f"[{self.name}] Successfully generated review via LLM.")
                review_text = result.output.strip()
            else:
                if io:
                    io.log(
                        f"[{self.name}] LLM tool failed during review generation, "
                        f"falling back to deterministic review: {result.error}"
                    )

        # --- Fallback: deterministic review if no LLM or LLM failed ---
        if review_text is None:
            if io:
                io.log(f"[{self.name}] Using fallback deterministic review.")

            review_text = dedent(
                """
                # Overall Assessment

                The proposed design for the Expense Comparator provides a reasonable
                foundation: it separates concerns into modules for CSV IO,
                normalization, categorization, aggregation, comparison, and
                visualization. The requirements and test skeletons cover the core
                user value of comparing spending across time periods and categories.

                # Alignment with Requirements

                1. Functional requirements for manual entry, CSV upload, categorization,
                   aggregation, and comparison are reflected in the code skeleton modules.
                2. Non-functional requirements such as deterministic behavior and testability
                   are supported by the clear separation of pure logic modules and test files.
                3. Data and integration requirements (e.g., normalized Transaction model,
                   configurable CSV mappings) map cleanly to models.py, csv_io.py,
                   normalization.py, and config.settings.
                4. Visualization and reporting requirements are partially addressed by
                   visualization.py and textual reporting helpers, though specific
                   charting decisions remain open.

                # Gaps and Risks

                1. Error handling and validation strategies (for malformed CSVs, invalid dates,
                   and non-numeric amounts) are not fully specified; this may lead to
                   inconsistent behavior across modules.
                2. Configuration management (bank-specific mappings, category rules,
                   default time windows) is only loosely defined via config.settings.
                3. Performance characteristics for larger datasets are not explicitly tested
                   or bounded; there is a risk of slow comparisons for very large CSVs.
                4. There is no explicit story yet for persisting user-defined categories
                   or rules beyond a single run (e.g., file-based config vs database).
                5. The current design assumes a CLI-style entrypoint; if a web API or UI
                   is planned later, additional layers (request handlers, DTOs, auth) will
                   need to be introduced.

                # Recommendations and Next Steps

                1. Define a clear validation and error-handling policy for CSV parsing and
                   normalization (what is fatal vs recoverable, how errors are reported).
                2. Flesh out config.settings with concrete structures for:
                   - bank-specific CSV column mappings
                   - default and custom categories
                   - default time window presets
                3. Expand test coverage to include:
                   - malformed CSV inputs
                   - empty and degenerate datasets
                   - extreme but realistic dataset sizes
                4. Decide on a basic persistence strategy for configuration (e.g., JSON/YAML
                   files) to make the tool reusable across runs without modifying code.
                5. If a web or GUI frontend is expected in the future, introduce a thin
                   service layer around the core comparison logic so that both CLI and web
                   frontends can call it consistently.
                """
            ).strip()

        # --- Persist review via File tool, if available ---
        if "file" in tools_dict:
            if io:
                io.log(f"[{self.name}] Writing review via file tool.")
            file_result = tools.invoke(
                "file",
                {
                    "operation": "write",
                    # Relative to FileTool's sandbox root (generated/)
                    "path": "artifacts/review.md",
                    "content": review_text,
                },
            )
            if not file_result.success and io:
                io.log(
                    f"[{self.name}] Failed to write review via file tool: "
                    f"{file_result.error}"
                )
        else:
            if io:
                io.log(f"[{self.name}] File tool not registered; skipping review write.")

        return review_text
