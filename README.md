# tutorial_ICDAR

A hands-on workshop for building AI agents with **Pydantic AI**, tools, RAG, and MCP.

---

## Setup

1. **Clone the repository and enter its directory:**
   ```bash
   git clone https://github.com/ovaccarelli/tutorial_ICDAR.git
   cd tutorial_ICDAR
   ```

2. **Install the project dependencies:**
   ```bash
   uv sync
   ```

3. **Load the bundled vLLM API key.** The scripts read `.vllm_api_key`
   automatically, so this export is optional:
   ```bash
   export VLLM_API_KEY="$(<.vllm_api_key)"
   ```

   Verify that it was loaded without printing the secret:
   ```bash
   test -n "$VLLM_API_KEY" && echo "VLLM API key loaded"
   ```

4. **Run the first exercise** with `uv`:
   ```bash
   uv run python exercises/part_01/01_entry_point.py
   ```

> **Model:** The default is `qwen3.8:27b`, served through `https://litellm.kube-ext.isc.heia-fr.ch/v1`. API documentation is available at [LiteLLM Swagger UI](https://litellm.kube-ext.isc.heia-fr.ch/).

---

## Project Structure

| Directory | Purpose |
|---|---|
| `exercises/` | Your workspace — fill in the blanks here |
| `solutions/` | Reference implementations |
| `src/tutorial_ICDAR/` | Shared utilities (`rag_utils.py`, `document_tools.py`, `pydantic_utils.py`) |
| `data/` | Documents and the ChromaDB vector store |
| `observability/` | Local Langfuse Docker Compose stack |

---

## Workshop Exercises

### Part 01 — Intro: Creating Agents and Basic RAG

| Script | What it does |
|---|---|
| [`01_entry_point.py`](exercises/part_01/01_entry_point.py) | Minimal "Hello World" agent (CLI) |
| [`02_document_tools.py`](exercises/part_01/02_document_tools.py) | Step-by-step PDF and image text extraction (CLI) |
| [`03_rag_step_by_step.py`](exercises/part_01/03_rag_step_by_step.py) | Four-step RAG pipeline — chunks, indexes, retrieves, and answers (CLI) |

```bash
export VLLM_API_KEY="$(<.vllm_api_key)"
uv run python exercises/part_01/01_entry_point.py
uv run python exercises/part_01/02_document_tools.py
uv run python exercises/part_01/03_rag_step_by_step.py
```

---

### Part 02 — Agentic RAG, MCP, Document Tools & Guardrails

| Script | What it does |
|---|---|
| [`01_rag_agent.py`](exercises/part_02/01_rag_agent.py) | Agentic RAG — ChromaDB retrieval exposed as an agent tool — web app on port 8000 |
| [`02a_mcp_rag_server.py`](exercises/part_02/02a_mcp_rag_server.py) | MCP server exposing the shared RAG collection over Streamable HTTP on port 8001 |
| [`02b_mcp_rag_agent.py`](exercises/part_02/02b_mcp_rag_agent.py) | Agent consuming the MCP server's RAG tool — web app on port 8000 |
| [`03_mcp_document_web_agent.py`](exercises/part_02/03_mcp_document_web_agent.py) | Agent combining MCP RAG, document tools, and web search — web app on port 8000 |

```bash
uv run python exercises/part_02/01_rag_agent.py # port 8000
```

> **Note:** Run Part 01's completed `03_rag_step_by_step.py` once before the Part 02 RAG agent or MCP server. Part 02 prefers the collection you create in `data/chroma_db`. If you cannot create it, the agents automatically use the ready-made collection committed in `data/chroma_db_prebuilt` instead.

**Run in this order** (two terminals):

```bash
# Terminal 1 — start the MCP server first
uv run python exercises/part_02/02a_mcp_rag_server.py # port 8001

# Terminal 2 — then start the agent
uv run python exercises/part_02/02b_mcp_rag_agent.py # port 8000
```

> **Important:** The MCP server must be running before any MCP-dependent agent. Agents discover the `search_relevant_context_from_HAL_9000_policy` tool automatically via the MCP protocol at `localhost:8001/mcp`.

---

### Part 02 BONUS — Guardrails & Safety

| Script | What it does |
|---|---|
| [`simple_guardrail.py`](exercises/part_02_BONUS/simple_guardrail.py) | Agent with `pydantic_ai_shields` `PromptInjection()` — blocks prompt injection attacks (CLI) |
| [`guardrails_with_hooks.py`](exercises/part_02_BONUS/guardrails_with_hooks.py) | Agent with a custom `before_model_request` hook — inspects and blocks/redacts forbidden content (web app on port 8000) |

```bash
uv run python exercises/part_02_BONUS/simple_guardrail.py
uv run python exercises/part_02_BONUS/guardrails_with_hooks.py
```

---

### Part 03 — Observability with Langfuse

Part 03 compares an ungrounded model answer with a tool-assisted RAG answer,
then uses Langfuse to inspect what happened inside each agent run.

#### 1. Start the local Langfuse instance

Docker Desktop (or Docker Engine with Compose) must be running. The first start
downloads the Langfuse services and can take a few minutes.

```bash
docker compose -f observability/docker-compose.yml up -d --wait
curl --fail "http://localhost:3000/api/public/health?failIfDatabaseUnavailable=true"
```

Open [http://localhost:3000](http://localhost:3000) and sign in with the
preconfigured local workshop account:

- Email: `student@tutorial.local`
- Password: `tutorial-langfuse`

The Compose file creates the **Tutorial Agents** project and matching API keys
automatically. These credentials are deliberately public and safe only because
the workshop services bind to your local machine.

#### 2. Instrument and run the lab

Complete `exercises/part_03/01_observability.py`, then run it:

```bash
uv run python exercises/part_03/01_observability.py
```

The exercise requires a healthy Langfuse instance and tells you how to start it
if the health or authentication check fails. Short-lived scripts flush their
pending trace data before they exit.

#### 3. Investigate the traces

In the Langfuse **Tracing** view, compare `observability_baseline_agent` with
`observability_rag_agent`:

1. How many model requests did each run make?
2. Which span contains the search query and retrieved policy chunks?
3. What information is added to the second RAG model request?
4. Which operation dominates latency?
5. How do input and output token counts differ?

To trace any earlier exercise, set `LANGFUSE_ENABLED=true` for the agent process:

```bash
LANGFUSE_ENABLED=true uv run python exercises/part_02/01_rag_agent.py
```

For the MCP example, leave the server unchanged and enable tracing on the agent:

```bash
# Terminal 1
uv run python exercises/part_02/02a_mcp_rag_server.py

# Terminal 2
LANGFUSE_ENABLED=true uv run python exercises/part_02/02b_mcp_rag_agent.py
```

The trace shows the agent-side MCP selection, arguments, result, and duration.
It does not continue as a distributed trace inside the separate FastMCP server.

As an error-trace experiment, run the hook guardrail with observability enabled
and ask its web UI a question containing `cat`. Inspect where the run fails:

```bash
LANGFUSE_ENABLED=true uv run python exercises/part_02_BONUS/guardrails_with_hooks.py
```

The custom workshop model reports token usage, but Langfuse may leave cost empty
because it has no pricing table for that model name.

#### 4. Stop or reset Langfuse

Normal shutdown preserves traces in Docker volumes:

```bash
docker compose -f observability/docker-compose.yml down
```

To delete all local Langfuse traces, accounts, and project data and recreate a
clean workshop instance, remove the volumes explicitly:

```bash
docker compose -f observability/docker-compose.yml down -v
```

If startup fails, inspect the service state and logs:

```bash
docker compose -f observability/docker-compose.yml ps
docker compose -f observability/docker-compose.yml logs --tail=100
```

---

## FAQ

**How do I re-index the PDF vector store?**
Delete `data/chroma_db/` and rerun the completed Part 01 `03_rag_step_by_step.py` script. Later agents and the MCP server only reuse that collection.

**Where is the reference solution?**
Every exercise in `exercises/` has a matching file in `solutions/` with the same name.
