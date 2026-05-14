from fastapi import FastAPI, HTTPException
from deep.schemas import PredictRequest
from deep.services.model_service import ModelService

# FastAPI app for deep ML analysis
app = FastAPI(title="Deep Analysis API", version="1.0.0")

# Initialize the model service
model_service = ModelService()


@app.get("/")
def root():
    return {"message": "Deep analysis backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/deep_analysis")
def deep_analysis(request: PredictRequest):
    try:
        result = model_service.predict(request.features)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))