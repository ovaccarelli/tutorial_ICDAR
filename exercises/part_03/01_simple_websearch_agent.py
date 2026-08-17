"""Script to demonstrate a simple web search agent."""

import uvicorn
from loguru import logger
from pydantic_ai import Agent
from pydantic_ai.capabilities import WebSearch

from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model

agent = Agent(
    model=get_vllm_model(),
    instructions=(
        "You are a helpful assistant that can search the web to provide up-to-date information. "
        "Always use the search tool when you need current information and cite your findings."
    ),
    capabilities=[
        WebSearch(builtin=False),
    ],
)

if __name__ == "__main__":
    # EXERCISE - Web search agent:
    # Start the agent and ask it questions that require up-to-date information
    # that is not in the training data.
    # Example question: Give me the train ticket from Solothurn to Fribourg for today.
    # and tell me the departure times and prices.
    app = agent.to_web()
    logger.info("Starting Web Search Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
