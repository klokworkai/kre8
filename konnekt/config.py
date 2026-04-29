from pydantic import BaseModel


class KonnektConfig(BaseModel):
    temperature: float = 0.2
    max_tokens: int = 2000
    timeout: int = 30
