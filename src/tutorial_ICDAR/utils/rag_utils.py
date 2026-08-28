"""Shared retrieval helper for the persistent workshop RAG collection."""

from pathlib import Path

import chromadb
from chromadb.errors import NotFoundError
from loguru import logger

TOP_K = 8
COLLECTION_NAME = "HAL_9000_Expense_Reimbursement_Policy_chunks"
PREBUILT_COLLECTION_NAME = f"{COLLECTION_NAME}_prebuilt"


def get_policy_collection(data_dir: Path) -> chromadb.Collection:
    """Load the learner's collection, or fall back to the bundled collection."""
    learner_client = chromadb.PersistentClient(path=str(data_dir / "chroma_db"))
    try:
        collection = learner_client.get_collection(name=COLLECTION_NAME)
        logger.info("Using the collection created in Part 01")
        return collection
    except NotFoundError:
        logger.warning(
            "The Part 01 collection was not found; using the bundled prebuilt collection"
        )

    prebuilt_client = chromadb.PersistentClient(
        path=str(data_dir / "chroma_db_prebuilt")
    )
    return prebuilt_client.get_collection(name=PREBUILT_COLLECTION_NAME)


def retrieve_context(
    collection: chromadb.Collection,
    question: str,
    top_k: int = TOP_K,
) -> str:
    """Retrieve the text chunks most relevant to a question.

    Args:
        collection: The ChromaDB collection created in Part 01.
        question: The user's question.
        top_k: The number of chunks to retrieve.

    Returns:
        The retrieved chunks joined into one context string.
    """
    logger.info(f"Retrieving context for question: '{question}'")
    results = collection.query(query_texts=[question], n_results=top_k)
    documents = results.get("documents") or [[]]
    retrieved_chunks = documents[0]

    if not retrieved_chunks:
        return "No relevant document chunks were found."

    context = "\n------------\n".join(retrieved_chunks)
    logger.info(f"Retrieved {len(retrieved_chunks)} chunks")
    return context
