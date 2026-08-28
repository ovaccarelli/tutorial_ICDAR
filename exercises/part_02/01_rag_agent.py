"""Agentic version of the pipeline introduced in Part 01's 03_rag_step_by_step.py."""

from pathlib import Path

import uvicorn
from loguru import logger
from pydantic_ai import Agent, ModelSettings

from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model
from tutorial_ICDAR.utils.rag_utils import get_policy_collection, retrieve_context

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"
TOP_K = 8

# Prefer the collection created in Part 01; use the bundled fallback if needed.
collection = get_policy_collection(DATA_DIR)

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
