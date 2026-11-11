from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    rows: list[list[float]] = Field(min_length=1, max_length=1000)


class PredictionOut(BaseModel):
    label: int
    confidence: float


class PredictResponse(BaseModel):
    model_version: str
    predictions: list[PredictionOut]
