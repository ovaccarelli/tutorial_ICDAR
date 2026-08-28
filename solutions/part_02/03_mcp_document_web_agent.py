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
    tools=[
        list_my_available_documents,
        extract_text_from_md_or_txt_file,
        extract_text_from_image_file,
        extract_text_from_pdf_file,
    ],
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
    capabilities=[
        MCP(url=MCP_SERVER_URL, native=False),
        WebSearch(native=False, local="duckduckgo"),
    ],
)

if __name__ == "__main__":
    app = agent.to_web()
    logger.info("Starting MCP Document Web Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
