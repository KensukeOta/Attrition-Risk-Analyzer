import io

import pandas as pd

from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from .schemas import EmployeeInput, PredictionResponse, FeatureImportanceItem
from .services.predictor import predict_attrition, predict_csv
from .config import get_settings

settings = get_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"message": "Attrition Risk API is running"}


@app.post("/api/v1/predict", response_model=PredictionResponse)
def predict(data: EmployeeInput):
    return predict_attrition(data)


@app.post("/api/v1/predict/csv")
async def predict_csv_route(file: UploadFile = File(...)):
    content = await file.read()

    result_csv = predict_csv(content)

    return StreamingResponse(
        io.BytesIO(result_csv),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=prediction_result.csv"},
    )


@app.get(
    "/api/v1/model/feature-importance",
    response_model=list[FeatureImportanceItem],
)
def get_feature_importance():
    path = Path("artifacts/feature_importance.csv")

    df = pd.read_csv(path)

    return df.to_dict(orient="records")
