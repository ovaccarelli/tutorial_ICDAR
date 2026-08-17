"""Utility functions for a simple Retrieval-Augmented Generation (RAG) workflow."""

from pathlib import Path

import chromadb
from loguru import logger
from pdfminer.high_level import extract_text

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent.parent.parent / "data"
CHROMA_DIR = DATA_DIR / "chroma_db"
COLLECTION_NAME = "part_01_step_by_step_pdf_chunks"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 5


def extract_pdf_to_markdown(pdf_file: Path) -> str:
    """Extract text from one PDF file and save it as a Markdown file.

    Args:
        pdf_file: The path to the PDF file.

    Returns:
        A string containing the extracted text.
    """
    text = extract_text(pdf_file)
    markdown_file = pdf_file.with_suffix(".md")
    markdown_file.write_text(text, encoding="utf-8")
    logger.info(f"Extracted text from {pdf_file.name}: {len(text)} characters")
    logger.info(f"Saved extracted text to {markdown_file}")
    return text


def build_chunks(
    text: str,
    source_name: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """Split extracted text into overlapping chunks with source metadata."""
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    for position in range(0, len(text), chunk_size - chunk_overlap):
        chunk = text[position : position + chunk_size]
        documented_chunk = (
            f"Source: {source_name}\nPosition: {position}\nContent:\n{chunk}"
        )
        chunks.append(documented_chunk)

    logger.info(f"Total chunks created: {len(chunks)}")
    return chunks


def create_vector_collection(
    chunks: list[str],
    chroma_dir: Path = CHROMA_DIR,
    collection_name: str = COLLECTION_NAME,
    reindex: bool = True,
) -> chromadb.Collection:
    """Create a ChromaDB collection and store the chunks.

    Args:
        chunks: A list of text chunks to store in the vector database.
        chroma_dir: The directory where ChromaDB will store its data.
        collection_name: The name of the ChromaDB collection to create or load.
        reindex: Whether to upsert chunks if the collection already has documents.

    Returns:
        A ChromaDB collection containing the stored chunks.
    """
    client = chromadb.PersistentClient(path=str(chroma_dir))
    collection = client.get_or_create_collection(name=collection_name)

    if not reindex and collection.count() > 0:
        logger.info(
            f"Using existing ChromaDB collection '{collection_name}' "
            f"with {collection.count()} chunks"
        )
        return collection

    if not chunks:
        logger.warning("No chunks to store in ChromaDB")
        return collection

    collection.upsert(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )
    logger.info(
        f"Upserted {len(chunks)} chunks into ChromaDB collection '{collection_name}'"
    )

    return collection


def retrieve_context(
    collection: chromadb.Collection,
    question: str,
    top_k: int = TOP_K,
) -> str:
    """Retrieve the most relevant chunks based on semantic similarity.

    Args:
        collection: The ChromaDB collection to query.
        question: The user's question.
        top_k: The number of chunks to retrieve.

    Returns:
        A string containing the retrieved chunks.
    """
    logger.info(f"Retrieving context for question: '{question}'")
    results = collection.query(query_texts=[question], n_results=top_k)
    documents = results.get("documents") or [[]]
    retrieved_chunks = documents[0]

    if not retrieved_chunks:
        return "No relevant document chunks were found."

    context = "\n------------\n".join(retrieved_chunks)
    logger.info(f"Retrieved context:\n{context}\nEnd of retrieved context.")
    return context


def build_vector_collection(
    pdf_path: Path,
    chroma_dir: Path,
    collection_name: str,
    chunk_size: int,
    chunk_overlap: int,
    reindex: bool = True,
) -> chromadb.Collection:
    """Build a ChromaDB vector collection from a PDF.

    Args:
        pdf_path: The path to the PDF file to process.
        chroma_dir: The directory where ChromaDB will store its data.
        collection_name: The name of the ChromaDB collection to create or load.
        chunk_size: The size of each text chunk.
        chunk_overlap: The number of overlapping characters between chunks.
        reindex: Whether to upsert chunks if the collection already has documents.

    Returns:
        A ChromaDB collection containing the stored chunks.
    """
    text = extract_pdf_to_markdown(pdf_path)
    chunks = build_chunks(text, pdf_path.name, chunk_size, chunk_overlap)
    return create_vector_collection(chunks, chroma_dir, collection_name, reindex)
