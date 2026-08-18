"""Step-by-step RAG exercise.

This script shows the full RAG flow one step at a time:
1. Extract text from a PDF.
2. Split the extracted text into chunks.
3. Store the chunks in ChromaDB.
4. Retrieve relevant context for a user question.
5. Ask the model to answer using only the retrieved context.
"""

from pathlib import Path

import chromadb
from pdfminer.high_level import extract_text
from pydantic_ai import Agent, ModelSettings

from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent.parent / "data"
HAL_9000_POLICY_PDF = DATA_DIR / "HAL_9000_Expense_Reimbursement_Policy.pdf"
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

    # EXERCISE 1 - PDF extraction:
    # The PDF is not directly useful for the model,
    # so we first extract its text content into a normal Python string.
    # Complete this line with pdfminer's extract_text function.
    text = ...

    print(f"Extracted {len(text)} characters")
    print("\nPreview of extracted text:")
    print(text[:700])

    return text


# EXERCISE 2 - Parameters for chunking:
# Adjust these parameters and see how they affect the results.
CHUNK_SIZE = ...
CHUNK_OVERLAP = ...


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

    # EXERCISE 3 - Upsert chunks into ChromaDB:
    # The upsert method takes a list of documents and their corresponding IDs.
    # Upsert means "insert or update" - if the ID already exists, it will update the document.
    # Complete the upsert call with the chunks and their IDs.
    # The IDs are already generated for you.
    collection.upsert(
        documents=...,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )

    print(f"Collection name: {COLLECTION_NAME}")
    print(f"Collection count: {collection.count()}")

    return collection


# EXERCISE 4 - Parameters for retrieval:
# Adjust TOP_K to retrieve more or fewer chunks and see how it affects the answer.
TOP_K = ...


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

    # EXERCISE 5 - Retrieval:
    # ChromaDB compares the question embedding with the stored chunk embeddings
    # and returns the most similar chunks.
    # Complete the query call below using the question and TOP_K.
    results = collection.query(query_texts=..., n_results=...)

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

    # EXERCISE 6 - Define the system prompt:
    # The model receives both the user question and the retrieved chunks.
    # Important: the model should answer only from the retrieved context.
    agent = Agent(
        model=get_vllm_model(),
        instructions=("..."),
        model_settings=ModelSettings(thinking="minimal"),
    )

    # EXERCISE 6 - Final RAG prompt:
    # This is where retrieval and generation meet. Without the retrieved context,
    # the model would have to rely on its own knowledge.
    # Write the prompt to include both the question and retrieved context.
    prompt = ...

    result = agent.run_sync(prompt)
    return result.output


if __name__ == "__main__":
    user_question = "What is reimbursed for transportation expenses?"

    extracted_text = extract_pdf_to_markdown(HAL_9000_POLICY_PDF)
    # pdf_chunks = build_chunks(extracted_text, HAL_9000_POLICY_PDF.name)
    # vector_collection = create_vector_collection(pdf_chunks)
    # retrieved_context = retrieve_context(vector_collection, user_question)
    # answer = answer_with_context(user_question, retrieved_context)

    # print("\nFINAL ANSWER")
    # print(answer)
