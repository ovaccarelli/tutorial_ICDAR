"""Agent combining MCP RAG, document tools, and web search."""

import uvicorn
from loguru import logger
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.capabilities import MCP, WebSearch

from tutorial_ICDAR.utils.document_tools import (
    extract_text_from_image_file,
    extract_text_from_md_or_txt_file,
    extract_text_from_pdf_file,
    list_my_available_documents,
)
from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model

MCP_SERVER_URL = "http://localhost:8001/mcp"

agent = Agent(
    model=get_vllm_model(),
    # EXERCISE 1 - Document tools:
    # Add the document tools to the agent so it can use them
    # to answer questions about the workshop documents.
    # They are defined in tutorial_ICDAR.utils.document_tools (see imports above).
    # Tip: Add the tools directly as a list of python functions.
    tools=[...],
    instructions=(
        "You are a helpful document assistant. Decide which tools are needed "
        "for the user's question. First check whether an available document is "
        "related to the question. Use the Markdown/text tool only for .md and .txt "
        "files, the image tool only for supported images, and the PDF tool only "
        "for .pdf files. For questions about the HAL 9000 policy PDF, prefer the "
        "MCP RAG search tool. If a tool asks you "
        "to retry, follow its guidance and choose the appropriate tool. Mention "
        "the filenames you use."
    ),
    model_settings=ModelSettings(thinking="minimal"),
    # The local vLLM model does not provide model-native MCP or web-search
    # tools, so execute both capabilities locally. MCP connects to the HTTP
    # server above; web search uses the DuckDuckGo strategy provided by ddgs.
    capabilities=[
        MCP(url=MCP_SERVER_URL, native=False, local=True),
        WebSearch(native=False, local="duckduckgo"),
    ],
)


if __name__ == "__main__":
    # EXERCISE 2 - Start this agent and ask it questions that require using the
    # local document tools, MCP retrieval, and web search to see how it uses all
    # the capabilities together.
    app = agent.to_web()
    logger.info("Starting MCP Document Web Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
