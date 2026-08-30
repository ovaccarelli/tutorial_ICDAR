import uvicorn
from loguru import logger
from pydantic_ai import (
    Agent,
    ModelRequestContext,
    RunContext,
    UserPromptPart,
)
from pydantic_ai.capabilities.hooks import Hooks

from tutorial_ICDAR.utils.pydantic_utils import get_vllm_model

hooks = Hooks()

agent = Agent(
    model=get_vllm_model(),
    instructions="You are a helpful assistant",
    capabilities=[hooks],
)


@hooks.on.before_model_request
async def before_request_hook(
    ctx: RunContext, request_context: ModelRequestContext
) -> ModelRequestContext:
    logger.info(f"Before model request: {request_context.messages}")

    for message in request_context.messages:
        for part in message.parts:
            if isinstance(part, UserPromptPart) and isinstance(part.content, str) and "cat" in part.content.lower():
                logger.warning(
                    "Inappropriate content detected in the request. Blocking the request."
                )
                raise ValueError(
                    "Inappropriate content detected. Request blocked."
                )
    return request_context


if __name__ == "__main__":
    app = agent.to_web()
    logger.info("Starting Guardrails with Hooks Agent on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
