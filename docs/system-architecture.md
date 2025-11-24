# System Architecture – MCP Multi-Agent Expense Comparator

## 1. Overview

This document describes the architecture of the **SWE270P Expense Comparator** project.

The system is a **multi-agent, MCP-based code generation service** that:
1. Accepts a software description and requirements via a UI.
2. Uses collaborating LLM-driven agents to generate:
   - Executable application code.
   - Executable test cases.
3. Tracks LLM usage (API calls and tokens).
4. Returns results through a FastAPI backend.

---

## 2. High-Level Architecture

```mermaid
flowchart LR
    User[User (Browser / Client)] --> UI[UI Frontend (simple web form)]
    UI --> API[FastAPI Backend]

    API --> Orchestrator[Agent Orchestrator]
    Orchestrator --> Planner[Planner Agent]
    Orchestrator --> Requirements[Requirements Interpreter Agent]
    Orchestrator --> CodeGen[Code Generator Agent]
    Orchestrator --> TestGen[Test Generator Agent]
    Orchestrator --> Reviewer[Reviewer Agent]

    subgraph MCP["MCP Tools / Servers"]
        FileTool[File System / Template Tool]
        UsageTool[LLM Usage Tracker]
    end

    Planner <---> MCP
    Requirements <---> MCP
    CodeGen <---> MCP
    TestGen <---> MCP
    Reviewer <---> MCP

    Orchestrator --> OpenAI[LLM Provider (OpenAI API)]
    MCP --> OpenAI
```

## 3. Main Components

### 3.1 UI Layer

- **Responsibility:** Collect input and display outputs.
- **Input:**
  - Software description (e.g., "Expense Comparator").
  - Requirements (structured text).
- **Output:**
  - Generated code.
  - Generated tests.
  - LLM usage metrics.
- Minimal UI needed (HTML/JS or lightweight frontend).
- Communicates with FastAPI using JSON.

---

### 3.2 FastAPI Backend (`src/app/main.py`)

- Exposes API endpoints:
  - `POST /generate` – triggers the multi-agent workflow.
  - `GET /usage` – returns token usage stats.
- Validates requests using Pydantic.
- Calls the **Agent Orchestrator** to perform the workflow.

---

### 3.3 Agent Orchestrator (`src/agents/orchestrator.py`)

Coordinates the entire multi-agent MCP pipeline:

1. Accepts validated user input.
2. Calls the **Planner Agent** to create a task plan.
3. Calls the **Requirements Interpreter Agent**.
4. Calls the **Code Generator Agent** to produce code.
5. Calls the **Test Generator Agent** to produce tests.
6. Calls the **Reviewer Agent** to sanity-check outputs.
7. Tracks usage per agent via the MCP tracking tool.
8. Returns final aggregated results to the API.

---

### 3.4 Agents (`src/agents/`)

Each agent is a focused LLM-powered module:

#### **Planner Agent**
- Input: description + requirements.
- Output: step-by-step task plan.

#### **Requirements Interpreter Agent**
- Output: structured JSON-like requirements.

#### **Code Generator Agent**
- Generates executable Python code.
- Uses Jinja2 templates when needed.

#### **Test Generator Agent**
- Produces pytest-based test suites.

#### **Reviewer Agent**
- Reviews code + tests for correctness and requirement alignment.

All agents:
- Use the OpenAI SDK.
- Report token usage to the MCP Usage Tool.

---

### 3.5 MCP Layer (`src/mcp/`)

Provides “tools” agents can use:

#### **File Tool**
- Writes generated code to disk:
  - `generated_app/`
  - `generated_tests/`

#### **Usage Tracker Tool**
- Records:
  - API calls
  - Input/output tokens per call

#### **LLM Wrapper**
- Centralized wrapper for OpenAI calls.
- Ensures consistent logging + usage tracking.

---

### 3.6 LLM Provider (OpenAI SDK)

- All LLM work pipelines through the SDK.
- Reads API key from `.env`.
- Provides:
  - Prompt execution
  - Function/tool calling
  - Usage metrics

---

## 4. Request Lifecycle

1. **User submits** description + requirements.
2. UI sends `POST /generate` to FastAPI.
3. FastAPI + Pydantic validate input.
4. Backend triggers Orchestrator.
5. Orchestrator → Planner Agent (task plan).
6. Orchestrator → Requirements Agent (structured requirements).
7. Orchestrator → CodeGen Agent (source code).
8. Orchestrator → TestGen Agent (tests).
9. Reviewer Agent checks everything.
10. Usage Tracker aggregates all token/call data.
11. API returns JSON with:
    - Code summary / file paths
    - Tests
    - Usage stats

---

## 5. LLM Usage Tracking

All LLM calls pass through a wrapper that records:

- Agent Name  
- Task performed  
- Model used  
- Input tokens  
- Output tokens  

Usage is stored in memory or a small JSON file.  
`/usage` returns:
- Total calls
- Total tokens
- Per-agent breakdown (if implemented)

---

## 6. Error Handling and Observability

- **Validation errors** → 400 responses.
- **LLM API failures** → logged + 500 response.
- **Agent flow errors** → caught by Orchestrator.
- Basic logging for demo/debugging (`logging` module).

---

## 7. Future Extensions (Optional)

- Store run history in a real database.
- Add more specialized agents (UI Generator, Refactoring Agent).
- Support multiple programming languages.
- Auto-generate Plotly charts for the expense visualizer.
- Add GitHub-like project templates for code generation.

