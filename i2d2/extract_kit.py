# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Klokwork AI Inc.

import json
import os

from .schemas import IntentType, Kit, KitSignal


def extract_kit(raw_input: str, konnekt) -> Kit:
    if konnekt is None:
        return Kit(
            raw_input=raw_input,
            intent=IntentType.PROVISION,
            app_type=[KitSignal(value="stub", source_span=None, inferred=False)],
        )

    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "extract_kit.txt")
    with open(prompt_path) as f:
        prompt_template = f.read()

    prompt = prompt_template.replace("{{raw_input}}", raw_input)

    from konnekt.config import KonnektConfig

    response = konnekt.complete(
        role="extractor",
        task="extract",
        prompt=prompt,
        config=KonnektConfig(),
    )

    try:
        parsed = json.loads(response)
        return Kit.model_validate(parsed)
    except Exception as e:
        raise ValueError(f"Kit validation failed: {e}") from e
