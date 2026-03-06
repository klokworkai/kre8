from typing import Any, Dict, List

from pydantic import BaseModel, Field


class StructuredIntent(BaseModel):
    """
    Normalized representation of user infrastructure intent.

    Produced by the intent extraction pipeline and consumed by the
    kre8_think design engine.
    """

    raw_input: str = Field(
        ...,
        description="Original user input in natural language."
    )

    goal: str = Field(
        ...,
        description="Normalized summary of the user's infrastructure objective."
    )

    signals: Dict[str, Any] = Field(
        default_factory=dict,
        description="Inferred signals extracted from the input."
    )

    constraints_hint: Dict[str, Any] = Field(
        default_factory=dict,
        description="User-stated or inferred constraints."
    )

    questions: List[str] = Field(
        default_factory=list,
        description="Clarification questions required before design."
    )

    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence score for extracted intent."
    )