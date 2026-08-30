"""Step-by-Step RAG Exercise

In this exercise, we build a small Retrieval-Augmented Generation pipeline.

1. Split the extracted policy text into overlapping chunks.
2. Store the chunks in ChromaDB.
3. Retrieve the chunks most relevant to a question.
4. Give the question and retrieved context to an AI model.

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

print("\n----------- STEP 1: SPLIT INTO CHUNKS -----------")

policy_text = extract_text(str(POLICY_PDF))

# EXERCISE - Chunk settings:
# Choose a chunk size and overlap for splitting the extracted policy text.
CHUNK_SIZE = ...
CHUNK_OVERLAP = ...
STEP_SIZE = CHUNK_SIZE - CHUNK_OVERLAP

chunks: list[str] = []

for position in range(0, len(policy_text), STEP_SIZE):
    content = policy_text[position : position + CHUNK_SIZE]
    if content.strip():
        chunks.append(content)

print(
    f"Created {len(chunks)} chunks "
)
print(f"Preview of first chunk:\n{chunks[0][:500]}")


#################################################################
# STEP 2 - Store the chunks in ChromaDB
#################################################################

print("\n----------- STEP 2: STORE CHUNKS -----------")

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# EXERCISE - Store the chunks:
# Pass the chunks to ChromaDB as documents. Each document already has a
# stable ID generated below.
collection.upsert(
    documents=...,
    ids=[f"chunk_{index}" for index in range(len(chunks))],
)

print(
    f"Stored chunks in ChromaDB collection '{COLLECTION_NAME}', "
    f"with {collection.count()} chunks"
)


#################################################################
# STEP 3 - Retrieve context for a question
#################################################################

print("\n----------- STEP 3: RETRIEVE CONTEXT -----------")

question = "What transportation expenses are reimbursable?"

# EXERCISE - Retrieval settings:
# Choose how many relevant chunks to retrieve for the question.
TOP_K = ...

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

print("\n----------- STEP 4: GENERATE ANSWER -----------")

# EXERCISE - Define the system prompt:
# Tell the model to answer only from the retrieved context and to say when
# the context does not contain the answer.
SYSTEM_PROMPT = ...

agent = Agent(
    model=get_vllm_model(),
    instructions=SYSTEM_PROMPT,
    model_settings=ModelSettings(thinking="minimal"),
)

result = agent.run_sync(
    f"Question: {question}\n\nRetrieved context:\n{context}"
)

print(f"Final answer:\n{result.output}")
