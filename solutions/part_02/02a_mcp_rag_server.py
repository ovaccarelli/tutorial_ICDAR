from pathlib import Path

from mcp.server.fastmcp import FastMCP

from tutorial_ICDAR.utils.rag_utils import get_policy_collection, retrieve_context

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"
TOP_K = 8

# Prefer the collection created in Part 01; use the bundled fallback if needed.
collection = get_policy_collection(DATA_DIR)

# Start a FastMCP server that will serve the RAG retrieval tool over HTTP. 
# The agent will connect to this server to perform retrieval.
mcp = FastMCP(
    "RAG Server for HAL 9000 Policy",
    streamable_http_path="/mcp",
    port=8001,
    stateless_http=True,
)

# Solution: the tool simply calls the existing retrieval function with the collection and user question.
@mcp.tool()
def search_relevant_context_from_HAL_9000_policy(question: str) -> str:
    """Search relevant context from the HAL 9000 policy using semantic search.

    Args:
        question: The user's question.

    Returns:
        The top matching HAL 9000 policy chunks.
    """
    return retrieve_context(collection, question, TOP_K)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
