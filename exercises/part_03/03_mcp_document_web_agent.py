"""Agent combining MCP RAG, document tools, web search, and time."""

from datetime import datetime

import uvicorn
from loguru import logger
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.capabilities import MCP, WebSearch

from tutorial_ICDAR.utils.document_tools import (
    extract_text_from_image_file,
    extract_text_from_md_or_txt_file,
    list_my_available_documents,
)
from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model

MCP_SERVER_URL = "http://localhost:8001/mcp"

agent = Agent(
    model=get_vllm_model(),
    tools=[
        list_my_available_documents,
        extract_text_from_md_or_txt_file,
        extract_text_from_image_file,
    ],
    instructions=(
        "You are a helpful document assistant. Decide which tools are needed "
        "for the user's question. First check whether an available document is "
        "related to the question. Mention the filenames you use."
    ),
    model_settings=ModelSettings(thinking="minimal"),
    capabilities=[
        MCP(url=MCP_SERVER_URL),
        WebSearch(builtin=False),
    ],
)


@agent.tool_plain
def get_current_time() -> str:
    """Get the current local date and time."""
    logger.info("Agent is using the tool to get the current local time.")
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


if __name__ == "__main__":
    # EXERCISE 1 - Start this agent and ask it questions that require using the local document tools,
    # MCP retrieval, web search, and the current time tool to see how it uses all the capabilities
    # together.
    app = agent.to_web()
    logger.info("Starting MCP Document Web Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
