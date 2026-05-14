from pydantic import BaseModel
from typing import Dict

# Pydantic model for deep analysis request

class PredictRequest(BaseModel):
    features: Dict[str, float]