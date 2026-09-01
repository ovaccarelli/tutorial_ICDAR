"""Optional Langfuse observability for the tutorial agents."""

from __future__ import annotations

import os
from threading import Lock

from langfuse import Langfuse
from loguru import logger
from pydantic_ai import Agent
from pydantic_ai.models.instrumented import InstrumentationSettings

DEFAULT_LANGFUSE_BASE_URL = "http://localhost:3000"
DEFAULT_LANGFUSE_PUBLIC_KEY = "lf_pk_7a9d6c0f3b2e4a1d8c5f9e7b6a4c2d1e"
DEFAULT_LANGFUSE_SECRET_KEY = "lf_sk_8b0e7d1a4c3f5b2e9d6a8c7f1e4b3d2a"
LANGFUSE_START_COMMAND = (
    "docker compose -f observability/docker-compose.yml up -d --wait"
)

_TRUE_VALUES = {"1", "true", "yes", "on"}
_configuration_lock = Lock()
_configuration_attempted = False
_langfuse_client: Langfuse | None = None
_configuration_error: str | None = None


def _observability_enabled() -> bool:
    """Return whether optional observability was enabled through the environment."""
    return os.getenv("LANGFUSE_ENABLED", "").strip().lower() in _TRUE_VALUES


def _unavailable_message(base_url: str) -> str:
    return (
        f"Langfuse is unavailable or rejected the tutorial credentials at {base_url}. "
        f"Start the local instance with: {LANGFUSE_START_COMMAND}"
    )


def configure_observability(*, required: bool = False) -> Langfuse | None:
    """Configure Langfuse tracing for all subsequently created Pydantic AI agents.

    Observability is disabled unless ``LANGFUSE_ENABLED`` is truthy or ``required``
    is set. Optional configuration failures are logged and do not prevent an agent
    from running. Required configuration failures raise a ``RuntimeError`` with the
    command needed to start the local workshop stack.

    Args:
        required: Require a reachable, authenticated Langfuse instance.

    Returns:
        The configured Langfuse client, or ``None`` when tracing is disabled or an
        optional configuration attempt failed.
    """
    global _configuration_attempted, _configuration_error, _langfuse_client

    if not required and not _observability_enabled():
        return None

    with _configuration_lock:
        if _langfuse_client is not None:
            return _langfuse_client

        if _configuration_attempted:
            if required:
                raise RuntimeError(
                    _configuration_error
                    or _unavailable_message(
                        os.getenv("LANGFUSE_BASE_URL", DEFAULT_LANGFUSE_BASE_URL)
                    )
                )
            return None

        _configuration_attempted = True
        base_url = os.getenv("LANGFUSE_BASE_URL", DEFAULT_LANGFUSE_BASE_URL)
        client: Langfuse | None = None

        try:
            client = Langfuse(
                public_key=os.getenv(
                    "LANGFUSE_PUBLIC_KEY", DEFAULT_LANGFUSE_PUBLIC_KEY
                ),
                secret_key=os.getenv(
                    "LANGFUSE_SECRET_KEY", DEFAULT_LANGFUSE_SECRET_KEY
                ),
                base_url=base_url,
                environment="tutorial",
                timeout=3,
            )
            if not client.auth_check():
                raise RuntimeError("Langfuse authentication failed")

            Agent.instrument_all(
                InstrumentationSettings(
                    include_content=True,
                    include_binary_content=False,
                )
            )
        except Exception as exc:
            if client is not None:
                client.shutdown()
            _configuration_error = _unavailable_message(base_url)
            if required:
                raise RuntimeError(_configuration_error) from exc
            logger.warning(f"{_configuration_error} Continuing without tracing.")
            return None

        _langfuse_client = client
        logger.info(f"Langfuse tracing enabled: {base_url}")
        return client
