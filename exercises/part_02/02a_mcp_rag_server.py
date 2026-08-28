from pathlib import Path

from mcp.server.fastmcp import FastMCP

from tutorial_ICDAR.utils.rag_utils import get_policy_collection, retrieve_context

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"
TOP_K = 8

# Prefer the collection created in Part 01; use the bundled fallback if needed.
collection = get_policy_collection(DATA_DIR)

mcp = FastMCP("RAG Server", streamable_http_path="/mcp", port=8001)

# EXERCISE 1 - MCP Tool:
# Implement the search_relevant_context_from_HAL_9000_policy function as an MCP tool.
...
def search_relevant_context_from_HAL_9000_policy(question: str) -> str:
    """Search relevant context from the HAL 9000 policy using semantic search.

    Args:
        question: The user's question.

    Returns:
        The top matching HAL 9000 policy chunks.
    """
    return retrieve_context(collection, question, TOP_K)


if __name__ == "__main__":
    # EXERCISE 2 - RAG Server:
    # Start this RAG server and go to part_02/02b_mcp_rag_agent.py
    # to connect the agent to this mcp server for RAG retrieval.
    mcp.run(transport="streamable-http")
