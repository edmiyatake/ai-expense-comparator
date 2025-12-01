# src/mcp/tools/file_stub.py
from __future__ import annotations
import pathlib
from .base import FileTool


class LocalFileTool(FileTool):
    """
    Writes to the local filesystem relative to repo root.
    """

    def __init__(self, base_dir: str = "generated"):
        self.base_dir = pathlib.Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write_file(self, path: str, content: str) -> None:
        full_path = self.base_dir / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")

    def read_file(self, path: str) -> str:
        full_path = self.base_dir / path
        return full_path.read_text(encoding="utf-8")
