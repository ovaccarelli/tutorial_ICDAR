"""Compare an ungrounded answer with an observable, tool-assisted RAG run."""

from pathlib import Path

from pydantic_ai import Agent, ModelSettings

from tutorial_ICDAR.utils.console_utils import console, print_result, print_step
from tutorial_ICDAR.utils.observability import configure_observability
from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model
from tutorial_ICDAR.utils.rag_utils import get_policy_collection, retrieve_context

HERE = Path(__file__).parent
DATA_DIR = HERE.parent.parent / "data"
TOP_K = 8
QUESTION = "What transportation expenses are reimbursable?"

# EXERCISE 1 - Enable required observability before creating any agents.
# Use configure_observability and make the exercise fail clearly if the local
# Langfuse instance is not running.
langfuse = ...

model = get_vllm_model()
collection = get_policy_collection(DATA_DIR)

baseline_agent = Agent(
    model=model,
    name="observability_baseline_agent",
    instructions=(
        "Answer concisely using only your general knowledge. If the question "
        "depends on a policy you cannot see, say you don't know."
    ),
    model_settings=ModelSettings(thinking="minimal"),
)

rag_agent = Agent(
    model=model,
    name="observability_rag_agent",
    instructions=(
        "Answer questions about the HAL 9000 policy using the search tool. "
        "If the retrieved policy does not contain the answer, say you don't know."
    ),
    model_settings=ModelSettings(thinking="minimal"),
)


@rag_agent.tool_plain
def search_policy(query: str) -> str:
    """Retrieve the policy chunks most relevant to a question."""
    return retrieve_context(collection, query, TOP_K)


if __name__ == "__main__":
    try:
        print_step("Baseline agent: no retrieval tool")
        console.print(f"Question: {QUESTION}")
        baseline_result = baseline_agent.run_sync(QUESTION)
        print_result(baseline_result.output)

        print_step("RAG agent: model, tool, model")
        console.print(f"Question: {QUESTION}")
        rag_result = rag_agent.run_sync(
            f"Use the policy search tool before answering: {QUESTION}"
        )
        print_result(rag_result.output)
    finally:
        # Short-lived programs should flush pending spans before exiting.
        langfuse.flush()
