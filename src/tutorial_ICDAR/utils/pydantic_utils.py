"""Utility functions for working with Pydantic AI models and providers."""

import os

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from tutorial_ICDAR.settings import (
    DEFAULT_VLLM_BASE_URL,
    DEFAULT_VLLM_MODEL,
)


def get_vllm_model(
    model_name: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> OpenAIChatModel:
    """Create a Pydantic AI model backed by the remote vLLM OpenAI API.

    Args:
        model_name: Optional name of the vLLM model to use. If not provided, it will be read from the VLLM_MODEL environment variable or default to DEFAULT_VLLM_MODEL.
        base_url: Optional base URL for the vLLM API. If not provided, it will be read from the VLLM_BASE_URL environment variable or default to DEFAULT_VLLM_BASE_URL.
        api_key: Optional API key. If not provided, it is read from the required VLLM_API_KEY environment variable.

    Returns:
        An instance of OpenAIChatModel configured to use the specified vLLM model and API base URL.
    """
    return OpenAIChatModel(
        model_name=model_name or os.getenv("VLLM_MODEL", DEFAULT_VLLM_MODEL),
        provider=OpenAIProvider(
            base_url=base_url or os.getenv("VLLM_BASE_URL", DEFAULT_VLLM_BASE_URL),
            api_key=api_key or os.environ["VLLM_API_KEY"],
        ),
    )
