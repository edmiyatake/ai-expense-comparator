# src/mcp/tools/__init__.py  (or wherever you centralize this)

from pathlib import Path

from .base import ToolRegistry
from .llm import LLMTool
from .usage_tracker import UsageTracker
from .file import FileTool


def build_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()

    # Register existing tools
    registry.register(LLMTool())
    registry.register(UsageTracker())

    # Register File tool, sandboxed to generated/
    project_root = Path(__file__).resolve().parents[3]
    generated_root = project_root / "generated"
    registry.register(FileTool(root=generated_root))

    return registry
