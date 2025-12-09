# src/mcp/tools/file.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from .base import Tool, ToolContext, ToolResult


class FileTool(Tool):
    """
    MCP-style File tool for the AI Expense Comparator.

    All operations are sandboxed under the project's `generated/` directory.

    Operations (arguments):
    - {"operation": "list", "path": "subdir/optional"}
    - {"operation": "read", "path": "some/file.py"}
    - {"operation": "write", "path": "some/file.py", "content": "..."}
    """

    def __init__(self, root: Optional[Path] = None) -> None:
        # Determine sandbox root
        if root is None:
            # file.py -> tools -> mcp -> src -> project root
            project_root = Path(__file__).resolve().parents[3]
            root = project_root / "generated"

        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)

        super().__init__(
            name="file",
            description="Read, write, and list files within the generated/ directory.",
            parameters_schema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["list", "read", "write"],
                        "description": "The file operation to perform.",
                    },
                    "path": {
                        "type": "string",
                        "description": "Path relative to the generated/ root.",
                    },
                    "content": {
                        "type": "string",
                        "description": "File content for write operations.",
                    },
                },
                "required": ["operation", "path"],
            },
        )

    # --------------------------------------------------------------------- #
    # Tool interface
    # --------------------------------------------------------------------- #

    def invoke(
        self,
        arguments: Dict[str, Any],
        context: Optional[ToolContext] = None,
    ) -> ToolResult:
        operation = arguments.get("operation")
        rel_path = arguments.get("path")

        try:
            if not isinstance(operation, str):
                raise ValueError("'operation' is required and must be a string.")
            if not isinstance(rel_path, str):
                raise ValueError("'path' is required and must be a string.")

            target = self._safe_path(rel_path)

            if operation == "list":
                output = self._op_list(target)
            elif operation == "read":
                output = self._op_read(target)
            elif operation == "write":
                content = arguments.get("content")
                if not isinstance(content, str):
                    raise ValueError("'content' is required and must be a string for write.")
                output = self._op_write(target, content)
            else:
                raise ValueError(f"Unsupported operation '{operation}'.")

            return ToolResult(
                name=self.name,
                success=True,
                output=output,
                error=None,
            )

        except Exception as exc:
            return ToolResult(
                name=self.name,
                success=False,
                output=None,
                error=str(exc),
            )

    # --------------------------------------------------------------------- #
    # Internal helpers
    # --------------------------------------------------------------------- #

    def _safe_path(self, rel_path: str) -> Path:
        """
        Resolve a path inside the sandbox root and prevent path traversal.
        """
        rel = Path(rel_path)

        if rel.is_absolute():
            raise ValueError("Absolute paths are not allowed.")

        full = (self._root / rel).resolve()

        # Ensure the resolved path is still under root
        if self._root not in full.parents and full != self._root:
            raise ValueError("Path escapes the sandbox root.")

        return full

    def _op_list(self, target: Path) -> Dict[str, Any]:
        if not target.exists():
            # Return empty listing if directory does not exist yet
            return {
                "directory": str(target.relative_to(self._root)),
                "files": [],
            }

        if not target.is_dir():
            raise ValueError("The 'list' operation expects a directory path.")

        files = []
        for p in sorted(target.rglob("*")):
            if p.is_file():
                files.append(
                    {
                        "path": str(p.relative_to(self._root)),
                        "size": p.stat().st_size,
                    }
                )

        return {
            "directory": str(target.relative_to(self._root)),
            "files": files,
        }

    def _op_read(self, target: Path) -> Dict[str, Any]:
        if not target.exists():
            raise FileNotFoundError(f"File not found: {target}")

        if not target.is_file():
            raise ValueError("The 'read' operation expects a file path.")

        content = target.read_text(encoding="utf-8")
        return {
            "path": str(target.relative_to(self._root)),
            "content": content,
        }

    def _op_write(self, target: Path, content: str) -> Dict[str, Any]:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        return {
            "path": str(target.relative_to(self._root)),
            "bytes_written": len(content.encode("utf-8")),
        }
