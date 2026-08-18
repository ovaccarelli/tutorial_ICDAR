from pathlib import Path

from mcp.server.fastmcp import FastMCP

from tutorial_ICDAR.utils.rag_utils import (
    build_vector_collection,
    retrieve_context,
)

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5
COLLECTION_NAME = "pdf_chunks_part_03_mcp_rag_server"
HAL_9000_POLICY_PDF = DATA_DIR / "HAL_9000_Expense_Reimbursement_Policy.pdf"


collection = build_vector_collection(
    pdf_path=HAL_9000_POLICY_PDF,
    chroma_dir=CHROMA_DIR,
    collection_name=COLLECTION_NAME,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

mcp = FastMCP("RAG Server", streamable_http_path="/mcp", port=8001)


@mcp.tool()
def search_relevant_context_from_HAL_9000_policy(question: str) -> str:
    """Search relevant context from the HAL 9000 policy using semantic search.

    Args:
        question: The user's question.

    Returns:
        The top matching HAL 9000 policy chunks with source filename and positions.
    """
    # Solution: the tool simply calls the existing retrieval
    # function with the collection and user question.
    return retrieve_context(collection, question, TOP_K)


if __name__ == "__main__":
    # EXERCISE 1 - RAG Server:
    # Start this RAG server and go to part_03/02b
    # to connect the agent to this mcp server for RAG retrieval.
    mcp.run(transport="streamable-http")
