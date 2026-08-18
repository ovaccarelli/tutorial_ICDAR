# AGENTS.md

## Prerequisites
- **Python 3.13** (see `.python-version`).
- **LiteLLM gateway** at `https://litellm.kube-ext.isc.heia-fr.ch/v1`, authenticated through the required `VLLM_API_KEY` environment variable and serving the vLLM-hosted model.
- Default model: `qwen3.5:27b` (from `src/tutorial_ICDAR/settings.py`). Override with `VLLM_MODEL`; `VLLM_BASE_URL` is also supported.

## Commands
All scripts run via `uv run python exercises/<path>` or `uv run python solutions/<path>`.

| Script | Mode | Port |
|---|---|---|
| `part_01/01_entry_point.py` | CLI | — |
| `part_01/02_document_tools.py` | CLI | — |
| `part_01/03_rag_step_by_step.py` | CLI | — |
| `part_02/01_rag_agent.py` | Web app | 8000 |
| `part_02/02_document_tools_agent.py` | Web app | 8000 |
| `part_03/01_mcp_rag_server.py` | MCP server (streamable-http on 8001) | 8001 |
| `part_03/02_simple_mcp_rag_agent.py` | Web app | 8000 |
| `part_03/03_mcp_document_web_agent.py` | Web app | 8000 |
| `part_03_BONUS/simple_guardrail.py` | CLI | — |
| `part_03_BONUS/guardrails_with_hooks.py` | Web app | 8000 |

### MCP execution order
`01_mcp_rag_server.py` MUST start before `02_simple_mcp_rag_agent.py` or `03_mcp_document_web_agent.py`. The agents discover the `search_relevant_context_from_HAL_9000_policy` tool via MCP over HTTP at `localhost:8001/mcp`.

### Port conflicts
Most web apps default to **8000**, while the MCP server uses **8001**. You cannot run two web apps on port 8000 simultaneously. The supported multi-service combo is MCP server (8001) + one agent (8000).

### No tests or lint
This is a workshop. No CI, no formatters, no pre-commit, no test suite.

## Architecture
- **`exercises/`** — target tasks, organized by part (01-04).
- **`solutions/`** — reference implementations with the same structure as `exercises/`.
- **`src/tutorial_ICDAR/`** — shared utilities:
  - `utils/pydantic_utils.py` — `get_vllm_model()` factory
  - `utils/rag_utils.py` — shared `retrieve_context()` helper for the collection created in Part 01
  - `utils/document_tools.py` — `list_my_available_documents()`, `extract_text_from_md_or_txt_file()`, `extract_text_from_image_file()`
  - `settings.py` — `DEFAULT_VLLM_MODEL`, `DEFAULT_VLLM_BASE_URL`
- **`data/`** — workshop documents under `data/my_documents/` and the local ChromaDB vector store.
- **Vector Store**: ChromaDB at `data/chroma_db/`. Part 01 creates `HAL_9000_Expense_Reimbursement_Policy_chunks`; all Part 02 and Part 03 RAG components reuse that collection instead of rebuilding it.

## Gotchas
- `part_01/01_entry_point.py` defines its own `get_vllm_model()` locally (duplicates `utils/pydantic_utils.py`). Don't add a redundant import when modifying it.
- `01_entry_point.py` also supports the `VLLM_BASE_URL` and `VLLM_API_KEY` environment variables.
