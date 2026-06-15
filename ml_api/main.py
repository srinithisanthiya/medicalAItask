from fastapi import FastAPI, HTTPException

from ml_api.predictor import HealthRiskPredictor
from ml_api.schemas import PredictionRequest, PredictionResponse

app = FastAPI(
    title="MIRA Health ML API",
    description="External AI/ML service for health risk prediction",
    version="1.0.0",
)

_predictor: HealthRiskPredictor | None = None


def get_predictor() -> HealthRiskPredictor:
    global _predictor
    if _predictor is None:
        _predictor = HealthRiskPredictor()
    return _predictor


@app.get("/health")
def health_check():
    try:
        get_predictor()
        return {"status": "ok", "service": "MIRA Health ML API", "detail": None}
    except FileNotFoundError as exc:
        return {"status": "model_missing", "service": "MIRA Health ML API", "detail": str(exc)}


@app.post("/predict", response_model=PredictionResponse)
def predict_health_risk(payload: PredictionRequest):
    try:
        predictor = get_predictor()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    remarks, risk_level, confidence = predictor.predict(
        date_of_birth=payload.date_of_birth,
        glucose=payload.glucose,
        haemoglobin=payload.haemoglobin,
        cholesterol=payload.cholesterol,
    )
    return PredictionResponse(
        remarks=remarks, risk_level=risk_level, confidence=round(confidence, 4)
    )
