"""Script doing the same thing as 02_rag_step_by_step.py but with agentic RAG."""

from pathlib import Path

import uvicorn
from loguru import logger
from pydantic_ai import Agent, ModelSettings

from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model
from tutorial_ICDAR.utils.rag_utils import (
    build_vector_collection,
    retrieve_context,
)

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"
HAL_9000_POLICY_PDF = DATA_DIR / "HAL_9000_Expense_Reimbursement_Policy.pdf"

CHROMA_DIR = DATA_DIR / "chroma_db"
COLLECTION_NAME = "pdf_chunks_part_02_simple_rag_agent"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5


collection = build_vector_collection(
    pdf_path=HAL_9000_POLICY_PDF,
    chroma_dir=CHROMA_DIR,
    collection_name=COLLECTION_NAME,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

agent = Agent(
    model=get_vllm_model(),
    instructions=(
        "You are a helpful assistant. Be concise and accurate. "
        "Always use the available tools when answering questions about the documents. "
        "Always cite sources using the PDF name and position in the format: "
        "[Source: filename.pdf, Position: X]. "
        "If the information is not found in the documents, say you don't know."
    ),
    model_settings=ModelSettings(thinking="minimal"),
)


# Solution: expose retrieval as a tool so the agent can call it when needed
# to get relevant context for answering user questions.
@agent.tool_plain
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
    app = agent.to_web()
    logger.info("Starting Simple RAG Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
