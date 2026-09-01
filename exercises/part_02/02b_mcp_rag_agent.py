import uvicorn
from loguru import logger
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset

from tutorial_ICDAR.utils.observability import configure_observability
from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model

MCP_SERVER_URL = "http://localhost:8001/mcp"

configure_observability()

# EXERCISE 1 - Check the MCPToolset documentation and initialize
# the toolset to connect to part_02/02a_mcp_rag_server.py.
# Link to documentation: https://ai.pydantic.dev/mcp/client/
toolset = ...

agent = Agent(
    model=get_vllm_model(),
    name="mcp_rag_agent",
    instructions=(
        "You are a helpful assistant. Be concise and accurate. "
        "Always use the available tools when providing document information. "
        "If the information is not found in the documents, say you don't know. "
        "Do not answer questions unrelated to the document content."
    ),
    toolsets=[toolset],
)


if __name__ == "__main__":
    # EXERCISE 2 - Start this agent and ask it questions about the HAL 9000 policy.
    # Example question: According to the HAL 9000 policy, what is the maximum amount
    # that can be reimbursed for a meal without itemized receipts? And what is the source
    # of this information?
    app = agent.to_web()
    logger.info("Starting MCP RAG Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
