# src/agents/code_generator.py

from __future__ import annotations

from textwrap import dedent
from typing import Optional

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry, ToolContext


class CodeGeneratorAgent(Agent):
    """
    Agent that turns plans + requirements into a concrete code skeleton for the
    Expense Comparator application.

    It proposes:
      - Project structure (folders/files)
    ...
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
        Build the prompt for generating the code skeleton (Markdown).
        """
        parts: list[str] = []

        parts.append(
            dedent(
                """
                You are designing the initial code skeleton for an "AI Expense Comparator"
                application. Produce a high-level project layout and brief file-level
                descriptions in **Markdown**.

                The goal is to give another engineer a clear starting point for implementing
                the system, not to write full implementation code.
                """
            ).strip()
        )

        parts.append("## Overall Goal\n")
        parts.append(user_request.strip())

        if planner_plan:
            parts.append("\n## Planner Plan\n")
            parts.append(planner_plan.strip())

        if requirements_text:
            parts.append("\n## Requirements\n")
            parts.append(requirements_text.strip())

        parts.append(
            dedent(
                """
                ## Instructions

                - Output must be valid Markdown.
                - Start with a short section titled "Project Structure".
                - Use a tree-like bullet list for folders and key files.
                - For each important file, include a one-sentence description.
                - Do **not** include any marketing language or extra commentary.
                """
            ).strip()
        )

        return "\n\n".join(parts)

    def _build_app_module_prompt(
        self,
        user_request: str,
        planner_plan: Optional[str],
        requirements_text: Optional[str],
    ) -> str:
        """
        Build the prompt for generating a runnable Python app module (app/app.py).

        This version expects the generated module to:
        - Act as a thin CLI wrapper.
        - Forward the prompt into the existing `mcp.orchestrator` CLI via subprocess.
        """
        parts: list[str] = []

        parts.append(
            dedent(
                """
                You are generating a runnable Python 3.9 module for the AI Expense Comparator.

                The output module must comply with **all requirements** provided in the prompt sections below
                - High level description
                - Planner plan
                - Requirements

                Additional Requirements for the generated module:

                - Return only **valid Python 3 code**.
                - Do **not** wrap the code in Markdown fences.
                - Do **not** include commentary or prose outside of comments.

                Functional requirements:

                - Import `argparse`, `sys`, and `subprocess`.
                - Define a function `run_expense_comparator(prompt: str | None = None) -> int` that:
                  - Builds a command list like `[sys.executable, "-m", "mcp.orchestrator"]`.
                  - If `prompt` is not None, append `"--prompt"` and the prompt string to the command.
                  - Prints a few clear status messages to stdout (starting, delegating to orchestrator, done).
                  - Uses `subprocess.run` (or `subprocess.call`) to invoke the command.
                  - Returns the subprocess return code (or 0 on success).

                - Define a `main(argv: list[str] | None = None) -> int` that:
                  - Uses `argparse.ArgumentParser` with a description such as "AI Expense Comparator CLI".
                  - Adds an optional `--prompt` argument (string).
                  - If `--prompt` is not provided, use a default like
                    "Build an Expense Comparator application.".
                  - Calls `run_expense_comparator(prompt)` and returns its exit code.

                - Include the standard CLI guard at the bottom:

                    if __name__ == "__main__":
                        raise SystemExit(main())

                The module does not need to directly import or construct agents,
                tools, or orchestrator objects. Delegation to `python -m mcp.orchestrator`
                is sufficient; the orchestrator module is responsible for running
                the full multi-agent pipeline.

                Keep the code clear and fully runnable.
                """
            ).strip()
        )

        parts.append("\n# High-level description of the system\n")
        parts.append(user_request.strip())

        if planner_plan:
            parts.append("\n# Planner plan\n")
            parts.append(planner_plan.strip())

        if requirements_text:
            parts.append("\n# Requirements\n")
            parts.append(requirements_text.strip())

        return "\n\n".join(parts)

    # ------------------------------------------------------------------ #
    # Deterministic fallbacks (no LLM)
    # ------------------------------------------------------------------ #

    def _fallback_skeleton(self) -> str:
        """
        Simple deterministic skeleton used when no LLM is available.
        """
        return dedent(
            """
            # AI Expense Comparator – Code Skeleton (Fallback)

            ## Project Structure

            - src/
              - app/
                - main.py          # CLI entrypoint for running the pipeline
              - agents/
                - planner.py       # High-level plan generator
                - requirements_interpreter.py  # Turns plan into detailed requirements
                - code_generator.py # Generates code skeleton + app module
                - test_generator.py # Generates test skeletons
                - reviewer.py       # Performs architectural review
              - mcp/
                - orchestrator.py   # Orchestrates agents and tools
                - tools/
                  - base.py         # Tool base classes and registry
                  - llm.py          # LLMTool implementation
                  - file.py         # FileTool implementation
                  - usage_tracker.py# Usage tracking

            This is a minimal, deterministic fallback in case the LLM tool
            is not available.
            """
        ).strip()

    def _fallback_app_module(self) -> str:
        """
        Simple deterministic app/app.py module used when no LLM is available.

        This version shells out to `python -m mcp.orchestrator` so that the
        existing pipeline is reused.
        """
        return dedent(
            """
            \"\"\"Fallback Expense Comparator CLI application.

            This module is intentionally simple. It forwards the prompt to the
            existing `mcp.orchestrator` module, which is responsible for running
            the full AI Expense Comparator pipeline.
            \"\"\"


            from __future__ import annotations

            import argparse
            import subprocess
            import sys
            from typing import List, Optional


            def run_expense_comparator(prompt: Optional[str] = None) -> int:
                \"\"\"Run the AI Expense Comparator pipeline via mcp.orchestrator.

                This function builds a `python -m mcp.orchestrator` command and
                optionally passes through a `--prompt` argument.
                \"\"\"
                cmd: List[str] = [sys.executable, "-m", "mcp.orchestrator"]

                if prompt:
                    cmd.extend(["--prompt", prompt])

                print("Starting AI Expense Comparator via mcp.orchestrator...")
                print(f"Using command: {' '.join(cmd)}")
                result = subprocess.run(cmd)
                print(f"AI Expense Comparator finished with exit code {result.returncode}.")
                return int(result.returncode)


            def main(argv: Optional[List[str]] = None) -> int:
                parser = argparse.ArgumentParser(
                    description="AI Expense Comparator CLI (fallback wrapper)"
                )
                parser.add_argument(
                    "--prompt",
                    type=str,
                    default="Build an Expense Comparator application.",
                    help="Natural language request describing the desired expense tool.",
                )

                args = parser.parse_args(argv)
                return run_expense_comparator(prompt=args.prompt)


            if __name__ == "__main__":
                raise SystemExit(main())
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

            # this LLM call with a ToolContext that includes caller
            ctx = ToolContext(
                run_id="code-generator-skeleton",
                caller=self.name,  # "code_generator"
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
                context=ctx,   # <-- pass context so LLMTool sees caller
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
        # generate executable Python app module under generated/app/
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

            # separate context for this LLM call, same caller
            ctx_app = ToolContext(
                run_id="code-generator-app-module",
                caller=self.name,
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
                context=ctx_app,   # <-- pass context here too
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
