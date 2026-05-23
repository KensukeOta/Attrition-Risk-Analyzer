from pathlib import Path

import joblib
import pandas as pd

from ..schemas import EmployeeInput


ARTIFACT_PATH = Path("artifacts/attrition_artifacts.pkl")


artifacts = joblib.load(ARTIFACT_PATH)

model = artifacts["model"]
threshold = artifacts["threshold"]
categorical_features = artifacts["categorical_features"]
drop_cols = artifacts["drop_cols"]


def risk_label(probability: float) -> str:
    if probability >= 0.15:
        return "High"
    elif probability >= threshold:
        return "Middle"
    return "Low"


def build_risk_factors(data: EmployeeInput) -> list[str]:
    factors = []

    if data.OverTime == "Yes":
        factors.append(
            "OverTime が Yes のため、離職リスクに影響している可能性があります。"
        )

    if data.JobSatisfaction <= 2:
        factors.append("JobSatisfaction が低めです。")

    if data.EnvironmentSatisfaction <= 2:
        factors.append("EnvironmentSatisfaction が低めです。")

    if data.DistanceFromHome >= 10:
        factors.append("DistanceFromHome が長めです。")

    if data.StockOptionLevel == 0:
        factors.append("StockOptionLevel が 0 です。")

    if not factors:
        factors.append("明確に強いリスク要因は検出されませんでした。")

    return factors


def predict_attrition(data: EmployeeInput) -> dict:
    df = pd.DataFrame([data.model_dump()])

    for col in categorical_features:
        if col in df.columns:
            df[col] = df[col].astype("category")

    df = df.drop(columns=drop_cols, errors="ignore")

    yes_idx = list(model.classes_).index("Yes")
    probability = float(model.predict_proba(df)[:, yes_idx][0])

    prediction = "Yes" if probability >= threshold else "No"

    return {
        "attrition_probability": round(probability, 3),
        "prediction": prediction,
        "risk_level": risk_label(probability),
        "threshold": round(float(threshold), 2),
        "risk_factors": build_risk_factors(data),
    }
