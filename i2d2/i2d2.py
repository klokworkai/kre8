import os
import yaml

from .kit_schema import Kit
from .extract_kit import extract_kit


def load_config():
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def process_intent(raw_input: str, konnekt):
    """
    Main i2d2 orchestration entry point.

    Flow:
        raw input
        ↓
        Kit extraction
        ↓
        (future) design reasoning → Kanvas
        ↓
        Gate 1 + Gate 2 (konform)
    """

    # Step 1 — extract Kit from raw NLP input
    kit = extract_kit(raw_input, konnekt)

    # TODO: konform gate goes here

    return kit
