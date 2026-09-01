"""Utility functions for working with Pydantic AI models and providers."""

import os
from pathlib import Path

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from tutorial_ICDAR.settings import (
    DEFAULT_VLLM_BASE_URL,
    DEFAULT_VLLM_MODEL,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
VLLM_API_KEY_FILE = PROJECT_ROOT / ".vllm_api_key"


def _get_vllm_api_key(api_key: str | None = None) -> str:
    """Resolve the API key from an argument, the environment, or the local key file."""
    resolved_api_key = api_key or os.getenv("VLLM_API_KEY")
    if not resolved_api_key and VLLM_API_KEY_FILE.is_file():
        resolved_api_key = VLLM_API_KEY_FILE.read_text(encoding="utf-8").strip()

    if not resolved_api_key:
        raise RuntimeError(
            "VLLM_API_KEY is not set and .vllm_api_key was not found. Add your "
            "LiteLLM key (starting with 'sk-') to .vllm_api_key."
        )
    return resolved_api_key


def get_vllm_model(
    model_name: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> OpenAIChatModel:
    """Create a Pydantic AI model backed by an OpenAI-compatible vLLM API.

    Args:
        model_name: Optional name of the vLLM model to use. If not provided, it will be read from the VLLM_MODEL environment variable or default to DEFAULT_VLLM_MODEL.
        base_url: Optional base URL for the vLLM API. If not provided, it will be read from the VLLM_BASE_URL environment variable or default to DEFAULT_VLLM_BASE_URL.
        api_key: Optional API key. If not provided, ``VLLM_API_KEY`` is used.

    Returns:
        An instance of OpenAIChatModel configured to use the specified vLLM model and API base URL.
    """
    resolved_api_key = _get_vllm_api_key(api_key)
    resolved_model_name = model_name or os.getenv("VLLM_MODEL") or DEFAULT_VLLM_MODEL

    return OpenAIChatModel(
        model_name=resolved_model_name,
        provider=OpenAIProvider(
            base_url=base_url or os.getenv("VLLM_BASE_URL", DEFAULT_VLLM_BASE_URL),
            api_key=resolved_api_key,
        ),
    )
