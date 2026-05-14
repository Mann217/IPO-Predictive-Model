from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.schemas import PredictRequest
from app.services.scorer import predict as scorer_predict
# from app.predict_performance import ModelService  # Commented out alternative model service
from typing import Dict

# FastAPI app for IPO scoring predictions
app = FastAPI(title="IPO Scorer API", version="1.0.0")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "IPO Scorer backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict_ipo(request: PredictRequest):
    try:
        result = scorer_predict(request.model_dump())
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
