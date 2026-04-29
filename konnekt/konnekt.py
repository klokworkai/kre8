import logging

import litellm

from konnekt.config import KonnektConfig
from konnekt.errors import KonnektError
from konnekt.models import resolve_model
from konnekt.secrets import get_api_key

logger = logging.getLogger(__name__)


def complete(
    role: str,
    task: str,
    prompt: str,
    config: KonnektConfig,
    model_select: tuple[int, int] | None = None,
) -> str:
    provider = "unknown"
    litellm_model = "unknown"
    try:
        provider, litellm_model = resolve_model(role, model_select)
        api_key = get_api_key(provider)

        logger.info(
            "konnekt | role=%s task=%s model=%s select=%s",
            role, task, litellm_model, model_select,
        )

        response = litellm.completion(
            model=litellm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout=config.timeout,
            api_key=api_key,
        )
        message = response.choices[0].message
        content = message.content
        if not content:
            # DeepSeek V4 thinking models return chain-of-thought in reasoning_content
            # when content is empty. LiteLLM >=1.35.0 handles passthrough automatically
            # but we still need to extract the field correctly.
            content = getattr(message, "reasoning_content", None) or ""
            if content:
                logger.debug("konnekt | content empty, fell back to reasoning_content | model=%s", litellm_model)
        return content
    except KonnektError:
        raise
    except Exception as e:
        raise KonnektError(provider=provider, model=litellm_model, task=task, message=str(e))
