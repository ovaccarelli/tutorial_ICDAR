"""Script to demonstrate a simple Pydantic AI agent using a remote vLLM model. Used to test connectivity to vLLM."""

import os
import time

import uvicorn
from loguru import logger
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

DEFAULT_VLLM_MODEL = "qwen3.5:27b"
DEFAULT_VLLM_BASE_URL = "https://litellm.kube-ext.isc.heia-fr.ch/v1"


def get_vllm_model(
    model_name: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> OpenAIChatModel:
    """Create a Pydantic AI model backed by the remote vLLM OpenAI API."""
    return OpenAIChatModel(
        model_name=model_name or os.getenv("VLLM_MODEL", DEFAULT_VLLM_MODEL),
        provider=OpenAIProvider(
            base_url=base_url or os.getenv("VLLM_BASE_URL", DEFAULT_VLLM_BASE_URL),
            api_key=api_key or os.environ["VLLM_API_KEY"],
        ),
    )


agent = Agent(
    model=get_vllm_model(),
    instructions="You are a helpful assistant",
    model_settings=ModelSettings(thinking="minimal"),
)

if __name__ == "__main__":
    start_time = time.perf_counter()

    result = agent.run_sync("What is the capital of Italy?")

    end_time = time.perf_counter()
    output_tokens = result.usage().output_tokens
    logger.info(
        f"Token per second: {output_tokens / (end_time - start_time):.2f} tokens/s"
    )

    print(result.output)


#    app = agent.to_web()
#    logger.info("Starting Simple Pydantic AI Agent on http://127.0.0.1:8000")
#    uvicorn.run(app, host="127.0.0.1", port=8000)
