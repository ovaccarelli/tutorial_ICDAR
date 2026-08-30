"""Script to demonstrate a simple Pydantic AI agent using a remote vLLM model. Used to test connectivity to vLLM."""

import time

import uvicorn
from pydantic_ai import Agent, ModelSettings

from tutorial_ICDAR.utils.console_utils import (
    INFO_STYLE,
    console,
    print_step,
)
from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model


agent = Agent(
    model=get_vllm_model(),
    instructions="You are a helpful assistant",
    model_settings=ModelSettings(thinking="minimal"),
)

if __name__ == "__main__":
    print_step("Pydantic AI Agent - Entry Point Demo")
    start_time = time.perf_counter()

    result = agent.run_sync("What is the capital of Austria?")

    end_time = time.perf_counter()
    output_tokens = result.usage.output_tokens
    console.print(
        f"Token per second: {output_tokens / (end_time - start_time):.2f} tokens/s",
        style=INFO_STYLE,
    )

    print_step("Agent Output")
    console.print(result.output, markup=False)

# Uncomment the lines below to expose the agent as a small local web app.

#    app = agent.to_web()
#    console.print(
#        "Starting Simple Pydantic AI Agent on http://127.0.0.1:8000",
#        style=INFO_STYLE,
#    )
#    uvicorn.run(app, host="127.0.0.1", port=8000)
