# Agent Design – MCP Multi-Agent Expense Comparator

This document defines each agent in the system, including its role, inputs, outputs, and interaction pattern with other agents and MCP tools.

---

## 1. Overview

The system uses several LLM-driven agents coordinated by an orchestrator:

- Planner Agent
- Requirements Interpreter Agent
- Code Generator Agent
- Test Generator Agent
- Reviewer Agent

All agents:
- Are invoked by the **Agent Orchestrator**.
- Use a shared LLM client (OpenAI SDK wrapper).
- Report usage (tokens, calls) through the **Usage Tracker** MCP tool.
- Communicate via structured Python data models (e.g., Pydantic).

---

## 2. Common Agent Interface (Conceptual)

All agents follow a similar logical interface:

- **Input:**
  - A structured `AgentContext`:
    - `description`: High-level software description.
    - `requirements`: Structured or raw requirements.
    - `plan`: (Optional) Task plan from the Planner.
    - `code_artifacts`: (Optional) Generated code snippets or file references.
    - `test_artifacts`: (Optional) Generated tests.
    - `metadata`: (Optional) run/session metadata.

- **Output:**
  - Agent-specific result (plan, structured requirements, code, tests, or review report).
  - Updated `AgentContext` fields as needed.

- **LLM Call Pattern:**
  - Create prompt → Call shared LLM client → Parse structured output → Log usage.

---

## 3. Planner Agent

### 3.1 Purpose

Defines a **high-level task plan** for transforming the raw input (description + requirements) into code and tests.

### 3.2 Inputs

- Software description (string).
- Raw requirements (string or list).
- Any professor/TA constraints (if provided).

### 3.3 Outputs

- A structured task plan, e.g.:

  ```json
  {
    "phases": [
      {
        "name": "Requirements Structuring",
        "steps": ["Normalize requirements", "Identify entities", "Identify core features"]
      },
      {
        "name": "Code Generation",
        "steps": ["Design data models", "Implement API endpoints", "Implement comparison logic"]
      },
      {
        "name": "Test Generation",
        "steps": ["Unit tests for comparison", "Tests for input validation"]
      }
    ]
  }

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

## 3.5 MCP Layer (`src/mcp/`)

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
- Centralized module wrapping OpenAI calls.
- Ensures consistent logging + usage tracking.

---

## 3.6 LLM Provider (OpenAI SDK)

- All LLM work funnels through the SDK.
- Reads the API key from `.env`.
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
10. Usage Tracker aggregates token/call data.
11. API returns:
    - Code summary / file paths  
    - Tests  
    - Usage stats  

---

## 5. LLM Usage Tracking

All LLM calls pass through one wrapper that records:

- Agent name  
- Operation  
- Model used  
- Input tokens  
- Output tokens  

Usage is stored in memory or a small JSON file.

`/usage` returns:
- Total calls  
- Total tokens  
- Per-agent usage (optional)  

---

## 6. Error Handling and Observability

- **Validation errors** → FastAPI returns 400.
- **LLM API issues** → logged + 500.
- **Agent failures** → caught by Orchestrator and logged.

Basic Python logging is used for debugging and demo-day visibility.

---

## 7. Future Extensions (Optional)

- Persistent database for storing:
  - Generated apps
  - Past runs
  - Usage history
- Additional agents:
  - UI Generator Agent
  - Refactoring Agent
  - Visualization Agent
- Support for multiple output languages (Python, JS, etc.)
- More advanced chart generation for the Expense Comparator (Plotly templates).

