# Project Dependencies – Explanation (requirements.md)

This document explains the purpose of each dependency listed in requirements.txt and how it supports the multi-agent MCP system for the Expense Comparator project.

## requirements.txt
- fastapi
- uvicorn
- openai
- pydantic
- httpx
- python-dotenv
- pytest
- jinja2

## Dependency Breakdown
### 1. fastapi

What it is: A modern, high-performance web framework for building APIs.
Why we need it:

Provides the backend for our MCP system.

Handles incoming requests containing software descriptions + requirements.

Returns generated code, tests, and usage reports.

Used for:

/generate endpoint

/usage endpoint

UI backend

### 2. uvicorn

What it is: A super-fast ASGI server for running FastAPI.
Why we need it:

Runs the local development server for demos and agent interactions.

Supports auto-reload and async execution.

Used for:

Launching the MCP backend

Running the UI/API server

### 3. openai

What it is: The official OpenAI Python SDK.
Why we need it:

All agents (planner, coder, tester, reviewer) rely on LLM calls.

Handles token usage reporting and structured responses.

Used for:

Code generation

Test generation

Planning + validation

Tracking LLM usage

### 4. pydantic

What it is: A Python data validation and modeling library.
Why we need it:

Ensures clean, structured inputs from the UI.

Validates agent outputs (generated code, tests, metadata).

Integrates tightly with FastAPI.

Used for:

Request/response schemas

Data validation for MCP messages

### 5. httpx

What it is: An async HTTP client for Python.
Why we need it:

Allows agents to communicate with each other.

Useful for any MCP tool server or external API calls.

Replaces the older requests library with async support.

Used for:

Agent → Agent communication

MCP → Tool communication

External API calls

### 6. python-dotenv

What it is: Loads environment variables from a .env file.
Why we need it:

Keeps API keys out of GitHub.

Makes configuring OpenAI, ports, and settings easier.

Used for:

Loading OPENAI_API_KEY

Managing configuration securely

### 7. pytest

What it is: A simple, powerful testing framework.
Why we need it:

Our system must generate executable test cases.

Pytest is LLM-friendly and minimal-boilerplate.

Used for:

Generated tests for the Expense Comparator app

Tests for agent behavior

### 8. jinja2

What it is: A templating engine for Python.
Why we need it:

Helps agents generate consistent code & test templates.

Useful for scaffolding files or formatting outputs.

Used for:

Code templates

Test templates

Boilerplate generation