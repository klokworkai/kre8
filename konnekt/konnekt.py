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
        return response.choices[0].message.content
    except KonnektError:
        raise
    except Exception as e:
        raise KonnektError(provider=provider, model=litellm_model, task=task, message=str(e))
