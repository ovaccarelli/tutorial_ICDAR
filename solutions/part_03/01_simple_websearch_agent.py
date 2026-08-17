"""Script to demonstrate a simple web search agent."""

import uvicorn
from loguru import logger
from pydantic_ai import Agent
from pydantic_ai.capabilities import WebFetch, WebSearch

from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model

agent = Agent(
    model=get_vllm_model(),
    instructions=(
        "You are a helpful assistant that can search the web to provide up-to-date information. "
        # "Always use the search tool when you need current information and cite your findings. "
        "After searching, use the fetch tool to get more details from the most relevant url. "
        # "Do not trust the search results blindly, always check the source and provide the url in your answer. "
    ),
    capabilities=[
        WebSearch(builtin=False),
        # WebFetch(builtin=False),
    ],
)

if __name__ == "__main__":
    app = agent.to_web()
    logger.info("Starting Web Search Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
