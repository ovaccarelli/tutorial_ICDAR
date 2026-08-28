"""Solution for the Step-by-Step RAG Exercise.

This file mirrors exercises/part_01/03_rag_step_by_step.py and fills every
exercise placeholder.

"""

from pathlib import Path

import chromadb
from pdfminer.high_level import extract_text
from pydantic_ai import Agent, ModelSettings

from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model

# Define file paths and constants
HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent.parent / "data"
MY_DOCUMENTS = DATA_DIR / "my_documents"
POLICY_PDF = MY_DOCUMENTS / "HAL_9000_Expense_Reimbursement_Policy.pdf"
CHROMA_DIR = DATA_DIR / "chroma_db"
COLLECTION_NAME = "HAL_9000_Expense_Reimbursement_Policy_chunks"


#################################################################
# STEP 1 - Split the text into overlapping chunks
#################################################################

policy_text = extract_text(str(POLICY_PDF))

# SOLUTION - Chunk settings:
# A step of 800 characters leaves 200 characters shared by adjacent chunks.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
STEP_SIZE = CHUNK_SIZE - CHUNK_OVERLAP

chunks: list[str] = []

for position in range(0, len(policy_text), STEP_SIZE):
    content = policy_text[position : position + CHUNK_SIZE]
    if content.strip():
        chunks.append(content)

print(
    f"Created {len(chunks)} chunks "
    f"(size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})"
)
print(f"Preview of first chunk:\n{chunks[0][:500]}")


#################################################################
# STEP 2 - Store the chunks in ChromaDB
#################################################################

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# SOLUTION - Store the chunks:
# Pass the chunks as the documents stored and embedded by ChromaDB.
collection.upsert(
    documents=chunks,
    ids=[f"chunk_{index}" for index in range(len(chunks))],
)

print(
    f"Stored chunks in ChromaDB collection '{COLLECTION_NAME}', "
    f"with {collection.count()} chunks"
)


#################################################################
# STEP 3 - Retrieve context for a question
#################################################################

question = "What transportation expenses are reimbursable?"

# SOLUTION - Retrieval settings:
# Retrieve the eight chunks most similar to the question.
TOP_K = 8

# SOLUTION - Semantic retrieval:
# Wrap the question in a list because ChromaDB supports multiple queries.
results = collection.query(
    query_texts=[question],
    n_results=TOP_K,
)

retrieved_chunks = (results.get("documents") or [[]])[0]
context = "\n\n------------\n\n".join(retrieved_chunks)

print(f"Question: {question}")
print(f"Preview of retrieved context:\n{context[:1000]}")


#################################################################
# STEP 4 - Generate an answer from the retrieved context
#################################################################

# SOLUTION - Define the system prompt:
# Ground the model in the context and define behavior for missing answers.
SYSTEM_PROMPT = """
You are a helpful assistant that answers questions from the provided context.
- Use only the context to answer the question.
- If the context does not contain the answer, say "I don't know."
"""

agent = Agent(
    model=get_vllm_model(),
    instructions=SYSTEM_PROMPT,
    model_settings=ModelSettings(thinking="minimal"),
)

result = agent.run_sync(
    f"Question: {question}\n\nRetrieved context:\n{context}"
)

print(f"Final answer:\n{result.output}")
