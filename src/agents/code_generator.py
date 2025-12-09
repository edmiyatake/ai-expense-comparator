# src/agents/code_generator.py

from __future__ import annotations

from textwrap import dedent
from typing import Optional

from agents.base import Agent, OrchestratorIO
from mcp.tools.base import ToolRegistry, ToolContext  # <-- import ToolContext


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
        ...
        return "\n".join(parts)

    def _build_app_module_prompt(
        self,
        user_request: str,
        planner_plan: Optional[str],
        requirements_text: Optional[str],
    ) -> str:
        ...
        return "\n".join(parts)

    # ------------------------------------------------------------------ #
    # Deterministic fallbacks (no LLM)
    # ------------------------------------------------------------------ #

    def _fallback_skeleton(self) -> str:
        ...
        ).strip()

    def _fallback_app_module(self) -> str:
        ...
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

            # NEW: tag this LLM call with a ToolContext that includes caller
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

            # NEW: separate context for this LLM call, same caller
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
