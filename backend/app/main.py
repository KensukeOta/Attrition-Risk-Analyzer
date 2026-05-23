from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .schemas import EmployeeInput, PredictionResponse
from .services.predictor import predict_attrition
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
