from datetime import date
from pathlib import Path

import joblib
import numpy as np

MODEL_PATH = Path(__file__).resolve().parent / "model" / "health_risk_model.joblib"


class HealthRiskPredictor:
    def __init__(self, model_path: Path = MODEL_PATH) -> None:
        if not model_path.exists():
            raise FileNotFoundError(
                f"Trained model not found at {model_path}. "
                "Run: python -m ml_api.train_model"
            )
        artifact = joblib.load(model_path)
        self.model = artifact["model"]
        self.label_encoder = artifact["label_encoder"]

    def _age_from_dob(self, date_of_birth: date) -> float:
        today = date.today()
        return today.year - date_of_birth.year - (
            (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
        )

    def predict(
        self,
        *,
        date_of_birth: date,
        glucose: float,
        haemoglobin: float,
        cholesterol: float,
    ) -> tuple[str, str, float]:
        age = self._age_from_dob(date_of_birth)
        features = np.array([[age, glucose, haemoglobin, cholesterol]], dtype=float)

        probabilities = self.model.predict_proba(features)[0]
        class_index = int(np.argmax(probabilities))
        risk_level = self.label_encoder.inverse_transform([class_index])[0]
        confidence = float(probabilities[class_index])

        remarks = self._build_remarks(
            risk_level=risk_level,
            confidence=confidence,
            glucose=glucose,
            haemoglobin=haemoglobin,
            cholesterol=cholesterol,
            age=age,
        )
        return remarks, risk_level, confidence

    def _build_remarks(
        self,
        *,
        risk_level: str,
        confidence: float,
        glucose: float,
        haemoglobin: float,
        cholesterol: float,
        age: float,
    ) -> str:
        observations: list[str] = []

        if glucose >= 126:
            observations.append("elevated fasting glucose")
        elif glucose >= 100:
            observations.append("borderline glucose levels")

        if haemoglobin < 12:
            observations.append("low haemoglobin suggesting possible anaemia")
        elif haemoglobin > 17:
            observations.append("high haemoglobin")

        if cholesterol >= 240:
            observations.append("high cholesterol")
        elif cholesterol >= 200:
            observations.append("borderline high cholesterol")

        if age >= 45:
            observations.append("age-related metabolic risk factors")

        observation_text = (
            "; ".join(observations) if observations else "values within typical ranges"
        )

        return (
            f"AI Assessment: {risk_level} health risk "
            f"({confidence * 100:.1f}% model confidence). "
            f"Key indicators: {observation_text}. "
            f"Recommend clinical follow-up if symptoms persist."
        )
