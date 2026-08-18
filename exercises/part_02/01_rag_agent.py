"""Agentic version of the pipeline introduced in Part 01's 03_rag_step_by_step.py."""

from pathlib import Path

import chromadb
import uvicorn
from loguru import logger
from pydantic_ai import Agent, ModelSettings

from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model
from tutorial_ICDAR.utils.rag_utils import retrieve_context

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
COLLECTION_NAME = "HAL_9000_Expense_Reimbursement_Policy_chunks"
TOP_K = 8

# Reuse the persistent collection created in Part 01.
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_collection(name=COLLECTION_NAME)

agent = Agent(
    model=get_vllm_model(),
    instructions=(
        "You are a helpful assistant. Be concise and accurate. "
        "Always use the available tools when answering questions about the documents. "
        "If the information is not found in the documents, say you don't know."
    ),
    model_settings=ModelSettings(thinking="minimal"),
)

# EXERCISE - Add a tool to the agent that retrieves relevant context from the HAL 9000 policy.
...
def search_relevant_context_from_HAL_9000_policy(query: str) -> str:
    """Search relevant context from the HAL 9000 policy.

    Args:
        query: The search query.

    Returns:
        The top matching HAL 9000 policy chunks.
    """
    return retrieve_context(collection, query, TOP_K)


if __name__ == "__main__":
    app = agent.to_web()
    logger.info("Starting Simple RAG Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
