"""Script to demonstrate tool calls with a simple Pydantic AI agent."""

from datetime import datetime

import uvicorn
from loguru import logger
from pydantic_ai import Agent

from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model

agent = Agent(
    model=get_vllm_model(),
    instructions=(
        "You are a helpful assistant that can perform tasks using tools. "
        "Use the provided tools when they are useful for the user's question."
    ),
)

# EXERCISE 1 - Tool definition:
# Define a function that gets the current date and time.
# Decorate it so Pydantic AI exposes it as a tool.
# Tip: Use @agent.tool_plain to register a simple tool without parameters or structured output.
# Tip: datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Solution: @agent.tool_plain registers this function as a tool the agent can call.
@agent.tool_plain
def get_current_date() -> str:
    """Get the current date and time.
    Returns:
        A string representation of the current date and time.
    """
    logger.info("Agent is using the tool to get the current date and time.")
    # Solution: datetime.now() reads local time and strftime formats the output.
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    app = agent.to_web()
    logger.info("Starting Simple Tool Call Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
