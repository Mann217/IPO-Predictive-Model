from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
from pydantic import BaseModel
from typing import List

# FastAPI app for sector-wise IPO predictions
app = FastAPI(title="Sectorwise IPO Scorer API", version="1.0.0")

# Directory paths for models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

# Mapping of sectors to their trained model files
SECTOR_MODEL_MAP = {
    "Banking & Nbfc": "Banking_and_Nbfc_best.pkl",
    "Fmcg": "Fmcg_best.pkl",
    "Industrial & Engineering": "Industrial_and_Engineering_best.pkl",
    "Infrastructure": "Infrastructure_best.pkl",
    "It & Technology": "It_and_Technology_best.pkl",
    "Pharma & Healthcare": "Pharma_and_Healthcare_best.pkl"
}

@app.get("/")
def root(): 
    return {"message": "Sectorwise IPO Scorer backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

class PredictionRequest(BaseModel):
    sector: str
    features: List[float]

@app.post("/predict")
async def predict(data: PredictionRequest):
    # Validate sector is supported
    if data.sector not in SECTOR_MODEL_MAP:
        raise HTTPException(status_code=400, detail=f"Sector '{data.sector}' not supported.")

    model_filename = SECTOR_MODEL_MAP[data.sector]
    model_path = os.path.join(MODEL_DIR, model_filename)

    try:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file {model_filename} missing at {model_path}")

        loaded = joblib.load(model_path)

        model = loaded["model"]
        expected_features = loaded["features"]

        if len(data.features) != len(expected_features):
            raise ValueError(
                f"Expected {len(expected_features)} features: {expected_features}, got {len(data.features)}"
            )

        prediction = model.predict([data.features])

        return {
            "sector": data.sector,
            "prediction": float(prediction[0]),
            "status": "success",
            "model_type": loaded.get("model_type"),
            "r2": loaded.get("r2"),
            "features_used": expected_features
        }

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))