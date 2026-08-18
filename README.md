# tutorial_ICDAR

A hands-on workshop for building AI agents with **Pydantic AI**, tools, RAG, and MCP.

---

## Setup

1. **Set the vLLM API key** in your shell:
   ```bash
   export VLLM_API_KEY="your-api-key"
   ```

2. **Run any script** with `uv`:
   ```bash
   uv run --env-file .env python exercises/part_01/01_entry_point.py
   ```

> **Model:** The default is `qwen3.5:27b`, served through `https://litellm.kube-ext.isc.heia-fr.ch/v1`. API documentation is available at [LiteLLM Swagger UI](https://litellm.kube-ext.isc.heia-fr.ch/).

---

## Project Structure

| Directory | Purpose |
|---|---|
| `exercises/` | Your workspace — fill in the blanks here |
| `solutions/` | Reference implementations |
| `src/tutorial_ICDAR/` | Shared utilities (`rag_utils.py`, `document_tools.py`, `pydantic_utils.py`) |
| `data/` | Documents and the ChromaDB vector store |

---

## Workshop Exercises

### Part 01 — Intro: Creating Agents and Basic RAG

| Script | What it does |
|---|---|
| [`01_entry_point.py`](exercises/part_01/01_entry_point.py) | Minimal "Hello World" agent (CLI) |
| [`02_document_tools.py`](exercises/part_01/02_document_tools.py) | Step-by-step PDF and image text extraction (CLI) |
| [`03_rag_step_by_step.py`](exercises/part_01/03_rag_step_by_step.py) | Four-step RAG pipeline — chunks, indexes, retrieves, and answers (CLI) |

```bash
uv run --env-file .env python exercises/part_01/01_entry_point.py
uv run python exercises/part_01/02_document_tools.py
uv run --env-file .env python exercises/part_01/03_rag_step_by_step.py
```

---

### Part 02 — Built-in Tools, Agentic RAG & Document Handling

| Script | What it does |
|---|---|
| [`01_rag_agent.py`](exercises/part_02/01_rag_agent.py) | Agentic RAG — ChromaDB retrieval exposed as an agent tool — web app on port 8000 |
| [`02_document_tools_agent.py`](exercises/part_02/02_document_tools_agent.py) | Agent combining the shared RAG collection with document tools — web app on port 8000 |

```bash
uv run --env-file .env python exercises/part_02/01_rag_agent.py            # port 8000
uv run --env-file .env python exercises/part_02/02_document_tools_agent.py # port 8000
```

> **Note:** Run Part 01's completed `03_rag_step_by_step.py` once before any later RAG agent or MCP server. Every Part 02 and Part 03 component reuses its persistent ChromaDB collection and does not index the policy again.

---

### Part 03 — MCP: Decoupled RAG via the Model Context Protocol

This part introduces a two-component architecture: a standalone MCP server exposes the retrieval tool over HTTP, and the agent discovers and calls it at runtime.

| Script | What it does |
|---|---|
| [`01_mcp_rag_server.py`](exercises/part_03/01_mcp_rag_server.py) | MCP server exposing the shared RAG collection over Streamable HTTP on port 8001 |
| [`02_simple_mcp_rag_agent.py`](exercises/part_03/02_simple_mcp_rag_agent.py) | Agent that consumes the MCP server's RAG tool — web app on port 8000 |
| [`03_mcp_document_web_agent.py`](exercises/part_03/03_mcp_document_web_agent.py) | Agent combining MCP RAG, document tools, and web search — web app on port 8000 |

**Run in this order** (two terminals):

```bash
# Terminal 1 — start the MCP server first
uv run --env-file .env python exercises/part_03/01_mcp_rag_server.py # port 8001

# Terminal 2 — then start the agent
uv run --env-file .env python exercises/part_03/02_simple_mcp_rag_agent.py # port 8000
```

> **Important:** The MCP server must be running before any MCP-dependent agent. Agents discover the `search_relevant_context_from_HAL_9000_policy` tool automatically via the MCP protocol at `localhost:8001/mcp`.

---

### Part 03 BONUS — Guardrails & Safety

| Script | What it does |
|---|---|
| [`simple_guardrail.py`](exercises/part_03_BONUS/simple_guardrail.py) | Agent with `pydantic_ai_shields` `PromptInjection()` — blocks prompt injection attacks (CLI) |
| [`guardrails_with_hooks.py`](exercises/part_03_BONUS/guardrails_with_hooks.py) | Agent with a custom `before_model_request` hook — inspects and blocks/redacts forbidden content (web app on port 8000) |

```bash
uv run python exercises/part_03_BONUS/simple_guardrail.py
uv run python exercises/part_03_BONUS/guardrails_with_hooks.py
```

---

## FAQ

**How do I re-index the PDF vector store?**
Delete `data/chroma_db/` and rerun the completed Part 01 `03_rag_step_by_step.py` script. Later agents and the MCP server only reuse that collection.

**Where is the reference solution?**
Every exercise in `exercises/` has a matching file in `solutions/` with the same name.
