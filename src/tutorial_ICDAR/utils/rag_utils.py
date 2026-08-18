"""Shared retrieval helper for the persistent workshop RAG collection."""

import chromadb
from loguru import logger

TOP_K = 8


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
