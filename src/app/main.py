# src/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .orchestrator import Orchestrator
from .schemas import GenerationRequest, GenerationResult, UsageStats

app = FastAPI(title="AI Expense Comparator – AI Coder")

# CORS so your future UI can call this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can lock this down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# One orchestrator instance for now (simple, in-memory).
orchestrator = Orchestrator()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/generate", response_model=GenerationResult)
async def generate(request: GenerationRequest) -> GenerationResult:
    state = await orchestrator.run(
        description=request.description,
        requirements=request.requirements,
    )

    return GenerationResult(
        code_paths=state.get("code_paths", []),
        test_paths=state.get("test_paths", []),
        notes=state.get("plan", {}).get("notes", "Stub pipeline completed."),
    )


@app.get("/usage", response_model=UsageStats)
async def usage() -> UsageStats:
    stats = orchestrator.get_usage_stats()
    return UsageStats(
        total_calls=stats["total_calls"],
        total_tokens_prompt=stats["total_tokens_prompt"],
        total_tokens_completion=stats["total_tokens_completion"],
        per_agent=stats["per_agent"],
    )
