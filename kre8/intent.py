from kre8_think.intent_models import StructuredIntent


def extract_intent(raw_input: str, agent) -> StructuredIntent:
    """
    Extract structured infrastructure intent from raw user input.

    Flow:
        raw input
        ↓
        agent intent extraction
        ↓
        StructuredIntent validation
    """

    intent_data = agent.extract_intent(raw_input=raw_input)

    return StructuredIntent(**intent_data)