# src/app/schemas.py
from typing import List, Optional
from pydantic import BaseModel


class GenerationRequest(BaseModel):
    """
    Input from the UI to /generate.
    """
    app_name: Optional[str] = "Expense Comparator"
    description: str
    requirements: List[str]


class GenerationResult(BaseModel):
    """
    High-level result of a generation run.
    """
    code_paths: List[str]
    test_paths: List[str]
    notes: str


class UsageStats(BaseModel):
    """
    What /usage returns.
    """
    total_calls: int
    total_tokens_prompt: int
    total_tokens_completion: int
    per_agent: dict
