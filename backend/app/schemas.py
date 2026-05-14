from pydantic import BaseModel, Field
from typing import Dict, Literal

# Pydantic models for API request and response validation

class PredictRequest(BaseModel):
    mode: Literal["short_term", "long_term"]
    subscription: float | None = Field(default=None, ge=0)
    vix: float | None = Field(default=None, ge=0)
    roce: float | None = None
    de_ratio: float | None = Field(default=None, ge=0)


class PredictResponse(BaseModel):
    mode: str
    score: int
    predicted_return: float
    predicted_return_percent: float
    verdict: str
    contributions: Dict[str, float]
    inputs_used: Dict[str, float]