"""Train a health-risk classifier from a public diabetes dataset."""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

MODEL_DIR = Path(__file__).resolve().parent / "model"
MODEL_PATH = MODEL_DIR / "health_risk_model.joblib"
DATA_URL = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"


def _derive_risk_labels(df: pd.DataFrame) -> pd.Series:
    risk_scores = []
    for _, row in df.iterrows():
        score = 0
        if row["Glucose"] >= 140:
            score += 2
        elif row["Glucose"] >= 110:
            score += 1
        if row["BMI"] >= 30:
            score += 2
        elif row["BMI"] >= 25:
            score += 1
        if row["Age"] >= 50:
            score += 1
        if row["BloodPressure"] >= 90:
            score += 1
        if row["Outcome"] == 1:
            score += 2
        if score >= 5:
            risk_scores.append("High")
        elif score >= 3:
            risk_scores.append("Moderate")
        else:
            risk_scores.append("Low")
    return pd.Series(risk_scores, name="risk_level")


def _synthetic_haemoglobin(ages: pd.Series) -> np.ndarray:
    rng = np.random.default_rng(42)
    base = 14.0 - (ages - 30).clip(lower=0) * 0.02
    return np.clip(base + rng.normal(0, 0.4, size=len(ages)), 9.5, 18.0)


def _synthetic_cholesterol(bmi: pd.Series, ages: pd.Series) -> np.ndarray:
    rng = np.random.default_rng(42)
    base = 170 + (bmi - 25).clip(lower=0) * 3 + (ages - 30).clip(lower=0) * 0.8
    return np.clip(base + rng.normal(0, 12, size=len(bmi)), 120, 320)


def train_and_save() -> Path:
    df = pd.read_csv(DATA_URL)
    training_df = pd.DataFrame(
        {
            "age": df["Age"],
            "glucose": df["Glucose"],
            "haemoglobin": _synthetic_haemoglobin(df["Age"]),
            "cholesterol": _synthetic_cholesterol(df["BMI"], df["Age"]),
        }
    )
    training_df["risk_level"] = _derive_risk_labels(df)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(training_df["risk_level"])
    feature_order = ["age", "glucose", "haemoglobin", "cholesterol"]
    X = training_df[feature_order].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200, random_state=42, class_weight="balanced"
    )
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": model, "label_encoder": label_encoder, "feature_order": feature_order},
        MODEL_PATH,
    )
    print(f"Model saved to {MODEL_PATH}")
    print(f"Validation accuracy: {accuracy:.2%}")
    return MODEL_PATH


if __name__ == "__main__":
    train_and_save()
