"""Solution for the step-by-step RAG exercise.

This solution mirrors exercises/part_01/02_rag_step_by_step.py and fills in the
exercise blanks with short comments explaining each completed line.
"""

from pathlib import Path

import chromadb
from pdfminer.high_level import extract_text
from pydantic_ai import Agent, ModelSettings

from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent.parent / "data"
HEIDITECH_POLICY_PDF = DATA_DIR / "HeidiTech_Expense_Reimbursement_Policy.pdf"
CHROMA_DIR = DATA_DIR / "chroma_db"
COLLECTION_NAME = "part_01_step_by_step_pdf_chunks"


def extract_pdf_to_markdown(pdf_file: Path) -> str:
    """Extract text from one PDF file.

    Args:
        pdf_file: The path to the PDF file.

    Returns:
        A string containing the extracted text.
    """
    print("\nSTEP 1 - Extract PDF text")
    print(f"Reading PDF: {pdf_file}")

    # Solution: extract_text reads the PDF and returns its text as a string.
    text = extract_text(pdf_file)

    print(f"Extracted {len(text)} characters")
    print("\nPreview of extracted text:")
    print(text[:700])

    return text


# Solution: use overlapping chunks of 1000 characters with 200 characters repeated.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def build_chunks(text: str, source_name: str) -> list[str]:
    """Split extracted text into overlapping chunks with source metadata.

    Args:
        text: The extracted text to split into chunks.
        source_name: The name of the source document, used for metadata.

    Returns:
        A list of strings, each representing a chunk of the extracted text.
    """
    print("\nSTEP 2 - Split text into chunks")
    chunks = []

    for position in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP):
        chunk = text[position : position + CHUNK_SIZE]

        documented_chunk = (
            f"Source: {source_name}\nPosition: {position}\nContent:\n{chunk}"
        )
        chunks.append(documented_chunk)

    print(f"Created {len(chunks)} chunks")
    print("\nPreview of first chunk:")
    print(chunks[0][:700])

    return chunks


def create_vector_collection(chunks: list[str]) -> chromadb.Collection:
    """Create a ChromaDB collection and store the chunks.

    Args:
        chunks: A list of text chunks to store in the vector database.

    Returns:
        A ChromaDB collection containing the stored chunks.
    """
    print("\nSTEP 3 - Store chunks in ChromaDB")

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    collection.upsert(
        # Solution: store the generated text chunks as ChromaDB documents.
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )

    print(f"Collection name: {COLLECTION_NAME}")
    print(f"Collection count: {collection.count()}")

    return collection


# Solution: retrieve the five most relevant chunks for the question.
TOP_K = 5


def retrieve_context(collection: chromadb.Collection, question: str) -> str:
    """Retrieve the most relevant chunks based on semantic similarity for a user question.

    Args:
        collection: The ChromaDB collection containing the chunks.
        question: The user's question.

    Returns:
        A string containing the TOP_K retrieved chunks.
    """
    print("\nSTEP 4 - Retrieve context from ChromaDB")
    print(f"Question: {question}")

    results = collection.query(
        # Solution: Chroma expects a list of query strings, even for one question.
        query_texts=[question],
        # Solution: n_results controls how many matching chunks are returned.
        n_results=TOP_K,
    )

    documents = results.get("documents") or [[]]
    retrieved_chunks = documents[0]

    print(f"Retrieved {len(retrieved_chunks)} chunks")

    if not retrieved_chunks:
        return "No relevant document chunks were found."

    context = "\n\n------------\n\n".join(retrieved_chunks)
    print("\nPreview of retrieved context:")
    print(context[:1200])

    return context


def answer_with_context(question: str, context: str) -> str:
    """Ask the model to answer using the retrieved context

    Args:
        question: The user's question.
        context: The retrieved context from ChromaDB.

    Returns:
        The model's answer based on the retrieved context.
    """
    print("\nSTEP 5 - Ask the model with retrieved context")

    agent = Agent(
        model=get_vllm_model(),
        # Solution: tell the model to answer only from retrieved context.
        instructions=(
            "You are a helpful assistant. Use the retrieved document context to "
            "answer the user's question. If the answer is not in the context, "
            "say you don't know. Cite sources using the PDF name and position."
        ),
        model_settings=ModelSettings(thinking="minimal"),
    )

    # Solution: the final RAG prompt combines the user question and retrieved context.
    prompt = f"Question: {question}\n\nRetrieved context:\n{context}"

    result = agent.run_sync(prompt)
    return result.output


if __name__ == "__main__":
    user_question = "What is reimbursed for transportation expenses?"

    extracted_text = extract_pdf_to_markdown(HEIDITECH_POLICY_PDF)
    pdf_chunks = build_chunks(extracted_text, HEIDITECH_POLICY_PDF.name)
    vector_collection = create_vector_collection(pdf_chunks)
    retrieved_context = retrieve_context(vector_collection, user_question)
    answer = answer_with_context(user_question, retrieved_context)

    print("\nFINAL ANSWER")
    print(answer)
