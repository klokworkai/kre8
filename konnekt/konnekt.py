import logging

import litellm

from konnekt.config import KonnektConfig
from konnekt.errors import KonnektError
from konnekt.models import resolve_model
from konnekt.secrets import get_api_key

logger = logging.getLogger(__name__)


def complete(model: str, task: str, prompt: str, config: KonnektConfig) -> str:
    resolved_model = None
    provider = "unknown"
    try:
        resolved_model = resolve_model(model)
        provider = resolved_model.split("/")[0]
        api_key = get_api_key(provider)

        logger.info("konnekt call | task=%s model=%s resolved=%s", task, model, resolved_model)

        response = litellm.completion(
            model=resolved_model,
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
        raise KonnektError(provider=provider, model=model, task=task, message=str(e))
