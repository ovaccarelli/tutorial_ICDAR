"""Pydantic AI agent that can use the document tools."""

from pathlib import Path

import chromadb
import uvicorn
from loguru import logger
from pydantic_ai import Agent, ModelSettings

from tutorial_ICDAR.utils.document_tools import (
    extract_text_from_image_file,
    extract_text_from_md_or_txt_file,
    list_my_available_documents,
)
from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model
from tutorial_ICDAR.utils.rag_utils import retrieve_context

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
COLLECTION_NAME = "HAL_9000_Expense_Reimbursement_Policy_chunks"
TOP_K = 5

# Reuse the persistent collection created in Part 01.
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_collection(name=COLLECTION_NAME)


agent = Agent(
    model=get_vllm_model(),
    # EXERCISE 1 - Document tools:
    # Add the document tools to the agent so it can use them
    # to answer questions about the workshop documents.
    # They are defined in tutorial_ICDAR.utils.document_tools (see imports above).
    # Tip: Add the tools directly as a list of python functions.
    tools=[...],
    instructions=(
        "You are a helpful document assistant. Decide which tools are needed "
        "for the user's question. First check whether an available document is "
        "related to the question. Mention the filenames you use."
    ),
    model_settings=ModelSettings(thinking="minimal"),
)

@agent.tool_plain
def search_relevant_context_from_HAL_9000_policy(query: str) -> str:
    """Search relevant context from the HAL 9000 policy using semantic search.

    Args:
        query: The search query.

    Returns:
        The top matching HAL 9000 policy chunks.
    """
    return retrieve_context(collection, query, TOP_K)


if __name__ == "__main__":
    # EXERCISE 2 - Test the agent with document tools and RAG retrieval:
    # Start the agent and ask it questions about the workshop documents and the HAL 9000 policy.
    # Example questions: With respect to the HAL 9000 policy, is my restaurant too expensive?
    app = agent.to_web()
    logger.info("Starting Document Context Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
