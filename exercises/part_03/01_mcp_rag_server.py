from pathlib import Path

import chromadb
from mcp.server.fastmcp import FastMCP

from tutorial_ICDAR.utils.rag_utils import retrieve_context

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
TOP_K = 5
COLLECTION_NAME = "HAL_9000_Expense_Reimbursement_Policy_chunks"

# Reuse the persistent collection created in Part 01.
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_collection(name=COLLECTION_NAME)

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
    # Start this RAG server and go to part_03/02_simple_mcp_rag_agent.py
    # to connect the agent to this mcp server for RAG retrieval.
    mcp.run(transport="streamable-http")
