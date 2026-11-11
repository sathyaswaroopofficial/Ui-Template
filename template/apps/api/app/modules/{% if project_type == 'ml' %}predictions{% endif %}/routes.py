from fastapi import APIRouter, Depends
from ml_core.inference import Predictor

from app.modules.predictions.schemas import PredictRequest, PredictResponse
from app.modules.predictions.service import PredictionService, get_predictor

router = APIRouter()


@router.post("", response_model=PredictResponse)
def predict(req: PredictRequest, predictor: Predictor = Depends(get_predictor)):
    return PredictionService(predictor).predict(req)
